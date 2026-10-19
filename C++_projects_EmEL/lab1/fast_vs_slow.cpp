#include <iostream>
#include <fstream>
#include <chrono>
#include <random>
#include <iomanip>

using namespace std;

const int N[] = {100, 200, 400, 800, 1600, 3200, 6400, 12800};
const int SIZE_COUNT = sizeof(N) / sizeof(N[0]);
const int MAX_N = 12800;

int source[MAX_N];
int bubble_array[MAX_N];
int selection_array[MAX_N];
int insertion_array[MAX_N];
int heap_array[MAX_N];
int quick_array[MAX_N];
int merge_array[MAX_N];
int temp_array[MAX_N];

int rand_uns()
{
    static default_random_engine e(54);
    uniform_int_distribution<int> d(-1000000, 1000000);
    return d(e);
}

void massive_initialization(int* a, int n)
{
    for (int i = 0; i < n; i++)
    {
        a[i] = rand_uns();
    }
}

void copy_array(const int* source_array, int* destination, int n)
{
    for (int i = 0; i < n; i++)
    {
        destination[i] = source_array[i];
    }
}


//Сортировки O(N^2)

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

// Heap sort: O(N log N)
void heapify(int* a, int n, int i)
{
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && a[left] > a[largest])
    {
        largest = left;
    }

    if (right < n && a[right] > a[largest])
    {
        largest = right;
    }

    if (largest != i)
    {
        int temp = a[i];
        a[i] = a[largest];
        a[largest] = temp;
        heapify(a, n, largest);
    }
}

void heap_sort(int* a, int n)
{
    for (int i = n / 2 - 1; i >= 0; i--)
    {
        heapify(a, n, i);
    }

    for (int i = n - 1; i > 0; i--)
    {
        int temp = a[0];
        a[0] = a[i];
        a[i] = temp;
        heapify(a, i, 0);
    }
}

//Quick sort Hoare: в среднем O(N log N)
int partition_hoare(int* a, int left, int right)
{
    int pivot = a[left + (right - left) / 2];
    int i = left - 1;
    int j = right + 1;

    while (true)
    {
        do
        {
            i++;
        }
        while (a[i] < pivot);

        do
        {
            j--;
        }
        while (a[j] > pivot);

        if (i >= j)
        {
            return j;
        }

        int temp = a[i];
        a[i] = a[j];
        a[j] = temp;
    }
}

void quick_sort(int* a, int left, int right)
{
    if (left < right)
    {
        int split = partition_hoare(a, left, right);
        quick_sort(a, left, split);
        quick_sort(a, split + 1, right);
    }
}

//Merge sort: O(N log N) 

void merge(int* a, int* temp, int left, int middle, int right)
{
    int i = left;
    int j = middle + 1;
    int k = left;

    while (i <= middle && j <= right)
    {
        if (a[i] <= a[j])
        {
            temp[k] = a[i];
            i++;
        }
        else
        {
            temp[k] = a[j];
            j++;
        }
        k++;
    }

    while (i <= middle)
    {
        temp[k] = a[i];
        i++;
        k++;
    }

    while (j <= right)
    {
        temp[k] = a[j];
        j++;
        k++;
    }

    for (i = left; i <= right; i++)
    {
        a[i] = temp[i];
    }
}

void merge_sort(int* a, int* temp, int left, int right)
{
    if (left >= right)
    {
        return;
    }

    int middle = left + (right - left) / 2;
    merge_sort(a, temp, left, middle);
    merge_sort(a, temp, middle + 1, right);
    merge(a, temp, left, middle, right);
}

int main()
{
    const char* output_filename = "O3.csv.csv";
    ofstream f(output_filename);

    if (!f.is_open())
    {
        cout << "Error: cannot create CSV file " << output_filename << endl;
        return 1;
    }

    f << "N,bubble,selection,insertion,heap,quick,merge\n";
    f << setprecision(10);

    for (int p = 0; p < SIZE_COUNT; p++)
    {
        int n = N[p];

        massive_initialization(source, n);
        copy_array(source, bubble_array, n);
        copy_array(source, selection_array, n);
        copy_array(source, insertion_array, n);
        copy_array(source, heap_array, n);
        copy_array(source, quick_array, n);
        copy_array(source, merge_array, n);

        auto start = chrono::steady_clock::now();
        bubble_sort(bubble_array, n);
        auto end = chrono::steady_clock::now();
        double bubble_time = chrono::duration<double>(end - start).count();

        start = chrono::steady_clock::now();
        selection_sort(selection_array, n);
        end = chrono::steady_clock::now();
        double selection_time = chrono::duration<double>(end - start).count();
        start = chrono::steady_clock::now();
        insertion_sort(insertion_array, n);
        end = chrono::steady_clock::now();
        double insertion_time = chrono::duration<double>(end - start).count();

        start = chrono::steady_clock::now();
        heap_sort(heap_array, n);
        end = chrono::steady_clock::now();
        double heap_time = chrono::duration<double>(end - start).count();

        start = chrono::steady_clock::now();
        quick_sort(quick_array, 0, n - 1);
        end = chrono::steady_clock::now();
        double quick_time = chrono::duration<double>(end - start).count();

        start = chrono::steady_clock::now();
        merge_sort(merge_array, temp_array, 0, n - 1);
        end = chrono::steady_clock::now();
        double merge_time = chrono::duration<double>(end - start).count();

        cout << "N = " << n << '\n';
        cout << "Bubble:    " << bubble_time << " sec\n";
        cout << "Selection: " << selection_time << " sec\n";
        cout << "Insertion: " << insertion_time << " sec\n";
        cout << "Heap:      " << heap_time << " sec\n";
        cout << "Quick:     " << quick_time << " sec\n";
        cout << "Merge:     " << merge_time << " sec\n\n";

        f << n << ','
          << bubble_time << ','
          << selection_time << ','
          << insertion_time << ','
          << heap_time << ','
          << quick_time << ','
          << merge_time << '\n';
    }

    f.close();
    cout << "Results saved to " << output_filename << endl;
    return 0;
}
