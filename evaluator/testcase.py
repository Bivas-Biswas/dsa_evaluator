# evaluator/testcase.py
import os
import re

class TestCaseFinder:
    def __init__(self, testcase_dir):
        self.testcase_dir = testcase_dir

    def find_test_cases(self):
        test_cases = []
        input_files = {}
        output_files = {}

        if not os.path.isdir(self.testcase_dir):
            print(f"Error: Testcase directory '{self.testcase_dir}' not found.")
            return []

        for filename in os.listdir(self.testcase_dir):
            path = os.path.join(self.testcase_dir, filename)
            if not os.path.isfile(path):
                continue

            # Regex to match inputN.txt or outputN.txt
            match_input = re.match(r'input(\d+)\.txt', filename)
            match_output = re.match(r'output(\d+)\.txt', filename)

            if match_input:
                index = int(match_input.group(1))
                input_files[index] = path
            elif match_output:
                index = int(match_output.group(1))
                output_files[index] = path

        # Pair them up by index
        sorted_indices = sorted(set(input_files.keys()) & set(output_files.keys()))

        for index in sorted_indices:
            test_cases.append((input_files[index], output_files[index]))

        if not test_cases:
            print(f"Warning: No matching input/output test case pairs found in '{self.testcase_dir}'.")

        return test_cases

if __name__ == '__main__':
    # Basic test for TestCaseFinder
    test_dir = 'test_cases_for_finder'
    os.makedirs(test_dir, exist_ok=True)

    # Create dummy test files
    with open(os.path.join(test_dir, 'input1.txt'), 'w') as f: f.write('1 2')
    with open(os.path.join(test_dir, 'output1.txt'), 'w') as f: f.write('3')
    with open(os.path.join(test_dir, 'input2.txt'), 'w') as f: f.write('5 6')
    with open(os.path.join(test_dir, 'output2.txt'), 'w') as f: f.write('11')
    with open(os.path.join(test_dir, 'input3.txt'), 'w') as f: f.write('just an input') # No matching output
    with open(os.path.join(test_dir, 'some_other_file.txt'), 'w') as f: f.write('xyz')

    finder = TestCaseFinder(test_dir)
    found_cases = finder.find_test_cases()

    print("\n--- Found Test Cases ---")
    for in_file, out_file in found_cases:
        print(f"Input: {os.path.basename(in_file)}, Output: {os.path.basename(out_file)}")

    assert len(found_cases) == 2
    assert os.path.basename(found_cases[0][0]) == 'input1.txt'
    assert os.path.basename(found_cases[1][0]) == 'input2.txt'
    print("Test case finding successful.")

    # Clean up
    for f in os.listdir(test_dir):
        os.remove(os.path.join(test_dir, f))
    os.rmdir(test_dir)