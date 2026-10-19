#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdint>

using namespace std;

const int N[] = {100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 53200};
const int SIZE_COUNT = sizeof(N) / sizeof(N[0]);
const int MAX_N = 53200;

int source[MAX_N];
int work[MAX_N];
volatile long long checksum_sink = 0;

void massive_inzialization(int* a, int n)
{
    uint32_t state = 54u;

    for (int i = 0; i < n; i++)
    {
        state = state * 1664525u + 1013904223u;
        a[i] = static_cast<int>(state % 2000001u) - 1000000;
    }
}

void copy_array(const int* source_array, int* destination, int n)
{
    for (int i = 0; i < n; i++)
    {
        destination[i] = source_array[i];
    }
}

void bubble_sort(int* a, int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (a[j] > a[j + 1])
            {
                int temp = a[j];
                a[j] = a[j + 1];
                a[j + 1] = temp;
            }
        }
    }
}

void selection_sort(int* a, int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        int min_index = i;

        for (int j = i + 1; j < n; j++)
        {
            if (a[j] < a[min_index])
            {
                min_index = j;
            }
        }

        int temp = a[i];
        a[i] = a[min_index];
        a[min_index] = temp;
    }
}

void insertion_sort(int* a, int n)
{
    for (int i = 1; i < n; i++)
    {
        int key = a[i];
        int j = i - 1;

        while (j >= 0 && a[j] > key)
        {
            a[j + 1] = a[j];
            j--;
        }

        a[j + 1] = key;
    }
}

int main()
{
    ofstream f("cpp_simple.csv");

    if (!f.is_open())
    {
        cout << "Cannot create cpp_simple.csv" << endl;
        return 1;
    }

    f << "N,bubble,selection,insertion\n";

    for (int i = 0; i < SIZE_COUNT; i++)
    {
        int n = N[i];

        massive_inzialization(source, n);

        cout << "\nN = " << n << endl;

        copy_array(source, work, n);

        auto start = chrono::steady_clock::now();
        bubble_sort(work, n);
        auto end = chrono::steady_clock::now();

        double bubble_time = chrono::duration<double>(end - start).count();

        copy_array(source, work, n);

        start = chrono::steady_clock::now();
        selection_sort(work, n);
        end = chrono::steady_clock::now();

        double selection_time = chrono::duration<double>(end - start).count();

        copy_array(source, work, n);

        start = chrono::steady_clock::now();
        insertion_sort(work, n);
        end = chrono::steady_clock::now();

        double insertion_time = chrono::duration<double>(end - start).count();

        cout << "Bubble:    " << bubble_time << " sec" << endl;
        cout << "Selection: " << selection_time << " sec" << endl;
        cout << "Insertion: " << insertion_time << " sec" << endl;

        f << n << "," << bubble_time << ","
          << selection_time << "," << insertion_time << "\n";
    }

    f.close();
    cout << "\nResults saved to cpp_simple.csv" << endl;

    return 0;
}
