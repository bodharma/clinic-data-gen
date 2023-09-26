import csv
import random

from datetime import date, timedelta, datetime
from pathlib import Path
from string import Template


class EDI:
    """
    Used to convert generated client data into edi format.
    :param templates_dir_path: path where edi tamplates exist and used for valid data conversion
    :param csv_dir_path: path, where we import member csv files for conversion
    :param edi_dir_path: path, where we store converted edi files in *.txt format
    """

    def __init__(self, templates_dir_path=None, csv_dir_path=None, edi_dir_path=None):
        workdir = Path.cwd()
        templates_dir_path = Path(f"{workdir}/templates/edi")
        csv_dir_path = Path(f"{workdir}/csv")
        edi_dir_path = Path(f"{workdir}/edi")

        templates_dir_path.mkdir(exist_ok=True)
        csv_dir_path.mkdir(exist_ok=True)
        edi_dir_path.mkdir(exist_ok=True)
        self.TEMPLATE_BASE = templates_dir_path
        self.CSV_BASE = csv_dir_path
        self.EDI_BASE = edi_dir_path

    control_number: str = "7501" + str(random.randrange(10000, 99999))
    message_date = (datetime.now() - timedelta(days=random.randrange(3, 15))).strftime(
        "%Y%m%d"
    )
    short_message_date = (
        datetime.now() - timedelta(days=random.randrange(3, 15))
    ).strftime("%y%m%d")
    message_time = str(random.randrange(10, 23)) + str(random.randrange(10, 59))
    message_group_control = str(random.randrange(1001, 9999))
    current_segment = random.randrange(1001, 9999)

    def read_csv_file(self, path):
        return [el for el in csv.DictReader(open(path, "r"))]

    def generate(self, segments_num, members_data, edidata=None):
        # edi start
        edi = [self.buildISASegement(), self.buildGSSegment()]
        # loop
        segment_count = 0
        for _ in range(segments_num):
            message_date = (
                datetime.now() - timedelta(days=random.randrange(3, 15))
            ).strftime("%Y%m%d")
            # short_message_date = (
            #     datetime.now() - timedelta(days=random.randrange(3, 15))
            # ).strftime("%y%m%d")
            message_time = str(random.randrange(10, 23)) + str(random.randrange(10, 59))
            # message_group_control = str(random.randrange(1001, 9999))
            current_segment = random.randrange(1001, 9999)
            mrn = (
                str(random.randrange(1001, 9999))
                + "-"
                + str(random.randrange(1001, 9999))
            )

            # Generate BHT
            edi.extend(
                [
                    self.buildSTSegment(current_segment),
                    # Generate an ass ton of encounters
                    self.buildBHTSegment(mrn, message_time, message_date),
                    # Generate Loop 2000A - Billing Provider
                    self.buildProviderSegment(),
                ]
            )
            if edidata:
                edi.extend(
                    [
                        # Generate Loop 2000B - Subscriber
                        self.buildSubscriberSegment(members_data, edidata.subscriber),
                        # Generate Loop 2300 - Claim Information
                        self.buildClaimsSegment(mrn, message_time, edidata.claim),
                    ]
                )
            else:
                edi.extend(
                    [
                        # Generate Loop 2000B - Subscriber
                        self.buildSubscriberSegment(members_data),
                        # Generate Loop 2300 - Claim Information
                        self.buildClaimsSegment(mrn, message_time),
                    ]
                )
            # Generate SE
            edi.extend([self.buildSESegment(current_segment)])

        # edi end

        edi.extend(
            [
                self.buildGESegment(self.message_group_control, segment_count),
                self.buildIEASegment(),
            ]
        )
        return edi

    def buildISASegement(self):
        # banana CARE is 719689, banana direct is 66066
        isa_schema = {
            "control_number": self.control_number,
            "sender": "719689",
            "receiver": "66066",
            "time": self.message_time,
            "date": self.short_message_date,
        }

        # load the ISA template and merge
        isaString = self.loadFileTemplate("ISA.txt")
        isaSection = Template(isaString).substitute(isa_schema)

        return isaSection

    def buildGSSegment(self):
        # banana CARE is 719689, banana direct is 66066
        gs_schema = {
            "sender": "719689",
            "receiver": "66066",
            "time": self.message_time,
            "date": self.short_message_date,
            "control_group": self.message_group_control,
        }

        gsString = self.loadFileTemplate("GS.txt")
        gsSection = Template(gsString).substitute(gs_schema)

        return gsSection

    def buildGESegment(self, message_group_control, segment_count):
        ge_schema = {
            "control_group": message_group_control,
            "segment_count": segment_count,
        }

        # load the GE template and merge
        geString = self.loadFileTemplate("GE.txt")
        geSection = Template(geString).substitute(ge_schema)

        return geSection

    def buildIEASegment(self,):
        iea_schema = {"control_group": self.control_number}

        ieaString = self.loadFileTemplate("IEA.txt")
        ieaSection = Template(ieaString).substitute(iea_schema)

        return ieaSection

    def buildSTSegment(self, current_segment):
        st_schema = {"segment_number": current_segment}

        # load the ISA template and merge
        stString = self.loadFileTemplate("ST.txt")
        stSection = Template(stString).substitute(st_schema)

        return stSection

    def buildBHTSegment(self, mrn_number, message_time, message_date):
        bht_schema = {"time": message_time, "date": message_date, "mrn": mrn_number}

        # load the BHT template and merge
        bhtString = self.loadFileTemplate("BHT.txt")
        bhtString = Template(bhtString).substitute(bht_schema)

        return bhtString

    def buildProviderSegment(self):
        # provider_dict = dict()

        # provider_dict["time"] = message_time
        # provider_dict["encounter_date"] = encounter_date
        # provider_dict["mrn"] = mrn_number

        # load the BHT template and merge
        providerString = self.loadFileTemplate("Provider.txt")
        # providerString = Template(providerString).substitute(provider_dict)

        return providerString

    def buildSubscriberSegment(self, member_data, subscriber_data=None):
        member_record = random.choice(member_data)

        #

        bithdate = member_record["birth_date"]
        datetimeobject = datetime.strptime(bithdate, "%m/%d/%Y")
        newformatBirthdate = datetimeobject.strftime("%Y%m%d")
        gender = member_record["gender"]
        subscriber_dict_base = {
            "group_id": member_record["Plan"],
            "last_name": member_record["last_name"],
            "first_name": member_record["first_name"],
            "member_number": member_record["banana ID"],
            "street_address": member_record["primary_address_line1"],
            "city": member_record["primary_address_city"],
            "state": member_record["primary_address_state"],
            "zip_code": member_record["primary_address_zipcode"],
            "birthdate": newformatBirthdate,
            "gender": "F" if gender == "Female" else "M",
        }
        subscriber_dict = subscriber_dict_base.copy()
        if subscriber_data:
            subscriber_dict.update(subscriber_data)
        for k, v in subscriber_dict.items():
            if v is None:
                subscriber_dict[k] = subscriber_dict_base[k]

        subscriberString = self.loadFileTemplate("Subscriber.txt")
        subscriberString = Template(subscriberString).substitute(subscriber_dict)
        return subscriberString

    def buildClaimsSegment(self, mrn_number, message_time, claim_data=None):
        encounter_date = (
            datetime.now() - timedelta(days=random.randrange(10, 30))
        ).strftime("%Y%m%d")
        # encounter_time = str(random.randrange(10, 16)) + str(random.randrange(0, 59))

        # TODO: should we have strong accordance between diagnosis_code and procedure_code ?
        diagnosis_codes_list = [
            "N926",
            "R5382",
            "J209",
            "J069",
            "M75122",
            "F1520",
            "Z23",
        ]
        service_codes_list = [
            "U0004",
            "U0005",
            "U0006",
            "U0007",
            "U0008",
            "U0009",
            "U0003",
        ]
        procedure_codes_list = [
            99214,
            99211,
            99283,
            "J0696",
            97530,
            99336,
            90700,
            93306,
        ]

        claims_schema_base = {
            "time": message_time,
            "encounter_date": encounter_date,
            "mrn": mrn_number,
            "diagnosis_code": random.choice(diagnosis_codes_list),
            "service_code": random.choice(service_codes_list),
            "procedure_code": random.choice(procedure_codes_list),
            "service_price": random.uniform(10.0, 400.0),
            "procedure_price": random.uniform(10.0, 400.0),
        }
        claims_schema = claims_schema_base.copy()

        if claim_data:
            claims_schema.update(claim_data)

        for k, v in claims_schema.items():
            if v is None:
                claims_schema[k] = claims_schema_base[k]

        claims_schema["mrn_sum"] = (
            claims_schema["service_price"] + claims_schema["procedure_price"]
        )
        claimsString = self.loadFileTemplate("Claim.txt")
        claimsString = Template(claimsString).substitute(claims_schema)

        return claimsString

    def buildSESegment(self, current_segment):
        se_schema = {
            "segment_number": current_segment,
            "segment_count": random.randrange(20, 32),
        }

        # load the ISA template and merge
        seString = self.loadFileTemplate("SE.txt")
        seSection = Template(seString).substitute(se_schema)

        return seSection

    def writeEDIDocument(self, segment_list, path=None):
        path = path if path else self.EDI_BASE
        document_string = "".join(segment_list)
        edi_file_name = f"{path}/{self.control_number}.txt"
        edi_file = open(edi_file_name, "w+")
        edi_file.write(document_string)
        edi_file.close()
        return edi_file_name

    def loadFileTemplate(self, fileName):
        with open(f"{self.TEMPLATE_BASE}/{fileName}", "r") as file:
            return file.read()


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    edi = EDI()
    edi_doc = edi.generate(10, edi.read_csv_file("csv/test_data.csv"))
    edi.writeEDIDocument(edi_doc)
