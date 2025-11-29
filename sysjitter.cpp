#include <iostream>
#include <fstream>
#include <vector>
#include <unistd.h>
#include <x86intrin.h>
#include <algorithm>

using namespace std;

int main() {
    const int SAMPLES = 1000000;
    vector<unsigned long long> latencies;
    latencies.reserve(SAMPLES);

    for(int i=0; i<5000; i++) getpid();

    unsigned int junk;

    for (int i = 0; i < SAMPLES; i++) {
        unsigned long long start = __rdtscp(&junk);
        getpid();
        unsigned long long end = __rdtscp(&junk);

        if (end > start) {
            latencies.push_back(end - start);
        }
    }

    ofstream file("sysjitter_data.csv");
    file << "Sample,Cycles\n";
    for (int i = 0; i < SAMPLES; i++) {
        file << i << "," << latencies[i] << "\n";
    }
    file.close();

    cout << "Data collection complete." << endl;
    return 0;
}