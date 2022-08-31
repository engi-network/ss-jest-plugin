import os

from ..helpful_scripts import run, setup_logging

log = setup_logging()


class LanguageHelperBase(object):
    LANG = None

    def __init__(self, tmpdir, *args, **kwargs):
        self.tmpdir = tmpdir
        self.args = args
        self.kwargs = kwargs

    def get_env_var(self, name, default=None):
        return os.environ.get(f"{self.LANG}_{name}", default)

    def get_docker_cmd(self):
        cmd = self.get_env_var("DOCKER_COMPOSE", "docker-compose")
        docker_compose_file = self.get_env_var("DOCKER_COMPOSE_FILE")
        if docker_compose_file:
            cmd = f"{cmd} -f {docker_compose_file}"
        return cmd

    def get_docker_test_service(self):
        return self.kwargs.get("docker_test_service", "tests")

    async def run_tests(self):
        log.info(f"run_tests")
        cmd = self.get_docker_cmd()
        await run(f"{cmd} up --build")
        await run(f"{cmd} down")

    async def parse_failing_tests(self):
        raise NotImplementedError
