@analyse
Feature: Analyse repository
    As someone in need of help writing code,
    I want to analyse my code repository
    So I can create a draft job listing to post on the Engi marketplace

    Scenario Outline: Create check object containing list of failing tests
        Given the codebase located at <repo>
        When the codebase is written in <language>
        And optional branch named <branch>
        And optional commit hash <commit>
        And has <docker> support
        And contains <failing_tests>
        Then a JSON check object containing a list of failing tests is printed to stdout
        And there should be no <error>

        # image failing_tests is a list of length shown in the column
        # TODO write a custom parser for lists
        Examples:
            | repo                             | branch | commit  | language | docker | failing_tests | error |
            | engi-network/engi-blockchain-gql | master | b0486b6 | C#       | 1      | 1             | 0     |
            | engi-network/engi-blockchain-gql | master | b0486b6 | C#       | 0      | 0             | 1     |
            | engi-network/same-story-api      | master | b0486b6 | Python   | 1      | 0             | 1     |