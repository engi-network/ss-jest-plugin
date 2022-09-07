import pytest
from engi_cli.helpful_scripts import (
    delete_test_messages,
    get_language_module,
    sorted_dict,
)


async def check_language_helper(language, check_object):
    m = get_language_module(language)
    failing_tests = sorted_dict(
        await m.LanguageHelper(
            "", m, test_output_dir=f"test/data/{language}"
        ).parse_failing_tests()
    )
    delete_test_messages(failing_tests)
    print(failing_tests)
    print(check_object["FailingTests"])
    assert failing_tests == check_object["FailingTests"]


@pytest.mark.asyncio
async def test_should_be_able_to_parse_csharp_failing_tests(csharp_check_object):
    await check_language_helper("C#", csharp_check_object)


@pytest.mark.asyncio
async def test_should_be_able_to_parse_python_failing_tests(python_check_object):
    await check_language_helper("Python", python_check_object)


@pytest.mark.asyncio
async def test_should_be_able_to_parse_javascript_failing_tests(javascript_check_object):
    await check_language_helper("JavaScript", javascript_check_object)
