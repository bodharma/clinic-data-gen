import httpx
from abc import ABC
from generate_protobuf_data import (
    ProviderGroupGenerator,
    PartyGenerator,
    FacilityGenerator,
    MemberGenerator,
    ProviderGenerator,
    SponsorGenerator,
    PlanGenerator,
)
from datetime import datetime
from loguru import logger
import random
from pathlib import Path
import json
from csv import DictWriter


class API(ABC):
    """
    Base class used for handling of generated data through api endpoints.
    """

    def __init__(
        self, url="https://localhost:8000", api_version="api/v3"
    ):
        self.url = url
        self.api_version = api_version
        self.api_base_url = f"{self.url}/{self.api_version}"

    def create(self):
        pass

    def get(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class Member(API):
    def __init__(self, url, api_version):
        super(Member, self).__init__(url, api_version)
        if "3" in self.api_version:
            self.member_api_url = f"{self.api_base_url}/members"
            self.member = MemberGenerator()

    async def get(self, _id=None):
        if _id:
            response = httpx.post(f"{self.member_api_url}/{_id}/getById")
        else:
            response = httpx.post(f"{self.member_api_url}/query")
        if response.status_code != 200:
            logger.warning(
                f"Response code: {response.status_code} | content:\n{response.text}"
            )
        return response.json()

    async def create(self, **kwargs):
        response_data_list = []
        for body in self.member.convert_protobuf_to_request_body(
            self.member.generate(1), **kwargs
        ):
            response = httpx.post(
                f"{self.member_api_url}/create",
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer <token_example>",
                },
            )
            if response.status_code not in [201, 200]:
                logger.warning(
                    f"Response code: {response.status_code} | content:\n{response.text}"
                )
            else:
                status = "created" if response.status_code == 201 else "exists"
                logger.debug(f"Member {status}: {response.json()['_id']}")
            response_data_list.append(response.json())
        return response_data_list


class ProviderGroup(API):
    def __init__(self, url, api_version):
        super(ProviderGroup, self).__init__(url, api_version)
        if "3" in self.api_version:
            self.provider_group_api_url = f"{self.api_base_url}/providerGroups"

    async def get(self, _id=None):
        if _id:
            response = httpx.post(f"{self.provider_group_api_url}/{_id}/getById")
        else:
            response = httpx.post(f"{self.provider_group_api_url}/query")

        if response.status_code != 200:
            logger.warning(
                f"Response code: {response.status_code} | content:\n{response.text}"
            )

        return response.json()

    async def create(self, **kwargs):
        bodies_list = ProviderGroupGenerator.convert_protobuf_to_request_body(
            ProviderGroupGenerator().generate(1), **kwargs
        )
        response_data = []
        for body in bodies_list:
            response = httpx.post(
                f"{self.provider_group_api_url}/create",
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer <token_example>",
                },
            )
            if response.status_code not in [201, 200]:
                logger.warning(
                    f"Response code: {response.status_code} | content:\n{response.text}"
                )
            else:
                status = "created" if response.status_code == 201 else "exists"
                logger.debug(f"Provider group {status}: {response.json()['_id']}")
            response_data.append(response.json())
        return response_data


class Party(API):
    def __init__(self, url, api_version):
        super(Party, self).__init__(url, api_version)
        if "3" in self.api_version:
            self.party_api_url = f"{self.api_base_url}/parties"

    async def get(self):
        response = httpx.post(f"{self.party_api_url}/query")

        if response.status_code != 200:
            logger.warning(
                f"Response code: {response.status_code} | content:\n{response.text}"
            )
        return response.json()

    async def create(self, count, organization=False):
        if organization:
            body_list = PartyGenerator.convert_protobuf_to_request_body(
                PartyGenerator(person=False).generate(count)
            )
        else:
            body_list = PartyGenerator.convert_protobuf_to_request_body(
                PartyGenerator(person=True).generate(count)
            )
        response_list = []
        for body in body_list:
            response = httpx.post(
                f"{self.party_api_url}/create",
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer <token_example>",
                },
            )

            if response.status_code not in [201, 200]:
                logger.warning(
                    f"Response code: {response.status_code} | content:\n{response.text}"
                )
            else:
                status = "created" if response.status_code == 201 else "exists"
                logger.debug(
                    f"{'Organisation' if organization else 'Person'} Party {status}: {response.json()['_id']}"
                )
                response_list.append(response.json())
        return response_list


class Provider(API):
    def __init__(self, url, api_version):
        super(Provider, self).__init__(url, api_version)
        if "3" in self.api_version:
            self.provider_api_url = f"{self.api_base_url}/providers"

    async def get(self, _id=None):
        if _id:
            response = httpx.post(f"{self.provider_api_url}/{_id}/getById")
        else:
            response = httpx.post(f"{self.provider_api_url}/query")

        if response.status_code != 200:
            logger.warning(
                f"Response code: {response.status_code} | content:\n{response.text}"
            )

        return response.json()

    async def create(self, party_id):
        bodies_list = ProviderGenerator.convert_protobuf_to_request_body(
            ProviderGenerator().generate(1), party_id=party_id
        )
        response_data = []
        for body in bodies_list:
            response = httpx.post(
                f"{self.provider_api_url}/create",
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer <token_example>",
                },
            )
            if response.status_code not in [201, 200]:
                logger.warning(
                    f"Response code: {response.status_code} | content:\n{response.text}"
                )
            else:
                status = "created" if response.status_code == 201 else "exists"
                logger.debug(f"Provider {status}: {response.json()['_id']}")
            response_data.append(response.json())
        return response_data


async def create_provider_group(count, url, api_version):
    filename = Path(
        f'results/{datetime.now().strftime("%Y_%m_%d_%H_%M")}_providergroup_2_party.csv'
    )
    csv_writer = DictWriter(
        open(filename, "w+"), fieldnames=["party_id", "provider_group_id"]
    )
    csv_writer.writeheader()

    for _ in range(count):
        prt = Party(url, api_version)
        prvd_grp = ProviderGroup(url, api_version)
        fclt = Facility(url, api_version)

        created_facilities_list = await fclt.create(random.randint(1, 5))
        practice_facilities = [
            {"facility_id": facility["_id"]} for facility in created_facilities_list
        ]

        prt_id_result = await prt.create(organization=True, count=1)
        prt_id = prt_id_result[-1]["_id"]

        prvd_grp_result = await prvd_grp.create(
            party_id=prt_id, practice_facilities=practice_facilities
        )
        prvd_grp_id = prvd_grp_result[-1]["_id"]

        csv_writer.writerow({"party_id": prt_id, "provider_group_id": prvd_grp_id})
    return filename.absolute()


async def create_member(member_data):
    members_count = member_data.members_count
    url = member_data.url
    api_version = member_data.api_version

    prt = Party(url, api_version)
    spnsr = Sponsor(url, api_version)
    mmbr = Member(url, api_version)

    results_dir = Path(f"{Path.cwd()}/results")
    results_dir.mkdir(exist_ok=True)
    filename = Path(
        f'{results_dir}/{datetime.now().strftime("%Y_%m_%d_%H_%M")}_members.json'
    )
    json_data_list = []

    json_file = open(filename, "w+")
    for _ in range(members_count):
        org_prt_result = await prt.create(count=1, organization=True)
        org_prt_id = org_prt_result[-1]["_id"]
        spnsr_id_result = await spnsr.create(1, party_id=org_prt_id)
        spnsr_id = spnsr_id_result[-1]["_id"]
        prt_id_result = await prt.create(1)
        prt_id = prt_id_result[-1]["_id"]
        mmbr_id_result = await mmbr.create(party_id=prt_id, sponsor_id=spnsr_id)
        mmbr_id = mmbr_id_result[-1]["_id"]
        json_data_list.append(
            {
                "organisation_party_id": org_prt_id,
                "sponsor_id": spnsr_id,
                "person_party_id": prt_id,
                "member_id": mmbr_id,
            }
        )
    json_file.write(json.dumps(json_data_list))

    return str(filename.absolute())


async def create_provider_group_with_providers_and_facilities(provider_group_data):
    facilities_count = provider_group_data.facilities_count
    providers_count = provider_group_data.providers_count
    provider_groups_count = provider_group_data.provider_group_count
    url = provider_group_data.url
    api_version = provider_group_data.api_version

    results_dir = Path(f"{Path.cwd()}/results")
    results_dir.mkdir(exist_ok=True)
    filename = Path(
        f'{results_dir}/{datetime.now().strftime("%Y_%m_%d_%H_%M")}_provider_2_providergroup.json'
    )
    json_data_list = []

    json_file = open(filename, "w+")
    for _ in range(provider_groups_count):
        prt = Party(url, api_version)
        prvd = Provider(url, api_version)
        prvd_grp = ProviderGroup(url, api_version)
        fclt = Facility(url, api_version)
        facilities_count = (
            facilities_count if facilities_count else random.randint(1, 5)
        )
        providers_count = providers_count if providers_count else random.randint(0, 10)
        prvds_list = []

        created_facilities_list = await fclt.create(facilities_count)
        practice_facilities = [
            {"facility_id": facility["_id"]} for facility in created_facilities_list
        ]

        for _ in range(providers_count):
            party_result = await prt.create(1)
            prt_id = party_result[-1]["_id"]
            provider_result = await prvd.create(party_id=prt_id)
            prvds_list.append(provider_result[-1]["_id"])

        org_prt_result = await prt.create(count=1, organization=True)
        org_prt_id = org_prt_result[-1]["_id"]
        prvd_grp_result = await prvd_grp.create(
            party_id=org_prt_id,
            providers=prvds_list,
            practice_facilities=practice_facilities,
        )
        prvd_grp_id = prvd_grp_result[-1]["_id"]

        json_data_list.append(
            {
                "org_party_id": org_prt_id,
                "provider_group_id": prvd_grp_id,
                "provider_ids_list": prvds_list,
                "facility_ids_list": practice_facilities,
            }
        )
    json_file.write(json.dumps(json_data_list))

    return str(filename.absolute())


class Facility(API):
    def __init__(self, url, api_version):
        super(Facility, self).__init__(url, api_version)
        if "3" in self.api_version:
            self.facility_api_url = f"{self.api_base_url}/facilities"
            self.facility = FacilityGenerator()

    async def get(self):
        async with httpx.AsyncClient() as client:
            response = client.post(f"{self.facility_api_url}/query")

        if response.status_code != 200:
            logger.warning(
                f"Response code: {response.status_code} | content:\n{response.text}"
            )
        return response.json()

    async def create(self, count):
        body_list = self.facility.convert_protobuf_to_request_body(
            self.facility.generate(count)
        )
        response_list = []
        async with httpx.AsyncClient() as client:
            for body in body_list:
                response = await client.post(
                    f"{self.facility_api_url}/create",
                    data=body,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer <token_example>",
                    },
                )
                if response.status_code not in [201, 200]:
                    logger.warning(
                        f"Response code: {response.status_code} | content:\n{response.text}"
                    )
                else:
                    status = "created" if response.status_code == 201 else "exists"
                    logger.debug(f"Facility {status}: {response.json()['_id']}")
                response_list.append(response.json())
        return response_list


class Sponsor(API):
    def __init__(self, url, api_version):
        super(Sponsor, self).__init__(url, api_version)
        if "3" in self.api_version:
            self.sponsor_api_url = f"{self.api_base_url}/sponsors"
            self.sponsor = SponsorGenerator()
            self.plan = PlanGenerator()

    async def create(self, count, party_id):
        body_list = self.sponsor.convert_protobuf_to_request_body(
            self.sponsor.generate(count), party_id=party_id
        )
        response_list = []
        async with httpx.AsyncClient() as client:
            for body in body_list:
                response = await client.post(
                    f"{self.sponsor_api_url}/create",
                    data=body,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer <token_example>",
                    },
                )
                if response.status_code not in [201, 200]:
                    logger.warning(
                        f"Response code: {response.status_code} | content:\n{response.text}"
                    )
                else:
                    status = "created" if response.status_code == 201 else "exists"
                    logger.debug(f"Sponsor {status}: {response.json()['_id']}")
                response_list.append(response.json())
        return response_list

    async def add_plan(self, sponsor_id, count):
        plan_codes_list = []
        body_list = self.plan.convert_protobuf_to_request_body(
            self.plan.generate(count)
        )
        async with httpx.AsyncClient() as client:
            for body in body_list:
                response = await client.post(
                    f"{self.sponsor_api_url}/{sponsor_id}/addPlans",
                    data=body,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": "Bearer <token_example>",
                    },
                )
                if response.status_code not in [201, 200]:
                    logger.info(
                        f"Response code: {response.status_code} | content:\n{response.text}"
                    )
                    plan_codes_list.append(response.json()["plan_code"])
                else:
                    status = "created" if response.status_code == 201 else "exists"
                    logger.debug(
                        f"Plan {status}: {response.json()['plan_code']}{response.json()['plan_name']}"
                    )
        return plan_codes_list

    async def add_members_ids(self, plan_code, sponsor_id, members_ids_list):
        body = {
            "members_ids": members_ids_list,
            "planCode": plan_code,
            "sponsorId": sponsor_id,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.sponsor_api_url}/{sponsor_id}/plans/{plan_code}/addMembers",
                data=body,
                headers={"Content-Type": "application/json"},
            )
        if response.status_code not in [201, 200]:
            logger.warning(
                f"Response code: {response.status_code} | content:\n{response.text}"
            )
        else:
            status = "created" if response.status_code == 201 else "exists"
            logger.debug(f"Sponsor {status}: {response.json()['_id']}")


async def create_sponsor_with_plan(sponsor_data):
    sponsors_count = sponsor_data.sponsors_count
    plans_count = (
        sponsor_data.plans_count if sponsor_data.plans_count else random.randint(1, 10)
    )
    url = sponsor_data.url
    api_version = sponsor_data.api_version
    members_ids_list = sponsor_data.members_ids_list
    spnsr = Sponsor(url=url, api_version=api_version)
    prt = Party(url, api_version)

    results_dir = Path(f"{Path.cwd()}/results")
    results_dir.mkdir(exist_ok=True)
    filename = Path(
        f'{results_dir}/{datetime.now().strftime("%Y_%m_%d_%H_%M")}_sponsor.json'
    )
    json_data_list = []

    json_file = open(filename, "w+")
    for _ in range(sponsors_count):
        org_prt_result = await prt.create(count=1, organization=True)
        org_prt_id = org_prt_result[-1]["_id"]
        spnsr_result = await spnsr.create(1, party_id=org_prt_id)
        spnsr_id = spnsr_result[-1]["_id"]
        plans_codes_list = await spnsr.add_plan(sponsor_id=spnsr_id, count=plans_count)
        if members_ids_list:
            for plan_code in plans_codes_list:
                await spnsr.add_members_ids(
                    sponsor_id=spnsr_id,
                    plan_code=plan_code,
                    members_ids_list=members_ids_list,
                )
        json_data_list.append(
            {
                "organisation_party_id": org_prt_id,
                "sponsor_id": spnsr_id,
                "plans_ids_list": plans_codes_list,
                "members_ids_list": members_ids_list,
            }
        )
    json_file.write(json.dumps(json_data_list))

    return str(filename.absolute())


if __name__ == "__main__":
    import asyncio

    class A:
        provider_group_count = 1
        providers_count = 1
        facilities_count = 1
        url = "https://localhost:8000"
        api_version = "api/v3"

    asyncio.run(create_provider_group_with_providers_and_facilities(A))
