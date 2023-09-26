import random
from generator_helpers import date_generator, string_generator
from mimesis import Person, Business, Address
import pandas as pd
import time
from datetime import datetime
from pathlib import Path


class Generator:
    def generate_entries(self):
        pass

    def csv(self, filepath=None):
        now = datetime.now()
        filepath = (
            filepath
            if filepath
            else Path(f"{Path.cwd()}/{now.year}/{now.month}/{now.day}")
        )
        Path(filepath).mkdir(exist_ok=True, parents=True)

        filename = f"{filepath}/mock_vaccine_databus_sample_{int(now.timestamp())}.csv"
        self.generate_entries().to_csv(filename, index=False, header=True)
        return filename

    def json(self, filepath=None, filename=""):
        now = datetime.now()
        filepath = (
            filepath
            if filepath
            else Path(f"{Path.cwd()}/{now.year}/{now.month}/{now.day}")
        )
        Path(filepath).mkdir(exist_ok=True, parents=True)

        filename = f"{filepath}/{filename}_mock_vaccine_databus_sample_{int(now.timestamp())}.json"
        self.generate_entries().to_json(filename, orient="records", double_precision=0)
        return filename


class Encounters(Generator):
    def __init__(self, entries_number, dose_number=None, vaccine_type=None):
        self.vaccine_type = vaccine_type
        self.dose_number = dose_number
        self.entries_number = int(entries_number)
        self.address = Address("en")
        self.business = Business("en")
        self.person = Person("en")

    def generate_entries(self):
        insurance_data = pd.read_csv(
            "templates/databus/Banana Care Insurance Master List 14-May-2021.csv"
        )
        location_data = pd.read_csv(
            "templates/databus/Banana Care Location Master List 14-May-2021 v2.csv"
        )

        insurance_member_id_str = [
            f"{string_generator.bothify('??#####??')}"
            for i in range(insurance_data["memberID"].count())
        ]
        insurance_data["memberID"] = insurance_member_id_str

        member_ids_list = [
            random.choice(insurance_member_id_str) if count % 10 == 0 else ""
            # , string_generator.bothify(text="1???7")
            for count, i in enumerate(range(self.entries_number))
        ]

        schema = {
            "mrnNumber": [
                string_generator.bothify(text="#####-#####")
                for i in range(self.entries_number)
            ],
            "beginningDateOfService": [
                date_generator.date_time_between(start_date="-2w").strftime(
                    "%Y-%m-%dT%H:%M:%S"
                )
                for i in range(self.entries_number)
            ],
            # "locationAddress": [
            #     self.address.address() for _ in range(self.entries_number)
            # ],
            # "locationCity": [self.address.city() for _ in range(self.entries_number)],
            # "locationZipCode": [
            #     self.address.state(abbr=True) for i in range(self.entries_number)
            # ],
            "memberID": member_ids_list,
            "no_insurance": [
                False if member_id else True for member_id in member_ids_list
            ],
            # "insurance_name": [self.business.company() for _ in range(self.entries_number)],
            # "insurance_plan_phone": [self.person.telephone() for _ in range(self.entries_number)],
            "procedure": [
                {
                    "procedure_type": "vaccination",
                    "vaccine_type": str(self.vaccine_type)
                    if self.vaccine_type
                    else random.choice(
                        ["Pfizer", "Moderna", "Janssen", "AstraZeneca", "Novavax"]
                    ),
                    "dose": str(self.dose_number)
                    if self.dose_number
                    else random.choice(["1", "2"]),
                }
                for _ in range(self.entries_number)
            ],
            "Organization ID": [
                random.randint(1, 37) for _ in range(self.entries_number)
            ],
        }
        encounter_data_frame = pd.DataFrame(schema, columns=schema.keys())
        merged_insurance = encounter_data_frame.merge(
            insurance_data[["insurance_name", "insurance_plan_phone", "memberID"]],
            on=["memberID"],
            how="left",
        )
        merged_insurance.insurance_plan_phone_number = merged_insurance.insurance_plan_phone.fillna(
            0
        ).astype(
            int
        )
        merged_location = merged_insurance.merge(
            location_data[
                [
                    "locationAddress",
                    "locationCity",
                    "locationZipCode",
                    "Organization ID",
                ]
            ],
            on=["Organization ID"],
            how="left",
        )
        merged_location.fillna("")
        merged_location["Organization ID"] = merged_location["Organization ID"].apply(
            str
        )

        del merged_location["Organization ID"]
        return merged_location


class EncounterPatient(Generator):
    def __init__(self, entries_number):
        self.entries_number = int(entries_number) - 1
        self.address = Address("en")
        self.person = Person("en")

    def generate_entries(self):
        schema = {
            "patient_first_name": [
                self.person.first_name() for _ in range(self.entries_number)
            ],
            "patient_last_name": [
                self.person.last_name() for _ in range(self.entries_number)
            ],
            "patient_dob": [
                date_generator.date_time_between(
                    start_date="-80y", end_date="-10y"
                ).strftime("%Y-%m-%d")
                for _ in range(self.entries_number)
            ],
            "patient_gender": [
                random.choice(["male", "female", "other"])
                for _ in range(self.entries_number)
            ],
            "patient_address": [
                self.address.address() for _ in range(self.entries_number)
            ],
            "patient_address2": [
                self.address.address() for _ in range(self.entries_number)
            ],
            "patient_city": [self.address.city() for _ in range(self.entries_number)],
            "patient_state": [self.address.state() for _ in range(self.entries_number)],
            "patient_zip": [
                self.address.zip_code() for _ in range(self.entries_number)
            ],
            "patient_phone": [
                self.person.telephone() for _ in range(self.entries_number)
            ],
            "patient_email": [
                self.person.email(domains=["example.com"])
                for _ in range(self.entries_number)
            ],
            "patient_ssn": [
                f"{random.randint(100000000, 999999999)}"
                for _ in range(self.entries_number)
            ],
            "subscriber_first_name": [
                self.person.first_name() for _ in range(self.entries_number)
            ],
            "subscriber_last_name": [
                self.person.last_name() for _ in range(self.entries_number)
            ],
            "subscriber_dob": [
                date_generator.date_time_between(
                    start_date="-80y", end_date="-10y"
                ).strftime("%Y-%m-%d")
                for _ in range(self.entries_number)
            ],
            "subscriber_gender": [
                random.choice(["male", "female", "other"])
                for _ in range(self.entries_number)
            ],
            "subscriber_address": [
                self.address.address() for _ in range(self.entries_number)
            ],
            "subscriber_address2": [
                self.address.address() for _ in range(self.entries_number)
            ],
            "subscriber_city": [
                self.address.city() for _ in range(self.entries_number)
            ],
            "subscriber_state": [
                self.address.state() for _ in range(self.entries_number)
            ],
            "subscriber_zip": [
                self.address.zip_code() for _ in range(self.entries_number)
            ],
            "subscriber_phone": [
                self.person.telephone() for _ in range(self.entries_number)
            ],
            "subscriber_email": [
                self.person.email(domains=["example.com"])
                for _ in range(self.entries_number)
            ],
            "subscriber_ssn": [
                f"{random.randint(100000000, 999999999)}"
                for _ in range(self.entries_number)
            ],
        }
        encounter_patient_data_frame = pd.DataFrame(schema, columns=schema.keys())
        return encounter_patient_data_frame


if __name__ == "__main__":
    data = {
        "Pfizer": {1: 2000, 2: 2000},
        "Moderna": {1: 2000, 2: 2000},
        "Janssen": {1: 4000},
        "AstraZeneca": {1: 2000, 2: 2000},
        "Novavax": {1: 2000, 2: 2000},
    }

    for company, dose_info in data.items():
        for dose_number, dose_count in dose_info.items():
            start = time.time()
            encounters = Encounters(
                dose_count, vaccine_type=company, dose_number=dose_number
            )
            encounters.json(filename=f"{company}_{dose_number}_{dose_count}")
            end = time.time() - start
            print(end)
