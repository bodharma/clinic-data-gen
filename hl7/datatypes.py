import random
from mimesis import Address as addre
from generator_helpers import date_generator, string_generator


class Attachment:
    """
    https://www.hl7.org/fhir/datatypes.html#Attachment
    """

    schema = {
        "contentType": "<code>",  # // Mime type of the content, with charset etc.
        "language": "<code>",  # // Human language of the content (BCP-47)
        "data": "<base64Binary>",  # // Data inline, base64ed
        "url": "<url>",  # // Uri where the data can be found
        "size": "<unsignedInt>",  # // Number of bytes of content (if url provided)
        "hash": "<base64Binary>",  # // Hash of the data (sha-1, base64ed)
        "title": "<string>",  # // Label to display in place of the data
        "creation": "<dateTime>",  # // Date attachment was first created
    }


class Timing:
    """
    https://www.hl7.org/fhir/datatypes.html#Timing
    """

    pass


class SimpleQuantity:
    """
    https://www.hl7.org/fhir/datatypes.html#SimpleQuantity
    """

    pass


class Period:
    """
    https://www.hl7.org/fhir/datatypes.html#Period
    """

    def schema(self):
        start_date = date_generator.date_time_between(start_date="-90y")
        return {
            "start": start_date.timestamp(),  # // C? Starting time with inclusive boundary
            "end": date_generator.date_time_between(
                start_date
            ).timestamp(),  # // C? End time with inclusive boundary, if not ongoing
        }


class Coding:
    """
    https://www.hl7.org/fhir/datatypes.html#Coding
    """

    schema = {
        "system": "https://acme.lab/resultcodes",
        "version": "<string>",
        "code": random.choice(["12333334", "NEG"]),
        "display": "Negative",
        "userSelected": random.choice([True, False]),
    }


class CodeableConcept:
    """
    https://www.hl7.org/fhir/datatypes.html#CodeableConcept
    """

    schema = {"coding": [{Coding()}], "text": "<string>"}


class Media:
    schema = {}


class Identifier:
    """
    https://www.hl7.org/fhir/datatypes.html#Identifier
    """

    def schema(self):
        return {
            # "use" : random.choice(["usual" ,"official" ,"temp" ,"secondary" ,"old"]),
            # "type" : { CodeableConcept().schema },
            # "system" : "https://acme.lab/resultcodes",
            "value": f"{string_generator.bothify(text='?#?#?#?#?#')}",
            # "period" : Period().schema,
            # "assigner" : { Organization().schema }
        }


class ContactPoint:
    """
    https://www.hl7.org/fhir/datatypes.html#ContactPoint
    """

    period = Period()
    schema = {
        "system": random.choice(
            ["phone", "fax", "email", "pager", "url", "sms", "other"]
        ),
        "value": "<string>",
        "use": random.choice(["home", "work", "temp", "old", "mobile"]),
        "rank": random.randint(1, 10),
        "period": period.schema,
    }


class HumanName:
    """
    https://www.hl7.org/fhir/datatypes.html#HumanName
    """

    schema = {
        "use": random.choice(
            ["usual", "official", "temp", "nickname", "anonymous", "old", "maiden"]
        ),
        "text": "<string>",  # // Text representation of the full name
        "family": "<string>",  # // Family name (often called 'Surname')
        "given": [
            "<string>"
        ],  # // Given names (not always 'first'). Includes middle names
        "prefix": ["<string>"],  # // Parts that come before the name
        "suffix": ["<string>"],  # // Parts that come after the name
        "period": {Period()},  # // Time period when name was/is in use
    }


class Address:
    """
    https://www.hl7.org/fhir/datatypes.html#Address
    """

    def schema(self):
        period = Period()
        address = addre("en")

        return {
            "use": random.choice(["home", "work", "temp", "old", "billing"]),
            "type": random.choice(["postal", "physical", "both"]),
            "text": address.address(),
            "line": [address.street_name()],
            "city": address.city(),
            "district": address.country(),
            "state": address.state(abbr=True),
            "postalCode": address.postal_code(),
            "country": address.country(),
            "period": period.schema(),
        }
