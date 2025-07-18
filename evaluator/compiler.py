# evaluator/compiler.py
import os
import subprocess

class Compiler:
    def __init__(self, config):
        self.config = config
        self.exec_dir = config.exec_dir

    def detect_language(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.c':
            return 'c'
        elif ext == '.cpp':
            return 'cpp'
        elif ext == '.py':
            return 'python'
        else:
            return 'unknown'

    def compile_code(self, source_path, program_name, language):
        output_path = os.path.join(self.exec_dir, program_name)
        compile_command = []

        if language == 'c':
            compile_command = ['gcc', source_path, '-o', output_path, '-Wall', '-O2']
        elif language == 'cpp':
            compile_command = ['g++', source_path, '-o', output_path, '-Wall', '-O2']
        else:
            # Python files don't need compilation in this sense
            print(f"Warning: Attempted to compile unsupported language '{language}'. Skipping.")
            return None # Or raise an error if strict

        print(f"  Compiling {source_path}...")
        try:
            # Using check_output to capture stderr for detailed error messages
            result = subprocess.run(
                compile_command,
                capture_output=True,
                text=True,
                check=True, # Raise CalledProcessError if return code is non-zero
                timeout=self.config.time_limit_seconds # Apply a time limit for compilation too
            )
            print(f"  Compilation successful: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"  Compilation failed for {source_path}:")
            print(f"    STDOUT: {e.stdout}")
            print(f"    STDERR: {e.stderr}")
            return None
        except subprocess.TimeoutExpired:
            print(f"  Compilation timed out for {source_path}.")
            return None
        except FileNotFoundError:
            print(f"  Compiler ({compile_command[0]}) not found. Please ensure it's in your PATH.")
            return None
        except Exception as e:
            print(f"  An unexpected error occurred during compilation of {source_path}: {e}")
            return None

if __name__ == '__main__':
    # Basic test for compiler
    import json
    # Setup dummy config and directories for test
    dummy_config_content = {
        "language": "auto",
        "time_limit_seconds": 5,
        "exec_dir": "test_executables"
    }
    os.makedirs('test_executables', exist_ok=True)
    os.makedirs('submissions/test_compiler_files', exist_ok=True)
    with open('dummy_compiler_config.json', 'w') as f:
        json.dump(dummy_config_content, f, indent=2)

    class DummyConfig:
        def __init__(self, data):
            for k, v in data.items():
                setattr(self, k, v)

    cfg = DummyConfig(dummy_config_content)
    compiler = Compiler(cfg)

    # Create a dummy C file
    with open('submissions/test_compiler_files/test_add.c', 'w') as f:
        f.write("""
        #include <stdio.h>
        int main() {
            int a, b;
            scanf("%d %d", &a, &b);
            printf("%d\\n", a + b);
            return 0;
        }
        """)

    # Create a dummy C++ file
    with open('submissions/test_compiler_files/test_mul.cpp', 'w') as f:
        f.write("""
        #include <iostream>
        int main() {
            int a, b;
            std::cin >> a >> b;
            std::cout << (a * b) << std::endl;
            return 0;
        }
        """)

    # Create a dummy Python file (no compilation needed, but for language detection)
    with open('submissions/test_compiler_files/test_py.py', 'w') as f:
        f.write("print('Hello from Python')")

    print("\n--- Testing C compilation ---")
    c_exec = compiler.compile_code('submissions/test_compiler_files/test_add.c', 'test_add', 'c')
    if c_exec and os.path.exists(c_exec):
        print(f"C executable created at: {c_exec}")
    else:
        print("C compilation failed.")

    print("\n--- Testing C++ compilation ---")
    cpp_exec = compiler.compile_code('submissions/test_compiler_files/test_mul.cpp', 'test_mul', 'cpp')
    if cpp_exec and os.path.exists(cpp_exec):
        print(f"C++ executable created at: {cpp_exec}")
    else:
        print("C++ compilation failed.")

    print("\n--- Testing Python language detection (no compilation) ---")
    py_lang = compiler.detect_language('submissions/test_compiler_files/test_py.py')
    print(f"Detected language for test_py.py: {py_lang}")
    assert py_lang == 'python'
    assert compiler.compile_code('submissions/test_compiler_files/test_py.py', 'test_py', 'python') == None # Should return None as it's not compiled here

    # Cleanup
    os.remove('dummy_compiler_config.json')
    if c_exec and os.path.exists(c_exec):
        os.remove(c_exec)
    if cpp_exec and os.path.exists(cpp_exec):
        os.remove(cpp_exec)
    os.remove('submissions/test_compiler_files/test_add.c')
    os.remove('submissions/test_compiler_files/test_mul.cpp')
    os.remove('submissions/test_compiler_files/test_py.py')
    os.rmdir('submissions/test_compiler_files')
    os.rmdir('test_executables')