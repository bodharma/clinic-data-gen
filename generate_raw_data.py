import random
import uuid
import csv
from multiprocessing import Pool
from mimesis import Person, Finance, Address
from generator_helpers import date_generator
import datetime
from pathlib import Path


def generate_address():
    """
    generate data that can be used by account, member, etc
    :return:
    """
    address = Address("en")

    address_schema = {
        "primary_address_line1": address.address(),
        "primary_address_line2": address.address(),
        "primary_address_city": address.city(),
        "primary_address_state": address.state(abbr=True),
        "primary_address_zipcode": address.postal_code(),
    }

    return address_schema


class MemberRoster:
    """
    Used to generate data for EDI file for adjudication.
    Member scheme is reversed from edi converter -> generate_edi.py
    """

    def __init__(self, processes_number=8):
        self.processes_number = processes_number

    def member_schema(self, _):
        fake_person = Person("en")
        fake_businees = Finance("en")
        """
        Values that are commented are not yet needed for use.
        :return: data for 1 member according to edi converter required values
        """
        first_name = fake_person.first_name()
        last_name = fake_person.last_name()
        company = fake_businees.company()
        member_schema = {
            "identity_id": f"{uuid.uuid4()}",
            "last_name": last_name,
            "first_name": first_name,
            "middle_name": f"{random.choice(['A', 'B', 'C', 'D', 'Z'])}",
            "gender": random.choice(["Male", "Female"]),
            "birth_date": date_generator.date_time_between(start_date="-90y").strftime(
                "%m/%d/%Y"
            ),
            "ssn": f"{random.randint(111, 999)}-{random.randint(11, 99)}-{random.randint(1111, 9999)}",
            "mobile_phone_number": f"({random.randint(111, 999)}) {random.randint(111, 999)}-{random.randint(1111, 9999)}",
            "home_phone_number": f"({random.randint(111, 999)}) {random.randint(111, 999)}-{random.randint(1111, 9999)}",
            "ethnicity": random.choice(["Asian", "Black", "White", "Hispanic"]),
            "email": fake_person.email(domains=["example.com"]),
            "Sponsor": company,
            "Plan": "MIGR-10010",
            "banana ID": random.randint(1111111, 9999999),
            "Note": random.choice(["Executive, Sponsor", f"Member - {company}"]),
        }
        member_schema.update(generate_address())

        return member_schema

    def generate(self, members_num):
        """
        Generate member data list
        :param members_num: number of members to generate
        :return: members list ready for use
        """
        pool = Pool(self.processes_number)
        result = pool.map(self.member_schema, range(members_num))
        return result

    def save_to_csv(self, filename, data_list):
        """
        Saves generated datalist int csv file.
        Currently we use member data only.

        :param filename: name of the file we want to save to.
        :param data_list: list of generated entries
        :return: *.csv file on disk
        """
        field_names = [
            "identity_id",
            "last_name",
            "first_name",
            "middle_name",
            "gender",
            "birth_date",
            "ssn",
            "mobile_phone_number",
            "home_phone_number",
            "ethnicity",
            "primary_address_line1",
            "primary_address_line2",
            "primary_address_city",
            "primary_address_state",
            "primary_address_zipcode",
            "email",
            "Sponsor",
            "Plan",
            "banana ID",
            "Note",
        ]
        csv_file = csv.DictWriter(open(f"{filename}", "w+"), field_names)
        csv_file.writeheader()
        csv_file.writerows(data_list)


class VaccinedPatient:
    def __init__(self, entries_number=1, processes_number=8):
        self.processes_number = int(processes_number)
        self.entries_number = int(entries_number)

    def build_schema(self, _):
        self.fake = Person("en")
        vaccine_administered = date_generator.date_time_between(start_date="-3M")
        dob = date_generator.date_time_between(start_date="-70y", end_date="-15y")
        schema = {
            "Vaccine Administered Date/Time": vaccine_administered.strftime(
                "%d/%m/%Y %H:%M:%S"
            ),
            "Manufacturer": random.choice(["PFIZER", "MODERNA", "JOHNSON"]),
            "Email Address": self.fake.email(domains=["example.com"]),
            "Date of Birth": dob.strftime("%d/%m/%Y"),
            "Dose": random.choice(["Initial Dose", "Second Dose"]),
            "First Name": self.fake.first_name(),
            "Last Name": self.fake.last_name(),
            "Full Name": "",
            "Patient ID": str(uuid.uuid4()),
        }
        schema["Full Name"] = f"{schema['First Name']} {schema['Last Name']}"
        return schema

    def generate(self):
        pool = Pool(self.processes_number)
        result = pool.map(self.build_schema, range(self.entries_number))
        return result

    def csv(self, filepath=None):
        now = datetime.datetime.now()
        filepath = (
            filepath
            if filepath
            else Path(f"{Path.cwd()}/{now.year}/{now.month}/{now.day}/")
        )
        Path(filepath).mkdir(exist_ok=True, parents=True)

        filename = f"{filepath}test_delta_match_data_{int(now.timestamp())}.csv"
        data_list = self.generate()
        csv_file = csv.DictWriter(open(filename, "w+"), fieldnames=data_list[-1].keys())
        csv_file.writeheader()
        csv_file.writerows(data_list)
        return filename


if __name__ == "__main__":
    mmbr = VaccinedPatient(entries_number=10)
    data_list = mmbr.generate()
    mmbr.csv("test_data.csv")
