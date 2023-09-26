from datetime import datetime

import numpy as np
from mimesis import Person, Datetime, Address, Code, Text
from pathlib import Path

from generate_rt_eligibility_data import AN_DATA_TYPE

BODY_PART_NAME = np.array(
    [
        "Head",
        "Brain",
        "Ear",
        "Eye",
        "Jaw",
        "Mouth",
        "Teeth",
        "Nose",
        "Face",
        "Skull",
        "Neck",
    ]
)
NOIC = {"GR": "NCCI Nature of Injury Code", "NI": "Nature of Injury Code"}
CODE_SET_B = np.array(
    [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "30",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40",
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48",
        "49",
        "50",
        "51",
        "52",
        "53",
        "54",
        "55",
        "56",
        "57",
        "58",
        "59",
        "60",
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "67",
        "68",
        "69",
        "70",
        "71",
        "72",
        "73",
        "74",
        "75",
        "76",
        "77",
        "78",
        "79",
        "80",
        "81",
        "82",
        "83",
        "84",
        "85",
        "86",
        "87",
        "88",
        "89",
        "90",
        "91",
        "92",
        "93",
        "94",
        "95",
        "96",
        "97",
        "98",
        "99",
        "A0",
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
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
        "AK",
        "AL",
        "AM",
        "AN",
        "AO",
        "AP",
        "AQ",
        "AR",
        "B1",
        "B2",
        "B3",
        "BA",
        "BB",
        "BC",
        "BD",
        "BE",
        "BF",
        "BG",
        "BH",
        "BI",
        "BJ",
        "BK",
        "BL",
        "BM",
        "BN",
        "BO",
        "BP",
        "BQ",
        "BR",
        "BS",
        "BT",
        "BU",
        "BV",
        "BW",
        "BX",
        "BY",
        "BZ",
        "C1",
        "CA",
        "CB",
        "CC",
        "CD",
        "CE",
        "CF",
        "CG",
        "CH",
        "CI",
        "CJ",
        "CK",
        "CL",
        "CM",
        "CN",
        "CO",
        "CP",
        "CQ",
        "DG",
        "DM",
        "DS",
        "GF",
        "GN",
        "GY",
        "IC",
        "MH",
        "NI",
        "ON",
        "PT",
        "PU",
        "RN",
        "RT",
        "TC",
        "TN",
        "UC",
    ]
)
CODE_SET_C = np.array(
    [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "A",
        "B",
        "C",
        "CB",
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
        "MC",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
)
CODE_SET_D = np.array(
    [
        "12",
        "13",
        "14",
        "15",
        "16",
        "41",
        "42",
        "43",
        "47",
        "AP",
        "C1",
        "CO",
        "CP",
        "D",
        "DB",
        "EP",
        "FF",
        "GP",
        "HM",
        "HN",
        "HS",
        "IN",
        "IP",
        "LC",
        "LD",
        "LI",
        "LT",
        "MA",
        "MB",
        "MC",
        "MH",
        "MI",
        "MP",
        "OT",
        "PE",
        "PL",
        "PP",
        "PR",
        "PS",
        "QM",
        "PR",
        "SP",
        "TF",
        "WC",
        "WU",
    ]
)
CODE_SET_E = np.array(
    [
        "6",
        "7",
        "13",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
    ]
)
CODE_SET_F = np.array(
    [
        "8H",
        "99",
        "CA",
        "CE",
        "D3",
        "DB",
        "DY",
        "HS",
        "LA",
        "LE",
        "M2",
        "MN",
        "P6",
        "QA",
        "S7",
        "S8",
        "VS",
        "YY",
    ]
)
CODE_SET_G = np.array(["AD", "CJ", "HC", "ID", "IV", "N4", "ZZ"])
CODE_SET_H = np.array(
    [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
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
        "P",
        "Q",
        "R",
        "S",
        "SG",
        "SL",
        "SP",
        "SX",
        "SY",
        "SZ",
        "T",
        "U",
        "V",
    ]
)
CODE_SET_I = np.array(
    [
        "6",
        "7",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
    ]
)


class RTPlanBenefitData:
    def __init__(
        self, entries_number: int, load_type: str, optional_fields: bool = False
    ):
        self._fake_person = Person("en")
        self._fake_date = Datetime()
        self._fake_text = Text()

        self._optional_fields = optional_fields
        self.load_type = load_type
        self._entries_number = entries_number
        self._file_name = ""
        self._payer_id = "".join(np.random.choice(AN_DATA_TYPE, size=10))
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
            self._fake_person.first_name() if self._optional_fields else ""
        )
        self.header_schema["Payer Support Telephone Number"] = (
            self._fake_person.telephone("##########") if self._optional_fields else ""
        )
        self.header_schema["Payer Support Email Address"] = (
            self._fake_person.email() if self._optional_fields else ""
        )
        self.header_schema["Load Type"] = self.load_type
        self.header_schema["Payer Unique File Identifier"] = datetime.now().strftime(
            "%Y%m%d%H%M%S"
        )
        self.header_schema["File Type"] = "Planbene"
        self.header_schema["Version Code"] = "03"
        self.header_schema["Release Code"] = "00"
        self.header_schema["File Validation Code"] = (
            5 if self._optional_fields else np.random.choice([0, 1, 2, 3, 4, 5])
        )
        self.header_schema["Record Terminator"] = "CR"

    def _generate_detail_schema(self):
        self.detail_schema["Record Id"] = np.array(
            ["DTL" for _ in range(self._entries_number)]
        )
        self.detail_schema["Record Number"] = np.array(
            [_ for _ in range(2, self._entries_number + 2)]
        )
        self.detail_schema["Payer ID"] = np.array(
            [self._payer_id for _ in range(self._entries_number)]
        )
        self.detail_schema["Maintenance Type Code"] = np.array(
            ["030" for _ in range(self._entries_number)]
        )
        self.detail_schema["Member Plan Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Member Group Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Benefit Information"] = np.array(
            [np.random.choice(CODE_SET_C) for _ in range(self._entries_number)]
        )
        self.detail_schema["Service Type Code"] = np.array(
            [np.random.choice(CODE_SET_B) for _ in range(self._entries_number)]
        )
        self.detail_schema["Coverage Level Code"] = np.array(
            [
                np.random.choice(
                    np.array(
                        ["CHD", "DEP", "ECH", "EMP", "ESP", "FAM", "IND", "SPC", "SPO"]
                    )
                )
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Insurance Type Code"] = np.array(
            [
                np.random.choice(CODE_SET_D) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Procedure Qualifier"] = np.array(
            [
                np.random.choice(CODE_SET_G) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Procedure Code"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=5))
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Procedure Range End"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=5))
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Procedure Modifier 1"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self.detail_schema["Procedure Modifier 2"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self.detail_schema["Procedure Modifier 3"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self.detail_schema["Procedure Modifier 4"] = np.array(
            ["" for _ in range(self._entries_number)]
        )
        self.detail_schema["Plan Coverage Description"] = np.array(
            [
                self._fake_text.sentence() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Time Period Qualifier"] = np.array(
            [
                np.random.choice(CODE_SET_E) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Benefit Amount"] = np.array(
            [
                np.random.randint(1, 9999999) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Benefit Percentage"] = np.array(
            [
                str(np.random.randint(1, 100) / 100)[1:]
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Quantity Qualifier"] = np.array(
            [
                np.random.choice(CODE_SET_F) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Quantity"] = np.array(
            [
                np.random.randint(1, 9999999) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Authorization/Certification Indicator"] = np.array(
            [
                np.random.choice(np.array(["Y", "N", "U"]))
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["In Plan Network Indicator"] = np.array(
            [
                np.random.choice(np.array(["Y", "N", "U", "W"]))
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Benefits Effective Date"] = np.array(
            [
                self._fake_date.date(start=2010, end=2015).strftime("%Y%m%d")
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Benefits Termination Date"] = np.array(
            [
                self._fake_date.date(start=2015, end=2020).strftime("%Y%m%d")
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Benefit Message 1"] = np.array(
            [
                self._fake_text.sentence() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Benefit Message 2"] = np.array(
            [
                self._fake_text.sentence() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Benefit Message 3"] = np.array(
            [
                self._fake_text.sentence() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Benefit Message 4"] = np.array(
            [
                self._fake_text.sentence() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Benefit Message 5"] = np.array(
            [
                self._fake_text.sentence() if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Nature of Injury Code Qualifier"] = np.array(
            [
                np.random.choice(list(NOIC.keys())) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Nature of Injury Code"] = np.array(
            [
                NOIC[self.detail_schema["Nature of Injury Code Qualifier"][_]]
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Injured Body Part Name"] = np.array(
            [
                np.random.choice(BODY_PART_NAME) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Facility Type Code"] = np.array(
            [
                np.random.choice([1, 2, 3, 4, 6, 7, 8]) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Alternative List ID"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Coverage List ID"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=10))
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Drug Formulary Number"] = np.array(
            [
                "".join(np.random.choice(AN_DATA_TYPE, size=5))
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Medical Assistance Category"] = np.array(
            [
                np.random.choice(
                    [
                        "HIV/ AIDS",
                        "Medicaid and Medicare",
                        "Medicare Social Security",
                        "Disability Assistance",
                        "Veterans Health",
                        "Children's Health",
                        "Counsel and Counseling",
                    ]
                )
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Delivery Quantity Qualifier"] = np.array(
            [
                np.random.choice(["DY", "LO", "HS", "MN", "VS"])
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Delivery Quantity"] = np.array(
            [
                np.random.randint(1, 50) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Delivery Sampling Frequency Qualifier"] = np.array(
            [
                np.random.choice(["DA", "MO", "VS", "WK", "YR"])
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Delivery Sampling Frequency"] = np.array(
            [
                np.random.randint(1, 10) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Delivery Period Qualifier"] = np.array(
            [
                np.random.choice(CODE_SET_I) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Delivery Period Count "] = np.array(
            [
                np.random.randint(1, 10) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Delivery Pattern Code "] = np.array(
            [
                np.random.choice(CODE_SET_H) if self._optional_fields else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Delivery Time Code"] = np.array(
            [
                np.random.choice(["A", "B", "C", "D", "E", "F", "G", "Y"])
                if self._optional_fields
                else ""
                for _ in range(self._entries_number)
            ]
        )
        self.detail_schema["Record Terminator "] = np.array(
            ["CR" for _ in range(self._entries_number)]
        )

    def _generate_trailer_schema(self):
        self.trailer_schema["RecordID"] = "TRLR"
        self.trailer_schema["Record Count"] = self._entries_number
        self.trailer_schema["Record Terminator "] = "CR"

    def generate_all_schemas(self):

        self._generate_header_schema()
        self._generate_detail_schema()
        self._generate_trailer_schema()
        self._file_name = (
            f'{datetime.now().strftime("%Y%m%d%H%M%S")}_{self._payer_id}_test.plan'
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

        self._one_line_schema_to_file(self.header_schema, filepath)
        self._detailed_schema_to_file(self.detail_schema, filepath)
        self._one_line_schema_to_file(self.trailer_schema, filepath)

        return f"{filepath}/{self._file_name}"


if __name__ == "__main__":
    generator = RTPlanBenefitData(100, "F", True)
    generator.generate_all_schemas()
    generator.schemas_to_file()
