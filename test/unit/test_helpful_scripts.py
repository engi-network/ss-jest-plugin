import json
from pathlib import Path

import pytest
from engi_cli.helpful_scripts import (
    GitHubRepoAnalyser,
    Job,
    JobDraft,
    RepoAnalyser,
    delete_test_messages,
    github_checkout,
    github_linguist,
    set_tmpdir,
)


@pytest.fixture(scope="module")
def tmpdir():
    with set_tmpdir() as tmpdir:
        yield tmpdir


@pytest.mark.asyncio
@pytest.mark.dependency()
@pytest.mark.github
async def test_should_be_able_checkout_repo(tmpdir, csharp_check_object):
    await github_checkout(csharp_check_object["Repo"], tmpdir)
    assert Path(tmpdir) / ".git"


@pytest.mark.asyncio
@pytest.mark.dependency(depends=["test_should_be_able_checkout_repo"])
@pytest.mark.github
async def test_should_be_able_to_run_linguist(tmpdir):
    breakdown = await github_linguist(tmpdir)
    print(f"{breakdown=}")
    assert "C#" in breakdown


def check_analyser_attributes(analyser, check_object):
    assert analyser.error == 0, "analyser error"
    json_object = json.loads(analyser.json())
    delete_test_messages(json_object["FailingTests"])
    print(json_object)
    print(check_object)
    assert json_object == check_object, "unexpected analyser JSON output"


async def check_analyser(language, check_object):
    analyser = GitHubRepoAnalyser(
        check_object["Repo"], branch=check_object["Branch"], commit=check_object["Commit"]
    )
    await analyser.analyse()
    assert analyser.language == language, "analyser language"
    check_analyser_attributes(analyser, check_object)


@pytest.mark.asyncio
async def test_should_be_able_to_analyse_csharp_github_repo(csharp_check_object):
    await check_analyser("C#", csharp_check_object)


@pytest.mark.asyncio
async def test_should_be_able_to_analyse_python_github_repo(python_check_object):
    await check_analyser("Python", python_check_object)


@pytest.mark.asyncio
async def test_should_be_able_to_analyse_javascript_github_repo(javascript_check_object):
    await check_analyser("JavaScript", javascript_check_object)


@pytest.fixture()
def python_job_draft(python_check_object):
    analyser = RepoAnalyser(python_check_object["Repo"])
    analyser.loads(json.dumps(python_check_object))
    draft = JobDraft(analyser)
    draft.set_title("My first Python job")
    draft.set_amount(10)
    draft.set_failing_tests(["test/test_demo.py::test_fail"])
    draft.set_is_editable("*.py")
    draft.set_is_addable("*.py")
    draft.set_is_deletable("*.py")
    return draft


def test_should_be_able_to_create_python_draft_object(python_job_draft, python_draft_object):
    assert (
        json.loads(python_job_draft.json())["Draft"] == python_draft_object
    ), "unexpected Python draft output"


@pytest.mark.asyncio
async def test_should_be_able_to_create_job(python_job_draft, user):
    job = Job(python_job_draft)
    job.set_secret(user.mnemonic)
    result = await job.create()
    assert result["data"]["createJob"] == "xyz789"


def test_should_be_able_to_create_javascript_draft_object(
    javascript_check_object, javascript_draft_object
):
    analyser = RepoAnalyser(javascript_check_object["Repo"])
    analyser.loads(json.dumps(javascript_check_object))
    draft = JobDraft(analyser)
    draft.set_title("My first JavaScript job")
    draft.set_amount(10)
    draft.set_failing_tests(["subtracts 4 - 2 to equal 2"])
    draft.set_is_editable("*.js")
    draft.set_is_addable("*.js")
    draft.set_is_deletable("*.js")
    assert (
        json.loads(draft.json())["Draft"] == javascript_draft_object
    ), "unexpected JavaScript draft output"
