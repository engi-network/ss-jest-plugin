from engi_cli.helpful_scripts import RepoAnalyser
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../features/analyse_repository.feature")


@given(parsers.parse("the codebase located at {repo}"), target_fixture="analyser")
def given_analyser(repo):
    return RepoAnalyser(repo)


@when(parsers.parse("optional branch named {branch}"))
def branch(analyser, branch):
    analyser.set_branch(branch)


@when(parsers.parse("optional commit hash {commit}"))
def commit(analyser, commit):
    analyser.set_commit(commit)


@when(parsers.parse("the codebase is written in {language}"))
def language(analyser, language):
    analyser.set_language(language)


@when(parsers.parse("has {docker:d} support"))
def docker(analyser, docker):
    analyser.set_docker(docker)


@when(parsers.parse("contains {failing_tests:d}"))
def failing_tests(analyser, failing_tests):
    # failing_tests should really be a list but pytest-bdd doesn't support that,
    # so pretent the integer is the length of the list
    if failing_tests:
        analyser.set_failing_tests(failing_tests)


@then(parsers.parse("a JSON check object containing a list of failing tests is printed to stdout"))
def should_have_json_output(analyser):
    analyser.analyse()
    print(analyser.json())


@then(parsers.parse("there should be no {error:d}"))
def should_be_no_error(analyser, error):
    assert int(analyser.error) == error
