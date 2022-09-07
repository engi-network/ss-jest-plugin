import parse
from engi_cli.helpful_scripts import JobDraft, RepoAnalyser
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../features/create_draft.feature")


class MockAnalyser(RepoAnalyser):
    def __init__(self):
        super().__init__()
        self.set_failing_tests([{"TestId": "X"}, {"TestId": "Y"}])
        self.set_files(["Y", "Y"])


@given(
    parsers.parse("the check object output from the analyse function"),
    target_fixture="draft",
)
def given_draft():
    return JobDraft(MockAnalyser())


@parse.with_pattern(r"\d*")
def parse_number(text):
    return int(text) if text else None


@parse.with_pattern(r".*")
def parse_string(text):
    return text


CONVERTERS = {"String": parse_string, "Number": parse_number}


@when(parsers.cfparse("a {title:String} is given", CONVERTERS))
def title(draft, title):
    draft.set_title(title)


@when(parsers.cfparse("an {amount:Number} is set", CONVERTERS))
def amount(draft, amount):
    draft.set_amount(amount)


@when(
    parsers.cfparse(
        "an optional list of {failing_tests:Number} that is a subset of the same property in the check object",
        CONVERTERS,
    )
)
def failing_tests(draft, failing_tests):
    # hack to convert int to list
    draft.set_failing_tests(["X"] * failing_tests)


@when(
    parsers.cfparse(
        "an optional {is_editable:String} glob to match files that may be edited", CONVERTERS
    )
)
def is_editable(draft, is_editable):
    draft.set_is_editable(is_editable)


@when(
    parsers.cfparse(
        "an optional {is_addable:String} glob to match files that may be added", CONVERTERS
    )
)
def is_addable(draft, is_addable):
    draft.set_is_addable(is_addable)


@when(
    parsers.cfparse(
        "an optional {is_deletable:String} glob to match files that may be deleted", CONVERTERS
    )
)
def is_deletable(draft, is_deletable):
    draft.set_is_deletable(is_deletable)


@then(
    parsers.parse(
        "a JSON draft object containing the title, amount, failing_tests, is_editable, is_addable, is_deletable is printed to stdout"
    )
)
def should_have_json_output(draft):
    print(draft.json())


@then(parsers.parse("there should be no {error:d}"))
def should_be_no_error(draft, error):
    print(f"{draft=} {error=}")
    assert int(draft.error) == error
