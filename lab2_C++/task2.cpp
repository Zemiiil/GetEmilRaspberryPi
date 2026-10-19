#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>
using namespace std;
void binary_zemil(unsigned int a)
{
    unsigned int m=0x80000000;
    for (unsigned int i=0; i<32; i++, m>>=1)
    {
        cout<< bool(a&m);
    }
}
int main()
{
    float F = 137.375f;

    union U
    {
        unsigned int i;
        float f;
    } u;

    u.f = F;
    cout<<u.i<<endl;
    cout << "Our float is " << F << endl;

    cout << "Float bits: ";
    binary_zemil(u.i);
    cout << endl;

    cout << "Sign bit: " << ((u.i >> 31) & 1u) << endl;

    cout << "Exponent: ";
    for (int bit = 30; bit >= 23; bit--)
    {
        cout << ((u.i >> bit) & 1u);
    }
    cout << endl;

    cout << "Mantissa: ";
    for (int bit = 22; bit >= 0; bit--)
    {
        cout << ((u.i >> bit) & 1u);
    }
    cout << endl;

    return 0;
}