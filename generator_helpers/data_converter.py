import pandas as pd
from datetime import datetime


def convert_csv_to_json(input_csv_file):
    now = datetime.now()
    filename = f'{input_csv_file.split("/")[-1]}-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.json'
    pdObj = pd.read_csv(input_csv_file)
    pdObj.to_json(filename, orient="records")
    return filename


def convert_json_to_csv(input_json_file):
    now = datetime.now()
    filename = f'{input_json_file.split("/")[-1]}-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.csv'
    pdObj = pd.read_json(input_json_file)
    pdObj.to_csv(filename, index=False, header=True)
    return filename


def convert_csv_to_jsonlike(input_csv_file):
    now = datetime.now()
    filename = f'{input_csv_file.split("/")[-1]}-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}'
    pdObj = pd.read_csv(input_csv_file)
    data = pdObj.to_json(orient="records").replace("},{", "}{").lstrip("[").rstrip("]")
    with open(filename, "w+") as jsonlikefile:
        jsonlikefile.write(data)
    return filename


def convert_json_to_jsonlike(input_json_file):
    now = datetime.now()
    filename = f'{input_json_file.split("/")[-1]}-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}'
    json_file_content = open(input_json_file, "r").read()
    data = json_file_content.replace("},{", "}{").lstrip("[").rstrip("]")
    with open(filename, "w+") as jsonlikefile:
        jsonlikefile.write(data)
    return filename


if __name__ == "__main__":
    convert_json_to_csv("")
