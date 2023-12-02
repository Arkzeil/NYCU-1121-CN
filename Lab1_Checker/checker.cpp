#include <iostream>
#include <fstream>
#include <algorithm>
#include <sstream>
#include <vector>
#include <string>
#include <colors.h>
#include <map>
using namespace std;

int check(string filename){
  // current check info output
  cout<<endl;
  cout<<BOLD(FBLU("[ INFO ] : current scenario and log check : "))<<filename<<endl;

  // reconstruct file path
  string scenario_path = "./scenario/" + filename;
  string log_path = "./logs/" + filename;

  // open file
  ifstream is(log_path);
  if(!is.is_open()){
    cout<<BOLD(FRED("[ Error ] : cannot open : "))<<scenario_path<<endl;
    return -1;    
  }
  string s;
  map<int, int> cons_inquiry;
  map<int, int> cons_getdata;
  map<int, int> prod;
  while(getline(is, s)){
    if(s.find("[INFO ] < DATA") != string::npos){
      stringstream ss(s);
      vector<string> v;
      string tmp;
      while(ss >> tmp){
        v.push_back(tmp);
      }
      int consumer = stoi(v[1]);
      cons_getdata[consumer] += 1;
    }
    else if(s.find("[INFO ] > Interest") != string::npos){
      stringstream ss(s);
      vector<string> v;
      string tmp;
      while(ss >> tmp){
        v.push_back(tmp);
      }
      int consumer = stoi(v[1]);
      cons_inquiry[consumer] += 1;
    }
    else if(s.find("responding with Data") != string::npos){
      stringstream ss(s);
      vector<string> v;
      string tmp;
      while(ss >> tmp){
        v.push_back(tmp);
      }
      int producer = stoi(v[1]);
      prod[producer] += 1;   
    }
  }

  // output parsing result
  for(auto it:cons_inquiry){
    cout<<BOLD(FBLU("[ INFO ] node : "))<<it.first<<" "<<BOLD(FBLU("inquiry "))<<it.second<<BOLD(FBLU(" times"))<<endl;
    cout<<BOLD(FBLU("                  receive "))<<cons_getdata[it.first]<<BOLD(FBLU(" times"))<<endl;
  }
  for(auto it:prod){
    cout<<BOLD(FBLU("[ INFO ] node : "))<<it.first<<" "<<BOLD(FBLU("response "))<<it.second<<BOLD(FBLU(" times"))<<endl;
  }
  return 0;
}

int main(int argc, char* argv[]){
  if(argc < 2){
    cout<<BOLD(FCYN("-------------------------------------------"))<<endl<<endl;
    cout<<BOLD(FRED("Error argument : please input your log file ..."))<<endl<<endl;
    cout<<BOLD(FCYN("-------------------------------------------"))<<endl;
    return 1;
  }
  
  // check input logs' name
  vector<string> files;
  for(int i=1;i<argc;i++){
    files.push_back(string(argv[i])+".txt");
  }

  // output number of files
  cout<<BOLD(FCYN("-------------------------------------------"))<<endl<<endl;
  cout<<BOLD(FBLU("[ INFO ] : number of log input : "))<<argc-1<<endl<<endl;
  cout<<BOLD(FCYN("-------------------------------------------"))<<endl;

  // check each log
  for(auto log_file:files){
    int result = check(log_file);
    cout<<endl<<BOLD(FCYN("-------------------------------------------"))<<endl;
  }

  return 0;
}
