import os

# ========== SETUP DIRECTORIES ==========
os.makedirs("testcases", exist_ok=True)
os.makedirs("submissions/stdin", exist_ok=True)
os.makedirs("submissions/file", exist_ok=True)

# ========== TESTCASES ==========
testcases = [
    ("input1.txt", "3 4\n", "output1.txt", "7\n"),
    ("input2.txt", "10 15\n", "output2.txt", "25\n")
]

for infile, in_content, outfile, out_content in testcases:
    with open(f"testcases/{infile}", "w") as f:
        f.write(in_content)
    with open(f"testcases/{outfile}", "w") as f:
        f.write(out_content)

# ========== SUBMISSIONS - STDIN MODE ==========
stdin_c = """
#include <stdio.h>
int main() {
    int a, b;
    scanf("%d %d", &a, &b);
    printf("%d\\n", a + b);
    return 0;
}
"""

stdin_cpp = """
#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}
"""

stdin_py = """
a, b = map(int, input().split())
print(a + b)
"""

with open("submissions/stdin/add.c", "w") as f:
    f.write(stdin_c.strip())

with open("submissions/stdin/add.cpp", "w") as f:
    f.write(stdin_cpp.strip())

with open("submissions/stdin/add.py", "w") as f:
    f.write(stdin_py.strip())

# ========== SUBMISSIONS - FILE MODE (argv[1], argv[2]) ==========
file_c = """
#include <stdio.h>
int main(int argc, char* argv[]) {
    FILE *in = fopen(argv[1], "r");
    FILE *out = fopen(argv[2], "w");
    int a, b;
    fscanf(in, "%d %d", &a, &b);
    fprintf(out, "%d\\n", a + b);
    fclose(in);
    fclose(out);
    return 0;
}
"""

file_cpp = """
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
"""

file_py = """
import sys
with open(sys.argv[1], 'r') as f:
    a, b = map(int, f.read().split())
with open(sys.argv[2], 'w') as f:
    f.write(str(a + b) + "\\n")
"""

with open("submissions/file/add.c", "w") as f:
    f.write(file_c.strip())

with open("submissions/file/add.cpp", "w") as f:
    f.write(file_cpp.strip())

with open("submissions/file/add.py", "w") as f:
    f.write(file_py.strip())

"✅ Testcases and updated submission files created for both stdin and file I/O modes."
