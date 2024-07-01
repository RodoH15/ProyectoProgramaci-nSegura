#include <iostream>
using namespace std;

int main() {
	int i,j,k,n[10];
	for(i=0;i<10;i++){
		cout<<"Ingresa el numero "<<i+1<<" :";
		cin>>n[i];
	}
	system("cls");
	for(i=1;i<10;i++){
		for(j=0;j<10-i;j++){
			if(n[j]>n[j+1]){
				k=n[j+1]; 
				n[j+1]=n[j]; 
				n[j]=k;
			}
		}
	}
	cout<<"El orden ascendente es el siguiente:"<<endl;
	for(i=0;i<10;i++){
		cout<<n[i]<<endl;
	}
	cout<<"El orden descendente es el siguiente:"<<endl;
	for(i=9;i>=0;i--){
		cout<<n[i]<<endl;
	}
	return 0;
}
