import subprocess
import sys
import tempfile
import os


def run_code(code, timeout=3):

    file_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False
        ) as file:

            file.write(code)
            file_path = file.name

        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode == 0:
            return {
                "status": "PASSED",
                "success": True,
                "output": result.stdout.strip(),
                "error": None
            }

        return {
            "status": "FAILED",
            "success": False,
            "output": result.stdout.strip(),
            "error": result.stderr.strip()
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "TIMEOUT",
            "success": False,
            "output": "",
            "error": "Code execution exceeded the time limit."
        }

    except Exception as error:
        return {
            "status": "ERROR",
            "success": False,
            "output": "",
            "error": str(error)
        }

    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)