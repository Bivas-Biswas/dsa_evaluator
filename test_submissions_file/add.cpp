#include <fstream>
using namespace std;
int main(int argc, char* argv[]) {
    ifstream in(argv[1]);
    ofstream out(argv[2]);
    int a, b;
    in >> a >> b;
    out << a + b << endl;
    return 0;
}