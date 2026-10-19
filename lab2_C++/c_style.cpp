#include <iostream>
#include <iomanip>
#include <limits>

using  std::cout, std::endl;

int main()
{
    float F = -123.456f; //число, с которым будем работать
    //Сразу настроим вывод float так, чтобы видеть больше знаков
    cout << std::fixed << std::setprecision(std::numeric_limits<float>::max_digits10);
    cout << "Our float is "<< F << endl; //Так-то лучше

    char c[32], r[32]; //массивы для бинарных разложений
    for(int i=0; i<32; i++) {c[i]=0; r[i]=0;} //Заполняет их нулями

    r[0] = (F < 0.0f); //нулевой бит - это знак числа
    cout<< "The sign bit is [" << (int)r[0] << "]" << endl;

    float f = F > 0.0f ? F : -F; //модуль числа
    int IP = f; //Целая часть
    float FP = f - IP; //дробная часть
    cout << "|f| is " << f << " = " << IP << " + " << FP << endl;
    cout << endl << "Integral part is " << IP << endl;

    int ipb = 0; //число бит для целой части - integer part bites
    for(int i=31; i>=0; i--)
    {
        ipb++;
        c[i] = IP%2;
        cout << IP << "%2\t= [" << (int)c[i] << "]   " << IP << "/2\t= ";
        IP = IP/2;
        cout << IP << endl;
        if (IP==0) break; //Целая часть закончилась
    }
    cout << endl << "Integral part bits are:" << endl << "[";
    for(int i=32-ipb; i<32;i++)
        cout << (int)c[i];
    cout << "]" << endl;

    cout<<endl<<"Fractional part is " << FP << endl;
    int fpb = 0; //чило бит для дробной части - fractionsl part bites
    while (c[0]==0)
    {
        if (FP==0.0f) break; //Дробная часть закончилась
        fpb++;
        for(int i=0;i<31;i++)
            c[i]=c[i+1];
        cout<<FP<<"*2 = ";
        FP *= 2.0f;
        cout << FP << "   The bit is [" << (int)FP << "]" << endl;
        c[31] = FP;
        FP = FP>=1.0f ? FP-1.0f : FP;
    }

    cout << endl << "The floating point possition is " << fpb << endl;
    cout << f << " = [";
    for(int i=32-fpb-ipb; i<32; i++)
    {
        cout << (int)c[i];
        if (31-i == fpb) cout << '.';
    }
    cout << "]" << endl;
    int ex=0;//показатель экспоненты
    if (ipb>1) //если наше число больше 1, то все просто
        ex = ipb-1;
    else //иначе нужно сдвигать точку в другую сторону
        for(int i=32-fpb-ipb; i<32; i++)
        {
            if (c[i]==0) ex--;
            else break;
        }

    cout << "The exponent is " << ex << endl;
    fpb += ex; //сдвигаем точку на показатель экспоненты (степень двойки)
    cout << f << " = [";
    for(int i=31-fpb; i<32; i++)
    {
        cout << (int)c[i];
        if (31-i == fpb) cout << '.';
    }
    cout << " x 2^" << ex << "]" << endl;
    ex += 127;
    cout << endl << "127+exponent = " << ex;
    for(int i=8; i>0; i--) //заполняем масиив битами экспоненты
    {
        r[i] = ex%2;
        ex = ex/2;
    }
    cout << " = [";
    for(int i=1; i<9; i++) //выводит биты экспоненты
        cout << (int)r[i];
    cout << "]" << endl;

    for(int i=9; i<32; i++) //заполняем массив битами мантиссы
    {
        int j = 31-fpb+i-8;
        if(j>31) break;
        r[i] = c[j];
    }
    //Окончательно получили такие вот биты:
    cout << endl << " s exponent        mantissa         " << endl << "[";
    for(int i=0; i<32; i++)
    {
        if (i==1 || i==9) cout << ' ';
        cout<<(int)r[i];
    }
    cout << "]" << endl;

    cout << endl << "Binary to HEX:" << endl;
    char hex[8]; //массих для hex-символов
    for(int j=0; j<8; j++) //переводим двоичный вид в шестнадцатиричный
    {
        int block = 0;
        for(int i=0; i<4; i++)
        {
            cout << (int)r[j*4+i];
            block = block<<1;
            block += r[j*4+i];
        }
        cout << "\t=>\t" << block;
        hex[j] = block<10?'0'+block:'a'+block-10;
        cout << "\t=>\t" << hex[j] << endl;
    }
    cout << "Hex value is 0x";
    for(int j=0; j<8; j++)
        cout << hex[j];

    //Проверяем правильно ли у нас получилось
    cout << "\n\nThe UNION magic\nPushing bits to the integer!"<<endl;
    union U //UNION для перевода полученных бит обратно во FLOAT
    {
        unsigned i;
        float f;
    } u; //Объявляем структуру и сразу же создаем её экземпляр
    u.i = 0;
    for(int i=0; i<32; i++)//загружаем биты в INT
        u.i = (u.i<<1) + r[i];

    cout << "u.i is " << u.i << " ... but who cares ..." << endl;
    cout << "u.f is " << u.f << endl;

    return 0;
}