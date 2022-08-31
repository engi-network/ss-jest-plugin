@analyse
Feature: Analyse repository
    As someone in need of help writing code,
    I want to analyse my code repository
    So I can create a draft job listing to post on the Engi marketplace

    Scenario Outline: Create check object containing list of failing tests
        Given the codebase located at <repo>
        When the codebase is written in <language>
        And has <docker> support
        And contains <failing_tests>
        Then a <json> check object containing a list of failing tests is printed to stdout
        And there should be no <error>

        Examples:
            | repo                             | language | docker | failing_tests | json | error |
            | engi-network/engi-blockchain-gql | C#       | 1      | 1             | 1    | 0     |
            | engi-network/engi-blockchain-gql | C#       | 0      | 0             | 0    | 1     |
            | engi-network/same-story-api      | Python   | 1      | 1             | 0    | 1     |