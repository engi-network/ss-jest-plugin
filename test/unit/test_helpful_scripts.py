import os
from pathlib import Path

import pytest
from engi_cli.helpful_scripts import (
    GitHubRepoAnalyser,
    github_checkout,
    github_linguist,
    set_tmpdir,
)

TEST_CSHARP_REPO = os.environ.get("TEST_CSHARP_REPO", "engi-network/engi-blockchain-gql")
TEST_PYTHON_REPO = os.environ.get("TEST_CSHARP_REPO", "engi-network/demo-python")


@pytest.fixture(scope="module")
def tmpdir():
    with set_tmpdir() as tmpdir:
        yield tmpdir


@pytest.mark.asyncio
@pytest.mark.dependency()
async def test_should_be_able_checkout_repo(tmpdir):
    github_checkout(TEST_CSHARP_REPO, tmpdir)
    assert Path(tmpdir) / ".git"


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_should_be_able_checkout_repo"])
async def test_should_be_able_to_run_linguist(tmpdir):
    breakdown = await github_linguist(tmpdir)
    print(f"{breakdown=}")
    assert "C#" in breakdown


@pytest.mark.asyncio
async def test_should_be_able_to_analyse_csharp_github_repo(csharp_failing_tests):
    analyser = GitHubRepoAnalyser(TEST_CSHARP_REPO)
    await analyser.analyse()
    assert analyser.language == "C#"
    assert analyser.json == 1
    assert analyser.error == 0
    assert analyser.failing_tests == csharp_failing_tests


@pytest.mark.asyncio
async def test_should_be_able_to_analyse_python_github_repo(python_failing_tests):
    analyser = GitHubRepoAnalyser(TEST_PYTHON_REPO)
    await analyser.analyse()
    assert analyser.language == "Python"
    assert analyser.json == 1
    assert analyser.error == 0
    assert analyser.failing_tests == python_failing_tests
