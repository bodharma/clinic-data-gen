import random
from datetime import datetime
import pandas as pd
from mimesis import Person, Finance, Address as addre
from generator_helpers import date_generator, string_generator
from pathlib import Path
import time
import boto3
import os
from datatypes import (
    Attachment,
    Address,
    Coding,
    CodeableConcept,
    ContactPoint,
    HumanName,
    Identifier,
    Period,
    Media,
    Timing,
    SimpleQuantity,
)

from fhir.resources.diagnosticreport import DiagnosticReport as DiagnosticReport_native


class Encounter:
    """
    https://www.hl7.org/fhir/encounter.html
    """

    def schema(self):
        return {
            "resourceType": "Encounter",
            "identifier": f"{string_generator.bothify(text='?#?#?#?#?#')}",
            # "status": "",
            # "statusHistory": [
            #     {"status": "",
            #      "period": ""}
            # ],
            # "class": "",
            # "classHistory": [
            #     {"class": "",
            #      "period": ""}
            # ],
            # "type": "",
            # "serviceType": "",
            # "priority": "",
            # "subject": "",
            # "episodeOfCare": [{}],
            # "basedOn": [{}],
            # "participant": [
            #     {"type": "",
            #      "period": "",
            #      "individual": ""}
            # ],
            # "appointment": [{}],
            "period": Period().schema(),
            # "length": {},
            # "reasonCode": [{}],
            # "reasonReference": [{}],
            # "diagnosis": [
            #     {"condition": {},
            #      "use": {},
            #      "rank": ""}
            # ],
            # "account": [{}],
            # "hospitalization": {
            #     "preAdmissionIdentifier": "",
            #     "origin": "",
            #     "admitSource": "",
            #     "reAdmission": "",
            #     "dietPreference": "",
            #     "specialCourtesy": "",
            #     "specialArrangement": "",
            #     "destination": "",
            #     "dischargeDisposition": ""
            # },
            # "location": [
            #     {"location": "",
            #      "status": "",
            #      "physicalType": "",
            #      "period": ""}
            # ],
            # "serviceProvider": {},
            # "partOf": {}
        }


class Location:
    """
    https://www.hl7.org/fhir/location.html
    """

    def schema(self):
        # contact_point = ContactPoint()
        return {
            "resourceType": "Location",
            "identifier": f"{string_generator.bothify(text='?#?#?#?#?#')}",
            # "status": random.choice(["active", "suspended", "inactive"]),
            # "operationalStatus": Coding().schema,
            # "name": "",
            # "alias": [""],
            # "description": "",
            # "mode": random.choice(["instance", "kind"]),
            # "type": CodeableConcept().schema,
            # "telecom": [contact_point.schema],
            "address": Address().schema(),
            # "physicalType": "",
            # "position": {
            #     "longitude": random.uniform(10.00000001, 99.00000001),
            #     "latitude": random.uniform(10.00000001, 99.00000001),
            #     "altitude": random.uniform(10.00000001, 99.00000001)
            # },
            # "managingOrganization": "", #{Reference(Organization)}
            # "partOf": "", #Reference(Location)
            # "hoursOfOperation": [
            #     {
            #         "daysOfWeek": random.choice(["mon", "tue", "wed", "thu", "fri", "sat", "sun"]),
            #         "allDay": random.choice([False, True]),
            #         "openingTime": datetime.now(),
            #         "closingTime": datetime.now(),
            #     }
            # ],
            # "availabilityExceptions": "",
            # "endpoint": [{}] #Reference(Endpoint)
        }


class Endpoint:
    """
    https://www.hl7.org/fhir/endpoint.html#Endpoint
    """

    schema = {
        "resourceType": "Endpoint",
        "identifier": [
            {Identifier}
        ],  # // Identifies this endpoint across multiple systems
        "status": "<code>",  # // R!  active | suspended | error | off | entered-in-error | test
        "connectionType": {
            Coding
        },  # // R!  Protocol/Profile/Standard to be used with this endpoint connection
        "name": "<string>",  # // A name that this endpoint can be identified by
        # "managingOrganization": Organization(),
        # // Organization that manages this endpoint (might not be the organization that exposes the endpoint)
        "contact": [
            ContactPoint()
        ],  # // Contact details for source (e.g. troubleshooting)
        "period": {Period()},  # // Interval the endpoint is expected to be operational
        "payloadType": [CodeableConcept()],
        # // R!  The type of content that may be used at this endpoint (e.g. XDS Discharge summaries)
        "payloadMimeType": ["<code>"],
        # // Mimetype to send. If not specified, the content could be anything (including no payload, if the connectionType defined this)
        "address": "<url>",  # // R!  The technical base address for connecting to this endpoint
        "header": ["<string>"],  # // Usage depends on the channel type
    }


class Organization:
    """
    https://www.hl7.org/fhir/organization.html#Organization
    """

    def schema(self):
        return {
            "resourceType": "Organization",
            "identifier": string_generator.bothify(
                text="#####-#####"
            ),  # // C? Identifies this organization  across multiple systems
            # "active": random.choice([True, False]),  # // Whether the organization's record is still in active use
            # "type": [CodeableConcept()],  # // Kind of organization
            "name": Finance("en").company(),  # // C? Name used for the organization
            # "alias": [""],
            # // A list of alternate names that the organization is known as, or was known as in the past
            # "telecom": [{ContactPoint()}],  # // C? A contact detail for the organization
            "address": [Address().schema()],  # // C? An address for the organization
            # "partOf": "",  # // The organization of which this organization forms a part
            # "contact": [
            #     {
            #         "purpose": {CodeableConcept},  # // The type of contact
            #         "name": {HumanName()},  # // A name associated with the contact
            #         "telecom": [{ContactPoint()}],  # // Contact details (telephone, email, etc.)  for a contact
            #         "address": {Address()}  # // Visiting or postal addresses for the contact
            #     }
            # ],
            # "endpoint": [
            #     Endpoint().schema]  # // Technical endpoints providing access to services operated for the organization
        }


class Practitioner:
    """
    https://www.hl7.org/fhir/practitioner.html#Practitioner
    """

    schema = {}


class PractitionerRole:
    """
    https://www.hl7.org/fhir/practitionerrole.html#PractitionerRole
    """

    schema = {}


class RelatedPerson:
    """
    https://www.hl7.org/fhir/relatedperson.html#RelatedPerson
    """

    schema = {}


class Patient:
    """
    https://www.hl7.org/fhir/patient.html
    """

    def schema(self):
        return {
            "resourceType": "Patient",
            "identifier": string_generator.bothify(
                text="#####-#####"
            ),  # // An identifier for this patient
            # "active": random.choice([False, True]),  # // Whether this patient's record is in active use
            # "name": [{HumanName().schema}],  # // A name associated with the patient
            # "telecom": [{ContactPoint().schema}],  # // A contact detail for the individual
            # "gender": "<code>",  # // male | female | other | unknown
            "birthDate": date_generator.date_time_between(
                start_date="-90y"
            ).timestamp(),  # // The date of birth for the individual
            # # // deceased[x]: Indicates if the individual is deceased or not. One of these 2:
            # "deceasedBoolean": random.choice([False, True]),
            # "deceasedDateTime": "<dateTime>",
            "address": [Address().schema()],  # // An address for the individual
            # "maritalStatus": {CodeableConcept().schema},  # // Marital (civil) status of a patient
            # // multipleBirth[x]: Whether patient is part of a multiple birth. One of these 2:
            # "multipleBirthBoolean": random.choice([False, True]),
            # "multipleBirthInteger": random.randint(1, 9),
            # "photo": [Attachment().schema],  # // Image of the patient
            # "contact": [{  # // A contact party (e.g. guardian, partner, friend) for the patient
            #     "relationship": [CodeableConcept],  # // The kind of relationship
            #     "name": {HumanName},  # // A name associated with the contact person
            #     "telecom": [ContactPoint],  # // A contact detail for the person
            #     "address": Address,  # // Address for the contact person
            #     "gender": "<code>",  # // male | female | other | unknown
            #     "organization": Organization,  # // C? Organization that is associated with the contact
            #     "period": {Period}
            #     # // The period during which this contact person or organization is valid to be contacted relating to this patient
            # }],
            # "communication": [{  # // A language which may be used to communicate with the patient about his or her health
            #     "language": {CodeableConcept},
            #     # // R!  The language which can be used to communicate with the patient about his or her health
            #     "preferred": random.choice([False, True])
            # }],
            # "generalPractitioner": random.choice([Organization().schema ,Practitioner().schema ,PractitionerRole().schema]),
            # // Patient's nominated primary care provider
            # "managingOrganization": Organization().schema,
            # // Organization that is the custodian of the patient record
            # "link": [{  # // Link to another patient resource that concerns the same actual person
            #     "other": random.choice([Patient, RelatedPerson]),
            # // R!  The other patient or related person resource that the link refers to
            # "type": "<code>"  # // R!  replaced-by | replaces | refer | seealso
            # }]
        }


class Observation:
    """
    https://www.hl7.org/fhir/observation.html#Observation
    """

    def schema(self):
        return {
            "resourceType": "Observation",
            "identifier": f"{string_generator.bothify(text='?#?#?#?#?#')}",  # // Business Identifier for observation
            "valueString": f"{string_generator.bothify(text='??????????')}",
        }


class PlanDefinition:
    """
    https://www.hl7.org/fhir/plandefinition.html#PlanDefinition
    """

    pass


class Questionnaire:
    """
    https://www.hl7.org/fhir/questionnaire.html#Questionnaire
    """

    pass


class Device:
    """
    https://www.hl7.org/fhir/device.html#Device
    """

    pass


class ActivityDefinition:
    """
    https://www.hl7.org/fhir/activitydefinition.html#ActivityDefinition
    """

    pass


class OperationDefinition:
    """
    https://www.hl7.org/fhir/operationdefinition.html#OperationDefinition
    """

    pass


class Measure:
    """
    https://www.hl7.org/fhir/measure.html#Measure
    """

    pass


class Group:
    """
    https://www.hl7.org/fhir/group.html#Group
    """

    pass


class CareTeam:
    """
    https://www.hl7.org/fhir/careteam.html#CareTeam
    """

    pass


class Condition:
    """
    https://www.hl7.org/fhir/condition.html#Condition
    """

    pass


class Any:
    """
    https://www.hl7.org/fhir/resourcelist.html
    """

    pass


class Goal:
    """
    https://www.hl7.org/fhir/goal.html#Goal
    """

    pass


class Annotation:
    """
    https://www.hl7.org/fhir/datatypes.html#Annotation
    """

    pass


class Appointment:
    """
    https://www.hl7.org/fhir/appointment.html#Appointment
    """

    pass


class CommunicationReport:
    """

    """

    pass


class DeviceRequest:
    """
    https://www.hl7.org/fhir/devicerequest.html#DeviceRequest
    """

    pass


class MedicationRequest:
    """
    https://www.hl7.org/fhir/medicationrequest.html#MedicationRequest
    """

    pass


class NutritionOrder:
    """
    https://www.hl7.org/fhir/nutritionorder.html#NutritionOrder
    """

    pass


class Task:
    """
    https://www.hl7.org/fhir/task.html#Task
    """

    pass


class ServiceRequest:
    """
    https://www.hl7.org/fhir/servicerequest.html#ServiceRequest
    """

    pass


class VisionPrescription:
    """
    https://www.hl7.org/fhir/visionprescription.html#VisionPrescription
    """

    pass


class CommunicationRequest:
    """
    https://www.hl7.org/fhir/communicationrequest.html#CommunicationRequest
    """

    pass


class RequestGroup:
    """
    https://www.hl7.org/fhir/requestgroup.html#RequestGroup
    """

    pass


class DiagnosticReport:
    """
    https://www.hl7.org/fhir/diagnosticreport.html#DiagnosticReport
    """

    pass


class DocumentReference:
    """
    https://www.hl7.org/fhir/documentreference.html#DocumentReference
    """

    pass


class Medication:
    """
    https://www.hl7.org/fhir/medication.html#Medication
    """

    pass


class Substance:
    """
    https://www.hl7.org/fhir/substance.html#Substance
    """

    pass


class HealthcareService:
    """
    https://www.hl7.org/fhir/healthcareservice.html#HealthcareService
    """

    pass


class ImmunizationRecommendation:
    """
    https://www.hl7.org/fhir/immunizationrecommendation.html#ImmunizationRecommendation
    """

    pass


class CarePlan:
    """
    https://www.hl7.org/fhir/careplan.html#CarePlan
    """

    def schema(self):
        template = {
            "resourceType": "CarePlan",
            "identifier": [Identifier()],  # // External Ids for this plan
            "instantiatesCanonical": [
                random.choice(
                    [
                        PlanDefinition(),
                        Questionnaire(),
                        Measure(),
                        ActivityDefinition(),
                        OperationDefinition(),
                    ]
                )
            ],
            # // Instantiates FHIR protocol or definition
            "instantiatesUri": [
                "<uri>"
            ],  # // Instantiates external protocol or definition
            "basedOn": [CarePlan()],  # // Fulfills CarePlan
            "replaces": [CarePlan()],  # // CarePlan replaced by this CarePlan
            "partOf": [CarePlan()],  # // Part of referenced CarePlan
            "status": "<code>",  # // R!  draft | active | on-hold | revoked | completed | entered-in-error | unknown
            "intent": "<code>",  # // R!  proposal | plan | order | option
            "category": [CodeableConcept()],  # // Type of plan
            "title": "<string>",  # // Human-friendly name for the care plan
            "description": "<string>",  # // Summary of nature of plan
            "subject": random.choice(
                [Patient(), Group()]
            ),  # // R!  Who the care plan is for
            "encounter": Encounter(),  # // Encounter created as part of
            "period": Period(),  # // Time period plan covers
            "created": "<dateTime>",  # // Date record was first recorded
            "author": random.choice(
                [
                    Patient(),
                    Practitioner(),
                    PractitionerRole(),
                    Device(),
                    RelatedPerson(),
                    Organization(),
                    CareTeam(),
                ]
            ),
            # // Who is the designated responsible party
            "contributor": [
                random.choice(
                    [
                        Patient(),
                        Practitioner(),
                        PractitionerRole(),
                        Device(),
                        RelatedPerson(),
                        Organization(),
                        CareTeam(),
                    ]
                )
            ],
            # // Who provided the content of the care plan
            "careTeam": [CareTeam()],  # // Who's involved in plan?
            "addresses": [Condition()],  # // Health issues this plan addresses
            "supportingInfo": [Any()],  # // Information considered as part of plan
            "goal": [Goal()],  # // Desired outcome of plan
            "activity": [
                {  # // Action to occur as part of plan
                    "outcomeCodeableConcept": [
                        CodeableConcept()
                    ],  # // Results of the activity
                    "outcomeReference": [
                        Any()
                    ],  # // Appointment, Encounter, Procedure, etc.
                    "progress": [
                        Annotation()
                    ],  # // Comments about the activity status/progress
                    "reference": random.choice(
                        [
                            Appointment(),
                            CommunicationRequest(),
                            DeviceRequest(),
                            MedicationRequest(),
                            NutritionOrder(),
                            Task(),
                            ServiceRequest(),
                            VisionPrescription(),
                            RequestGroup(),
                        ]
                    ),
                    # // C? Activity details defined in specific resource
                    "detail": {  # // C? In-line definition of activity
                        "kind": "<code>",
                        # // Appointment | CommunicationRequest | DeviceRequest | MedicationRequest | NutritionOrder | Task | ServiceRequest | VisionPrescription
                        "instantiatesCanonical": [
                            random.choice(
                                [
                                    PlanDefinition(),
                                    ActivityDefinition(),
                                    Questionnaire(),
                                    Measure(),
                                    OperationDefinition(),
                                ]
                            )
                        ],
                        # // Instantiates FHIR protocol or definition
                        "instantiatesUri": [
                            "<uri>"
                        ],  # // Instantiates external protocol or definition
                        "code": CodeableConcept(),  # // Detail type of activity
                        "reasonCode": [CodeableConcept()],
                        # // Why activity should be done or why activity was prohibited
                        "reasonReference": [
                            random.choice(
                                [
                                    Condition(),
                                    Observation(),
                                    DiagnosticReport(),
                                    DocumentReference(),
                                ]
                            )
                        ],
                        "goal": [Goal()],
                        "status": random.choice(
                            [
                                "not-started",
                                "scheduled",
                                "in-progress",
                                "on-hold",
                                "completed",
                                "cancelled",
                                "stopped",
                                "unknown",
                                "entered-in-error",
                            ]
                        ),
                        "statusReason": CodeableConcept(),
                        "doNotPerform": random.choice([True, False]),
                        "scheduledTiming": Timing(),
                        "scheduledPeriod": Period(),
                        "scheduledString": "<string>",
                        "location": Location(),
                        "performer": [
                            random.choice(
                                [
                                    Practitioner(),
                                    PractitionerRole(),
                                    Organization(),
                                    RelatedPerson(),
                                    Patient(),
                                    CareTeam(),
                                    HealthcareService(),
                                    Device(),
                                ]
                            )
                        ],
                        "productCodeableConcept": CodeableConcept,
                        "productReference": random.choice([Medication(), Substance()]),
                        "dailyAmount": SimpleQuantity(),
                        "quantity": SimpleQuantity(),
                        "description": "<string>",
                    },
                }
            ],
            "note": [Annotation()],
        }

        return template


class DiagnositcReport:
    def __init__(self, entries_number):
        self.entries_number = int(entries_number) - 1
        self.fake_person = Person("en")
        self.fake_businees = Finance("en")
        self.address = addre("en")

    def hl7_schema(self):
        schema = {
            "resourceType": "DiagnosticReport",
            "identifier": f"{string_generator.bothify(text='?#?#?#?#?#')}",
            # "basedOn": random.choice(
            #     [CarePlan().schema, ImmunizationRecommendation().schema, MedicationRequest().schema,
            #      NutritionOrder().schema, ServiceRequest().schema]),
            # "status": random.choice(["registered", "partial", "preliminary", "final"]),
            # "category": [CodeableConcept().schema],
            # "code": CodeableConcept().schema,
            # "subject": random.choice([Patient().schema, Group().schema, Device().schema, Location().schema]),
            # "encounter": Encounter().schema,
            # "effectiveDateTime": datetime.now().timestamp(),
            # "effectivePeriod": Period(),
            # "issued": "<instant>",  # // DateTime this version was made
            # "performer": [random.choice(
            #     [Practitioner().schema, PractitionerRole().schema, Organization().schema, CareTeam().schema])],
            # // Responsible Diagnostic Service
            # "resultsInterpreter": [random.choice(
            #     [Practitioner().schema, PractitionerRole().schema, Organization().schema, CareTeam().schema])],
            # // Primary result interpreter
            # "specimen": [Specimen().schema],  # // Specimens this report is based on
            # "result": [Observation().schema],  # // Observations
            # "imagingStudy": [ImagingStudy().schema],
            # // Reference to full details of imaging associated with the diagnostic report
            # "conclusion": "<string>",  # // Clinical conclusion (interpretation) of test results
            # "conclusionCode": [{CodeableConcept}],  # // Codes for the clinical conclusion of test results
            # "presentedForm": [{Attachment}]  # // Entire report as issued
        }
        return schema

    def generate_talend_entries(self):
        patients_list = [Patient().schema() for _ in range(self.entries_number)]
        locations_list = [Location().schema() for _ in range(self.entries_number)]
        diagnostic_reports_list = [
            self.hl7_schema() for _ in range(self.entries_number)
        ]
        encounters_list = [Encounter().schema() for _ in range(self.entries_number)]
        observations_list = [Observation().schema() for _ in range(self.entries_number)]
        organizations_list = [
            Organization().schema() for _ in range(self.entries_number)
        ]

        self.json(
            dateframe=pd.DataFrame(patients_list, columns=patients_list[0].keys()),
            filename="patiens",
        )
        self.json(
            dateframe=pd.DataFrame(locations_list, columns=locations_list[0].keys()),
            filename="locations",
        )
        self.json(
            dateframe=pd.DataFrame(
                diagnostic_reports_list, columns=diagnostic_reports_list[0].keys()
            ),
            filename="diagnostic_reports_hl7",
        )
        self.json(
            dateframe=pd.DataFrame(encounters_list, columns=encounters_list[0].keys()),
            filename="encounters",
        )
        self.json(
            dateframe=pd.DataFrame(
                observations_list, columns=observations_list[0].keys()
            ),
            filename="observations",
        )
        self.json(
            dateframe=pd.DataFrame(
                organizations_list, columns=organizations_list[0].keys()
            ),
            filename="organizations",
        )

        schema_talend = {
            "TEST_ID": [
                diagnostic_report["identifier"]
                for diagnostic_report in diagnostic_reports_list
            ],  # DIAGNOSTICREPORT.identifier
            "MRN": [
                patient["identifier"] for patient in patients_list
            ],  # PATIENT.identifier
            "TEST_SITE_ID": [
                location["identifier"] for location in locations_list
            ],  # LOCATION.identifier
            "DATE_ADMINISTERED": [
                encounter["period"]["end"] for encounter in encounters_list
            ],  # ENCOUNTER.period.end
            "DATE_COMMUNICATED": [
                diagnostic_report["effectiveDateTime"]
                for diagnostic_report in diagnostic_reports_list
            ],  # DIAGNOSTICREPORT.effective.effectiveDateTime
            "DATE_REPORTED": [
                diagnostic_report["effectiveDateTime"]
                for diagnostic_report in diagnostic_reports_list
            ],  # DIAGNOSTICREPORT.effective.effectiveDateTime
            "RESULT_VALUE": [
                observation["valueString"] for observation in observations_list
            ],  # OBSERVATION.value.valueString
            "AGE": [
                random.randint(10, 100) for _ in patients_list
            ],  # DATEDIFF(DATE_ADMINISTERED,PATIENT.birthDate)
            "TEST_SITE_ZIP_CODE": [
                organization["address"][-1]["postalCode"]
                for organization in organizations_list
            ],  # ORGANIZATION.address[0].postalCode
            "PATIENT_ZIP_CODE": [
                patient["address"][-1]["postalCode"] for patient in patients_list
            ],  # PATIENT.address[0].postalCode
            "LAB_NAME": [
                organization["name"] for organization in organizations_list
            ],  # ORGANIZATION.name
            "LOCATION_CODE": [
                f"{location['address']['line']} {location['address']['city']} {location['address']['state']} {location['address']['postalCode']}"
                for location in locations_list
            ],
            # String.join(" ",LOCATION.address.line___)+" "+LOCATION.address.city + " "+LOCATION.address.state + " " + LOCATION.address.zip
            "REGION_CODE": [
                location["address"]["state"] for location in locations_list
            ],  # LOCATION.address.state
            "PATIENT_TYPE": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "SCHOOL_SCHEDULE": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "RACE": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "ETHNICITY": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "UNDERSERVED": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "TEST_SITE_FIPS": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "PATIENT_FIPS": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "VACCINATED": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "VARIANT": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "ASYMPTOMATIC": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "COUGH": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "DECREASED_SMELL": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "FEVER": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "MUSCLE_ACHES": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "SHORTNESS_OF_BREATH": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "SORE_THROAT": ["" for _ in range(self.entries_number)],  # [EMPTY]
            "TEST_TYPE": ["" for _ in range(self.entries_number)],  # [EMPTY]
        }
        return pd.DataFrame(schema_talend, columns=schema_talend.keys())

    def json(self, dateframe, filepath=None, filename=None):
        now = datetime.now()
        filepath = (
            filepath
            if filepath
            else Path(f"{Path.cwd()}/{now.year}/{now.month}/{now.day}")
        )
        Path(filepath).mkdir(exist_ok=True, parents=True)

        filename = (
            f"{filepath}/mock_{filename}_sample_{int(now.timestamp())}.json"
            if filename
            else f"{filepath}/mock_diagnostic_report_sample_{int(now.timestamp())}.json"
        )
        dateframe.to_json(filename, orient="records")
        return filename

    def s3(self, first_bucket_name):
        assert self.verify_aws_keys()
        s3_resource = boto3.resource(
            "s3",
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            aws_session_token=os.environ["AWS_SESSION_TOKEN"],
        )

        generated_csv_file_path = self.json(self.generate_talend_entries())

        s3_resource.Bucket(first_bucket_name).upload_file(
            Filename=generated_csv_file_path, Key=generated_csv_file_path.split("/")[-1]
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
    # start = time.time()
    # dr = DiagnositcReport(1000)
    # entries = dr.generate_talend_entries()
    # data = dr.json(entries)
    #
    # end = time.time() - start
    a = DiagnosticReport_native
    b = 1
