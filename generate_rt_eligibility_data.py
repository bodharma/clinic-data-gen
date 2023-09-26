import random
import string
from datetime import datetime

import numpy as np
from mimesis import Person, Datetime, Address, Code, Text
from pathlib import Path

from mimesis.enums import CountryCode

from generator_helpers import string_generator

AN_DATA_TYPE = np.array(list(string.ascii_letters + string.digits))
CODE_SET_A = np.array(
    [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "14",
        "15",
        "16",
        "17",
        "18",
        "20",
        "21",
        "22",
        "25",
        "26",
        "27",
        "28",
        "29",
        "31",
        "32",
        "33",
        "37",
        "38",
        "39",
        "40",
        "41",
        "43",
        "59",
        "AA",
        "AB",
        "AC",
        "AD",
        "AE",
        "AF",
        "AG",
        "AH",
        "AI",
        "AJ",
        "AL",
        "EC",
        "XN",
        "XT",
    ]
)
CODE_SET_B = np.array(["01", "18", "19", "20", "21", "39", "40", "53", "G8"])
CODE_SET_C = np.array(
    [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "Q",
        "R",
        "S",
        "U",
        "W",
    ]
)
CODE_SET_D = np.array(
    [
        "A1",
        "A2",
        "A3",
        "B1",
        "B2",
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "C6",
        "C7",
        "C8",
        "C9",
        "E1",
        "F1",
        "F2",
        "F3",
        "F4",
        "G1",
        "G4",
        "L1",
        "L2",
        "L3",
        "L4",
        "L5",
        "L6",
        "M1",
        "M2",
        "M3",
        "M4",
        "M5",
        "M6",
        "P1",
        "P2",
        "P3",
        "P4",
        "P5",
        "R1",
        "R2",
        "S1",
        "S2",
        "S3",
        "S4",
        "S5",
        "S6",
        "S7",
        "S8",
        "S9",
        "SA",
        "SB",
        "SC",
        "T1",
        "V1",
        "W1",
    ]
)
CODE_SET_E = np.array(
    [
        "AE",
        "AO",
        "AS",
        "AT",
        "AU",
        "CC",
        "DD",
        "HD",
        "IR",
        "LX",
        "PE",
        "RE",
        "RM",
        "RR",
        "RU",
    ]
)


class RTEligibbility:
    def __init__(
        self, entries_number: int, load_type: str, optional_fields: bool = False
    ):
        self._fake_person = Person("en")
        self._fake_date = Datetime()
        self._fake_address = Address("en")
        self._fake_code = Code()
        self._fake_text = Text()

        self.optional_fields = optional_fields
        self.load_type = load_type
        self._entries_number = entries_number
        self._file_name = ""
        self.header_schema = {}
        self.detail_schema = {}
        self.trailer_schema = {}

    def _generate_header_schema(self):
        self.header_schema["Record Id"] = "HDR"
        self.header_schema["File Group ID"] = "".join(
            np.random.choice(AN_DATA_TYPE, size=10)
        )
        self.header_schema["File Group Sequence Number"] = "1"
        self.header_schema["File Group Count"] = "1"
        self.header_schema["Creation Date"] = self._fake_date.date(
            start=1980, end=2019
        ).strftime("%Y%m%d")
        self.header_schema["Creation Time"] = self._fake_date.time().strftime("%H%M%S")
        self.header_schema["Trading Partner ID"] = "".join(
            np.random.choice(AN_DATA_TYPE, size=10)
        )
        self.header_schema["Submitter Name"] = self._fake_person.first_name()
        self.header_schema["Payer Contact Name"] = (
            self._fake_person.first_name() if self.optional_fields else ""
        )
        self.header_schema["Payer Support Telephone Number"] = (
            self._fake_person.telephone("##########") if self.optional_fields else ""
        )
        self.header_schema["Payer Support Email Address"] = (
            self._fake_person.email() if self.optional_fields else ""
        )
        self.header_schema["Load Type"] = self.load_type
        self.header_schema["Payer Unique File Identifier"] = datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )
        self.header_schema["File Type"] = "Elig"
        self.header_schema["Version Code"] = "03"
        self.header_schema["Release Code"] = "01"
        self.header_schema["File Validation Code"] = (
            5 if self.optional_fields else np.random.choice([0, 1, 2, 3, 4, 5])
        )
        self.header_schema["Rosters Indicator"] = "Y" if self.optional_fields else "N"

    def _generate_detail_schema(self):
        self.detail_schema["Record Id"] = np.array(
            ["DTL" for _ in range(self._entries_number)]
        )
        self.detail_schema["Record Number"] = np.array(
            [_ for _ in range(2, self._entries_number + 2)]
        )
        self.detail_schema["Payer ID"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Action Indicator"] = np.array(
            [
                np.random.choice(["I", "L"])
                if self.header_schema["Load Type"] == "F"
                else np.random.choice(["U", "D"])
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Maintenance Reason Code"] = np.array(
            [
                np.random.choice(CODE_SET_A)
                if self.header_schema["Rosters Indicator"] == "Y"
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Correction Indicator"] = np.array(
            ["Y" if self.optional_fields else "N" for _ in range(self._entries_number)]
        )
        self.detail_schema["Primary Subscriber ID"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Unique Patient ID (UPID)"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Relationship to Subscriber"] = np.array(
            [
                np.random.choice(["01", "18", "19", "20", "21", "53", "G8"])
                if self.header_schema["Rosters Indicator"] == "N"
                else np.random.choice(CODE_SET_B)
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Date of Birth"] = np.array(
            [
                self._fake_date.date(start=1930, end=2019).strftime("%Y%m%d")
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Last Name"] = np.array(
            [self._fake_person.last_name() for _ in range(self._entries_number)]
        )
        self.detail_schema["Member First Name"] = np.array(
            [self._fake_person.first_name() for _ in range(self._entries_number)]
        )
        self.detail_schema["Member Middle Name"] = np.array(
            [
                self._fake_person.first_name() if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Name Prefix"] = np.array(
            [
                np.random.choice(["Mr", "Ms", "Prince"]) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Name Suffix"] = np.array(
            [
                np.random.choice(["I", "II", "III", "IV", "Jr", "Sr"])
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Gender"] = np.array(
            [np.random.choice(["M", "F", "U"]) for _ in range(self._entries_number)]
        )
        self.detail_schema["Member Street Address 1"] = np.array(
            [self._fake_address.address() for _ in range(self._entries_number)]
        )
        self.detail_schema["Member Street Address 2"] = np.array(
            [
                self._fake_address.address() if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member City"] = np.array(
            [
                self._fake_address.city() if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member State"] = np.array(
            [
                self._fake_address.state(True) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member ZIP Code"] = np.array(
            [
                self._fake_address.zip_code() if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Country"] = np.array(
            [
                self._fake_address.country_code(CountryCode.A3)
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Country Subdivision"] = np.array(
            [
                self._fake_address.province() if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Work Phone"] = np.array(
            [
                self._fake_person.telephone("##########")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Home Phone"] = np.array(
            [
                self._fake_person.telephone("##########")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Plan Effective Date"] = np.array(
            [
                self._fake_date.date(start=1930, end=2019).strftime("%Y%m%d")
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Plan Termination Date"] = np.array(
            [
                self._fake_date.date(start=2000, end=2030).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Plan Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Plan Name"] = np.array(
            [
                f"Plan {_}" if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Group Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.header_schema["File Validation Code"] in [2, 5]
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Group Name"] = np.array(
            [
                f"Group {_}" if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Insurance Policy Number"] = np.array(
            [
                f"{string_generator.bothify('??#####??')}"
                if self.header_schema["File Validation Code"] in [2, 5]
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Insurance Policy Effective Date"] = np.array(
            [
                self._fake_date.date(start=1950, end=2020).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Insurance Policy Expiration Date"] = np.array(
            [
                self._fake_date.date(start=2020, end=2030).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Status Code"] = np.array(
            [
                np.random.choice(["1", "2", "3", "4", "5", "6", "7", "8"])
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Social Security Number"] = np.array(
            [
                f"{random.randint(111111111, 999999999)}"
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Health Insurance Claim (HIC) Number"] = np.array(
            [
                "".join(np.random.choice(list(string.digits), size=10))
                if self.header_schema["File Validation Code"] in [3, 4, 5]
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Identity Card Number"] = np.array(
            [
                f"{random.randint(11111, 99999)}{random.randint(111111, 999999)}"
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Identity Card Serial Number"] = np.array(
            [
                self._fake_address.state(True) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Plan Network Identification Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Plan Network Name"] = np.array(
            [
                f"Network Name {_}" if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Secondary Subscriber ID"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Tertiary Subscriber ID"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Current Medicaid Recipient ID Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Original Medicaid Recipient ID Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Family Unit Number"] = np.array(
            [
                np.random.choice(["1", "2", "3", "4", "5"])
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Birth Sequence Number"] = np.array(
            [
                np.random.choice([1, 2, 3, 4, 5]) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Case Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Contract Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Medical Record Identification Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Issue Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Issue Date"] = np.array(
            [
                self._fake_date.date(start=2000, end=2020).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Care Management Eligible LOag"] = np.array(
            ["Y" if self.optional_fields else "" for _ in range(self._entries_number)]
        )
        self.detail_schema["Authorization Indicator"] = np.array(
            [
                np.random.choice(["Y", "N"]) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Student Status"] = np.array(
            [
                np.random.choice(["F", "P", "N"]) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Handicap Status"] = np.array(
            [
                np.random.choice(["Y", "N"]) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Disability type"] = np.array(
            [
                np.random.choice([1, 2, 3, 4]) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Date of Death"] = np.array(
            [
                self._fake_date.date(start=2000, end=2020).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Period Start Date"] = np.array(
            [
                self._fake_date.date(start=1950, end=2000).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Period End Date"] = np.array(
            [
                self._fake_date.date(start=2000, end=2020).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Premium Paid To Start Date"] = np.array(
            [
                self._fake_date.date(start=1950, end=2000).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Premium Paid To End Date"] = np.array(
            [
                self._fake_date.date(start=2000, end=2020).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Message"] = np.array(
            [
                self._fake_text.sentence() if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Medical Plan Indicator"] = np.array(
            ["Y" for _ in range(self._entries_number)]
        )
        self.detail_schema["Dental Plan Indicator"] = np.array(
            ["Y" if self.optional_fields else "N" for _ in range(self._entries_number)]
        )
        self.detail_schema["Prescription Plan Indicator"] = np.array(
            ["Y" for _ in range(self._entries_number)]
        )
        self.detail_schema["Vision Plan Indicator"] = np.array(
            ["Y" if self.optional_fields else "N" for _ in range(self._entries_number)]
        )
        self.detail_schema["Hospital Plan Indicator"] = np.array(
            ["Y" if self.optional_fields else "N" for _ in range(self._entries_number)]
        )
        self.detail_schema["Behavioral / Mental Health Plan Indicator"] = np.array(
            ["Y" if self.optional_fields else "N" for _ in range(self._entries_number)]
        )
        self.detail_schema["TRICARE Plan Indicator"] = np.array(
            ["Y" if self.optional_fields else "N" for _ in range(self._entries_number)]
        )
        self.detail_schema["Retiree Drug Subsidy Plan Indicator"] = np.array(
            ["Y" if self.optional_fields else "N" for _ in range(self._entries_number)]
        )
        self.detail_schema["Taft-Hartley Plan Indicator"] = np.array(
            ["Y" if self.optional_fields else "N" for _ in range(self._entries_number)]
        )
        self.detail_schema["HSA Account Indicator"] = np.array(
            ["Y" if self.optional_fields else "N" for _ in range(self._entries_number)]
        )
        self.detail_schema["HRA Account Indicator"] = np.array(
            ["Y" if self.optional_fields else "N" for _ in range(self._entries_number)]
        )
        self.detail_schema["FSA Account Indicator"] = np.array(
            ["Y" if self.optional_fields else "N" for _ in range(self._entries_number)]
        )
        self.detail_schema["Medicare Plan Code"] = np.array(
            ["E" if self.optional_fields else "" for _ in range(self._entries_number)]
        )
        self.detail_schema["Medicare Eligibility Reason Code"] = np.array(
            ["2" if self.optional_fields else "" for _ in range(self._entries_number)]
        )
        self.detail_schema["ESRD Coordination Period End Date"] = np.array(
            [
                self._fake_date.date(start=1980, end=2019).strftime("%Y%m%d")
                if self.detail_schema["Medicare Eligibility Reason Code"][_] == "2"
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Premium Amount"] = np.array(
            [
                random.randint(111111111, 999999999) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Rx Group Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Rx Insured ID Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Rx Plan Network Indicator"] = np.array(
            [np.random.choice(["1", "2", "3"]) for _ in range(self._entries_number)]
        )
        self.detail_schema["Small Employer Exception Indicator"] = np.array(
            [
                np.random.choice(["Y", "N"]) if self.optional_fields else "N"
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Employee Coverage Code"] = np.array(
            [
                np.random.choice(["1", "2", "3"])
                if self.header_schema["File Validation Code"] in [1, 2, 4, 5]
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Employee Status Code"] = np.array(
            [
                "CO"
                if self.optional_fields
                else np.random.choice(
                    ["CO", "FT", "PT", "RT", "RW", "AC", "AO", "AU", "L1", "TE"]
                )
                if self.header_schema["File Validation Code"] in [1, 2, 4, 5]
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["COBRA Begin Date"] = np.array(
            [
                self._fake_date.date(start=1960, end=2000).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["COBRA End Date"] = np.array(
            [
                self._fake_date.date(start=2000, end=2020).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Employment Class Code"] = np.array(
            [
                np.random.choice(
                    [
                        "01",
                        "02",
                        "03",
                        "04",
                        "05",
                        "06",
                        "07",
                        "08",
                        "09",
                        "10",
                        "11",
                        "12",
                        "17",
                        "18",
                        "19",
                        "20",
                        "21",
                        "22",
                        "23",
                    ]
                )
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Income Frequency"] = np.array(
            [
                np.random.choice(
                    [
                        "1",
                        "2",
                        "3",
                        "4",
                        "6",
                        "7",
                        "8",
                        "9",
                        "B",
                        "C",
                        "H",
                        "Q",
                        "S",
                        "U",
                    ]
                )
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Income"] = np.array(
            [
                random.randint(111111111, 999999999) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["RRE ID"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.header_schema["File Validation Code"] in [1, 2, 4, 5]
                and self.detail_schema["Medicare Plan Code"][_] not in ["E", "F"]
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["COBA ID"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.header_schema["File Validation Code"] in [3, 4, 5]
                and self.detail_schema["Medicare Plan Code"][_] == "E"
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["RDS Application Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self.header_schema["File Validation Code"] in [2, 5]
                and self.detail_schema["Retiree Drug Subsidy Plan Indicator"][_] == "Y"
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Military Information Status Code"] = np.array(
            [
                np.random.choice(["A", "C", "L", "O", "P", "S", "T"])
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Military Status Code"] = np.array(
            [
                np.random.choice(CODE_SET_E) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Military Service Affiliation Code"] = np.array(
            [
                np.random.choice(CODE_SET_C) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Military Unit"] = np.array(
            [
                np.random.choice(
                    ["corps", "division", "battalion", "company", "platoon"]
                )
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Military Service Rank Code"] = np.array(
            [
                np.random.choice(CODE_SET_D) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Military Service Start Date"] = np.array(
            [
                self._fake_date.date(start=1950, end=1999).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Military Service End Date"] = np.array(
            [
                self._fake_date.date(start=2000, end=2020).strftime("%Y%m%d")
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Health-related Code"] = np.array(
            [
                np.random.choice(["N", "S", "T", "U", "X"])
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Height"] = np.array(
            [
                self._fake_person.weight() if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Weight"] = np.array(
            [
                self._fake_person.height() if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Language Code Qualifier"] = np.array(
            [
                np.random.choice(["LD", "LE"]) if self.optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Language Reading Code"] = np.array(
            [
                self._fake_code.locale_code()[:2].upper()
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Language Writing Code"] = np.array(
            [
                self._fake_code.locale_code()[:2].upper()
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Language Speaking Code"] = np.array(
            [
                self._fake_code.locale_code()[:2].upper()
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Native Language Code"] = np.array(
            [
                self._fake_code.locale_code()[:2].upper()
                if self.optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )

    def _generate_trailer_schema(self):
        self.trailer_schema["RecordID"] = "TRLR"
        self.trailer_schema["Record Count"] = self._entries_number

    def generate_all_schemas(self):

        self._generate_header_schema()
        self._generate_detail_schema()
        self._generate_trailer_schema()
        self._file_name = f'{datetime.now().strftime("%Y%m%d%H%M%S")}_{self.header_schema["Trading Partner ID"]}_test.elig31.txt'

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

        self._one_line_schema_to_file(self.header_schema, filepath)
        self._detailed_schema_to_file(self.detail_schema, filepath)
        self._one_line_schema_to_file(self.trailer_schema, filepath)

        return f"{filepath}/{self._file_name}"


if __name__ == "__main__":
    generator = RTEligibbility(100, "I", True)
    generator.generate_all_schemas()
    generator.schemas_to_file()
