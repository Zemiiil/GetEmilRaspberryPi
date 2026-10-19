#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>
using namespace std;
int main()
{
    cout.precision(10);
    float a[3]={10000001.0f, 1000000100.0f, -1000000619.0f};
    float sum = a[1]+a[2]+a[0];
    cout<<sum<<endl;
    sum = a[0]+a[1]+a[2];
    cout<<sum;
}