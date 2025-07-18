# evaluator/logger.py
import csv
import os
import datetime

class Logger:
    def __init__(self, log_file_path, csv_file_path):
        self.log_file_path = log_file_path
        self.csv_file_path = csv_file_path
        self._ensure_dirs_exist()

    def _ensure_dirs_exist(self):
        # Ensure the directory for the log file exists
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
        # Ensure the directory for the CSV file exists
        os.makedirs(os.path.dirname(self.csv_file_path), exist_ok=True)

    def log_header(self):
        # Delete the log file if it already exists to ensure a clean start
        if os.path.exists(self.log_file_path):
            try:
                os.remove(self.log_file_path)
            except OSError as e:
                print(f"Warning: Could not delete existing log file {self.log_file_path}: {e}")

        # --- MODIFICATION START ---
        # Delete the CSV file if it already exists to ensure a clean start
        if os.path.exists(self.csv_file_path):
            try:
                os.remove(self.csv_file_path)
            except OSError as e:
                print(f"Warning: Could not delete existing CSV file {self.csv_file_path}: {e}")
        # --- MODIFICATION END ---

        # Log to plaintext file (will be created fresh due to 'w' mode)
        with open(self.log_file_path, 'w') as f:
            f.write(f"DSA Test Code Evaluator Log - {datetime.datetime.now()}\n")
            f.write("-" * 50 + "\n\n")

        # Log to CSV file (will be created fresh due to previous deletion, then header written)
        # The 'a' mode is fine here because we've explicitly removed it if it existed.
        with open(self.csv_file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            # Since we explicitly removed the file if it existed, it will always be "new" for the purpose of writing the header.
            writer.writerow(['Program', 'TestCase Input', 'Result', 'Time (s)', 'Memory (KB)', 'Error/Details'])

    def log_result(self, program_name, test_case_name, result, time_s, memory_kb, error_details=""):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log to plaintext file
        with open(self.log_file_path, 'a') as f:
            f.write(f"[{timestamp}] Program: {program_name}, Test Case: {test_case_name}\n")
            f.write(f"  Result: {result}\n")
            f.write(f"  Time: {time_s:.4f} s\n")
            f.write(f"  Memory: {memory_kb} KB\n")
            if error_details:
                f.write(f"  Details: {error_details}\n")
            f.write("\n")

        # Log to CSV file
        with open(self.csv_file_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([program_name, test_case_name, result, f"{time_s:.4f}", memory_kb, error_details])

if __name__ == '__main__':
    # Basic test for Logger
    log_dir = 'test_results'
    log_file = os.path.join(log_dir, 'test_eval_log.txt')
    csv_file = os.path.join(log_dir, 'test_eval_results.csv')

    # Ensure the test directory exists
    os.makedirs(log_dir, exist_ok=True)

    # The log_header method itself will now handle cleaning up existing files.
    logger = Logger(log_file, csv_file)
    logger.log_header() # This will now delete both log_file and csv_file if they exist

    print("\n--- Logging Test ---")
    logger.log_result("add.py", "input1.txt", "Correct", 0.0123, 1024)
    logger.log_result("add.py", "input2.txt", "Wrong Answer", 0.015, 1028, "Expected 10, got 12")
    logger.log_result("sort.cpp", "input_large.txt", "Time Limit Exceeded", 2.001, 50000, "Process killed due to timeout")
    logger.log_result("fibo.c", "input_small.txt", "Runtime Error", 0.005, 500, "Segmentation fault")

    print(f"Check '{log_file}' and '{csv_file}' for results.")

    # Verify content (basic check)
    with open(log_file, 'r') as f:
        content = f.read()
        assert "Program: add.py" in content
        assert "Result: Correct" in content
        assert "Time Limit Exceeded" in content

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        assert len(rows) == 5 # Header + 4 data rows
        assert rows[0] == ['Program', 'TestCase Input', 'Result', 'Time (s)', 'Memory (KB)', 'Error/Details']
        assert rows[2][2] == 'Wrong Answer'
        assert rows[4][0] == 'fibo.c'
    print("Logging test successful.")

    # Cleanup
    os.remove(log_file)
    os.remove(csv_file)
    os.rmdir(log_dir)
