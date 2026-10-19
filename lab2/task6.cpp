#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>
using namespace std;
int main()
{
    cout.precision(10);
    float a[3]={10000000.0f, 100000000.0f, 10000019.0f};
    float sum = a[1]+a[2]+a[0];
    cout<<sum;
}