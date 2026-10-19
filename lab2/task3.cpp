
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
    const unsigned long long int base = 3;

    cout << fixed;
    cout.precision(1);

    cout << "FLOAT\n";
    cout << "n\tmy_pow\t\tstd::pow(float)\tBits\n";

    for (int n = 0; n <= 40; n++)
    {
        unsigned long long exact = my_pow(base, n);

        float approx = pow(
            static_cast<float>(base),
            static_cast<float>(n));

        FloatBits bits;
        bits.f = approx;

        cout << n << "\t"
             << exact << "\t"
             << approx << "\t";

        binary_zemil(bits.i);
        cout << endl;
    }

    cout << "\nDOUBLE\n";

    cout << "n\tmy_pow\t\tstd::pow(double)\tBits\n";

    for (int n = 0; n <= 40; n++)
    {
        unsigned long long exact = my_pow(base, n);

        double approx = pow(
            static_cast<double>(base),
            static_cast<double>(n));

        DoubleBits bits;
        bits.d = approx;

        cout << n << "\t"
             << exact << "\t"
             << approx << "\t";

        binary_zemil64(bits.i);
        cout << endl;
    }

    return 0;
}