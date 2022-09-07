import json
import os
from pathlib import Path

from ..helpful_scripts import run, setup_logging
from .language_helper import LanguageHelperBase

log = setup_logging()

JAVASCRIPT_TEST_OUTPUT_FILE = os.environ.get("JAVASCRIPT_TEST_OUTPUT_FILE", "jest.json")


async def parse_jest(test_output_dir):
    failing_tests = []
    full_path = test_output_dir / JAVASCRIPT_TEST_OUTPUT_FILE
    log.info(f"parsing {full_path=} {Path().absolute()=}")
    if not full_path.exists():
        raise RuntimeError(f"jest output file {full_path} not found")
    test_results = []
    jest_obj = json.load(open(full_path))

    for t in jest_obj["testResults"][0]["assertionResults"]:
        if t["status"] == "failed":
            failing_tests.append(
                {
                    "TestId": t["fullName"],
                    "TestResult": "Failed",
                    "TestName": t["fullName"],
                    "TestMessage": t["failureMessages"][0],
                }
            )
        test_results.append(t)
    log.info(f"parsed {len(test_results)} from {full_path}, {len(failing_tests)} failing")
    return failing_tests


class LanguageHelper(LanguageHelperBase):
    LANG = "JAVASCRIPT"
