@analyse
Feature: Create job
    As someone in need of help writing code,
    I want to take the output of the draft function and create a new job
    So I can create a job listing to post on the Engi marketplace

    Scenario Outline: Create a new job
        Given the draft object output from the draft function
        When the <secret> string from the user account is given
        And an option <tip> is set
        Then a unique identifier for the job is printed to stdout

        Examples:
            | secret                                                                 | tip |
            | time treat merit corn crystal fiscal banner zoo jacket pulse frog long | 10  |
