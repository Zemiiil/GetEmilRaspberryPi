#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>

using namespace std;
void binary_zemil(unsigned int a)
{
    unsigned int m = 0x80000000u;

    for (unsigned int i = 0; i < 32; i++, m >>= 1)
    {
        cout << bool(a & m);

        if ((i + 1) % 8 == 0 && i < 31)
            cout << " ";
    }
}
void binary_zemil64(unsigned long long a)
{
    unsigned long long m = 1ULL << 63;

    for (int i = 0; i < 64; i++, m >>= 1)
    {
        cout << bool(a & m);

        if ((i + 1) % 8 == 0 && i < 63)
            cout << " ";
    }
}

union FloatBits
{
    float f;
    unsigned int i;
};

union DoubleBits
{
    double d;
    unsigned long long i;
};

unsigned long long int my_pow(
    unsigned long long int x,
    unsigned long long int n)
{
    unsigned long long int result = 1;

    for (unsigned long long int i = 0; i < n; i++)
        result *= x;

    return result;
}

int main()
{
    cout << fixed;
    cout.precision(1);
    cout << "\nTask 4\n";
    float a =1.0f/0.0f;
    float b =-1.0f/0.0f;
    float c =a+b;
    float special[] =
    {
        a, b , c
    };

    const char* names[] = {"+inf", "-inf", "NaN"};

    cout << "\nfloat (32 bits):\n";

    for (int k = 0; k < 3; k++)
    {
        FloatBits bits;
        bits.f = special[k];

        cout << names[k] << ": ";
        binary_zemil(bits.i);
        cout << endl;
    }
    double d=1.0/0.0;
    double e=-1.0/0.0;
    double f=d+e;
    double specialD[] =
    {
        d,e,f
    };

    cout << "\ndouble (64 bits):\n";

    for (int k = 0; k < 3; k++)
    {
        DoubleBits bits;
        bits.d = specialD[k];

        cout << names[k] << ": ";
        binary_zemil64(bits.i);
        cout << endl;
    }
    return 0;
}