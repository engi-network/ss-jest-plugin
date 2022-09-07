@analyse
Feature: Create draft
    As someone in need of help writing code,
    I want to take the output of the analyse function and select the tests and editable files
    I'll add a title and amount I'm willing to pay
    So I can create a job listing to post on the Engi marketplace

    Scenario Outline: Create draft job object containing a title, amount, tests and files
        Given the check object output from the analyse function
        When a <title> is given
        And an <amount> is set
        And an optional list of <failing_tests> that is a subset of the same property in the check object
        And an optional <is_editable> glob to match files that may be edited
        And an optional <is_addable> glob to match files that may be added
        And an optional <is_deletable> glob to match files that may be deleted
        Then a JSON draft object containing the title, amount, failing_tests, is_editable, is_addable, is_deletable is printed to stdout
        And there should be no <error>

        # imagine failing_tests and files are lists of length shown in the column
        # if the value in the column is 0, then assume all the things are editable
        # TODO write a custom parser for lists
        Examples:
            | title | amount | failing_tests | is_editable | is_addable | is_deletable | error |
            | one   | 10     | 2             | *.py        |            |              | 0     |
            | two   | 10     | 0             | *.cs        |            |              | 0     |
            | three | 10     | 2             | *.js        |            |              | 0     |
            |       | 10     | 2             | *.py        |            |              | 1     |
            | five  |        | 0             | *.py        |            |              | 1     |