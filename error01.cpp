#include <iostream>
using namespace std;
int main(){
    int a=2,b=3;
    int const *ptr=&a;
    //*ptr=5;
    ptr=&b;
    b++;
    cout<<*ptr;


}