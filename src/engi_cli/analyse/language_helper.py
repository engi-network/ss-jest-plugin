import os
from pathlib import Path

from ..helpful_scripts import get_lizard_metrics, run, setup_logging

log = setup_logging()

TEST_OUTPUT_DIR = os.environ.get("TEST_OUTPUT_DIR", os.environ.get("TMPDIR", "/tmp"))


class LanguageHelperBase(object):
    LANG = None

    def __init__(self, repo, module, *args, **kwargs):
        self.tmpdir = repo
        self.args = args
        self.kwargs = kwargs
        self.module = module
        self.test_output_dir = Path(
            self.kwargs.get(
                "test_output_dir", os.environ.get(f"{self.LANG}_TEST_OUTPUT_DIR", TEST_OUTPUT_DIR)
            )
        )
        log.info(f"{self.test_output_dir=}")

    def get_env_var(self, name, default=None):
        return os.environ.get(f"{self.LANG}_{name}", default)

    def get_docker_cmd(self):
        cmd = self.get_env_var("DOCKER_COMPOSE", "docker compose")
        docker_compose_file = self.get_env_var("DOCKER_COMPOSE_FILE")
        if docker_compose_file:
            cmd = f"{cmd} -f {docker_compose_file}"
        return cmd

    def get_docker_test_service(self):
        return self.kwargs.get("docker_test_service", "tests")

    async def run_tests(self):
        log.info(f"run_tests")
        cmd = self.get_docker_cmd()
        await run(f"{cmd} up --exit-code-from tests --build", raise_code=None)
        await run(f"{cmd} down")

    async def get_metrics(self):
        """Return dict(files=, sloc=, complexity=)"""
        return await get_lizard_metrics(".")

    async def parse_failing_tests(self):
        """Get a list of failing tests by calling all the functions in the
        language helper module starting with `parse_' until one returns not None"""
        for funcname in dir(self.module):
            if funcname.startswith("parse_"):
                failing_tests = await getattr(self.module, funcname)(self.test_output_dir)
                if failing_tests is not None:
                    return failing_tests
