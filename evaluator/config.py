# evaluator/config.py
import json
import os

class Config:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found at: {self.config_path}")

        with open(self.config_path, 'r') as f:
            config_data = json.load(f)

        self.language = config_data.get('language', 'auto').lower()
        self.time_limit_seconds = config_data.get('time_limit_seconds', 2)
        self.memory_limit_mb = config_data.get('memory_limit_mb', 64)
        self.source_dir = config_data.get('source_dir', 'submissions/stdin')
        self.testcase_dir = config_data.get('testcase_dir', 'testcases')
        self.exec_dir = config_data.get('exec_dir', 'executables')
        self.result_log = config_data.get('result_log', 'results/eval_log.txt')
        self.csv_file = config_data.get('csv_file', 'results/eval_results.csv')
        self.io_mode = config_data.get('io_mode', 'stdin').lower()

        # Ensure source_dir is valid
        if not os.path.isdir(self.source_dir):
            raise ValueError(f"Config error: source_dir '{self.source_dir}' does not exist or is not a directory.")
        if not os.path.isdir(self.testcase_dir):
            raise ValueError(f"Config error: testcase_dir '{self.testcase_dir}' does not exist or is not a directory.")
        if self.io_mode not in ['stdin', 'file']:
            raise ValueError(f"Config error: io_mode '{self.io_mode}' must be 'stdin' or 'file'.")
        if self.language not in ['auto', 'c', 'cpp', 'python']:
             raise ValueError(f"Config error: language '{self.language}' must be 'auto', 'c', 'cpp', or 'python'.")

        # Create necessary directories if they don't exist
        os.makedirs(self.exec_dir, exist_ok=True)
        os.makedirs(os.path.dirname(self.result_log), exist_ok=True) # results/
        os.makedirs(os.path.dirname(self.csv_file), exist_ok=True) # results/

    def __str__(self):
        return (f"Config loaded:\n"
                f"  Language: {self.language}\n"
                f"  Time Limit: {self.time_limit_seconds}s\n"
                f"  Memory Limit: {self.memory_limit_mb}MB\n"
                f"  Source Dir: {self.source_dir}\n"
                f"  Testcase Dir: {self.testcase_dir}\n"
                f"  Exec Dir: {self.exec_dir}\n"
                f"  Result Log: {self.result_log}\n"
                f"  CSV File: {self.csv_file}\n"
                f"  I/O Mode: {self.io_mode}")

if __name__ == '__main__':
    # Example usage and basic test
    # Create a dummy config.json for testing
    dummy_config_content = {
      "language": "python",
      "time_limit_seconds": 1,
      "memory_limit_mb": 32,
      "source_dir": "submissions/stdin",
      "testcase_dir": "testcases",
      "exec_dir": "executables",
      "result_log": "results/test_log.txt",
      "csv_file": "results/test_results.csv",
      "io_mode": "file"
    }
    with open('dummy_config.json', 'w') as f:
        json.dump(dummy_config_content, f, indent=2)

    try:
        cfg = Config('dummy_config.json')
        print(cfg)
        assert cfg.language == "python"
        assert cfg.time_limit_seconds == 1
        assert cfg.io_mode == "file"
        print("Config loading test successful.")
    except Exception as e:
        print(f"Config loading test failed: {e}")
    finally:
        os.remove('dummy_config.json') # Clean up dummy file