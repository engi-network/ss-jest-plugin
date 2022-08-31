import pytest
from engi_cli.helpful_scripts import get_language_module


@pytest.mark.asyncio
async def test_should_be_able_to_parse_csharp_failing_tests(csharp_failing_tests):
    m = get_language_module("C#")
    failing_tests = await m.LanguageHelper(
        "", test_output_dir="test/data/C#"
    ).parse_failing_tests()
    assert failing_tests == csharp_failing_tests


@pytest.mark.asyncio
async def test_should_be_able_to_parse_python_failing_tests(python_failing_tests):
    m = get_language_module("Python")
    failing_tests = await m.LanguageHelper(
        "", test_output_dir="test/data/Python"
    ).parse_failing_tests()
    assert failing_tests == python_failing_tests
