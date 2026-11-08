# Сборка отчёта «Зарядка и разрядка RC-цепи» в формате LibreOffice (.odt).
# Стили страницы, шрифты, заголовки и подписи берутся из шаблона кафедры
# (template_styles.xml), формулы вставляются объектами LibreOffice Math.
#
# Запуск (из папки report, после RC_analysis.py и make_schematic.py):
#   python3 build_odt.py
# Нужен LibreOffice с модулем Math и python3-uno (оглавление, формулы
# и номера рисунков обновляются через LibreOffice).
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import zipfile
from xml.sax.saxutils import escape

from PIL import Image

OUT = os.path.abspath("../Отчёт_RC.odt")
PDF = os.path.abspath("../Отчёт_RC.pdf")
R = json.load(open("results.json", encoding="utf-8"))


def num(x, d=2):
    """Число с запятой: 9.5 -> '9,50'."""
    return f"{x:.{d}f}".replace(".", ",")


# ---------------------------------------------------------------- разметка текста
# **жирный**, *курсив*, _{нижний индекс}, ^{верхний индекс}
TOKEN = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*|_\{(.+?)\}|\^\{(.+?)\}")


def inline(text):
    out, pos = [], 0
    for m in TOKEN.finditer(text):
        out.append(escape(text[pos:m.start()]))
        b, i, sub, sup = m.groups()
        if b is not None:
            out.append(f'<text:span text:style-name="TB">{inline(b)}</text:span>')
        elif i is not None:
            out.append(f'<text:span text:style-name="TI">{inline(i)}</text:span>')
        elif sub is not None:
            out.append(f'<text:span text:style-name="TSub">{inline(sub)}</text:span>')
        else:
            out.append(f'<text:span text:style-name="TSup">{inline(sup)}</text:span>')
        pos = m.end()
    out.append(escape(text[pos:]))
    return "".join(out)


body = []
formulas = {}      # имя объекта -> текст StarMath
images = []        # (имя файла в архиве, исходный файл)
counters = {"formula": 0, "fig": 0, "table": 0, "obj": 0, "img": 0}


def p(text, style="Text_20_body"):
    body.append(f'<text:p text:style-name="{style}">{inline(text)}</text:p>')


def h1(text):
    body.append(f'<text:h text:style-name="Heading_20_1" text:outline-level="1">{escape(text)}</text:h>')


def h2(text):
    body.append(f'<text:h text:style-name="Heading_20_2" text:outline-level="2">{escape(text)}</text:h>')


def formula(starmath, height_cm=1.2, numbered=True):
    """Формула по центру, номер (N) у правого края — как в шаблоне."""
    counters["obj"] += 1
    name = f"Формула{counters['obj']}"
    formulas[name] = starmath
    frame = (f'<draw:frame draw:style-name="frF" draw:name="{name}" text:anchor-type="as-char" '
             f'svg:width="6cm" svg:height="{height_cm}cm" draw:z-index="0">'
             f'<draw:object xlink:href="./Object {counters["obj"]}" xlink:type="simple" '
             f'xlink:show="embed" xlink:actuate="onLoad"/></draw:frame>')
    tail = ""
    if numbered:
        counters["formula"] += 1
        tail = f"<text:tab/>({counters['formula']})"
    body.append(f'<text:p text:style-name="Абзац_20_формулы"><text:tab/>{frame}{tail}</text:p>')
    return counters["formula"]


def figure(path, caption, width_cm=15.0):
    counters["fig"] += 1
    counters["img"] += 1
    w, h = Image.open(path).size
    height_cm = width_cm * h / w
    ext = os.path.splitext(path)[1]
    arc = f"Pictures/image{counters['img']}{ext}"
    images.append((arc, path))
    body.append(
        f'<text:p text:style-name="Абзац_20_рисунка"><draw:frame draw:style-name="frImg" '
        f'draw:name="Изображение{counters["img"]}" text:anchor-type="as-char" '
        f'svg:width="{width_cm:.2f}cm" svg:height="{height_cm:.2f}cm" draw:z-index="1">'
        f'<draw:image xlink:href="{arc}" xlink:type="simple" xlink:show="embed" '
        f'xlink:actuate="onLoad"/></draw:frame></text:p>')
    body.append(
        f'<text:p text:style-name="Drawing">Рисунок <text:sequence text:ref-name="refDrawing{counters["fig"]}" '
        f'text:name="Drawing" text:formula="ooow:Drawing+1" style:num-format="1">{counters["fig"]}'
        f'</text:sequence> — {inline(caption)}</text:p>')
    return counters["fig"]


table_styles = []


def table(caption, header, rows, widths_cm):
    counters["table"] += 1
    n = counters["table"]
    name = f"Таблица{n}"
    total = sum(widths_cm)
    table_styles.append(
        f'<style:style style:name="{name}" style:family="table"><style:table-properties '
        f'style:width="{total:.2f}cm" table:align="center"/></style:style>')
    cols = []
    for j, w in enumerate(widths_cm):
        cs = f"{name}.C{j}"
        table_styles.append(
            f'<style:style style:name="{cs}" style:family="table-column">'
            f'<style:table-column-properties style:column-width="{w:.2f}cm"/></style:style>')
        cols.append(f'<table:table-column table:style-name="{cs}"/>')
    body.append(
        f'<text:p text:style-name="PTabCap">Таблица <text:sequence text:ref-name="refTable{n}" '
        f'text:name="Table" text:formula="ooow:Table+1" style:num-format="1">{n}</text:sequence>'
        f' — {inline(caption)}</text:p>')

    def row(cells, style):
        return "<table:table-row>" + "".join(
            f'<table:table-cell table:style-name="Cell" office:value-type="string">'
            f'<text:p text:style-name="{style}">{inline(c)}</text:p></table:table-cell>'
            for c in cells) + "</table:table-row>"

    body.append(f'<table:table table:name="{name}" table:style-name="{name}">' + "".join(cols)
                + f'<table:table-header-rows>{row(header, "PCellHead")}</table:table-header-rows>'
                + "".join(row(r, "PCell") for r in rows) + "</table:table>")
    body.append('<text:p text:style-name="PAfterTable"/>')
    return n


# ================================================================ ТИТУЛЬНЫЙ ЛИСТ
p("Министерство науки и высшего образования РФ", "PTitleFirst")
p("", "PCenter")
p("Московский физико-технический университет", "PCenter")
p("", "PCenter")
p("Кафедра «Техническая физика космических летательных аппаратов»", "PCenter")
p("", "PCenter")
p("", "PCenter")
p("ЛАБОРАТОРНАЯ РАБОТА", "PTitleBig")
p("по дисциплине «Общая инженерная подготовка»", "PTitleBig")
p("на тему: «Зарядка и разрядка RC-цепи. Определение постоянной времени»", "PTitleBig")
p("", "PCenter")
p("", "PCenter")
p("Выполнил: студент группы Б03-605", "PCenter")
p("Тлеспаев Э.Е.", "PCenter")
p("Дата выполнения: 03.11.2026", "PCenter")
p("", "PCenter")
p("Проверил: доцент, к.т.н.", "PCenter")
p("Егор Анатольевич", "PCenter")
for _ in range(2):
    p("", "PCenter")
p("Москва, 2026", "PCenter")

# ================================================================ СОДЕРЖАНИЕ
body.append("@@TOC@@")

# ================================================================ 1 АННОТАЦИЯ
h1("Аннотация")
p("**Цель работы:** экспериментально получить зависимость напряжения на конденсаторе от времени "
  "при зарядке и разрядке RC-цепи; по полученным кривым определить постоянную времени цепи τ "
  "и сравнить её с номинальным значением τ = *RC*, рассчитанным по маркировке резистора и конденсатора.")
p("**В работе используются:** микрокомпьютер Raspberry Pi, плата AUX с RC-цепью (резистор R1, "
  "электролитический конденсатор C1), 10-битный аналого-цифровой преобразователь (АЦП) MCP3021 "
  "с интерфейсом I²C, программы на языке Python для управления выходом GPIO14, записи и обработки данных.")
p("Выход GPIO14 подключает RC-цепь к источнику напряжения (конденсатор заряжается) или к нулю "
  "(конденсатор разряжается через тот же резистор). Напряжение на конденсаторе непрерывно измеряет "
  "АЦП, данные сохраняются в файл и обрабатываются: постоянная времени определяется по уровням 63 % "
  "и 37 % и аппроксимацией экспериментальных кривых экспонентой методом наименьших квадратов.")

# ================================================================ 2 ТЕОРИЯ
h1("Теоретические сведения")
h2("Зарядка конденсатора")
p("Пусть конденсатор ёмкостью *C* заряжается через резистор сопротивлением *R* от источника "
  "с ЭДС *E*. По второму правилу Кирхгофа сумма напряжений на резисторе и конденсаторе равна ЭДС:")
f_kirch = formula("E = I R + U ,", 0.6)
p("где *I* — ток в цепи, *U* — напряжение на конденсаторе. Ток связан со скоростью изменения "
  "заряда конденсатора *q* = *CU*:")
f_cur = formula("I = {dq} over {dt} = C {dU} over {dt} .", 1.3)
p(f"Подставляя ({f_cur}) в ({f_kirch}), получаем дифференциальное уравнение")
formula("RC {dU} over {dt} + U = E .", 1.3)
p("Его решение при начальном условии *U*(0) = 0:")
f_charge = formula("U(t) = E left( 1 - e^{- t / %tau} right) , ~~~~ %tau = RC ,", 0.9)
p("где τ — **постоянная времени** цепи. При *t* ≫ τ напряжение на конденсаторе стремится к *E*.")

h2("Разрядка конденсатора")
p("Если отключить источник (подать на вход цепи нулевое напряжение), конденсатор разряжается "
  "через тот же резистор. Уравнение принимает вид")
formula("RC {dU} over {dt} + U = 0 ,", 1.3)
p("а его решение при начальном напряжении *U*_{0}:")
f_dis = formula("U(t) = U_0 e^{- t / %tau} .", 0.8)
p("Логарифмируя, получаем линейную зависимость, наклон которой равен −1/τ:")
f_ln = formula("ln U = ln U_0 - t over %tau .", 1.2)

h2("Способы определения постоянной времени")
p(f"Из ({f_charge}) и ({f_dis}) следует, что за время *t* = τ напряжение при зарядке достигает "
  "63 % установившегося значения, а при разрядке падает до 37 % начального:")
f_lvl = formula('U( %tau ) = E left( 1 - e^{-1} right) approx "0,63" E , ~~~~ U( %tau ) = U_0 e^{-1} approx "0,37" U_0 .', 0.9)
p("На этом основан простейший графический способ: по графику находят момент, когда напряжение "
  "проходит уровень 63 % (37 %) от полного изменения.")
p("Более точный способ использует все экспериментальные точки. Обе кривые описываются общей моделью")
f_model = formula("U(t) = A + B e^{- t / %tau} ,", 0.8)
p("где при зарядке *A* = *E*, *B* = −*E*, а при разрядке *A* = 0, *B* = *U*_{0}. Параметры *A*, *B*, τ "
  "находят методом наименьших квадратов (МНК), минимизируя сумму квадратов отклонений:")
f_mnk = formula("S( A, B, %tau ) = sum from{i=1} to{N} left( U_i - A - B e^{- t_i / %tau} right)^2 rightarrow func min .", 1.6)
p("При фиксированном τ задача линейна по *A* и *B* и решается точно, а τ подбирается перебором. "
  f"Дополнительно τ определяется по наклону прямой ({f_ln}) для разрядки.")

h2("Номинальные значения элементов")
p("Сопротивление выводного резистора с четырёхполосной цветовой маркировкой определяется "
  "по первым трём полосам: две цифры *a*, *b* и множитель 10^{*m*}:")
f_col = formula("R = left( 10 a + b right) cdot 10^m .", 0.8)
p("Для R1 (полосы коричневая, чёрная, зелёная) *a* = 1, *b* = 0, *m* = 5, то есть *R*_{1} = 10 · 10^{5} Ом = 1 МОм. "
  "Четвёртая полоса задаёт допуск. У SMD-резисторов с четырёхзначным кодом первые три цифры — "
  "значащие, последняя — показатель степени: код «1000» означает 100 · 10^{0} = 100 Ом (R2), "
  "код «5600» — 560 Ом (R3).")
p("Номинальная постоянная времени цепи:")
f_nom = formula('%tau_{"ном"} = R_1 C_1 = 10^6 " Ом" cdot 10^{-5} " Ф" = 10 " с" .', 0.9)

# ================================================================ 3 ИЗМЕРЕНИЯ
h1("Измерение экспериментальных данных")
h2("Экспериментальная установка")
fb = counters["fig"] + 1
p(f"Плата AUX с исследуемой цепью показана на рисунке {fb}, упрощённая схема измерений — "
  f"на рисунке {fb + 1}. Резистор R1 и конденсатор C1 образуют RC-цепь; напряжение на конденсаторе "
  "(вывод SIG) измеряет АЦП MCP3021, который передаёт результат в Raspberry Pi по шине I²C. "
  "Резистор R3, по-видимому, ограничивает ток светодиода питания V1, а R2 включён в цепь кнопки; "
  "кнопка в опыте не нажималась, поэтому R2 и R3 на постоянную времени не влияют.")
figure("fig_board.jpg", "Плата AUX с RC-цепью", 9.0)
figure("fig_schematic.png", "Упрощённая схема измерений", 11.0)
t_el = table("Элементы платы AUX",
             ["Элемент", "Маркировка", "Номинал", "Допуск"],
             [["R1 (выводной)", "коричневый, чёрный, зелёный, золотой^{1)}", "1 МОм", "±5 %"],
              ["C1 (электролитический)", "10 мкФ", "10 мкФ", "±20 %^{2)}"],
              ["R2 (SMD)", "1000", "100 Ом", "±1 %"],
              ["R3 (SMD)", "5600", "560 Ом", "±1 %"]],
             [4.2, 5.6, 2.8, 2.6])
p("^{1)} Четвёртая полоса R1 на фото выглядит жёлтой; для четырёхполосной маркировки это, скорее всего, "
  "золотая полоса (±5 %). ^{2)} Типичный допуск электролитических конденсаторов.", "PNote")

h2("Методика измерений")
p("Измерения выполняет программа RC_.py:")
p("1. Выход GPIO14 = 0 в течение 50 с, чтобы конденсатор полностью разрядился.")
p("2. GPIO14 = 1 на 50 с (≈ 5τ) — зарядка; всё это время напряжение непрерывно считывается АЦП.")
p("3. GPIO14 = 0 ещё на 50 с — разрядка, измерения продолжаются.")
p("4. Время, напряжение и состояние выхода записываются в файл lab.csv.")
n_pts = f"{R['n_points']:,}".replace(",", "\u00a0")
p(f"Динамический диапазон АЦП *U*_{{ДД}} = 5,186 В, всего получено *N* = {n_pts} измерений "
  f"за {num(R['duration'], 0)} с, средняя частота измерений {R['rate']:.0f} Гц "
  f"(интервал между отсчётами ≈ {num(R['dt_mean_ms'], 2)} мс).")
p(f"Полная запись сигнала показана на рисунке {counters['fig'] + 1}, выборка значений через каждые 5 с — "
  f"в таблице {counters['table'] + 1}.")
figure("fig_full.png", "Напряжение на конденсаторе при зарядке и разрядке", 15.5)
table("Напряжение на конденсаторе (выборка через 5 с от начала этапа)",
      ["*t*, с", "*U*_{зар}, В", "*U*_{раз}, В"],
      [[num(a, 0), num(b, 3), num(c, 3)] for a, b, c in R["samples"]],
      [3.0, 4.0, 4.0])

# ================================================================ 4 ОБРАБОТКА
h1("Обработка данных эксперимента")
h2("Приборные погрешности")
lsb = 5.186 / 1023 * 1000
table("Приборные погрешности",
      ["Прибор / элемент", "Величина", "Погрешность"],
      [["АЦП MCP3021", "*U*", f"σ_{{U}} = {num(lsb, 1)} мВ (1 ед. мл. разряда)"],
       ["Системное время Raspberry Pi", "*t*", f"≈ 1 мкс; шаг опроса {num(R['dt_mean_ms'], 2)} мс"],
       ["Резистор R1", "*R*", "δ_{R} = 5 %"],
       ["Конденсатор C1", "*C*", "δ_{C} = 20 %"]],
      [5.6, 2.6, 8.0])
p("Все способы определения τ используют отношения напряжений (уровни 63 % и 37 %, форма экспоненты), "
  "поэтому погрешность калибровки динамического диапазона АЦП на результат не влияет. "
  "Погрешность измерения времени пренебрежимо мала по сравнению с τ ≈ 10 с.")

h2("Формулы для расчёта погрешностей")
p("Относительная погрешность номинальной постоянной времени складывается из допусков элементов:")
f_dnom = formula('%delta_{%tau "ном"} = sqrt{ %delta_R^2 + %delta_C^2 } .', 1.0)
p("Среднее значение τ по *N* способам и его погрешность (по разбросу значений):")
f_mean = formula("overline{%tau} = 1 over N sum from{i=1} to{N} %tau_i , ~~~~ "
                 "%sigma_%tau = sqrt{ { sum from{i=1} to{N} ( %tau_i - overline{%tau} )^2 } over { N - 1 } } .", 1.8)
p(f"По ({f_dnom}): δ_{{τ ном}} = √(5² + 20²) % ≈ {R['delta_nom'] * 100:.0f} %, то есть "
  f"τ_{{ном}} = (10 ± {num(R['tau_nom'] * R['delta_nom'], 1)}) с.")

h2("Зарядка конденсатора")
fc = counters["fig"] + 1
p(f"Кривая зарядки и её аппроксимация показаны на рисунке {fc}. МНК по модели ({f_model}) даёт "
  f"установившееся напряжение *U*_{{∞}} = {num(R['A_c'], 3)} В и τ = {num(R['tau_c'])} с; "
  f"среднеквадратичное отклонение точек от экспоненты {num(R['rms_c'] * 1000, 1)} мВ, что "
  "соответствует примерно двум единицам младшего разряда АЦП. Уровень 63 % "
  f"({num(R['lvl63'], 3)} В) достигается через τ = {num(R['tau63'])} с.")
figure("fig_charge.png", "Зарядка конденсатора: измерение, аппроксимация экспонентой и уровень 63 %", 15.5)

h2("Разрядка конденсатора")
fd = counters["fig"] + 1
p(f"Кривая разрядки показана на рисунке {fd}. Напряжение падает с {num(R['u_dis_start'], 3)} В до "
  f"{num(R['u_dis_min'], 3)} В. МНК даёт τ = {num(R['tau_d'])} с (СКО {num(R['rms_d'] * 1000, 1)} мВ), "
  f"уровень 37 % ({num(R['lvl37'], 3)} В) достигается через τ = {num(R['tau37'])} с.")
figure("fig_discharge.png", "Разрядка конденсатора: измерение, аппроксимация экспонентой и уровень 37 %", 15.5)
p(f"В полулогарифмическом масштабе (рисунок {counters['fig'] + 1}) разрядка ложится на прямую, "
  f"что подтверждает экспоненциальный закон ({f_dis}). По наклону прямой ({f_ln}) "
  f"τ = {num(R['tau_ln'])} с.")
figure("fig_ln.png", "Разрядка в полулогарифмическом масштабе: зависимость линейна, наклон равен −1/τ", 15.5)

h2("Сводка результатов")
tr = counters["table"] + 1
p(f"Значения τ, полученные разными способами, сведены в таблицу {tr}, сравнение с номиналом — "
  f"в таблицу {tr + 1}. Среднее и погрешность рассчитаны по ({f_mean}) по четырём основным способам.")
table("Постоянная времени, определённая разными способами",
      ["Способ определения", "τ, с"],
      [["Уровень 63 %, зарядка", num(R["tau63"])],
       ["Уровень 37 %, разрядка", num(R["tau37"])],
       ["МНК, зарядка", num(R["tau_c"])],
       ["МНК, разрядка", num(R["tau_d"])],
       ["**Среднее**", f"**{num(R['tau_mean'])} ± {num(R['tau_sigma'])}**"],
       ["Наклон ln *U*(*t*), разрядка (контроль)", num(R["tau_ln"])]],
      [9.0, 4.0])
c_eff = R["tau_mean"] / 1e6 * 1e6
r_eff = R["tau_mean"] / 10e-6 / 1e6
table("Сравнение с номинальными значениями",
      ["Величина", "Номинал", "Эксперимент"],
      [["τ, с", f"10 ± {num(R['tau_nom'] * R['delta_nom'], 1)}", f"{num(R['tau_mean'])} ± {num(R['tau_sigma'])}"],
       ["*R*_{1} при *C*_{1} = 10 мкФ", "1 МОм", f"{num(r_eff)} МОм"],
       ["*C*_{1} при *R*_{1} = 1 МОм", "10 мкФ", f"{num(c_eff, 1)} мкФ"]],
      [6.5, 4.0, 4.5])
diff = (R["tau_mean"] - R["tau_nom"]) / R["tau_nom"] * 100

# ================================================================ 5 ОБСУЖДЕНИЕ
h1("Обсуждение")
p(f"1. **Согласие с номиналом.** Измеренная постоянная времени τ = ({num(R['tau_mean'])} ± "
  f"{num(R['tau_sigma'])}) с на {abs(diff):.0f} % меньше номинальной (10 с). Это отличие лежит "
  f"внутри допуска номиналов (±{R['delta_nom'] * 100:.0f} %), который в основном определяется большим "
  "разбросом ёмкости электролитических конденсаторов.")
p("2. **Зарядка и разрядка.** Значения τ, полученные при зарядке и при разрядке, совпадают с точностью "
  "около 1 %: цепь заряжается и разряжается через одно и то же сопротивление и хорошо описывается "
  "моделью RC-цепи. Разброс между способами (≈ 1 %) связан с тем, что способы по уровням используют "
  "одну точку кривой и чувствительны к шуму, а МНК — все точки.")
p(f"3. **Установившееся напряжение.** Конденсатор зарядился до {num(R['A_c'], 2)} В, что ниже "
  "динамического диапазона АЦП (5,19 В). Возможная причина — ток утечки электролитического "
  "конденсатора и входное сопротивление АЦП: они действуют как большое сопротивление, подключённое "
  "параллельно конденсатору, уменьшают установившееся напряжение и немного уменьшают эффективную "
  "постоянную времени. Это предположение, для проверки нужно измерить напряжение источника и "
  "сопротивление R1 мультиметром.")
p("4. **Шум.** На кривой зарядки видны единичные выбросы величиной в несколько единиц младшего "
  "разряда АЦП; на результат МНК они практически не влияют.")
p("5. **Разделение R и C.** Опыт даёт только произведение *RC*. Чтобы определить реальные "
  "значения *R*_{1} и *C*_{1} по отдельности, одно из них нужно измерить независимо.")

# ================================================================ 6 ВЫВОДЫ
h1("Выводы")
p("1. Получены зависимости напряжения на конденсаторе от времени при зарядке и разрядке RC-цепи; "
  f"обе кривые хорошо описываются экспонентой (отклонение точек ≈ {num(R['rms_c'] * 1000, 0)} мВ).")
p(f"2. Постоянная времени цепи, найденная четырьмя способами, τ = ({num(R['tau_mean'])} ± "
  f"{num(R['tau_sigma'])}) с. Номинальное значение τ = R_{{1}}C_{{1}} = (10 ± "
  f"{num(R['tau_nom'] * R['delta_nom'], 1)}) с; отличие {diff:+.0f} % лежит в пределах допусков элементов.")
p("3. Точность измерения τ (≈ 1 %) значительно выше точности номинала (≈ 21 %), основной вклад "
  "в которую вносит допуск ёмкости электролитического конденсатора.")

# ================================================================ XML
TOC = (
    '<text:table-of-content text:style-name="Sect1" text:protected="true" text:name="Оглавление1">'
    '<text:table-of-content-source text:outline-level="2">'
    '<text:index-title-template text:style-name="Contents_20_Heading">Содержание</text:index-title-template>'
    + "".join(
        f'<text:table-of-content-entry-template text:outline-level="{lv}" text:style-name="Contents_20_{lv}">'
        '<text:index-entry-link-start text:style-name="Index_20_Link"/><text:index-entry-chapter/>'
        '<text:index-entry-text/><text:index-entry-tab-stop style:type="right" style:leader-char="."/>'
        '<text:index-entry-page-number/><text:index-entry-link-end/></text:table-of-content-entry-template>'
        for lv in (1, 2))
    + '</text:table-of-content-source><text:index-body>'
    '<text:index-title text:style-name="Sect1" text:name="Оглавление1_Head">'
    '<text:p text:style-name="Contents_20_Heading">Содержание</text:p></text:index-title>'
    '</text:index-body></text:table-of-content>')

AUTO = """
<style:style style:name="PTitleFirst" style:family="paragraph" style:parent-style-name="Text_20_body" style:master-page-name="First_20_Page"><style:paragraph-properties fo:text-align="center" fo:text-indent="0cm" style:auto-text-indent="false" style:page-number="auto"/></style:style>
<style:style style:name="PCenter" style:family="paragraph" style:parent-style-name="Text_20_body"><style:paragraph-properties fo:text-align="center" fo:text-indent="0cm" style:auto-text-indent="false"/></style:style>
<style:style style:name="PTitleBig" style:family="paragraph" style:parent-style-name="Text_20_body"><style:paragraph-properties fo:text-align="center" fo:text-indent="0cm" style:auto-text-indent="false"/><style:text-properties fo:font-size="16pt" fo:font-weight="bold" style:font-size-asian="16pt" style:font-weight-asian="bold" style:font-size-complex="16pt" style:font-weight-complex="bold"/></style:style>
<style:style style:name="PNote" style:family="paragraph" style:parent-style-name="Text_20_body"><style:paragraph-properties fo:line-height="100%" fo:margin-top="0.2cm"/><style:text-properties fo:font-size="12pt"/></style:style>
<style:style style:name="PTabCap" style:family="paragraph" style:parent-style-name="Table"><style:paragraph-properties fo:text-align="start" fo:margin-top="0.4cm" fo:margin-bottom="0.1cm" fo:keep-with-next="always"/></style:style>
<style:style style:name="PAfterTable" style:family="paragraph" style:parent-style-name="Text_20_body"><style:paragraph-properties fo:line-height="100%" fo:margin-bottom="0cm"/><style:text-properties fo:font-size="8pt"/></style:style>
<style:style style:name="PCell" style:family="paragraph" style:parent-style-name="Table_20_Contents"><style:paragraph-properties fo:text-align="center" fo:text-indent="0cm" style:auto-text-indent="false" fo:line-height="100%"/></style:style>
<style:style style:name="PCellHead" style:family="paragraph" style:parent-style-name="Table_20_Contents"><style:paragraph-properties fo:text-align="center" fo:text-indent="0cm" style:auto-text-indent="false" fo:line-height="100%"/><style:text-properties fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold"/></style:style>
<style:style style:name="Cell" style:family="table-cell"><style:table-cell-properties style:vertical-align="middle" fo:padding="0.102cm" fo:border="0.5pt solid #000000"/></style:style>
<style:style style:name="TB" style:family="text"><style:text-properties fo:font-weight="bold" style:font-weight-asian="bold" style:font-weight-complex="bold"/></style:style>
<style:style style:name="TI" style:family="text"><style:text-properties fo:font-style="italic" style:font-style-asian="italic" style:font-style-complex="italic"/></style:style>
<style:style style:name="TSub" style:family="text"><style:text-properties style:text-position="sub 58%"/></style:style>
<style:style style:name="TSup" style:family="text"><style:text-properties style:text-position="super 58%"/></style:style>
<style:style style:name="frF" style:family="graphic" style:parent-style-name="Formula"><style:graphic-properties style:vertical-pos="middle" style:vertical-rel="text" draw:ole-draw-aspect="1"/></style:style>
<style:style style:name="frImg" style:family="graphic" style:parent-style-name="Graphics"><style:graphic-properties style:vertical-pos="top" style:vertical-rel="baseline" style:horizontal-pos="center" style:horizontal-rel="paragraph"/></style:style>
<style:style style:name="Sect1" style:family="section"><style:section-properties style:editable="false"><style:columns fo:column-count="1" fo:column-gap="0cm"/></style:section-properties></style:style>
"""

styles_xml = open("template_styles.xml", encoding="utf-8").read()
root = re.search(r"<office:document-styles[^>]*>", styles_xml).group(0)
root = root.replace("office:document-styles", "office:document-content")
seq = ('<text:sequence-decls><text:sequence-decl text:display-outline-level="0" text:name="Illustration"/>'
       '<text:sequence-decl text:display-outline-level="0" text:name="Table"/>'
       '<text:sequence-decl text:display-outline-level="0" text:name="Text"/>'
       '<text:sequence-decl text:display-outline-level="0" text:name="Drawing"/>'
       '<text:sequence-decl text:display-outline-level="0" text:name="Figure"/></text:sequence-decls>')
content = ('<?xml version="1.0" encoding="UTF-8"?>\n' + root
           + "<office:automatic-styles>" + AUTO + "".join(table_styles) + "</office:automatic-styles>"
           + '<office:body><office:text text:use-soft-page-breaks="true">' + seq
           + "".join(body).replace("@@TOC@@", TOC)
           + "</office:text></office:body></office:document-content>")

MATH = ('<?xml version="1.0" encoding="UTF-8"?>\n<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">'
        '<semantics><mrow><mi>x</mi></mrow><annotation encoding="StarMath 5.0">{}</annotation></semantics></math>')

manifest = ['<?xml version="1.0" encoding="UTF-8"?>\n<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.4">',
            '<manifest:file-entry manifest:full-path="/" manifest:version="1.4" manifest:media-type="application/vnd.oasis.opendocument.text"/>',
            '<manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>',
            '<manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>',
            '<manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>']
meta = ('<?xml version="1.0" encoding="UTF-8"?>\n<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" office:version="1.4"><office:meta>'
        '<dc:title>Зарядка и разрядка RC-цепи</dc:title><dc:creator>Тлеспаев Э.Е.</dc:creator>'
        '</office:meta></office:document-meta>')

tmp = tempfile.mkdtemp(dir=os.environ.get("BUILD_TMP"))
raw = os.path.join(tmp, "raw.odt")
with zipfile.ZipFile(raw, "w") as z:
    z.writestr("mimetype", "application/vnd.oasis.opendocument.text", compress_type=zipfile.ZIP_STORED)
    z.writestr("content.xml", content, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("styles.xml", styles_xml, compress_type=zipfile.ZIP_DEFLATED)
    z.writestr("meta.xml", meta, compress_type=zipfile.ZIP_DEFLATED)
    for i, (name, sm) in enumerate(formulas.items(), 1):
        z.writestr(f"Object {i}/content.xml", MATH.format(escape(sm)), compress_type=zipfile.ZIP_DEFLATED)
        manifest.append(f'<manifest:file-entry manifest:full-path="Object {i}/content.xml" manifest:media-type="text/xml"/>')
        manifest.append(f'<manifest:file-entry manifest:full-path="Object {i}/" manifest:version="1.4" '
                        'manifest:media-type="application/vnd.oasis.opendocument.formula"/>')
    for arc, src in images:
        z.write(src, arc, compress_type=zipfile.ZIP_STORED)
        mt = "image/png" if arc.endswith(".png") else "image/jpeg"
        manifest.append(f'<manifest:file-entry manifest:full-path="{arc}" manifest:media-type="{mt}"/>')
    manifest.append("</manifest:manifest>")
    z.writestr("META-INF/manifest.xml", "\n".join(manifest), compress_type=zipfile.ZIP_DEFLATED)
json.dump(formulas, open(os.path.join(tmp, "formulas.json"), "w", encoding="utf-8"), ensure_ascii=False)

# ---------------------------------------------------------------- доводка в LibreOffice
# Через UNO: задаём текст формул, обновляем оглавление и номера, сохраняем ODT и PDF.
FINALIZE = r'''
import json, sys, time, uno
from com.sun.star.beans import PropertyValue

def prop(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p

raw, out, pdf, fjson, port = sys.argv[1:6]
local = uno.getComponentContext()
resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
for _ in range(60):
    try:
        ctx = resolver.resolve(f"uno:socket,host=localhost,port={port};urp;StarOffice.ComponentContext")
        break
    except Exception:
        time.sleep(0.5)
desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(raw), "_blank", 0, (prop("Hidden", True),))
formulas = json.load(open(fjson, encoding="utf-8"))
objs = doc.getEmbeddedObjects()
for name in objs.getElementNames():
    m = objs.getByName(name).getEmbeddedObject()
    m.Formula = formulas[name]
    m.BaseFontHeight = 14
doc.getTextFields().refresh()
idx = doc.getDocumentIndexes()
for i in range(idx.getCount()):
    idx.getByIndex(i).update()
doc.refresh()
for i in range(idx.getCount()):
    idx.getByIndex(i).update()
doc.storeToURL(uno.systemPathToFileUrl(out), (prop("FilterName", "writer8"),))
doc.storeToURL(uno.systemPathToFileUrl(pdf), (prop("FilterName", "writer_pdf_Export"),))
doc.close(True)
'''
fin = os.path.join(tmp, "finalize.py")
open(fin, "w").write(FINALIZE)
port = "2099"
office = subprocess.Popen(["soffice", "--headless", "--invisible", "--norestore",
                           f"-env:UserInstallation=file://{tmp}/profile",
                           f"--accept=socket,host=localhost,port={port};urp;"])
try:
    subprocess.run(["python3", fin, raw, OUT, PDF, os.path.join(tmp, "formulas.json"), port], check=True)
finally:
    office.terminate()
    time.sleep(1)
    if not os.environ.get("BUILD_KEEP"):
        shutil.rmtree(tmp, ignore_errors=True)
print("Готово:", OUT)
