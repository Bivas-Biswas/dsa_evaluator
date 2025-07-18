
### Update the config according to your need:

```Flexible I/O Modes:``` Supports stdin/stdout or file-based I/O.

```js
{
  "language": "auto",               // "auto" | "c" | "cpp" | "python" (auto-detects or forces language)
  "time_limit_seconds": 2,          // Max execution time per test case (seconds)
  "memory_limit_mb": 64,            // Soft memory limit (MB, Linux-specific)
  "testcase_dir": "testcases",      // Path to input/output test pairs (inputN.txt, outputN.txt)
  "exec_dir": "executables",        // Path for compiled binaries (auto-cleaned)
  "result_log": "eval_log.txt",     // Detailed plaintext log (cleared each run)
  "io_mode": "stdin",               // "stdin" (read/write console) | "file" (pass file paths)
  "source_dir": "submissions",      // Path to user code (e.g., "submissions/file" for file I/O)
  "csv_file": "eval_results.csv"    // Structured CSV summary (cleared each run)
}
```
