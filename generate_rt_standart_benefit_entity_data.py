from datetime import datetime
from pathlib import Path

import numpy as np
from mimesis import Person, Datetime, Address, Code, Text

from generate_rt_eligibility_data import AN_DATA_TYPE


class RTStandardBenefitEntityData:
    def __init__(
        self, entries_number: int, load_type: str, optional_fields: bool = False
    ):
        self._fake_person = Person("en")
        self._fake_date = Datetime()
        self._fake_address = Address("en")

        self._optional_fields = optional_fields
        self._load_type = load_type
        self._entries_number = entries_number
        self._file_name = ""
        self._payer_id = "".join(np.random.choice(AN_DATA_TYPE, size=10))
        self._header_schema = {}
        self._detail_schema = {}
        self._trailer_schema = {}

    def _generate_header_schema(self):
        self._header_schema["Record Id"] = "HDR"
        self._header_schema["File Group ID"] = "".join(
            np.random.choice(AN_DATA_TYPE, size=10)
        )
        self._header_schema["File Group Sequence Number"] = "1"
        self._header_schema["File Group Count"] = "1"
        self._header_schema["Creation Date"] = self._fake_date.date(
            start=1980, end=2019
        ).strftime("%Y%m%d")
        self._header_schema["Creation Time"] = self._fake_date.time().strftime("%H%M%S")
        self._header_schema["Trading Partner ID"] = "".join(
            np.random.choice(AN_DATA_TYPE, size=10)
        )
        self._header_schema["Submitter Name"] = self._fake_person.first_name()
        self._header_schema["Payer Contact Name"] = (
            self._fake_person.first_name() if self._optional_fields else ""
        )
        self._header_schema["Payer Support Telephone Number"] = (
            self._fake_person.telephone("##########") if self._optional_fields else ""
        )
        self._header_schema["Payer Support Email Address"] = (
            self._fake_person.email() if self._optional_fields else ""
        )
        self._header_schema["Load Type"] = self._load_type
        self._header_schema["Payer Unique File Identifier"] = datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )
        self._header_schema["File Type"] = "Planbene"
        self._header_schema["Version Code"] = "03"
        self._header_schema["Release Code"] = "00"
        self._header_schema["File Validation Code"] = (
            2 if self._optional_fields else np.random.choice([0, 1, 2, 3, 4, 5])
        )
        self._header_schema["Record Terminator"] = "CR"

    def _generate_detail_schema(self):
        self._detail_schema["Record Id"] = np.array(
            ["DTL" for _ in range(self._entries_number)]
        )
        self._detail_schema["Record Number"] = np.array(
            [_ for _ in range(2, self._entries_number + 2)]
        )
        self._detail_schema["Payer ID"] = np.array(
            [self._payer_id for _ in range(self._entries_number)]
        )
        self._detail_schema["Maintenance Type Code"] = np.array(
            ["030" for _ in range(self._entries_number)]
        )
        self._detail_schema["Correction Indicator"] = np.array(
            ["Y" if self._optional_fields else "N" for _ in range(self._entries_number)]
        )
        self._detail_schema[
            "Benefit Entity Employers Identification Number"
        ] = np.array(["" for _ in range(self._entries_number)])
        self._detail_schema["Benefit Entity SSN"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self._detail_schema["Benefit Entity ETIN"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self._detail_schema["Benefit Entity Facility Identification"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self._detail_schema["Benefit Entity Tax Identification"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self._detail_schema["Benefit Entity Member Identification"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self._detail_schema["Benefit Entity NAIC Identification"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self._detail_schema["Benefit Entity Payer Identification"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self._detail_schema[
            "Benefit Entity Pharmacy Processor Number Identification"
        ] = np.array(["" for _ in range(self._entries_number)])
        self._detail_schema[
            "Benefit Entity Service Provider Number Identification"
        ] = np.array(["" for _ in range(self._entries_number)])
        self._detail_schema["Benefit Entity CMS Plan Identification"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self._detail_schema[
            "Benefit Entity National Provider Identification"
        ] = np.array(
            [
                np.random.randint(1111111111, 9999999999)
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Last Name (or Org Name)"] = np.array(
            [
                self._fake_person.last_name() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity First Name"] = np.array(
            [
                self._fake_person.first_name() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Middle Name"] = np.array(
            [
                self._fake_person.last_name() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Name Suffix"] = np.array(
            [
                np.random.choice(["I", "II", "III", "IV", "Jr", "Sr"])
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Address Line 1"] = np.array(
            [
                self._fake_address.address() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Address Line 2"] = np.array(
            [
                self._fake_address.address() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity City"] = np.array(
            [
                self._fake_address.city() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity State"] = np.array(
            [
                self._fake_address.state(True) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Zip Code"] = np.array(
            [
                self._fake_address.postal_code() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Contact Name"] = np.array(
            [
                self._fake_person.first_name() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Communication Qualifier1"] = np.array(
            [
                "TE"
                if self._header_schema["File Validation Code"] in [2, 5]
                and self._optional_fields
                else np.random.choice(["ED", "EM", "FX", "UR", "WP"])
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Communication Number1"] = np.array(
            [
                self._fake_person.telephone("##########")
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Communication Qualifier2"] = np.array(
            [
                np.random.choice(["ED", "TE", "EM", "FX", "UR", "WP"])
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Communication Number2"] = np.array(
            [
                self._fake_person.telephone("##########")
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Communication Qualifier3"] = np.array(
            [
                np.random.choice(["ED", "TE", "EM", "FX", "UR", "WP"])
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Communication Number3"] = np.array(
            [
                self._fake_person.telephone("##########")
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Benefit Entity Taxonomy"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self._detail_schema["Rx Bank Identification Number (BIN)"] = np.array(
            [
                np.random.randint(111111, 999999) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Employer Size"] = np.array(
            [np.random.choice([0, 1, 2]) for _ in range(self._entries_number)]
        )
        self._detail_schema["Benefit Entity Pseudo Tax Identification"] = np.array(
            [
                np.random.randint(111111111, 999999999)
                for _ in range(self._entries_number)
            ]
        )
        self._detail_schema["Record Terminator "] = np.array(
            ["" for _ in range(self._entries_number)]
        )

    def _generate_trailer_schema(self):
        self._trailer_schema["RecordID"] = "TRLR"
        self._trailer_schema["Record Count"] = self._entries_number
        self._trailer_schema["Record Terminator "] = "CR"

    def generate_all_schemas(self):

        self._generate_header_schema()
        self._generate_detail_schema()
        self._generate_trailer_schema()
        self._file_name = (
            f'{datetime.now().strftime("%Y%m%d%H%M%S")}_{self._payer_id}test.bene'
        )

    def _one_line_schema_to_file(self, schema, filepath):
        with open(f"{filepath}/{self._file_name}", "ab") as file:
            for key in schema.keys():
                file.write(f"{schema[key]}|".encode("ascii", "ignore"))
            file.write("\n".encode("ascii"))

    def _detailed_schema_to_file(self, schema, filepath):
        with open(f"{filepath}/{self._file_name}", "ab") as file:
            for _ in range(self._entries_number):
                for key in schema.keys():
                    file.write(f"{schema[key][_]}|".encode("ascii", "ignore"))
                file.write("\n".encode("ascii"))

    def schemas_to_file(self, filepath=None):
        now = datetime.now()
        filepath = (
            filepath
            if filepath
            else Path(f"{Path.cwd()}/{now.year}/{now.month}/{now.day}")
        )
        Path(filepath).mkdir(exist_ok=True, parents=True)

        self._one_line_schema_to_file(self._header_schema, filepath)
        self._detailed_schema_to_file(self._detail_schema, filepath)
        self._one_line_schema_to_file(self._trailer_schema, filepath)

        return f"{filepath}/{self._file_name}"


if __name__ == "__main__":
    generator = RTStandardBenefitEntityData(1, "F", False)
    generator.generate_all_schemas()
    generator.schemas_to_file()
