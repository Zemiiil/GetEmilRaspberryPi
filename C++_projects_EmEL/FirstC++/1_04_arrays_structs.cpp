#include <iostream>
using std::cout, std::endl;

#define L 10 //Определим длину массивов заранее
const unsigned N = 3; //Так тоже можно

int arr[N] = {0, 1, 2};

struct SomeStruct // Название
{
    int a = 0;  //Собстенные переменные
    long b = 0; //Полезно задать переменным значения "по умолчанию"
};

struct AnotherStruct
{
    double a;
    float f_arr[L];         //Структура с массивом
    SomeStruct some;        //Структура со структурой
    SomeStruct some_arr[N]; //Структура с массивом структур
};

int main()
{
    //СТРУКТУРЫ

    SomeStruct some0;
    SomeStruct some1 = {2, 3};  //Простая инициализация экземпляра структуры.
    //some.a = 2; //То же самое
    //some.b = 3;
    SomeStruct some2 = some1;   //Структуры хорошо умеют копироваться.

    AnotherStruct another = //Сложную структуру тоже можно инициализировать с помощью {}.
    {
        3.15,                                                        //double a
       {0.1f, 0.2f, 0.3f, 0.4f, 0.5f, 0.6f, 0.7f, 0.7f, 0.9f, 1.0f}, //float f_arr[L]
       {4, 5},                                                       //SomeStruct some
       {some0, some1, another.some}                                  //SomeStruct some_arr[N]
    };

    some0.a = another.some.b; //Пример обращения к полям сложных структур.
    another.some_arr[1].b++; //То же в случае с массивом.

    struct NextStruct //Можно описывать структуры внутри функций.
    {
        SomeStruct some;
        AnotherStruct another;
    } next = {{0, 1}, another}; //Мы можем описать структуру и сразу же создать её экземпляр.

    next.another.some_arr[0].a = 1; //И можно пользоваться.
    another = next.another; //Одинаковые названия разных переменных компилятору не мешают.

    //МАССИВЫ

    // Неумелой работой с индексами можно испортить значения других переменных (а можно и не испортить)
    cout<<endl<<"\tData corruption"<<endl<<endl;

    int a = 22;
    int b = 33;
    int m[L];
    int c = 44;
    int d = 55;
    cout << "It was:" << endl;
    cout << "a= " << a << " b=" << b << " c=" << c << " d=" << d << endl;
    for(int i = -80; i < L + 80; i++) //Выход за границы массива.
        m[i] = i;
    cout << "...but then:" << endl;
    cout << "a= " << a << " b=" << b << " c=" << c << " d=" << d << endl;

    cout<<". . . . . . . . . . . . . . . . . ."<<endl;


    //Массив - это...
    cout << endl << "\tWho are You mr. m?" << endl << endl;
    cout << "m = " << m << endl;
    cout << "Can we do something weird?" << endl;
    for(int i = 0; i < L; i++)
        cout << (m + i)[0] << ' ';
    cout << endl << "Yes we can!" << endl;

    //m = m + 1; //Так нельзя. Менять само m нам пока не разрешают.
    ///error: incompatible types in assignment of ‘int*’ to ‘int [10]’|

    cout<<". . . . . . . . . . . . . . . . . ."<<endl;

    //Базовый метод сортировки
    cout << endl << "\tBasic bubble" << endl << endl;
    int arr[L] = {4, 2, 5, 2, 1, 0, 3, 8, 0, 1}; //Исходный массив
    cout << "Initial:" << endl;
    for (int i = 0; i < L; i++)
        cout<< arr[i] << " ";

    cout << endl << "Sorting..." << endl;
    for (int i = 0; i < L - 1; i++)   //Вложенные циклы
    {
        for (int j = 0; j < L - i - 1; j++)
            if (arr[j] > arr[j + 1])    //Меняем местами, если выполнено условие
            {
                int tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
            }
        for (int i = 0; i < L; i++) //Выводим промежуточный результат.
            cout << arr[i] << " ";
        cout << endl;
    }
    cout << "Finaly:" << endl;
    for (int i = 0; i < L; i++) //Окончательно.
        cout<< arr[i] << " ";

    cout<<endl<<". . . . . . . . . . . . . . . . . ."<<endl;

    //Сортировка с более сложным условием:
    //Сделать сначала четные по возрастанию, а затем нечетные по убыванию
    cout << endl << "\tAdvanced sorting" << endl << endl;
    cout << "Initial:" << endl;
    for (int i = 0; i < L; i++)
        cout << arr[i] << " ";
    cout << endl << "Sorting..." << endl;
    for (int i = 0; i < L - 1; i++)   //Вложенные циклы
    {
        for (int j = 0; j < L - i - 1; j++)
        {
            bool doSwap = false; //Можно разбивать булевские операции на отдельные выражения, чтобы не запутаться в сложной конструкции
            if (arr[j] % 2 != 0 && arr[j+1] %2 == 0) doSwap = true; //нечетное с четным всегда меняем местами
            if (arr[j] % 2 == 0 && arr[j+1] %2==0 && arr[j] > arr[j+1]) doSwap=true; //если оба четные, то проверяем возрастание
            if (arr[j] % 2 != 0 && arr[j+1] %2!=0 && arr[j] < arr[j+1]) doSwap=true; //если оба нечетные, то проверяем убывание
            if(doSwap) //Любое ДА приводит нас к перестановке элементов
            {
                int tmp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = tmp;
            }
        }
        for (int i=0; i < L; i++)
            cout<< arr[i] << " ";
        cout << endl;
    }
    cout << "Finaly:" << endl;
    for (int i = 0; i < L; i++)
        cout << arr[i] << " ";
    cout<<endl<<". . . . . . . . . . . . . . . . . ."<<endl;

    //Аналогично можно сортировать массивы структур
    cout << endl << "\tSorting structs" << endl << endl;

    struct Task //Нам понадобилась структура, опишем её прямо здесь.
    {
        int priority_high; //Параметр сортировки с высоким приоритетом.
        int priority_low;  //Параметр с низким приоритетом (работает во вторую очередь).
    } //Тут нет _;_. Она дальше.
    task_arr[L] = {{0,4}, {7,2}, {1,1}, {5,8}, {9,0}, {1,3}, {4,7}, {2,1}, {0,9}, {0,4}}; //Тут _;_.
    //Объявили массив экземпляров и инициализировали каждый из них.

    cout << "Initial:" << endl;
    cout << "HP: ";
    for (int i = 0; i < L; i++)
        cout << task_arr[i].priority_high << " ";
    cout << endl<< "LP: ";
    for (int i = 0; i < L; i++)
        cout << task_arr[i].priority_low << " ";
    cout << endl;
    for (int i = 0; i < L - 1; i++)   //Вложенные циклы
        for (int j = 0; j < L - i - 1; j++)
            if (task_arr[j].priority_high > task_arr[j+1].priority_high        //высокий приоритет требует сортировки ИЛИ
                || (task_arr[j].priority_high == task_arr[j+1].priority_high   //высокий приоритет не определен и нужно обратиться к...
                    && task_arr[j].priority_low > task_arr[j+1].priority_low)) //низкому приоритету
            {
                Task tmp = task_arr[j];
                task_arr[j] = task_arr[j+1];
                task_arr[j+1] = tmp;
            }

    cout << "Finaly:" << endl;
    cout << "HP: ";
    for (int i = 0; i < L; i++)
        cout << task_arr[i].priority_high << " ";
    cout << endl<< "LP: ";
    for (int i = 0; i < L; i++)
        cout << task_arr[i].priority_low << " ";
    cout << endl<<". . . . . . . . . . . . . . . . . ."<<endl;

    return 0;
}
