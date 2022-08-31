import os
from pathlib import Path

import xmltodict

from ..helpful_scripts import setup_logging
from .language_helper import LanguageHelperBase

log = setup_logging()

CSHARP_TEST_OUTPUT_DIR = os.environ.get("CSHARP_TEST_OUTPUT_DIR")


class LanguageHelper(LanguageHelperBase):
    LANG = "CSHARP"

    async def parse_failing_tests(self):
        path = self.kwargs.get("test_output_dir", CSHARP_TEST_OUTPUT_DIR)
        if path is None:
            raise RuntimeError("Trx Logger output directory undefined")
        trx_files = [f for f in Path(path).glob("*.trx") if f.is_file()]
        if len(trx_files) == 0:
            raise RuntimeError(f"no TRX files found in dir {path}")
        doc = xmltodict.parse(open(trx_files[0], "rb"))
        test_results = doc["TestRun"]["Results"]["UnitTestResult"]
        failing_tests = []
        for t in test_results:
            if t["@outcome"] == "Failed":
                failing_tests.append(
                    {
                        "TestId": t["@testId"],
                        "TestResult": "Failed",
                        "TestName": t["@testName"],
                        "TestMessage": t["Output"]["ErrorInfo"]["Message"],
                    }
                )
        log.info(f"parsed {len(test_results)} from {trx_files[0]}, {len(failing_tests)} failing")
        return failing_tests
