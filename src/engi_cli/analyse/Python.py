import json
import os
from pathlib import Path

from ..helpful_scripts import setup_logging
from .language_helper import LanguageHelperBase

log = setup_logging()

PYTHON_TEST_OUTPUT_DIR = os.environ.get("PYTHON_TEST_OUTPUT_DIR", ".")
PYTHON_TEST_OUTPUT_FILE = os.environ.get("PYTHON_TEST_OUTPUT_FILE", "pytest.json")


class LanguageHelper(LanguageHelperBase):
    LANG = "PYTHON"

    async def parse_failing_tests(self):
        path = Path(self.kwargs.get("test_output_dir", PYTHON_TEST_OUTPUT_DIR))
        filename = self.kwargs.get("test_filename", PYTHON_TEST_OUTPUT_FILE)
        failing_tests = []
        full_path = path / filename
        if not full_path.exists():
            raise RuntimeError(f"pytest-reportlog output file {full_path} not found")
        test_results = []
        for line in open(full_path):
            t = json.loads(line)
            if t.get("when") != "call":
                continue
            if t.get("outcome") == "failed":
                failing_tests.append(
                    {
                        "TestId": t["nodeid"],
                        "TestResult": "Failed",
                        "TestName": t["location"][-1],
                        "TestMessage": t["longrepr"]["reprcrash"]["message"],
                    }
                )
            test_results.append(t)
        log.info(f"parsed {len(test_results)} from {full_path}, {len(failing_tests)} failing")
        return failing_tests
