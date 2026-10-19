#include <iostream>
#include <iomanip>
using std::cout, std::endl;

void PrintBinaryOld(unsigned int a); //Самый первый способ вывода бинарного разложения целого числа.
void PrintBinaryShift(unsigned int a); //Новый способ с помощью оператора сдвига.
void PrintBinaryMatrix(unsigned int a); //Другой способ на основе логического битового оператора.
void PrintHex(unsigned int a); //Функция-помощник: шестнадцатиричный вид целого числа.

const unsigned int I = 8 * sizeof(int); //Константа - число бит в unsigned int.

int main()
{
    /// Шстнадцатиричный вид целого числа.
    /// 0001 0010 1000 1001 1010 1011 1100 1111 - это число 311012303.
    ///    1    2    8    9   10   11   12   15
    ///    1    2    8    9    a    b    c    f
    ///  0x1289abcf
    /// "0x" означает, что дальше будет число в шестнацатиричном формате.

    unsigned int a=0x1289abcf,
                 b=0x1f301;
    cout << "a=" << endl;
    PrintBinaryOld(a);
    cout << "b=" << endl;
    PrintBinaryOld(b);

    // Логические операторы
    cout << endl << "a|b - bitwise OR" << endl;
    PrintBinaryOld(a | b);
    cout << endl << "a&b - bitwise AND" << endl;
    PrintBinaryOld(a & b);
    cout << endl << "a^b - bitwise XOR" << endl;
    PrintBinaryOld(a ^ b);
    cout << endl << "~a  - bitwise NOT" << endl;
    PrintBinaryOld(~a);
    cout << "a=" << endl;
    PrintBinaryOld(a);
    // Операторы сдвига
    cout << endl << "a>>4" << endl;
    PrintBinaryOld(a >> 4);
    cout << "b=" << endl;
    PrintBinaryOld(b);
    cout << endl << "b<<1" << endl;
    PrintBinaryOld(b << 1);

    // Нюансы
    cout << endl << " >> vs signed and unsigned int" << endl;
    cout << "unsigned >> 1" << endl;
    unsigned int ui = -1;
    PrintBinaryOld(ui);
    PrintBinaryOld(ui >> 1);
    cout << "signed >> 1" << endl;
    int i = -5;
    PrintBinaryOld(i);
    PrintBinaryOld(i >> 3);

    cout << endl << " << vs short" << endl;
    unsigned short us = 0xffff;
    PrintBinaryOld(us);
    PrintBinaryOld(us << 1);
    us = us << 1;
    PrintBinaryOld(us);

    //Применяем это для написания удобных алгоритмов.
    cout << endl << "    (PrintBinaryShift)" << endl;
    PrintBinaryShift(a);
    cout << endl << "    (PrintBinaryMatrix)" << endl;
    PrintBinaryMatrix(b);

    return 0;
}

void PrintBinaryOld(unsigned int a)
{
    PrintHex(a);//Выведем число в шетнадцатиричном формате.
    for(unsigned int i = 0; i < I; i++) //Старый алгоритм с двумя циклами.
    {
        unsigned int b = a;
        for(unsigned int j = 0; j < I - i - 1; j++)
            b = b / 2;
        cout << b % 2;
        cout << ((i + 1) % 4 == 0 ? ' ': '\0'); //Пробелы между четверками бит.
    }
    cout << endl;
}

void PrintBinaryShift (unsigned int a)
{
    PrintHex(a);
    for(unsigned int i = 0; i < I; i++, a <<= 1) // a<<=1 это a=a<<1
        cout << !(a << 1 >> 1 == a) << ((i + 1) % 4 == 0 ? ' ': '\0'); //Магия, которую нужно освоить.
}

void PrintBinaryMatrix(unsigned int a)
{
    PrintHex(a);
    unsigned int m = 0x80000000; // матрица  1000 ... 0000 (32 цифры)
    for(unsigned int i = 0; i < I; i++, m >>= 1) //m после первого сдвига 010...000 (32 цифры)
        cout << bool(a & m) << ((i + 1) % 4 == 0 ? ' ': '\0'); //оператор & - битовое И, а (bool) упрощает результат до 0 или 1
}

void PrintHex(unsigned int a)
{
    cout << "0x" << std::hex << std::setfill('0') << std::setw(I / 4) << a << std::dec << " = ";
}


