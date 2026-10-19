#include <iostream>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <cmath>
#include <limits>
using namespace std;
const unsigned int N=10;
int main()
{   
    unsigned int number_of_rectangles[N]={5,10,30,50,70,100,150,200,300,500};
    float divisions[N];
    float values[N][500];
    float sum[N]={0};
    double divisions_d[N];
    double values_d[N][500];
    double sum_d[N]={0};

    for (unsigned int i=0;i<N;i++)
    {
        divisions[i]=1.0f/number_of_rectangles[i];
        divisions_d[i]=1.0/number_of_rectangles[i];
    }
    for (unsigned int i=0;i<N;i++)
    {
        for(unsigned int j=0; j<number_of_rectangles[i];j++)
        {
            values[i][j]=sinh((j+1)*divisions[i]);
            values_d[i][j]=sinh((j+1)*divisions_d[i]);
        }
    }
    for (unsigned int i=0; i<N;i++)
    {
        for(unsigned int j=0; j<number_of_rectangles[i];j++)
        {
            sum[i]+=divisions[i]*values[i][j];
            sum_d[i]+=divisions_d[i]*values_d[i][j];
        }
    }

    double exact=cosh(1.0)-1.0;

    ofstream f("data.csv");
    f << setprecision(10);
    f << "n,float_sum,double_sum,exact\n";
    for (unsigned int i=0;i<N;i++)
    {
        f << number_of_rectangles[i] << ","
          << sum[i] << ","
          << sum_d[i] << ","
          << exact << "\n";
    }
    f.close();
}