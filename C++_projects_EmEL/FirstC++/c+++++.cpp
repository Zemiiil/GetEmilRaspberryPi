#include <iostream>
using namespace std;
// ваша реализация функции
int main()
{
    char a='0';
    cout<<int(a)<<"  "<<a<<endl;
    char i=-128;
    while(true)
    {
        cout<<int(i)<<" is : "<<i<<endl;
        if (i==127) break;
        i++;
    }
}