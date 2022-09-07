import asyncio

import pytest
import pytest_asyncio
from engi_cli.blockchain_api import GraphQLUser


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def user():
    user = GraphQLUser("cck197", "foo", "foo")
    await user.create()
    yield user


@pytest.fixture(scope="session")
def javascript_check_object():
    return {
        "Repo": "https://github.com/engi-network/engi-network/demo-javascript.git",
        "Branch": None,
        "Commit": None,
        "Language": "JavaScript",
        "Files": ["./calc.js", "./calc.test.js"],
        "Complexity": {"SLOC": 11, "Cyclomatic": 1.0},
        "FailingTests": [
            {
                "TestId": "subtracts 4 - 2 to equal 2",
                "TestResult": "Failed",
                "TestName": "subtracts 4 - 2 to equal 2",
            }
        ],
    }


@pytest.fixture(scope="session")
def python_check_object():
    return {
        "Repo": "https://github.com/engi-network/engi-network/demo-python.git",
        "Branch": "master",
        "Commit": "a81ab04b7439119ee29cbe1f2c9c1e467c17e738",
        "Language": "Python",
        "Files": ["./src/engi_python_demo/calc.py", "./test/test_demo.py"],
        "Complexity": {
            "SLOC": 8,
            "Cyclomatic": 1.0,
        },
        "FailingTests": [
            {
                "TestId": "test/test_demo.py::test_fail",
                "TestResult": "Failed",
                "TestName": "test_fail",
            }
        ],
    }


@pytest.fixture(scope="session")
def csharp_check_object():
    return {
        "Repo": "https://github.com/engi-network/engi-network/demo-csharp.git",
        "Branch": None,
        "Commit": None,
        "Language": "C#",
        "Files": [
            "./PrimeService.Tests/PrimeService_IsPrimeShould.cs",
            "./PrimeService/PrimeService.cs",
        ],
        "Complexity": {"SLOC": 17, "Cyclomatic": 1.3333333333333333},
        "FailingTests": [
            {
                "TestId": "6327b858-0fd0-99bb-d810-75db0e0aa61e",
                "TestResult": "Failed",
                "TestName": "Prime.UnitTests.Services.PrimeService_IsPrimeShould.IsPrime_ValuesLessThan2_ReturnFalse(value: -1)",
            },
            {
                "TestId": "7db5907a-e8c2-fd08-f6cd-19fe4bb587d4",
                "TestResult": "Failed",
                "TestName": "Prime.UnitTests.Services.PrimeService_IsPrimeShould.IsPrime_ValuesLessThan2_ReturnFalse(value: 0)",
            },
        ],
    }


@pytest.fixture(scope="session")
def python_draft_object():
    return {
        "FailingTests": ["test/test_demo.py::test_fail"],
        "IsEditable": "*.py",
        "IsAddable": "*.py",
        "IsDeletable": "*.py",
        "Amount": 10,
        "Title": "My first Python job",
    }


@pytest.fixture(scope="session")
def javascript_draft_object():
    return {
        "FailingTests": ["subtracts 4 - 2 to equal 2"],
        "IsEditable": "*.js",
        "IsAddable": "*.js",
        "IsDeletable": "*.js",
        "Amount": 10,
        "Title": "My first JavaScript job",
    }
