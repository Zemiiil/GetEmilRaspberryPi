# Сборка отчёта: report.md -> ../Отчёт_RC.odt (нужен pandoc).
# После pandoc добавляем таблицам рамки.
import subprocess
import zipfile

SRC = "report.md"
OUT = "../Отчёт_RC.odt"
BORDER = 'fo:border="0.5pt solid #000000" fo:padding="0.1cm"'

subprocess.run(["pandoc", SRC, "-o", OUT], check=True)

with zipfile.ZipFile(OUT) as z:
    files = {n: z.read(n) for n in z.namelist()}

content = files["content.xml"].decode("utf-8")
content = content.replace('<style:table-cell-properties fo:border="none" />',
                          f"<style:table-cell-properties {BORDER} />")
files["content.xml"] = content.encode("utf-8")

with zipfile.ZipFile(OUT, "w") as z:
    z.writestr("mimetype", files.pop("mimetype"), compress_type=zipfile.ZIP_STORED)
    for name, data in files.items():
        z.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)
print("Готово:", OUT)
