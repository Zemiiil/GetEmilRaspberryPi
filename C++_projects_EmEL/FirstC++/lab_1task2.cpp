#include <iostream>
#include <fstream>
#include <chrono>
#include <random>

using namespace std;



int N[] = {
    100,
    200,
    400,
    800,
    1600,
    3200,
    6400,
    12800,
    25600,
    53200
};


int rand_uns()
{
    unsigned seed =
        chrono::steady_clock::now().time_since_epoch().count();

    static default_random_engine e(54);

    uniform_int_distribution<int> d(-1000000, 1000000);

    return d(e);
}


void bubble_sort(int* a, int n)
{
    for(int i = 0; i < n - 1; i++)
    {
        for(int j = 0; j < n - i - 1; j++)
        {
            if(a[j] > a[j + 1])
            {
                int temp = a[j];
                a[j] = a[j + 1];
                a[j + 1] = temp;
            }
        }
    }
}



void massive_inzialization(int* a, int n)
{
    for(int i = 0; i < n; i++)
    {
        a[i] = rand_uns();
    }
}


int main()
{
    ofstream f("data-3.csv");

    f << "N,bubble\n";


    for(int i = 0; i < 10; i++)
    {
        int n = N[i];

        int a[100000];
        int bubble_array[100000];


        massive_inzialization(a, n);

        for(int j = 0; j < n; j++)
        {
            bubble_array[j] = a[j];
        }


        auto start = chrono::high_resolution_clock::now();


        bubble_sort(bubble_array, n);



        auto end = chrono::high_resolution_clock::now();



        double bubble_time =
            chrono::duration<double>(end - start).count();


        cout << "N = " << n << endl;
        cout << "Bubble: " << bubble_time << " sec" << endl;
        cout << endl;

        f << n << "," << bubble_time << "\n";
    }


    f.close();

    cout << "Results saved to data-1.csv" << endl;

    return 0;
}