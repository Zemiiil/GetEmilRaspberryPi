#include <iostream>
#include <fstream>
#include <chrono>
#include <random>
#include <cmath>

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
    static default_random_engine e(54);

    uniform_int_distribution<int> d(-1000000, 1000000);

    return d(e);
}


void heapify(int* a, int n, int i)
{
    int largest = i;

    int left = 2 * i + 1;
    int right = 2 * i + 2;


    if(left < n && a[left] > a[largest])
    {
        largest = left;
    }

    if(right < n && a[right] > a[largest])
    {
        largest = right;
    }


    if(largest != i)
    {
        int temp = a[i];
        a[i] = a[largest];
        a[largest] = temp;

        heapify(a, n, largest);
    }
}


void heap_sort(int* a, int n)
{

    for(int i = n / 2 - 1; i >= 0; i--)
    {
        heapify(a, n, i);
    }



    for(int i = n - 1; i > 0; i--)
    {
        int temp = a[0];
        a[0] = a[i];
        a[i] = temp;

        heapify(a, i, 0);
    }
}

int partition_hoare(int* a, int left, int right)
{
    int pivot = a[(left + right) / 2];

    int i = left - 1;
    int j = right + 1;


    while(true)
    {
        do
        {
            i++;
        }
        while(a[i] < pivot);


        do
        {
            j--;
        }
        while(a[j] > pivot);


        if(i >= j)
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
    if(left < right)
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


    while(i <= middle && j <= right)
    {
        if(a[i] <= a[j])
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


    while(i <= middle)
    {
        temp[k] = a[i];
        i++;
        k++;
    }


    while(j <= right)
    {
        temp[k] = a[j];
        j++;
        k++;
    }


    for(i = left; i <= right; i++)
    {
        a[i] = temp[i];
    }
}


void merge_sort(int* a, int* temp, int left, int right)
{
    if(left >= right)
    {
        return;
    }


    int middle = (left + right) / 2;


    merge_sort(a, temp, left, middle);

    merge_sort(a, temp, middle + 1, right);

    merge(a, temp, left, middle, right);
}
void massive_initialization(int* a, int n)
{
    for(int i = 0; i < n; i++)
    {
        a[i] = rand_uns();
    }
}



int main()
{
    ofstream f("fast_sort.csv");

    f << "N,heap,quick,merge\n";


    for(int i = 0; i < 10; i++)
    {
        int n = N[i];



        int source[100000];

  
        int heap_array[100000];
        int quick_array[100000];
        int merge_array[100000];


        int temp[100000];



        massive_initialization(source, n);


        for(int j = 0; j < n; j++)
        {
            heap_array[j] = source[j];
            quick_array[j] = source[j];
            merge_array[j] = source[j];
        }


        auto start = chrono::high_resolution_clock::now();

        heap_sort(heap_array, n);

        auto end = chrono::high_resolution_clock::now();

        double heap_time =
            chrono::duration<double>(end - start).count();


        volatile int check1 = heap_array[0];


        start = chrono::high_resolution_clock::now();

        quick_sort(quick_array, 0, n - 1);

        end = chrono::high_resolution_clock::now();

        double quick_time =
            chrono::duration<double>(end - start).count();


        volatile int check2 = quick_array[0];


        start = chrono::high_resolution_clock::now();

        merge_sort(merge_array, temp, 0, n - 1);

        end = chrono::high_resolution_clock::now();

        double merge_time =
            chrono::duration<double>(end - start).count();


        volatile int check3 = merge_array[0];



        cout << "N = " << n << endl;

        cout << "Heap:  "
             << heap_time
             << " sec" << endl;

        cout << "Quick: "
             << quick_time
             << " sec" << endl;

        cout << "Merge: "
             << merge_time
             << " sec" << endl;

        cout << endl;


        // Запись в CSV
        f << n << ","
          << heap_time << ","
          << quick_time << ","
          << merge_time << "\n";
    }


    f.close();


    cout << "Results saved to fast_sort.csv" << endl;


    return 0;
}