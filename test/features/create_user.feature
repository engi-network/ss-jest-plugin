@analyse
Feature: Create user
    As someone in need of help writing code,
    Or someone wanting to earn money for writing code
    I want to create an account
    So I can buy or sell work in the Engi marketplace

    Scenario Outline: New account created
        Given an account <name>, <password1> and <password2>
        When password1 equals password2
        # TODO password constraints
        And password1 meets constraints
        Then a JSON account object containing a generated recovery mnemonic and wallet address is printed to stdout
        And there should be no <error>

        Examples:
            | name   | password1 | password2 | error |
            | cck197 | password  | password  | 0     |
            | cck197 | foo       | bar       | 1     |
