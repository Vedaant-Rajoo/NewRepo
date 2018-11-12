#include<iostream>
using namespace std;
class values{
  int a,b,c;
  float x;
public:
  void display(void){
    x= a/float(b)-c;
    cout<<x<<endl;
  }
  void input(void){
    cin>>a>>b>>c;
  }

};
int main(){
  values o1;
  int t,i;
  cin>>t;
  for(i=0;i<t;i++){
    o1.input();
    o1.display();

  }
  return 0;
}
