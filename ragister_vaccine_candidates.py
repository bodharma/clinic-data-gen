import random
import httpx
import numpy as np
from mimesis import Person
from generator_helpers.date_generator import date_time_between
from loguru import logger
from pathlib import Path
from csv import DictReader, DictWriter
import datetime


class GetStateAddresses:
    """
    Class is used for getting/saving/reformatting valid addresses,
    it is donee, because Registration API has validator where it
    checks if the specified address is in some state or not.
    https://pointmatch.Staterevenue.com/General/AddressFiles.aspx
    """

    def __init__(self):
        self.address_data_dir = Path(f"{Path.cwd()}/addresses")

    def get_county_files_list(self):
        county_files_list = []
        for address_archive in self.address_data_dir.iterdir():
            for county_file in address_archive.iterdir():
                county_files_list.append(county_file)
        return county_files_list

    def load_county_addresses_list(self, county):
        with open(county) as csvfile:
            return np.array(
                [
                    {
                        "address_1": f"{row['NUMBER']} {row['STNAME']} {row['STSUFFIX']}",
                        "city": f"{row['MAILCITY']}",
                        "zip": f"{row['ZIP']}",
                    }
                    for row in DictReader(csvfile)
                ]
            )

    def write_csv_file(self, addreses_list, entries_count=3000):
        with open(self.address_data_dir / "addrreses.csv", "w+") as addreses_file:
            addreses_csv = DictWriter(addreses_file, fieldnames=addreses_list[0].keys())
            addreses_csv.writerows(addreses_list[:entries_count])


class VaccineCandidate:
    """
    Registrator engine
    """

    def __init__(self, authority="mdc"):
        self.authority = authority

    def load_addreses_csv(self):
        with open(f"{Path.cwd()}/addresses/addrreses.csv") as csvfile:
            return [row for row in DictReader(csvfile)]

    def generate_data(self, count):
        addresses_list = self.load_addreses_csv()
        data_list = []
        for _ in range(count):
            locale = "en"
            prsn = Person(locale)
            data = {
                "url_origin": "none",
                "authority": self.authority,
                "form_data": [
                    {
                        "address_2": "",
                        "dob": date_time_between(
                            start_date="-80y", end_date="-10y"
                        ).strftime("%Y-%m-%d"),
                        "email": prsn.email(domains=["example.com"]),
                        "locale": locale,
                        "apartment": str(random.randint(1, 99999)),
                        "last_name": prsn.last_name(),
                        "first_name": prsn.first_name(),
                        "phone": prsn.telephone(mask="#" * 10),
                        "mobile_phone": False,
                        "state": "LO",
                        "vaccination_data": {
                            "transportation_assistance": random.choice([True, False])
                        },
                    }
                ],
            }
            data["form_data"][-1].update(random.choice(addresses_list))
            data_list.append(data)
        return data_list

    def register_via_api(self, data_list):
        url = "https://localhost:8000/api/v1/register"

        for data in data_list:
            resp = httpx.post(
                url, headers={"Content-Type": "application/json"}, json=data
            )
            if resp.status_code in [200, 201]:
                logger.debug("User is registered")
            else:
                logger.debug(f"Bad happend, code {resp.status_code}: {resp.json()}")

    def save_data_to_csv(self, data, filepath=None):
        now = datetime.datetime.now()
        filepath = (
            filepath
            if filepath
            else Path(f"{Path.cwd()}/{now.year}/{now.month}/{now.day}/")
        )
        Path(filepath).mkdir(exist_ok=True, parents=True)
        data = np.array([entry["form_data"][-1] for entry in data])
        filename = f"{filepath}test_vaccine_candidates_data_{int(now.timestamp())}.csv"
        csv_file = DictWriter(open(filename, "w+"), fieldnames=data[-1].keys())
        csv_file.writeheader()
        csv_file.writerows(data)
        return filename


if __name__ == "__main__":
    vaccine_candidate = VaccineCandidate("mdc")
    data_list = vaccine_candidate.generate_data(1)
    vaccine_candidate.save_data_to_csv(data_list)
