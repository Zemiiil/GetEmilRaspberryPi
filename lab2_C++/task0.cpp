#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>
using namespace std;

unsigned long long int my_pow(unsigned long long int x,
unsigned long long int n)
{
    unsigned long long int result=1;
    for (unsigned long long int i=0; i<n;i++)
    {
        result*=x;
    }
    return result;
}
int main()
{
    cout << fixed;
    cout.precision(1);

    const unsigned long long int base = 3;

    cout << "float\n";
    cout << "n\tmy_pow\t\tstd::pow(float)\n";
    for (int n = 0; n <= 40; n++)
    {
        unsigned long long exact = my_pow(base, n);
        float approx = pow(static_cast<float>(base), static_cast<float>(n));
        cout << n << "\t" << exact << "\t\t" << approx << endl;
    }

    cout << "\ndouble\n";
    cout << "n\tmy_pow\t\tstd::pow(double)\n";
    for (int n = 0; n <= 40; n++)
    {
        unsigned long long exact = my_pow(base, n);
        double approx = pow(static_cast<double>(base), static_cast<double>(n));
        cout << n << "\t" << exact << "\t\t" << approx << endl;
    }

    return 0;
}