from engi_cli.blockchain_api import User
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../features/create_user.feature")


@given(
    parsers.parse("an account {name}, {password1} and {password2}"),
    target_fixture="user",
)
def given_user(name, password1, password2):
    return User(name, password1, password2)


@when(parsers.parse("the name is unique"))
def unique_user(user):
    assert user.name_unique


@when(parsers.parse("password1 equals password2"))
def passwords_match(user):
    pass


@when(parsers.parse("password1 meets constraints"))
def passwords_match(user):
    pass


@then(
    parsers.parse(
        "a JSON account object containing a generated recovery mnemonic and wallet address is printed to stdout"
    )
)
def should_have_json_output(user):
    print(user.json())


@then(parsers.parse("there should be no {error:d}"))
def should_be_no_error(user, error):
    assert int(user.error) == error
