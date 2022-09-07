import pytest
from engi_cli.helpful_scripts import Job, JobDraft
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../features/create_job.feature")


@given(
    parsers.parse("the draft object output from the draft function"),
    target_fixture="job",
)
def given_job():
    return Job(JobDraft())


@when(parsers.parse("the {secret} string from the user account is given"))
def secret(job, secret):
    job.set_secret(secret)


@when(parsers.parse("an option {tip:d} is set"))
def tip(job, tip):
    job.set_tip(tip)


@then(parsers.parse("a unique identifier for the job is printed to stdout"))
@pytest.mark.asyncio
async def create(job):
    # TODO does pytest_bdd play nice with asyncio?
    print(await job.create())
