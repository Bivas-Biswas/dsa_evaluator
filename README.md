### Question Format:

1. Description
2. Input Format
3. Ouptut Format
4. Sample Input N
5. Sample Ouput N

```
Description:

Write a program that reads two integers, a and b, from standard input and prints their sum to standard output.

Input Format:

The input consists of two space-separated integers, a and b, on a single line.

Output Format:

Print a single integer, which is the sum of a and b.

Sample Input 1:
5 3

Sample Output 1:
8
```


### Director Format for the DSA Evaluator
#### Input

```
Q1
|-- code
    |-- <roll_no>_Q1.cpp
|-- testcases
    |-- input<n>.txt
    |-- ouput<n>.txt
```
#### Output CSV
```
results
|-- Q1.csv
```



### Update the config according to your need:

```Flexible I/O Modes:``` Supports stdin/stdout or file-based I/O.

```js
{
  "language": "auto",               // "auto" | "c" | "cpp" | "python" (auto-detects or forces language)
  "time_limit_seconds": 2,          // Max execution time per test case (seconds)
  "memory_limit_mb": 64,            // Soft memory limit (MB, Linux-specific)
  "testcase_dir": "testcases",      // Path to input/output test pairs (inputN.txt, outputN.txt)
  "exec_dir": "executables",        // Path for compiled binaries (auto-cleaned)
  "result_log": "results/eval_log.txt",     // Detailed plaintext log (cleared each run)
  "io_mode": "stdin",               // "stdin" (read/write console) | "file" (pass file paths)
  "source_dir": "submissions",      // Path to user code (e.g., "submissions" for file I/O)
  "csv_file": "results/eval_results.csv"    // Structured CSV summary (cleared each run)
}
```

### 1. Verfiy Testcase using input.txt output.txt file

#### Change in `config.json`

- `io_mode` to `file`
- `time_limit_seconds` as you want
- `testcase_dir` as your testcase dir
- `source_dir` as your source dir

#### Programe execute format

```bash
file_name.o inputN.txt outputN.txt
```

#### The Testing Programme File

- follow this format inside the `source_dir`(default: submissions).
- the files must be flattern no nested directory supported.

#### Input and Output format

- follow this format inside the `testcase_dir`(default: testcases)
- for `inputN.txt` the output file must `outputN.txt`. eg. input1.txt output1.txt, input2.txt output2.txt


### 2. Verfiy Testcase using terminal input/output

#### Change in `config.json`

- `io_mode` to `stdin`
- `time_limit_seconds` as you want
- `testcase_dir` as your testcase dir
- `source_dir` as your source dir

#### Remaining as aboves


### The Result

- the result will in the `results/eval_results.csv`
- to show csv use `Edit CSV` extension

| Program | TestCase Input | Result       | Time (s) | Memory (KB) | Error/Details                                                 |
|---------|----------------|--------------|----------|-------------|----------------------------------------------------------------|
| add     | input1.txt     | Correct      | 0.0328   | 10308       |                                                                |
| add     | input2.txt     | Correct      | 0.0238   | 10308       |                                                                |
| add     | input1.txt     | Wrong Answer | 0.0038   | 20024       | "Expected:<br>7<br>Actual:<br>-1<br>STDERR:<br>"              |
| add     | input2.txt     | Wrong Answer | 0.0040   | 20024       | "Expected:<br>25<br>Actual:<br>-5<br>STDERR:<br>"             |
| add     | input1.txt     | Correct      | 0.0045   | 59928       |                                                                |
| add     | input2.txt     | Correct      | 0.0093   | 59928       |                                                                |



### Usefull script

- students will update the file as zip folder, it will have nested folder. But current implementation accept only flatten files.
- so use `flatten.py` for this. Output will be like below, the dir name will be added front.

```
Flattened files in dest_dir:
a_foo.txt
b_c_bar.txt
b_d_baz.txt
e_f_g_qux.txt
```

### Need

- a more script to create the final result form `results/eval_results.csv` for `Moodle`
- combine the result for each testcase per student. group by the student roll number
