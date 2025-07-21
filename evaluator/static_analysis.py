import subprocess

class StaticAnalysis:
    def __init__(self):
        return
    
    def uses_stl_headers(self, path: str) -> bool:
        """
        Scans C++ source files at the given path (file or folder)
        and returns True if STL headers are used, False otherwise.
        """
        include_cmd = [
            "grep", "-RE", r'#include\s*<[^>]+>', path
        ]
        stl_headers = (
            "vector|string|map|set|list|deque|queue|stack|"
            "unordered_map|unordered_set|algorithm|iterator|"
            "bitset|tuple|utility|numeric|"
            "functional|memory|optional|variant|any|execution|"
            "thread|mutex|future|condition_variable|bits"
        )
        filter_cmd = ["grep", "-E", stl_headers]

        try:
            # Run the first grep command
            include_proc = subprocess.Popen(
                include_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
            )
            # Pipe output to the second grep
            filter_proc = subprocess.Popen(
                filter_cmd,
                stdin=include_proc.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL
            )
            include_proc.stdout.close()  # Allow include_proc to receive SIGPIPE if filter_proc exits
            output, _ = filter_proc.communicate()

            return output.strip()
        except FileNotFoundError:
            raise RuntimeError("grep not found. Make sure it's installed and available in PATH.")
        except Exception as e:
            raise RuntimeError(f"Error while checking STL headers: {e}")