# evaluator/runner.py
import subprocess
import os
import time
import resource # Linux specific for memory usage
import filecmp # For file-based output comparison

class Runner:
    def __init__(self, config):
        self.config = config

    def _get_memory_usage_kb(self):
        """Returns current process's max resident set size in KB. Linux specific."""
        try:
            # resource.RUSAGE_CHILDREN includes resources used by child processes
            # resource.RUSAGE_SELF for current process only
            # Using RUSAGE_CHILDREN to account for actual program execution
            return resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
        except Exception:
            # Fallback for non-Linux or if resource module fails
            return 0 # Indicate no memory measurement

    def run_code(self, program_path, input_file, expected_output_file, language, program_name_for_py=None):
        cmd = []
        process = None
        start_time = time.time()
        memory_usage_kb = 0
        error_output = ""
        actual_output = ""
        temp_output_file = None

        try:
            if language == 'python':
                cmd = ['python3', program_path]
            elif language in ['c', 'cpp']:
                cmd = [program_path]
            else:
                return "Unsupported Language", 0, 0, "Unknown language for execution."

            # Prepare commands based on I/O mode
            if self.config.io_mode == 'stdin':
                with open(input_file, 'r') as infile:
                    try:
                        # Popen for more control, especially for resource limits
                        process = subprocess.Popen(
                            cmd,
                            stdin=infile,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            preexec_fn=self._set_memory_limit # Apply resource limit
                        )
                        # Communicate to get stdout/stderr and wait for process to finish
                        stdout, stderr = process.communicate(timeout=self.config.time_limit_seconds)
                        actual_output = stdout.strip()
                        error_output = stderr.strip()

                    except subprocess.TimeoutExpired:
                        process.kill()
                        stdout, stderr = process.communicate()
                        error_output = f"Execution timed out ({self.config.time_limit_seconds}s). STDOUT: {stdout.strip()}\nSTDERR: {stderr.strip()}"
                        return "Time Limit Exceeded", self.config.time_limit_seconds, self._get_memory_usage_kb(), error_output
                    except Exception as e:
                        return "Runtime Error", time.time() - start_time, self._get_memory_usage_kb(), f"General Error during execution: {e}"

            elif self.config.io_mode == 'file':
                # For file mode, program_name_for_py is the base name (e.g., 'add')
                # We need a unique temporary output file for each run to prevent conflicts
                temp_output_filename = f"{program_name_for_py}_{os.path.basename(input_file)}.tmp_out"
                temp_output_file = os.path.join(self.config.exec_dir, temp_output_filename)

                if language == 'python':
                    cmd = ['python3', program_path, input_file, temp_output_file]
                elif language in ['c', 'cpp']:
                    cmd = [program_path, input_file, temp_output_file]

                try:
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE, # Capture stdout/stderr just in case for debugging
                        stderr=subprocess.PIPE,
                        text=True,
                        preexec_fn=self._set_memory_limit
                    )
                    stdout, stderr = process.communicate(timeout=self.config.time_limit_seconds)
                    error_output = stderr.strip()
                    # After execution, read the content of the temporary output file
                    if os.path.exists(temp_output_file):
                        with open(temp_output_file, 'r') as f:
                            actual_output = f.read().strip()
                    else:
                        error_output += "\nProgram did not create expected output file."
                        return "Runtime Error", time.time() - start_time, self._get_memory_usage_kb(), error_output

                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()
                    error_output = f"Execution timed out ({self.config.time_limit_seconds}s). STDOUT: {stdout.strip()}\nSTDERR: {stderr.strip()}"
                    return "Time Limit Exceeded", self.config.time_limit_seconds, self._get_memory_usage_kb(), error_output
                except Exception as e:
                    return "Runtime Error", time.time() - start_time, self._get_memory_usage_kb(), f"General Error during execution: {e}"
            else:
                return "Config Error", 0, 0, "Invalid I/O mode in config."

            time_taken = time.time() - start_time
            memory_usage_kb = self._get_memory_usage_kb()

            if process.returncode != 0:
                # A non-zero return code usually indicates a runtime error
                return "Runtime Error", time_taken, memory_usage_kb, error_output

            # Compare outputs
            with open(expected_output_file, 'r') as expected_file:
                expected_output = expected_file.read().strip()

            if self.config.io_mode == 'stdin':
                if actual_output == expected_output:
                    return "Correct", time_taken, memory_usage_kb, error_output
                else:
                    error_output = f"Expected:\n{expected_output}\nActual:\n{actual_output}\nSTDERR:\n{error_output}"
                    return "Wrong Answer", time_taken, memory_usage_kb, error_output
            elif self.config.io_mode == 'file':
                # Using filecmp.cmp for direct file comparison, ignores timestamp, etc.
                if filecmp.cmp(temp_output_file, expected_output_file, shallow=False):
                    return "Correct", time_taken, memory_usage_kb, error_output
                else:
                    error_output = f"Output file mismatch. STDERR:\n{error_output}"
                    # Optionally, read differences for more detail
                    try:
                        with open(temp_output_file, 'r') as f_actual, \
                             open(expected_output_file, 'r') as f_expected:
                             actual_content = f_actual.read().strip()
                             expected_content = f_expected.read().strip()
                             error_output += f"\nExpected:\n{expected_content}\nActual:\n{actual_content}"
                    except Exception as e:
                        error_output += f"\nCould not read output files for detailed comparison: {e}"
                    return "Wrong Answer", time_taken, memory_usage_kb, error_output

        finally:
            if temp_output_file and os.path.exists(temp_output_file):
                try:
                    os.remove(temp_output_file)
                except OSError as e:
                    print(f"Warning: Could not remove temporary output file {temp_output_file}: {e}")
            if process and process.poll() is None: # If process is still running
                process.kill()

    def _set_memory_limit(self):
        """Set rlimit for virtual memory. This is a soft limit and Linux specific."""
        try:
            # RLIMIT_AS (address space) is for total virtual memory.
            # Convert MB to bytes.
            memory_limit_bytes = self.config.memory_limit_mb * 1024 * 1024
            # Set both soft and hard limits
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit_bytes, memory_limit_bytes))
            # print(f"Set memory limit to {self.config.memory_limit_mb}MB") # For debugging
        except Exception as e:
            # This will fail on non-Linux systems or if user lacks permissions
            print(f"Warning: Could not set memory limit using resource module: {e}")

if __name__ == '__main__':
    # Basic test for Runner
    import json
    # Setup dummy config and directories for test
    dummy_config_content_stdin = {
        "language": "python",
        "time_limit_seconds": 1,
        "memory_limit_mb": 64,
        "exec_dir": "test_runner_executables",
        "io_mode": "stdin"
    }
    dummy_config_content_file = {
        "language": "c",
        "time_limit_seconds": 1,
        "memory_limit_mb": 64,
        "exec_dir": "test_runner_executables",
        "io_mode": "file"
    }

    os.makedirs('test_runner_executables', exist_ok=True)
    os.makedirs('test_runner_testcases', exist_ok=True)
    os.makedirs('submissions/test_runner_submissions', exist_ok=True)


    class DummyConfig:
        def __init__(self, data):
            for k, v in data.items():
                setattr(self, k, v)

    # --- Test STDIN mode (Python) ---
    print("\n--- Testing STDIN mode (Python) ---")
    cfg_stdin = DummyConfig(dummy_config_content_stdin)
    runner_stdin = Runner(cfg_stdin)

    # Create dummy Python submission
    py_sum_path = 'submissions/test_runner_submissions/py_sum.py'
    with open(py_sum_path, 'w') as f:
        f.write("a, b = map(int, input().split())\nprint(a + b)")

    # Create dummy test cases
    with open('test_runner_testcases/input_sum1.txt', 'w') as f: f.write('10 20')
    with open('test_runner_testcases/output_sum1.txt', 'w') as f: f.write('30')
    with open('test_runner_testcases/input_sum2.txt', 'w') as f: f.write('5 7')
    with open('test_runner_testcases/output_sum2.txt', 'w') as f: f.write('13') # Deliberate wrong answer

    result, time_taken, memory_used, error_output = runner_stdin.run_code(
        py_sum_path,
        'test_runner_testcases/input_sum1.txt',
        'test_runner_testcases/output_sum1.txt',
        'python',
        'py_sum'
    )
    print(f"Test 1 (Correct): {result}, Time: {time_taken:.4f}s, Mem: {memory_used}KB, Err: {error_output}")
    assert result == "Correct"

    result, time_taken, memory_used, error_output = runner_stdin.run_code(
        py_sum_path,
        'test_runner_testcases/input_sum2.txt',
        'test_runner_testcases/output_sum2.txt',
        'python',
        'py_sum'
    )
    print(f"Test 2 (Wrong): {result}, Time: {time_taken:.4f}s, Mem: {memory_used}KB, Err: {error_output}")
    assert result == "Wrong Answer"

    # Test Time Limit Exceeded
    py_loop_path = 'submissions/test_runner_submissions/py_loop.py'
    with open(py_loop_path, 'w') as f:
        f.write("import time\nwhile True:\n  time.sleep(0.1)\n") # Loop forever

    result, time_taken, memory_used, error_output = runner_stdin.run_code(
        py_loop_path,
        'test_runner_testcases/input_sum1.txt',
        'test_runner_testcases/output_sum1.txt',
        'python',
        'py_loop'
    )
    print(f"Test 3 (TLE): {result}, Time: {time_taken:.4f}s, Mem: {memory_used}KB, Err: {error_output}")
    assert result == "Time Limit Exceeded"


    # --- Test FILE mode (C) ---
    print("\n--- Testing FILE mode (C) ---")
    cfg_file = DummyConfig(dummy_config_content_file)
    runner_file = Runner(cfg_file)

    # Create dummy C submission (requires compilation)
    c_sum_source_path = 'submissions/test_runner_submissions/c_sum.c'
    c_sum_exec_path = os.path.join(cfg_file.exec_dir, 'c_sum')
    with open(c_sum_source_path, 'w') as f:
        f.write("""
        #include <stdio.h>
        int main(int argc, char* argv[]) {
            FILE *in = fopen(argv[1], "r");
            FILE *out = fopen(argv[2], "w");
            int a, b;
            fscanf(in, "%d %d", &a, &b);
            fprintf(out, "%d\\n", a + b);
            fclose(in); fclose(out);
            return 0;
        }
        """)

    # Compile C code first
    compiler_test_cfg = DummyConfig({"exec_dir": cfg_file.exec_dir, "time_limit_seconds": 5})
    compiler_obj = __import__('evaluator.compiler').compiler.Compiler(compiler_test_cfg) # Dynamically import
    compiled_c_path = compiler_obj.compile_code(c_sum_source_path, 'c_sum', 'c')
    if compiled_c_path:
        print(f"C code compiled to {compiled_c_path}")
        result, time_taken, memory_used, error_output = runner_file.run_code(
            compiled_c_path,
            'test_runner_testcases/input_sum1.txt',
            'test_runner_testcases/output_sum1.txt',
            'c',
            'c_sum' # program_name for temp output file
        )
        print(f"Test 4 (C File Correct): {result}, Time: {time_taken:.4f}s, Mem: {memory_used}KB, Err: {error_output}")
        assert result == "Correct"

        result, time_taken, memory_used, error_output = runner_file.run_code(
            compiled_c_path,
            'test_runner_testcases/input_sum2.txt',
            'test_runner_testcases/output_sum2.txt',
            'c',
            'c_sum' # program_name for temp output file
        )
        print(f"Test 5 (C File Wrong): {result}, Time: {time_taken:.4f}s, Mem: {memory_used}KB, Err: {error_output}")
        assert result == "Wrong Answer"
    else:
        print("Skipping C file mode tests due to compilation failure.")

    # Cleanup
    os.remove(py_sum_path)
    os.remove(py_loop_path)
    os.remove('test_runner_testcases/input_sum1.txt')
    os.remove('test_runner_testcases/output_sum1.txt')
    os.remove('test_runner_testcases/input_sum2.txt')
    os.remove('test_runner_testcases/output_sum2.txt')
    os.rmdir('test_runner_testcases')

    if os.path.exists(c_sum_source_path):
        os.remove(c_sum_source_path)
    if os.path.exists(c_sum_exec_path):
        os.remove(c_sum_exec_path)
    os.rmdir('test_runner_executables')
    os.rmdir('submissions/test_runner_submissions')