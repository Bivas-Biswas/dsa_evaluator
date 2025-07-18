# main.py
import os
import sys
import shutil # Import shutil for rmtree

from evaluator.config import Config
from evaluator.compiler import Compiler
from evaluator.testcase import TestCaseFinder
from evaluator.runner import Runner
from evaluator.logger import Logger

def main():
    # Ensure necessary directories exist
    os.makedirs('executables', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    os.makedirs('submissions/stdin', exist_ok=True)
    os.makedirs('submissions/file', exist_ok=True)
    os.makedirs('testcases', exist_ok=True)

    config = None # Initialize config to None
    try:
        config = Config('config.json')
    except FileNotFoundError:
        print("Error: config.json not found. Please create it.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading config.json: {e}")
        sys.exit(1)

    compiler = Compiler(config)
    testcase_finder = TestCaseFinder(config.testcase_dir)
    runner = Runner(config)
    logger = Logger(config.result_log, config.csv_file)

    source_files = [f for f in os.listdir(config.source_dir) if os.path.isfile(os.path.join(config.source_dir, f))]
    if not source_files:
        print(f"No source files found in '{config.source_dir}'. Please add submissions.")
        # Ensure cleanup happens even if no sources are found
        if config: # Only attempt cleanup if config was loaded
            cleanup_executables(config.exec_dir)
        return

    test_cases = testcase_finder.find_test_cases()
    if not test_cases:
        print(f"No test cases found in '{config.testcase_dir}'. Please add input/output pairs.")
        if config: # Only attempt cleanup if config was loaded
            cleanup_executables(config.exec_dir)
        return

    logger.log_header()

    for source_file in source_files:
        full_source_path = os.path.join(config.source_dir, source_file)
        program_name = os.path.splitext(source_file)[0] # e.g., 'add' from 'add.c'

        print(f"\n--- Evaluating {source_file} ---")

        executable_path = None
        if config.language == "auto":
            lang = compiler.detect_language(source_file)
        else:
            lang = config.language

        if lang in ['c', 'cpp']:
            try:
                executable_path = compiler.compile_code(full_source_path, program_name, lang)
                if not executable_path:
                    print(f"Compilation failed for {source_file}. Skipping.")
                    continue
            except Exception as e:
                print(f"Error during compilation of {source_file}: {e}. Skipping.")
                logger.log_result(program_name, "N/A", "Compilation Error", 0, 0, f"Error: {e}")
                continue
        elif lang == 'python':
            executable_path = full_source_path # For Python, the source itself is the "executable"
        else:
            print(f"Unsupported language '{lang}' for {source_file}. Skipping.")
            logger.log_result(program_name, "N/A", "Unsupported Language", 0, 0, f"Language: {lang}")
            continue

        for i, (input_file, output_file) in enumerate(test_cases):
            test_case_name = os.path.basename(input_file)
            print(f"  Running Test Case {i+1}: {test_case_name}")

            try:
                result, time_taken, memory_used, error_output = runner.run_code(
                    executable_path,
                    input_file,
                    output_file,
                    lang,
                    program_name # Pass program_name for runner to identify Python scripts
                )
                logger.log_result(program_name, test_case_name, result, time_taken, memory_used, error_output)
            except Exception as e:
                print(f"    Error running test case {test_case_name}: {e}")
                logger.log_result(program_name, test_case_name, "Runner Error", 0, 0, f"Error: {e}")

    print("\n--- Evaluation Complete ---")
    print(f"Results logged to: {config.result_log}")
    print(f"CSV summary in: {config.csv_file}")

    # --- MODIFICATION START ---
    # Cleanup: Remove all compiled executables after evaluation
    cleanup_executables(config.exec_dir)
    # --- MODIFICATION END ---

def cleanup_executables(exec_dir):
    """Removes all files in the specified executables directory."""
    print(f"\n--- Cleaning up executables in '{exec_dir}' ---")
    try:
        # shutil.rmtree can remove a directory and its contents
        # os.makedirs will recreate it if needed by main()
        if os.path.exists(exec_dir):
            for item in os.listdir(exec_dir):
                item_path = os.path.join(exec_dir, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    print(f"  Removed: {item_path}")
                # If there were subdirectories, rmtree would handle them,
                # but for executables, we expect files directly.
            print(f"  Executables directory '{exec_dir}' cleaned.")
        else:
            print(f"  Executables directory '{exec_dir}' does not exist, no cleanup needed.")
    except Exception as e:
        print(f"  Error during executable cleanup: {e}")


if __name__ == "__main__":
    main()
