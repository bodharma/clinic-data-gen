import numpy as np

import csv
import json
import uuid
import random
from pathlib import Path
from pymongo import MongoClient
from datetime import datetime, timedelta
import pkg.models.member.member_pb2 as Member
import pkg.models.core.accounts_pb2 as Accounts
import pkg.models.sponsor.sponsor_pb2 as Sponsor
import pkg.models.sponsor.plan_pb2 as Plan
import pkg.models.provider.provider_pb2 as Provider
import pkg.models.provider_group.provider_group_pb2 as ProviderGroup
import pkg.models.core.party_pb2 as Party
import pkg.models.core.contact_pb2 as Contact
import pkg.models.core.facility_pb2 as Facility
from google.protobuf.json_format import MessageToDict
from abc import ABC
from collections import OrderedDict
from mimesis import Person, Finance, Address, Internet
from generator_helpers import string_generator


class Generator(ABC):
    """
    Base class that shares methods for child classes
    """

    collection = None

    def __init__(self, use_mongo=False):
        if use_mongo:
            client = MongoClient("mongodb://localhost:27017/")
            db = client.banana
            self.collection = db[self.collection]

    def generate(self, count):
        return f"No return specified for {self.__class__.__name__}"

    @staticmethod
    def convert_protobuf_to_dict(data):
        """
        Convert proto data into python OrderedDict
        :param data: proto data
        :return: OrderedDict data
        """
        return np.array(
            [
                OrderedDict(MessageToDict(item, preserving_proto_field_name=True))
                for item in data
            ]
        )

    @staticmethod
    def convert_protobuf_to_request_body(data, **kwargs):
        """
        Convert proto data into request json body
        :param data: proto data
        :param kwargs: additional key-value entries that should be included to each data item
        :return: Request json data
        """
        response_list = []
        if data:
            for item in data:
                item = MessageToDict(item, preserving_proto_field_name=True)
                item.update(kwargs)
                response_list.append(json.dumps(item))

        return response_list

    def save_data_to_file(self, count, filepath, file_format="json"):
        """
        Saves proto data into csv/json file on disk.
        :param count: number of data items
        :param filepath: path, where we should store generated data
        :param file_format: file format json/csv
        :return: saves file on disk
        """
        json_file_path = Path(filepath)
        json_file_path.mkdir(exist_ok=True, parents=True)
        file_format = (
            file_format
            if file_format in ["csv", "json"]
            else Exception("csv or json only allowed")
        )
        generated_protobuf_data = self.generate(count)
        dict_data = self.convert_protobuf_to_dict(generated_protobuf_data)

        with open(
            f"{filepath}/{self.__class__.__name__}_data.{file_format}", "w+"
        ) as f:
            if file_format == "json":
                f.write(json.dumps(dict_data))
            else:
                csv_file = csv.DictWriter(f, fieldnames=list(dict_data[-1].keys()))
                csv_file.writeheader()
                csv_file.writerows(dict_data)

    def get_data_from_mongo(self):
        """
        :return: specific collection from mongo
        """
        return self.collection.find()

    def insert_data_to_mongo(self, count):
        """
        :param count: number of dataitems that should be generated
        :return: dataentries into mongo collection
        """
        generated_protobuf_data = self.generate(count)
        data = self.convert_protobuf_to_dict(generated_protobuf_data)

        if data:
            if len(data) > 1:
                return self.collection.insert_many(data)
            else:
                return self.collection.insert_one(data[-1])
        else:
            raise Exception("No data available")


class ContactGenerator(Generator):
    collection = "contact"

    def generate(self, count):
        person_fake = Person("en")
        internet_fake = Internet()
        businees_fake = Finance("en")

        contact_types = {
            "UNKNOWN_CONTACT_TYPE": 0,
            "PHONE_NUMBER": 1,
            "FAX_NUMBER": 2,
            "EMAIL_ADDRESS": 3,
            "WEBSITE_ADDRESS": 4,
            "POSTAL_ADDRESS": 5,
            "SOCIAL_MEDIA_HANDLE": 6,
        }
        contacts_list = []
        for _ in range(count):
            contact = Contact.Contact()

            contact_type = random.choice(list(contact_types.keys()))

            contact.contact_type = contact_types[contact_type]
            if "EMAIL" in contact_type:
                contact.email_address.email = person_fake.email(domains=["example.com"])
            elif "FAX" in contact_type:
                contact.fax_number.fax = f"{random.randint(0, 1111)}"
            elif "PHONE" in contact_type:
                contact.phone_number.phone = person_fake.telephone()
            elif "POSTAL" in contact_type:
                contact.postal_address.building_name.value = businees_fake.company()
            elif "WEBSITE" in contact_type:
                contact.website_address.website = internet_fake.home_page()
            contacts_list.append(contact)
        return contacts_list


class SponsorGenerator(Generator):
    collection = "sponsor"

    def generate(self, count):
        self.lifecycle_states_map = {
            "IDENTIFIED": 0,
            "ENGAGING": 1,
            "CONTRACTED": 2,
            "ONBOARDED": 3,
            "ACTIVE": 4,
            "TERMINATED": 5,
        }

        sponsors_list = []
        for _ in range(count):
            """
            party_id - existing organisation party id
            plans - list of plans
            accounts - here we create account
            """
            sponsor = Sponsor.Sponsor()
            sponsor.party_id = ""
            # sponsor.plans = "TEST-1050"
            # sponsor.plans.add().plan_code = 'TEST-1050'
            sponsor.lifecycle_state = random.choice(
                list(self.lifecycle_states_map.values())
            )
            # sponsor.accounts = ""
            # sponsor.rosterUploadIds = ""
            sponsors_list.append(sponsor)
        return sponsors_list


class PlanGenerator(Generator):
    def generate(self, count):
        """
        member_ids - list of member ids that belong to current plan, that is circular dependency
        """
        plans_list = []
        for _ in range(count):
            businees_fake = Finance("en")
            self.lifecycle_states_map = {
                "PLAN_CREATED": 0,
                "PLAN_ONBOARDED": 1,
                "PLAN_ACTIVE": 2,
            }

            plan = Plan.Plan()

            plan.plan_name = businees_fake.company()
            plan.plan_code = string_generator.bothify(text="????-########")
            # plan.member_ids = ""
            effective_dates_from = datetime.now() - timedelta(days=31)
            effective_dates_to = effective_dates_from + timedelta(days=31)

            plan.effective_dates.from_date.FromDatetime(effective_dates_from)
            plan.effective_dates.to_date.FromDatetime(effective_dates_to)

            plan.lifecycle_state = random.choice(
                list(self.lifecycle_states_map.values())
            )
            # plan.accounts = ""
            plans_list.append(plan)
        return plans_list


class ProviderGenerator(Generator):
    """
    Generates provider initial data, that is extended while using api:
    :var party_id: should be linked to person party_id
    :var collection: used as mongo collection identifier
    """

    collection = "provider"

    def generate(self, count):
        self.lifecyclestate_map = {
            # "IDENTIFIED": 0,
            # "NONPARTICIPATING": 1,
            "INCORPORATED": 2,
            "CREDENTIALED": 3,
            "INTEGRATED": 4,
            # "TERMINATED": 5,
            # "INELIGIBLE": 6,
        }
        providers_list = []
        if count:
            for _ in range(count):
                provider = Provider.Provider()
                # pary_id links to party person
                provider.party_id = ""
                provider.npi = f"{random.randint(1111111111, 9999999999)}"
                provider.lifecycle_state = random.choice(
                    list(self.lifecyclestate_map.values())
                )
                providers_list.append(provider)
        return providers_list


class ProviderGroupGenerator(Generator):
    """
    Generates provider groups initial data, that is extended while using api:
    :var party_id: should contain party_id of the party, that exist on environment
    :var facility_id: should contain facility_id of the facility, that exist on environment
    :var providers: should contain list of providers, that exist on environment
    :var collection: used as mongo collection identifier
    """

    collection = "provider_group"

    def generate(self, count):
        lifecycle_states = {"INTEGRATED": 8}

        entity_types = {"MEDICAL_GROUP": 2}

        provider_groups_list = []
        for _ in range(count):
            provider_group = ProviderGroup.ProviderGroup()
            provider_group.entity_type = entity_types["MEDICAL_GROUP"]
            provider_group.lifecycle_state = lifecycle_states["INTEGRATED"]
            provider_group.npi = str(random.randint(1111111111, 9999999999))
            # new provider group should have new party_id
            provider_group.party_id = ""

            # provider_group.credentials = ""
            # provider_group.accounts.external_party_financial_account_id = ""
            # provider_group.accounts.banana_financial_account_id = ""
            # provider_group.accounts.banana_ledger_account_id = ""
            # party.contacts.add().contact_id = ""
            provider_group.practice_facilities.add().facility_id = ""
            # provider_group.practice_facilities.add().practice_specialties = [""]
            provider_group.providers.append("")
            # provider_group.specialties = ""
            provider_groups_list.append(provider_group)
        return provider_groups_list


class AccountGenerator(Generator):
    def generate(self, count):
        accounts_list = Accounts.Accounts()
        for _ in range(count):
            financial_account = Accounts.FinancialAccount()
            financial_account.account_id = ""

            effective_dates_from = datetime.now() - timedelta(days=31)
            effective_dates_to = effective_dates_from + timedelta(days=31)
            financial_account.effective_dates.from_date.FromDatetime(
                effective_dates_from
            )
            financial_account.effective_dates.to_date.FromDatetime(effective_dates_to)

            # empty message in proto file banana-services-layer/pkg/models/core/accounts.proto
            # financial_account.ledger_account
            # financial_account.partner_account

            financial_account.bank_account.name = ""
            financial_account.bank_account.nick_name = ""
            financial_account.bank_account.routing_number = ""
            financial_account.bank_account.external_type = 0

            financial_account.status = 0
            accounts_list.accounts.append(financial_account)
        return accounts_list.accounts


class MemberGenerator(Generator):
    collection = "member"

    def generate(self, count):
        self.lifecycle_state_map = {
            # "IDENTIFIED": 0, # 0 is default for proto, ask specifically to display, TBD
            "ONBOARDING": 1,
            "ACTIVE": 2,
            "TERMINATED": 3,
        }

        members_list = []
        for _ in range(count):
            member = Member.Member()
            # account = AccountGenerator().generate(count=1)
            # member.account.CopyFrom(account[0])
            coverage_start_date = datetime.now()
            coverage_end_date = coverage_start_date + timedelta(days=31)
            # member._id = str(uuid.uuid4())
            # member.card_id = str(random.randint(1000000000, 9999999999))
            member.coverage_start_date.FromDatetime(coverage_start_date)
            member.coverage_end_date.FromDatetime(coverage_end_date)
            member.employee_id.value = ""
            member.lifecycle_state = random.choice(
                list(self.lifecycle_state_map.values())
            )
            member.party_id = ""
            # TODO: party should be valid
            # TODO: make party generator
            # member.plan_code = f"TEST-{random.randint(10000, 99999)}"
            # member.plan_code = ""
            # member.primary_member_employee_id.value = ""
            # member.sponsor_id = ""
            # TODO: needs to be a real plan that is defined on the correct sponsor and that plan also contains the member id
            # TODO: make sponsor generator
            members_list.append(member)
            del member
        return members_list


class PartyGenerator(Generator):
    """
    Generates provider initial data, that is extended while using api:
    Methods:
        - gen_person: generates person party
        - gen_organisation: generates organisation party
        - gen: generates specified amount of both person and organisation parties data
    :var collection: used as mongo collection identifier
    """

    def __init__(self, person=True):
        super(PartyGenerator, self).__init__()
        self.person = person

    collection = "party"

    def generate(self, count):
        data_list = []
        organisation_kind_dict = {
            # "OTHER": 0,
            "INFORMAL_ORGANIZATION": 1,
            "LEGAL_ORGANIZATION": 2,
        }
        sex_dict = {"MALE": 1, "FEMALE": 2, "AMBIGUOUS": 3, "OTHER": 4}

        if self.person:
            for _ in range(count):
                party = Party.Party()
                person_fake = Person("en")
                party.party_type = 1

                party.person.current_name.names.append(person_fake.first_name())
                party.person.current_name.names.append(person_fake.last_name())
                party.person.birth_sex = sex_dict[random.choice(list(sex_dict.keys()))]
                party.person.birth_date = "test"
                party.person.ethnicity = ""
                for _ in range(random.randint(5, 10)):
                    party.contacts.add()
                    party.contacts[_].contact_id = f"{uuid.uuid4()}"
                    party.contacts[_].is_primary = False
                    party.contacts[_].purpose = f"Test {_}"
                party.effective_roles.add()
                party.effective_roles[-1].party_role_id = "111"
                effective_dates_from = datetime.now() - timedelta(days=31)
                effective_dates_to = effective_dates_from + timedelta(days=31)
                party.effective_roles[-1].effective_dates.from_date.FromDatetime(
                    effective_dates_from
                )
                party.effective_roles[-1].effective_dates.to_date.FromDatetime(
                    effective_dates_to
                )
                data_list.append(party)
        else:
            for _ in range(count):
                party = Party.Party()
                bussiness_fake = Finance("en")
                party.party_type = 2
                party.organization.entity_name = bussiness_fake.company()

                party.organization.organization_kind = organisation_kind_dict[
                    "LEGAL_ORGANIZATION"
                ]
                party.organization.legal_organization.legal_organization_type = 1
                party.organization.legal_organization.tax_id = (
                    f"{random.randint(11, 99)}-{random.randint(1111111, 9999999)}"
                )
                party.contacts.add()
                party.contacts[-1].contact_id = ""
                data_list.append(party)
        return data_list


class FacilityGenerator(Generator):
    """
    Generates facility data that is used by provider group
    """

    def generate(self, count):
        address_fake = Address("en")
        business_fake = Finance("en")
        facilities_list = []
        for _ in range(count):
            facility = Facility.Facility()
            facility.location_type = 1
            facility.postal_address.building_name.value = business_fake.company()
            facility.postal_address.city_town = address_fake.city()
            facility.postal_address.country.value = "USA"
            facility.postal_address.postal_code = address_fake.postal_code()
            facility.postal_address.state_province = address_fake.state()
            facility.postal_address.street_address1 = address_fake.address()
            facility.postal_address.street_address2.value = address_fake.address()
            facility.postal_address.unit_number.value = address_fake.street_number()
            facilities_list.append(facility)
        return facilities_list


if __name__ == "__main__":
    count = 1
    from pprint import pprint

    # ContactGenerator().generate(count)
    # SponsorGenerator().generate(count)
    # PlanGenerator().generate(count)
    # ProviderGenerator().generate(count)
    # ProviderGroupGenerator().generate(count)
    # AccountGenerator().generate(count)
    # MemberGenerator().generate(count)
    pprint(PartyGenerator(person=False).generate(1))
    # PartyGenerator(entries_number=count).generate()
    # FacilityGenerator().generate(count)
