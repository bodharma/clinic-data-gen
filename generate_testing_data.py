import os
import time

import numpy as np
import pandas as pd
from mimesis import Person, Finance, Address
import random
from datetime import datetime
from pathlib import Path
from generator_helpers import date_generator, string_generator
import boto3


class TestingData:
    def __init__(self, onsite_data):
        self.entries_number = onsite_data.entries
        self.banana_email = onsite_data.banana_email
        self.patient_last_name = onsite_data.patient_last_name
        self.patient_first_name = onsite_data.patient_first_name
        self.patient_dob = onsite_data.patient_dob
        self.patient_phone = onsite_data.patient_phone
        self.patient_email = onsite_data.patient_email

        self.fake_person = Person("en")
        self.fake_businees = Finance("en")
        self.address = Address("en")

    def generate_entries(self):
        insurance_data = pd.read_csv(
            "templates/onsite/banana CARE Insurance Master List 14-May-2021.csv"
        )
        location_data = pd.read_csv(
            "templates/onsite/banana CARE Location Master List 14-May-2021 v2.csv"
        )
        insurance_member_id_str = np.array(
            [
                f"{string_generator.bothify('??#####??')}"
                for i in range(insurance_data["insurance_member_id_str"].count())
            ]
        )
        insurance_data["insurance_member_id_str"] = insurance_member_id_str
        screening_datetime_list = np.array(
            [
                date_generator.date_time_between(start_date="-3M")
                for i in range(self.entries_number)
            ]
        )
        sample_datetime_list = np.array(
            [
                date_generator.date_time_between(start_date=screening_datetime)
                for screening_datetime in screening_datetime_list
            ]
        )
        result_datetime_list = np.array(
            [
                date_generator.date_time_between(start_date=sample_datetime)
                for sample_datetime in sample_datetime_list
            ]
        )
        appointment_datetime_list = np.array(
            [
                random.choice(
                    [date_generator.date_time_between(start_date=result_datetime), ""]
                )
                for result_datetime in result_datetime_list
            ]
        )
        sample_test_alias_list = np.array(
            [
                random.choice(
                    [
                        "rt_pcr_oral",
                        "rt_pcr_oral_logix_smart",
                        "rt_pcr_nasal",
                        "covid_ag",
                        "rt_pcr_saliva",
                    ]
                )
                for i in range(self.entries_number)
            ]
        )
        occupation_list = np.array(
            [
                random.choice(
                    ["faculty_employee", "student", "employee_or_volunteer", ""]
                )
                for i in range(self.entries_number)
            ]
        )
        lab_names_list = np.array(
            [
                random.choice(["banana M1", "banana CARE Lab Services"])
                for i in range(self.entries_number)
            ]
        )
        subscriber_birthdate_list = np.array(
            [
                random.choice(
                    [
                        date_generator.date_time_between(start_date="-90y").strftime(
                            "%Y-%m-%d"
                        ),
                        "",
                    ]
                )
                for i in range(self.entries_number)
            ]
        )
        schema = {
            "ResultSet ID": np.array(
                [
                    f"Result#{random.randint(1111111, 9999999)}"
                    for i in range(self.entries_number)
                ]
            ),
            "Patient ID": np.array(
                [
                    f"Patient#{random.randint(1111111, 9999999)}"
                    for i in range(self.entries_number)
                ]
            ),
            "Patient Last Name": np.array(
                [
                    self.patient_last_name
                    if self.patient_last_name
                    else self.fake_person.last_name()
                    for i in range(self.entries_number)
                ]
            ),
            "Patient First Name": np.array(
                [
                    self.patient_first_name
                    if self.patient_first_name
                    else self.fake_person.first_name()
                    for i in range(self.entries_number)
                ]
            ),
            "Patient DOB": np.array(
                [
                    self.patient_dob
                    if self.patient_dob
                    else date_generator.date_time_between(start_date="-90y").strftime(
                        "%Y%m%d"
                    )
                    for i in range(self.entries_number)
                ]
            ),
            "Patient Gender": np.array(
                [random.choice(["M", "F"]) for i in range(self.entries_number)]
            ),
            "Patient Address": np.array(
                [self.address.address() for i in range(self.entries_number)]
            ),
            "Patient City": np.array(
                [self.address.city() for i in range(self.entries_number)]
            ),
            "Patient State": np.array(
                [self.address.state(abbr=True) for i in range(self.entries_number)]
            ),
            "Patient Zip": np.array(
                [f"{self.address.postal_code()}" for i in range(self.entries_number)]
            ),
            "Patient Phone": np.array(
                [
                    f"{self.patient_phone}"
                    if self.patient_phone
                    else random.choice(
                        [
                            f"{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}",
                            f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                            f"+{random.randint(1000000000000, 9999999999999)}",
                            "NA",
                        ]
                    )
                    for i in range(self.entries_number)
                ]
            ),
            "Patient Email": np.array(
                [
                    self.patient_email
                    if self.patient_email
                    else self.fake_person.email(
                        domains=[
                            "bananamail.com"
                            if self.banana_email
                            else "example.com"
                        ]
                    )
                    for i in range(self.entries_number)
                ]
            ),
            "Test Kit ID": np.array(
                [
                    random.choice(
                        [
                            f'TestKit#{string_generator.bothify(text="?#?##??")}',
                            f'TestKit#{string_generator.bothify(text="?#?????")}',
                            f'TestKit#{string_generator.bothify(text="?#?####")}',
                        ]
                    )
                    for i in range(self.entries_number)
                ]
            ),
            "MRN": np.array(
                [
                    string_generator.bothify(text="#####-#####")
                    for i in range(self.entries_number)
                ]
            ),
            "Screening Date & Time": np.array(
                [
                    screening_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")
                    for screening_datetime in screening_datetime_list
                ]
            ),
            "Sample Date & Time": np.array(
                [
                    sample_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")
                    for sample_datetime in sample_datetime_list
                ]
            ),
            "Sample Value": np.array(
                [
                    random.choice(["pending", "complete"])
                    for i in range(self.entries_number)
                ]
            ),
            "Result Date & Time": np.array(
                [
                    result_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")
                    for result_datetime in result_datetime_list
                ]
            ),
            "Result Value": np.array(
                [
                    random.choice(
                        [
                            "SARS-CoV-2 Not Detected",
                            "SARS-CoV-2 Detected",
                            "SARS-CoV-2 Indeterminant",
                        ]
                    )
                    for i in range(self.entries_number)
                ]
            ),
            # "Location Name": [],
            # "Location Street 1": [],
            # "Location Street 2": [],
            # "Location City": [],
            # "Location State": [],
            # "Location Zipcode": [],
            "Appointment": np.array(
                [
                    True if appointment else False
                    for appointment in appointment_datetime_list
                ]
            ),
            "Appointment Time": np.array(
                [
                    appointment_datetime.strftime("%Y-%m-%d %H:%M:%S UTC")
                    if appointment_datetime
                    else ""
                    for appointment_datetime in appointment_datetime_list
                ]
            ),
            "Organization ID": np.array(
                [random.randint(1, 37) for i in range(self.entries_number)]
            ),
            "Sample Test Alias": sample_test_alias_list,
            "asymptomatic": np.array(
                [
                    random.choice(["Y", "N"])
                    if el
                    in [
                        "rt_pcr_oral_logix_smart",
                        "rt_pcr_nasal",
                        "covid_ag",
                        "rt_pcr_saliva",
                    ]
                    else ""
                    for el in sample_test_alias_list
                ]
            ),
            "cough": np.array(
                [
                    random.choice(["Y", "N"])
                    if el
                    in [
                        "rt_pcr_oral_logix_smart",
                        "rt_pcr_nasal",
                        "covid_ag",
                        "rt_pcr_saliva",
                    ]
                    else ""
                    for el in sample_test_alias_list
                ]
            ),
            "fever": np.array(
                [
                    random.choice(["Y", "N"])
                    if el
                    in [
                        "rt_pcr_oral_logix_smart",
                        "rt_pcr_nasal",
                        "covid_ag",
                        "rt_pcr_saliva",
                    ]
                    else ""
                    for el in sample_test_alias_list
                ]
            ),
            "decreased_smell": np.array(
                [
                    random.choice(["Y", "N"])
                    if el
                    in [
                        "rt_pcr_oral_logix_smart",
                        "rt_pcr_nasal",
                        "covid_ag",
                        "rt_pcr_saliva",
                    ]
                    else ""
                    for el in sample_test_alias_list
                ]
            ),
            "muscle_aches": np.array(
                [
                    random.choice(["Y", "N"])
                    if el
                    in [
                        "rt_pcr_oral_logix_smart",
                        "rt_pcr_nasal",
                        "covid_ag",
                        "rt_pcr_saliva",
                    ]
                    else ""
                    for el in sample_test_alias_list
                ]
            ),
            "sore_throat": np.array(
                [
                    random.choice(["Y", "N"])
                    if el
                    in [
                        "rt_pcr_oral_logix_smart",
                        "rt_pcr_nasal",
                        "covid_ag",
                        "rt_pcr_saliva",
                    ]
                    else ""
                    for el in sample_test_alias_list
                ]
            ),
            "shortness_of_breath": np.array(
                [
                    random.choice(["Y", "N"])
                    if el
                    in [
                        "rt_pcr_oral_logix_smart",
                        "rt_pcr_nasal",
                        "covid_ag",
                        "rt_pcr_saliva",
                    ]
                    else ""
                    for el in sample_test_alias_list
                ]
            ),
            "insurance_member_id_str": np.array(
                [
                    random.choice(insurance_member_id_str) if count % 10 == 0 else ""
                    for count, i in enumerate(range(self.entries_number))
                ]
            ),
            "occupation": occupation_list,
            "occupation_ident": np.array(
                [
                    f'{string_generator.bothify(text="#######")}' if occupation else ""
                    for occupation in occupation_list
                ]
            ),
            "work_outside_home": np.array(
                [random.choice(["Y", "N", ""]) for i in range(self.entries_number)]
            ),
            "work_requires_covid_test": np.array(
                [random.choice(["Y", "N", ""]) for i in range(self.entries_number)]
            ),
            "lab_name": lab_names_list,
            "lab_short_name": np.array(
                ["bananam01" if lab == "banana M1" else "banana" for lab in lab_names_list]
            ),
            "lab_address": np.array(
                [
                    "7000 NW 46th Street"
                    if lab == "banana M1"
                    else "1151 E 3900 SO, Suite B120"
                    for lab in lab_names_list
                ]
            ),
            "lab_city": np.array(
                [
                    "Stryi" if lab == "banana M1" else "Sweet River Town"
                    for lab in lab_names_list
                ]
            ),
            "lab_state_or_province": np.array(
                ["LO" if lab == "banana M1" else "LV" for lab in lab_names_list]
            ),
            "lab_postal_code": np.array(
                ["99313" if lab == "banana M1" else "84124" for lab in lab_names_list]
            ),
            "subscriber_forename": np.array(
                [
                    self.fake_person.first_name() if birthdate else ""
                    for birthdate in subscriber_birthdate_list
                ]
            ),
            "subscriber_surname": np.array(
                [
                    self.fake_person.last_name() if birthdate else ""
                    for birthdate in subscriber_birthdate_list
                ]
            ),
            "subscriber_birth_date": subscriber_birthdate_list,
            "subscriber_gender": np.array(
                [
                    random.choice(["m", "f"]) if birthdate else ""
                    for birthdate in subscriber_birthdate_list
                ]
            ),
            "subscriber_ssn": np.array(
                [
                    f"{random.randint(100000000, 999999999)}"
                    for i in range(self.entries_number)
                ]
            ),
            "patient_ssn": np.array(
                [
                    f"{random.randint(100000000, 999999999)}"
                    for i in range(self.entries_number)
                ]
            ),
            "subscriber_relationship_to_patient": np.array(
                [
                    random.choice(["parent", "spouse", "child", "self"])
                    if birthdate
                    else ""
                    for birthdate in subscriber_birthdate_list
                ]
            ),
            "patient_identifier": ["" for _ in range(self.entries_number)],
        }

        onsite_data_frame = pd.DataFrame(schema, columns=schema.keys())
        merged_insurance = onsite_data_frame.merge(
            insurance_data[
                [
                    "insurance_company_name",
                    "insurance_plan_phone_number",
                    "insurance_member_id_str",
                ]
            ],
            on=["insurance_member_id_str"],
            how="left",
        )
        merged_insurance.insurance_plan_phone_number = merged_insurance.insurance_plan_phone_number.fillna(
            "0"
        ).astype(
            str
        )

        merged_location = merged_insurance.merge(
            location_data, on=["Organization ID"], how="left"
        )
        merged_location.fillna("")
        merged_location["Organization ID"] = merged_location["Organization ID"].apply(
            str
        )
        return merged_location

    def csv(self, filepath=None):
        now = datetime.now()
        filepath = (
            filepath
            if filepath
            else Path(f"{Path.cwd()}/{now.year}/{now.month}/{now.day}")
        )
        Path(filepath).mkdir(exist_ok=True, parents=True)

        filename = f"{filepath}/mock_onsite_sample_{int(now.timestamp())}.csv"
        self.generate_entries().to_csv(filename, index=False, header=True)
        return filename

    def json(self, filepath=None):
        now = datetime.now()
        filepath = (
            filepath
            if filepath
            else Path(f"{Path.cwd()}/{now.year}/{now.month}/{now.day}")
        )
        Path(filepath).mkdir(exist_ok=True, parents=True)

        filename = f"{filepath}/mock_onsite_sample_{int(now.timestamp())}.json"
        self.generate_entries().to_json(filename, orient="records")
        return filename

    def json_like(self, filepath=None):
        now = datetime.now()
        filepath = (
            filepath
            if filepath
            else Path(f"{Path.cwd()}/{now.year}/{now.month}/{now.day}")
        )
        Path(filepath).mkdir(exist_ok=True, parents=True)

        filename = f"{filepath}/mock_onsite_sample_{int(now.timestamp())}"
        data = (
            self.generate_entries()
            .to_json(orient="records")
            .replace("},{", "}{")
            .lstrip("[")
            .rstrip("]")
        )
        with open(filename, "w+") as jsonlikefile:
            jsonlikefile.write(data)
        return filename

    def s3(self, bucket_name, input_file_path):
        assert self.verify_aws_keys()
        s3_resource = boto3.resource(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            aws_session_token=os.environ["AWS_SESSION_TOKEN"],
        )

        s3_resource.Bucket(bucket_name).upload_file(
            Filename=input_file_path, Key=input_file_path.split("/")[-1]
        )

    def verify_aws_keys(self):
        keys_list = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"]
        existing_keys = []
        for key in keys_list:
            if key in os.environ:
                existing_keys.append(True)

        if any(existing_keys) and len(existing_keys) == 3:
            return True
        else:
            raise EnvironmentError(
                f"Please, check your environment variables: {', '.join(keys_list)}"
            )


if __name__ == "__main__":
    start = time.time()
    onsite = TestingData(10)
    onsite.s3("dev-de-inbound")
    end = time.time() - start
    print(end)
