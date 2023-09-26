from datetime import datetime
from pathlib import Path

import numpy as np
from mimesis import Person, Datetime, Address, Code, Text

from generate_rt_eligibility_data import AN_DATA_TYPE

CODE_SET_B = np.array(
    [
        "X0",
        "A0",
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "P0",
        "P1",
        "P2",
        "P3",
        "P4",
        "P5",
        "F0",
        "F1",
        "F2",
        "F3",
        "F3F",
        "F3N",
        "F4",
        "F5",
        "E0",
        "E1",
        "E2",
        "D0",
    ]
)
CODE_SET_C = np.array(
    [
        "03",
        "13",
        "17",
        "1E",
        "1G",
        "1H",
        "1L",
        "1O",
        "1P",
        "1Q",
        "1R",
        "1S",
        "1T",
        "1U",
        "1V",
        "1W",
        "1X",
        "1Y",
        "1Z",
        "28",
        "2A",
        "2B",
        "2D",
        "2E",
        "2I",
        "2K",
        "2P",
        "2Q",
        "2S",
        "2Z",
        "4U",
        "4V",
        "4W",
        "4X",
        "4Y",
        "4Z",
        "5A",
        "5B",
        "5C",
        "5D",
        "5E",
        "5F",
        "5G",
        "5H",
        "5I",
        "5J",
        "5K",
        "5L",
        "5M",
        "5N",
        "5O",
        "5P",
        "5Q",
        "5R",
        "5S",
        "5T",
        "5U",
        "5V",
        "5W",
        "5X",
        "E1",
        "E2",
        "E7",
        "E9",
        "FA",
        "FD",
        "FE",
        "G0",
        "G3",
        "GB",
        "GD",
        "GI",
        "GJ",
        "GK",
        "GM",
        "GY",
        "HF",
        "HH",
        "I3",
        "IL",
        "IN",
        "LI",
        "LR",
        "MR",
        "OB",
        "OD",
        "OX",
        "P0",
        "P2",
        "30",
        "36",
        "3A",
        "3C",
        "3D",
        "3E",
        "3F",
        "3G",
        "3H",
        "3I",
        "3J",
        "3K",
        "3L",
        "3M",
        "3N",
        "3O",
        "3P",
        "3Q",
        "3R",
        "3S",
        "3T",
        "3U",
        "3V",
        "3W",
        "3X",
        "3Y",
        "3Z",
        "40",
        "43",
        "44",
        "5Y",
        "5Z",
        "61",
        "6A",
        "6B",
        "6C",
        "6D",
        "6E",
        "6F",
        "6G",
        "6H",
        "6I",
        "6J",
        "6K",
        "6L",
        "6M",
        "6N",
        "6O",
        "6P",
        "6Q",
        "6R",
        "6S",
        "6U",
        "6V",
        "6W",
        "6X",
        "6Y",
        "71",
        "72",
        "73",
        "P3",
        "P4",
        "P6",
        "P7",
        "PRP",
        "PT",
        "PV",
        "PW",
        "QA",
        "QB",
        "QC",
        "QD",
        "QE",
        "QH",
        "QK",
        "QL",
        "QN",
        "QO",
        "QS",
        "QV",
        "QY",
        "RC",
        "RW",
        "S4",
        "SEP",
        "SJ",
        "SU",
        "T4",
        "TL",
        "TQ",
        "TT",
        "4A",
        "4B",
        "4C",
        "4D",
        "4E",
        "4F",
        "4G",
        "4H",
        "4I",
        "4M",
        "4N",
        "4O",
        "4P",
        "4Q",
        "4R",
        "4S",
        "74",
        "77",
        "7C",
        "80",
        "82",
        "84",
        "85",
        "87",
        "95",
        "CK",
        "D2",
        "DD",
        "DJ",
        "DK",
        "DN",
        "DO",
        "DQ",
        "TTP",
        "TU",
        "UH",
        "X3",
        "X4",
        "X5",
        "MSC",
        "ZZ",
    ]
)


class RTClaimData:
    def __init__(
        self,
        load_type: str,
        optional_fields: bool,
        claim_level_record_count: int,
        claim_line_level_record_count: int,
    ):
        self._fake_person = Person("en")
        self._fake_date = Datetime()
        self._fake_address = Address("en")
        self._fake_code = Code()
        self._fake_text = Text()
        self._payer_id = "".join(np.random.choice(AN_DATA_TYPE, size=10))

        self._optional_fields = optional_fields
        self._load_type = load_type
        self._claim_level_record_count = claim_level_record_count
        self._claim_line_level_record_count = claim_line_level_record_count
        self._file_name = ""

        self._header_schema = {}
        self._claim_level_record_schema = {}
        self._claim_status_record_schema = {}
        self._claim_line_level_record = {}
        self._claim_detail_status_record_schema = {}
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
        self._header_schema["File Type"] = "CStat"
        self._header_schema["Version Code"] = "03"
        self._header_schema["Release Code"] = "00"
        self._header_schema["Record Terminator"] = "CR"

    def _generate_claim_level_record_schema(self):
        self._claim_level_record_schema["Record ID"] = np.array(
            ["CLM" for _ in range(self._claim_level_record_count)]
        )
        self._claim_level_record_schema["Record Number"] = np.array(
            [_ for _ in range(self._claim_level_record_count)]
        )
        self._claim_level_record_schema["Payer ID"] = np.array(
            [self._payer_id for _ in range(self._claim_level_record_count)]
        )
        self._claim_level_record_schema["Maintenance Type Code"] = np.array(
            [
                np.random.choice(["001", "002", "021", "030"])
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Billing Provider Federal Tax ID"] = np.array(
            [
                np.random.randint(111111111, 999999999)
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema[
            "Billing Provider Payer Assigned Number"
        ] = np.array(["" for _ in range(self._claim_level_record_count)])
        self._claim_level_record_schema[
            "Billing Provider National Provider ID"
        ] = np.array(["" for _ in range(self._claim_level_record_count)])
        self._claim_level_record_schema[
            "Billing Provider Last Name (or Org Name)"
        ] = np.array(
            [
                self._fake_person.last_name() if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Billing Provider First Name"] = np.array(
            [
                self._fake_person.first_name() if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Billing Provider Middle Name"] = np.array(
            [
                self._fake_person.first_name() if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Billing Provider Name Suffix"] = np.array(
            [
                np.random.choice(["Mr", "Ms", "Prince"])
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Service Provider Federal Tax ID"] = np.array(
            [
                np.random.randint(111111111, 999999999)
                if self._optional_fields
                else self._claim_level_record_schema["Billing Provider Federal Tax ID"][
                    _
                ]
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema[
            "Service Provider Payer Assigned Number"
        ] = np.array(["" for _ in range(self._claim_level_record_count)])
        self._claim_level_record_schema[
            "Service Provider National Provider ID"
        ] = np.array(
            [
                np.random.randint(111111111, 999999999) if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema[
            "Service Provider Last Name (or Org Name)"
        ] = np.array(
            [
                self._fake_person.last_name() if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Service Provider First Name"] = np.array(
            [
                self._fake_person.first_name() if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Service Provider Middle Name"] = np.array(
            [
                self._fake_person.first_name() if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Service Provider Name Suffix"] = np.array(
            [
                np.random.choice(["Mr", "Ms", "Prince"])
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Employer Identification Number"] = np.array(
            [
                f"{np.random.randint(11, 99)}-{np.random.randint(1111111, 9999999)}"
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Employer Name"] = np.array(
            [
                self._fake_person.first_name() if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Subscriber ID"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Subscriber Last Name"] = np.array(
            [
                self._fake_person.last_name() if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Subscriber First Name"] = np.array(
            [
                self._fake_person.first_name() if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Subscriber Middle Name"] = np.array(
            [
                self._fake_person.first_name() if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Subscriber Name Suffix"] = np.array(
            [
                np.random.choice(["Mr", "Ms", "Prince"])
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Patient ID"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Patient Last Name"] = np.array(
            [
                self._fake_person.last_name()
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Patient First Name"] = np.array(
            [
                self._fake_person.first_name()
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Patient Middle Name"] = np.array(
            [
                self._fake_person.first_name() if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Patient Name Suffix"] = np.array(
            [
                np.random.choice(["Mr", "Ms", "Prince"])
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Patient Date of Birth"] = np.array(
            [
                self._fake_date.date(start=1930, end=2019).strftime("%Y%m%d")
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Patient Gender"] = np.array(
            [
                np.random.choice(["F", "M"]) if self._optional_fields else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["EMDEON Claim Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Claim Charge Amount"] = np.array(
            [
                np.random.randint(-111111111, 999999999)
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Claim Payment Amount"] = np.array(
            [
                np.random.randint(-111111111, 999999999)
                if self._optional_fields
                else ""
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Claim Adjudication/Payment Date"] = np.array(
            [
                self._fake_date.date(start=2010, end=2020).strftime("%Y%m%d")
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Check/EFT Date"] = np.array(
            [
                self._fake_date.date(start=2010, end=2020).strftime("%Y%m%d")
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Check/EFT Number"] = np.array(
            [
                np.random.randint(-111111111, 999999999)
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Bill Type"] = np.array(
            [
                f"{np.random.randint(1, 9)}{np.random.randint(10, 19)}"
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Payer Claim Identification Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Patient Account Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Pharmacy Prescription Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Voucher Identifier"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema[
            "Application or Location System Identifier"
        ] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Group Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Claim Service Date Start"] = np.array(
            [
                self._fake_date.date(start=2000, end=2010).strftime("%Y%m%d")
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Claim Service Date End"] = np.array(
            [
                self._fake_date.date(start=2010, end=2020).strftime("%Y%m%d")
                if self._optional_fields
                else ""
                for _ in range(self._claim_level_record_count)
            ]
        )
        self._claim_level_record_schema["Record Terminator"] = np.array(
            ["CR" for _ in range(self._claim_level_record_count)]
        )

    def _generate_claim_line_level_record_schema(self):
        self._claim_line_level_record["Record ID"] = np.array(
            [
                ["DTL" for _ in range(self._claim_line_level_record_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Record Number"] = np.array(
            [
                [_ for _ in range(self._claim_line_level_record_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Payer ID"] = np.array(
            [
                [self._payer_id for _ in range(self._claim_line_level_record_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Payer Claim Identification Number"] = np.array(
            [
                [
                    self._claim_level_record_schema[
                        "Payer Claim Identification Number"
                    ][__]
                    for _ in range(self._claim_line_level_record_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Line Item Control Number"] = np.array(
            [
                [
                    "".join(np.random.choice(AN_DATA_TYPE, size=10))
                    for _ in range(self._claim_line_level_record_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Service Qualifier ID"] = np.array(
            [
                [
                    np.random.choice(["AD", "ER", "HC", "HP", "IV", "N4", "NU", "WK"])
                    for _ in range(self._claim_line_level_record_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Service Identification Code"] = np.array(
            [
                [
                    "".join(np.random.choice(AN_DATA_TYPE, size=10))
                    for _ in range(self._claim_line_level_record_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Procedure Modifier 1"] = np.array(
            [
                ["" for _ in range(self._claim_line_level_record_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Procedure Modifier 2"] = np.array(
            [
                ["" for _ in range(self._claim_line_level_record_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Procedure Modifier 3"] = np.array(
            [
                ["" for _ in range(self._claim_line_level_record_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Procedure Modifier 4"] = np.array(
            [
                ["" for _ in range(self._claim_line_level_record_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Line Item Charge Amount"] = np.array(
            [
                [
                    np.random.randint(-111111111, 999999999)
                    for _ in range(self._claim_line_level_record_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Line Item Provider Payment Amount"] = np.array(
            [
                [
                    np.random.randint(-111111111, 999999999)
                    for _ in range(self._claim_line_level_record_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Revenue Code"] = np.array(
            [
                [
                    np.random.randint(111111, 999999) if self._optional_fields else ""
                    for _ in range(self._claim_line_level_record_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Quantity(Units of Service)"] = np.array(
            [
                [
                    np.random.randint(1, 10)
                    for _ in range(self._claim_line_level_record_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["EMDEON Claim Number"] = np.array(
            [
                [
                    "".join(np.random.choice(AN_DATA_TYPE, size=10))
                    if self._optional_fields
                    else ""
                    for _ in range(self._claim_line_level_record_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Date of Service Start"] = np.array(
            [
                [
                    self._fake_date.date(start=2000, end=2010).strftime("%Y%m%d")
                    for _ in range(self._claim_line_level_record_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Date of Service End"] = np.array(
            [
                [
                    self._fake_date.date(start=2010, end=2020).strftime("%Y%m%d")
                    for _ in range(self._claim_line_level_record_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        self._claim_line_level_record["Record Terminator"] = np.array(
            [
                ["CR" for _ in range(self._claim_line_level_record_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )

    def _generate_claim_status_record_schema(
        self, status_schema, detail_records_count, status_type
    ):
        status_schema["Record ID"] = np.array(
            [
                ["STC" for _ in range(detail_records_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        status_schema["Record Number"] = np.array(
            [
                [_ for _ in range(detail_records_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        status_schema["Payer ID"] = np.array(
            [
                [self._payer_id for _ in range(detail_records_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        status_schema["Payer Claim Identification Number"] = np.array(
            [
                [
                    self._claim_level_record_schema[
                        "Payer Claim Identification Number"
                    ][__]
                    if status_type == "CLM"
                    else ""
                    for _ in range(detail_records_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        status_schema["Line Item Control Number"] = np.array(
            [
                [
                    self._claim_line_level_record["Line Item Control Number"][__][_]
                    if status_type == "DTL"
                    else ""
                    for _ in range(detail_records_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        status_schema["Status Information Effective Date"] = np.array(
            [
                [
                    self._fake_date.date(
                        start=datetime.now().year, end=datetime.now().year + 10
                    ).strftime("%Y%m%d")
                    for _ in range(detail_records_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        status_schema["Claim Status Category Code"] = np.array(
            [
                [
                    "F1" if self._optional_fields else np.random.choice(CODE_SET_B)
                    for _ in range(detail_records_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        status_schema["Claim Status Code"] = np.array(
            [
                [
                    np.random.choice([0, 1, 2, 3, 6, 12, 15, 16, 17, 18, 19, 20])
                    for _ in range(detail_records_count)
                ]
                for __ in range(self._claim_level_record_count)
            ]
        )
        status_schema["Entity Code"] = np.array(
            [
                [np.random.choice(CODE_SET_C) for _ in range(detail_records_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        status_schema["Data in Error"] = np.array(
            [
                ["" for _ in range(detail_records_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        status_schema["Emdeon Status Code"] = np.array(
            [
                ["" for _ in range(detail_records_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )
        status_schema["Record Terminator"] = np.array(
            [
                ["CR" for _ in range(detail_records_count)]
                for __ in range(self._claim_level_record_count)
            ]
        )

    def _generate_trailer_status_schema(self):
        self._trailer_schema["RecordID"] = "TRLR"
        self._trailer_schema["Record Number"] = (
            self._claim_level_record_count * 2
            + self._claim_line_level_record_count * 2 * self._claim_level_record_count
        )
        self._trailer_schema["Record Terminator"] = "CR"

    def generate_all_schemas(self):
        self._generate_header_schema()
        self._generate_claim_level_record_schema()
        self._generate_claim_status_record_schema(
            self._claim_status_record_schema, 1, "CLM"
        )
        self._generate_claim_line_level_record_schema()
        self._generate_claim_status_record_schema(
            self._claim_detail_status_record_schema,
            self._claim_line_level_record_count,
            "DTL",
        )
        self._generate_trailer_status_schema()

        self._file_name = (
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{self._payer_id}_test.cstat"
        )

    def _one_line_schema_to_file(self, schema, filepath):
        with open(f"{filepath}/{self._file_name}", "ab") as file:
            for key in schema.keys():
                file.write(f"{schema[key]}|".encode("ascii", "ignore"))
            file.write("\n".encode("ascii"))

    def _2d_schemas_to_file(self, filepath):
        counter = 2
        with open(f"{filepath}/{self._file_name}", "ab") as file:
            for _ in range(self._claim_level_record_count):
                self._claim_level_record_schema["Record Number"][_] = counter
                counter += 1
                for key in self._claim_level_record_schema.keys():
                    file.write(
                        f"{self._claim_level_record_schema[key][_]}|".encode(
                            "ascii", "ignore"
                        )
                    )
                file.write("\n".encode("ascii"))
                self._claim_status_record_schema["Record Number"][_][0] = counter
                counter += 1
                for key in self._claim_status_record_schema.keys():
                    file.write(
                        f"{self._claim_status_record_schema[key][_][0]}|".encode(
                            "ascii", "ignore"
                        )
                    )
                file.write("\n".encode("ascii"))
                for __ in range(self._claim_line_level_record_count):
                    self._claim_line_level_record["Record Number"][_] = counter
                    counter += 1
                    for line_level_key in self._claim_line_level_record.keys():
                        file.write(
                            f"{self._claim_line_level_record[line_level_key][_][__]}|".encode(
                                "ascii", "ignore"
                            )
                        )
                    file.write("\n".encode("ascii"))
                    self._claim_detail_status_record_schema["Record Number"][
                        _
                    ] = counter
                    counter += 1
                    for (
                        status_record_key
                    ) in self._claim_detail_status_record_schema.keys():
                        file.write(
                            f"{self._claim_detail_status_record_schema[status_record_key][_][__]}|".encode(
                                "ascii", "ignore"
                            )
                        )
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
        self._2d_schemas_to_file(filepath)
        self._one_line_schema_to_file(self._trailer_schema, filepath)

        return f"{filepath}/{self._file_name}"


if __name__ == "__main__":
    generator = RTClaimData("F", False, 4, 2)
    generator.generate_all_schemas()
    generator.schemas_to_file()
