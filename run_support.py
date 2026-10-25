"""Fresh workspace per run, shared working directory, and saved output evidence."""
from contextlib import chdir
from functools import wraps
from pathlib import Path
import ast
import shutil
import tempfile
from tools import code_tools


def isolated_run(function):
    @wraps(function)
    def run():
        root = Path(__file__).resolve().parent
        workspace = Path(tempfile.mkdtemp(prefix="lab14_run_"))
        code_tools.WORKSPACE = workspace
        with chdir(workspace):
            output = function()
        source = (workspace / "word_freq.py").read_text()
        tree = ast.parse(source)
        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "word_frequency"]
        if not functions or not functions[0].returns:
            raise RuntimeError("Missing typed word_frequency function")
        if len((workspace / "sample.txt").read_text().split()) < 20:
            raise RuntimeError("sample.txt must contain at least 20 words")
        if "DONE" not in output:
            raise RuntimeError("Agent did not confirm completion")
        destination = root / "comparison" / "artifacts" / function.__module__
        destination.mkdir(parents=True, exist_ok=True)
        for name in ("word_freq.py", "sample.txt"):
            shutil.copy2(workspace / name, destination / name)
        return output
    return run
