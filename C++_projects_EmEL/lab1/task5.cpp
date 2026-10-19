#include <iostream>
#include <fstream>
#include <chrono>
#include <random>

using namespace std;

const int N[] = {10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 53200};
const int SIZE_COUNT = sizeof(N) / sizeof(N[0]);
const int MAX_N = 53200;

int source[MAX_N];
int source_random[MAX_N];
int work[MAX_N];
int temp_array[MAX_N];

void sorted(int* a, int n)
{
    for (int i = 0; i < n; i++)
    {
        a[i] = i;
    }
}
int rand_uns()
{
    unsigned seed =
        chrono::steady_clock::now().time_since_epoch().count();

    static default_random_engine e(seed);

    uniform_int_distribution<int> d(-1000000, 1000000);

    return d(e);
}
void random(int* a, int n)
{
    for(int i = 0; i < n; i++)
    {
        a[i] = rand_uns();
    }
}

void reverse(int* a, int n)
{
    for (int i = 0; i < n; i++)
    {
        a[i] = n - i;
    }
}

void copy_array(const int* from, int* to, int n)
{
    for (int i = 0; i < n; i++)
    {
        to[i] = from[i];
    }
}


void bubble_sort(int* a, int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++)
        {
            if (a[j] > a[j + 1])
            {
                int t = a[j];
                a[j] = a[j + 1];
                a[j + 1] = t;
                swapped = true;
            }
        }
        if (!swapped)
        {
            break;
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
        int t = a[i];
        a[i] = a[min_index];
        a[min_index] = t;
    }
}

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
        int t = a[i];
        a[i] = a[largest];
        a[largest] = t;
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
        int t = a[0];
        a[0] = a[i];
        a[i] = t;
        heapify(a, i, 0);
    }
}

int partition_hoare(int* a, int left, int right)
{
    int pivot = a[(left + right) / 2];
    int i = left - 1;
    int j = right + 1;

    while (true)
    {
        do { i++; } while (a[i] < pivot);
        do { j--; } while (a[j] > pivot);

        if (i >= j)
        {
            return j;
        }

        int t = a[i];
        a[i] = a[j];
        a[j] = t;
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

void merge(int* a, int* temp, int left, int middle, int right)
{
    int i = left;
    int j = middle + 1;
    int k = left;

    while (i <= middle && j <= right)
    {
        if (a[i] <= a[j])
        {
            temp[k++] = a[i++];
        }
        else
        {
            temp[k++] = a[j++];
        }
    }
    while (i <= middle)
    {
        temp[k++] = a[i++];
    }
    while (j <= right)
    {
        temp[k++] = a[j++];
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

double measure_bubble(const int* base, int n)
{
    copy_array(base, work, n);
    auto start = chrono::steady_clock::now();
    bubble_sort(work, n);
    auto end = chrono::steady_clock::now();
    return chrono::duration<double>(end - start).count();
}

double measure_insertion(const int* base, int n)
{
    copy_array(base, work, n);
    auto start = chrono::steady_clock::now();
    insertion_sort(work, n);
    auto end = chrono::steady_clock::now();
    return chrono::duration<double>(end - start).count();
}

double measure_selection(const int* base, int n)
{
    copy_array(base, work, n);
    auto start = chrono::steady_clock::now();
    selection_sort(work, n);
    auto end = chrono::steady_clock::now();
    return chrono::duration<double>(end - start).count();
}

double measure_heap(const int* base, int n)
{
    copy_array(base, work, n);
    auto start = chrono::steady_clock::now();
    heap_sort(work, n);
    auto end = chrono::steady_clock::now();
    return chrono::duration<double>(end - start).count();
}

double measure_quick(const int* base, int n)
{
    copy_array(base, work, n);
    auto start = chrono::steady_clock::now();
    quick_sort(work, 0, n - 1);
    auto end = chrono::steady_clock::now();
    return chrono::duration<double>(end - start).count();
}

double measure_merge(const int* base, int n)
{
    copy_array(base, work, n);
    auto start = chrono::steady_clock::now();
    merge_sort(work, temp_array, 0, n - 1);
    auto end = chrono::steady_clock::now();
    return chrono::duration<double>(end - start).count();
}

int main()
{
    ofstream f("task5.csv");

    f << "N,"
      << "bubble_sorted,bubble_random,bubble_reverse,"
      << "insertion_sorted,insertion_random,insertion_reverse,"
      << "selection_sorted,selection_random,selection_reverse,"
      << "heap_sorted,heap_random,heap_reverse,"
      << "merge_sorted,merge_random,merge_reverse,"
      << "quick_sorted,quick_random,quick_reverse\n";


    for (int i = 0; i < SIZE_COUNT; i++)
    {
        int n = N[i];
        double bubble_time[3];
        double insertion_time[3];
        double selection_time[3];
        double heap_time[3];
        double merge_time[3];
        double quick_time[3];

        random(source, n);
        for (int i = 0; i < n; i++)
        {
            source_random[i] = source[i];
        }

        bubble_time[1] = measure_bubble(source_random, n);
        insertion_time[1] = measure_insertion(source_random, n);
        selection_time[1] = measure_selection(source_random, n);
        heap_time[1] = measure_heap(source_random, n);
        merge_time[1] = measure_merge(source_random, n);
        quick_time[1] = measure_quick(source_random, n);
        
        sorted(source, n);
        bubble_time[0] = measure_bubble(source, n);
        insertion_time[0] = measure_insertion(source, n);
        selection_time[0] = measure_selection(source, n);
        heap_time[0] = measure_heap(source, n);
        merge_time[0] = measure_merge(source, n);
        quick_time[0] = measure_quick(source, n);

        reverse(source, n);
        bubble_time[2] = measure_bubble(source, n);
        insertion_time[2] = measure_insertion(source, n);
        selection_time[2] = measure_selection(source, n);
        heap_time[2] = measure_heap(source, n);
        merge_time[2] = measure_merge(source, n);
        quick_time[2] = measure_quick(source, n);

        cout << "N = " << n << " finished" << endl;
        f << n << ","
          << bubble_time[0] << "," << bubble_time[1] << "," << bubble_time[2] << ","
          << insertion_time[0] << "," << insertion_time[1] << "," << insertion_time[2] << ","
          << selection_time[0] << "," << selection_time[1] << "," << selection_time[2] << ","
          << heap_time[0] << "," << heap_time[1] << "," << heap_time[2] << ","
          << merge_time[0] << "," << merge_time[1] << "," << merge_time[2] << ","
          << quick_time[0] << "," << quick_time[1] << "," << quick_time[2] << "\n";
    }

    f.close();
    cout << "Results saved to task5.csv" << endl;
    return 0;
}
