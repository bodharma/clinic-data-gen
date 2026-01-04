import pytest
from flaky import flaky
from generate_protobuf_data import (
    ContactGenerator,
    SponsorGenerator,
    PlanGenerator,
    ProviderGenerator,
    ProviderGroupGenerator,
    AccountGenerator,
    MemberGenerator,
    PartyGenerator,
    FacilityGenerator,
)


@flaky(max_runs=2)
@pytest.mark.parametrize(
    "generator",
    [
        ContactGenerator,
        SponsorGenerator,
        PlanGenerator,
        ProviderGenerator,
        ProviderGroupGenerator,
        AccountGenerator,
        MemberGenerator,
        FacilityGenerator,
        PartyGenerator,
    ],
)
def test_generate_data(generator):
    assert generator().generate(1)


def test_generate_organisation_party():
    assert PartyGenerator(person=False).generate(1)
