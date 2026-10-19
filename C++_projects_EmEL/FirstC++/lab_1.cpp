#include <iostream>
#include <fstream>
#include <chrono>
#include <random>

using namespace std;

int N[] = {100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 53200};

int rand_uns()
{
    unsigned seed =
        chrono::steady_clock::now().time_since_epoch().count();

    static default_random_engine e(seed);

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

void insertion_sort(int* a, int n)
{
    for(int i = 1; i < n; i++)
    {
        int key = a[i];
        int j = i - 1;

        while(j >= 0 && a[j] > key)
        {
            a[j + 1] = a[j];
            j--;
        }

        a[j + 1] = key;
    }
}

void selection_sort(int* a, int n)
{
    for(int i = 0; i < n - 1; i++)
    {
        int min_index = i;

        for(int j = i + 1; j < n; j++)
        {
            if(a[j] < a[min_index])
            {
                min_index = j;
            }
        }

        int temp = a[i];
        a[i] = a[min_index];
        a[min_index] = temp;
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
    ofstream f("data.csv");

    f << "N,bubble,selection,insertion\n";


    for(int i = 0; i < 10; i++)
    {
        int n = N[i];

        int a[100000];

        int bubble_array[100000];
        int selection_array[100000];
        int insertion_array[100000];

        massive_inzialization(a, n);

        for(int j = 0; j < n; j++)
        {
            bubble_array[j] = a[j];
            selection_array[j] = a[j];
            insertion_array[j] = a[j];
        }

        auto start = chrono::high_resolution_clock::now();

        bubble_sort(bubble_array, n);

        auto end = chrono::high_resolution_clock::now();

        double bubble_time =
            chrono::duration<double>(end - start).count();

        volatile int check1 = bubble_array[0];

        start = chrono::high_resolution_clock::now();

        selection_sort(selection_array, n);

        end = chrono::high_resolution_clock::now();

        double selection_time =
            chrono::duration<double>(end - start).count();

        volatile int check2 = selection_array[0];

        start = chrono::high_resolution_clock::now();

        insertion_sort(insertion_array, n);

        end = chrono::high_resolution_clock::now();

        double insertion_time =
            chrono::duration<double>(end - start).count();

        volatile int check3 = insertion_array[0];

        cout << "N = " << n << endl;
        cout << "Bubble:     " << bubble_time << " sec" << endl;
        cout << "Selection:  " << selection_time << " sec" << endl;
        cout << "Insertion:  " << insertion_time << " sec" << endl;
        cout << endl;

        f << n << ","
          << bubble_time << ","
          << selection_time << ","
          << insertion_time << "\n";
    }


    f.close();

    cout << "Results saved to data1.csv" << endl;

    return 0;
}