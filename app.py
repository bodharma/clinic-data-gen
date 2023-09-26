import uvicorn
from fastapi import FastAPI, HTTPException
from generate_raw_data import MemberRoster, VaccinedPatient
from generate_edi import EDI
from datetime import datetime
from pathlib import Path
from fastapi.responses import FileResponse
from api_connector import (
    create_provider_group_with_providers_and_facilities,
    create_sponsor_with_plan,
    create_member,
)
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from generate_testing_data import TestingData
from generate_rt_claim_data import RTClaimData
from generate_rt_eligibility_data import RTEligibbility
from generate_rt_standart_benefit_entity_data import RTStandardBenefitEntityData
from generate_rt_individual_usage_benefit_data import RTIndividualUsageBenefitData
from generate_rt_plan_benefit_data import RTPlanBenefitData
from ragister_vaccine_candidates import VaccineCandidate
from generate_vaccine_data import Encounters
from generator_helpers.data_converter import (
    convert_csv_to_jsonlike,
    convert_csv_to_json,
    convert_json_to_jsonlike,
)


class ProviderGroupData(BaseModel):
    provider_group_count: int
    url: Optional[str] = "https://localhost:8000"
    api_version: Optional[str] = "api/v3"
    facilities_count: Optional[int]
    providers_count: Optional[int]


class SponsorData(BaseModel):
    sponsors_count: int
    url: Optional[str] = "https://localhost:8000"
    api_version: Optional[str] = "api/v3"
    plans_count: Optional[int]
    members_ids_list: Optional[list]


class MemberData(BaseModel):
    members_count: int = 1
    url: Optional[str] = "https://localhost:8000"
    api_version: Optional[str] = "api/v3"


class ClaimData(BaseModel):
    diagnosis_code: Optional[str]
    service_code: Optional[str]
    procedure_code: Optional[str]
    service_price: Optional[float]
    procedure_price: Optional[float]


class SubscriberData(BaseModel):
    group_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    member_number: Optional[str]


class EdiData(BaseModel):
    claim: Optional[ClaimData]
    subscriber: Optional[SubscriberData]


class VaccineData(BaseModel):
    vaccine_type: Annotated[
        str,
        Field(
            description="Select one of following types: Pfizer, Moderna, Janssen, AstraZeneca, Novavax"
        ),
    ]
    dose_number: Annotated[
        int, Field(description="Select one of following options: 1, 2")
    ]
    entries: int


class RTEligibility(BaseModel):
    members_count: int = 1
    load_type: str = "F"
    optional_fields: bool = False


class RTClaim(BaseModel):
    load_type: str
    optional_fields: bool
    claim_level_record_count: int = 1
    claim_line_level_record_count: int


class RTStandardBenefitEntity(BaseModel):
    members_count: int = 1
    load_type: str
    optional_fields: bool


class RTPlanBenefit(BaseModel):
    members_count: int = 1
    load_type: str
    optional_fields: bool


class RTIndividualUsageBenefit(BaseModel):
    members_count: int
    load_type: str
    optional_fields: bool


class TestingDataModel(BaseModel):
    entries: int = 1
    s3_upload: Optional[bool] = False
    s3_file_extension: Annotated[
        str, Field(description="Select one of following types: jsonlike, json, csv")
    ] = "jsonlike"
    download_file_extension: Annotated[
        str, Field(description="Select one of following types: jsonlike, json, csv")
    ] = "csv"
    s3_bucket_name: Optional[str] = "dev-de-phi-backup"
    banana_email: Optional[bool]
    patient_last_name: Optional[str]
    patient_first_name: Optional[str]
    patient_dob: Optional[str]
    patient_phone: Optional[str]
    patient_email: Optional[str]


app = FastAPI()


@app.get("/")
async def root():
    """check API status"""
    return {"status": "OK"}


@app.get("/members/{data_format}/", status_code=200)
async def get_members_csv(data_format, members_num: int = 1, segments: int = 1):
    """
    create & download csv/edi file using:
    GET http://0.0.0.0:8000/members/<csv/edi>/?members_num=<10>&relationship=<False/True>&segments=<1>
    """
    now = datetime.now()
    file_path = f"/tmp/data/{now.year}/{now.month}/{now.day}/{now.hour}/"
    Path(file_path).mkdir(parents=True, exist_ok=True)
    mmbr = MemberRoster()
    members_data = mmbr.generate(members_num)

    if data_format == "csv":
        filename = f"{file_path}{now.hour}_{now.minute}_{now.second}.csv"
        mmbr.save_to_csv(filename=filename, data_list=members_data)
    elif data_format == "edi":
        edi = EDI()
        edi_doc = edi.generate(segments, members_data)
        filename = edi.writeEDIDocument(edi_doc, path=file_path)
    else:
        raise HTTPException(status_code=404, detail=f"Format: {data_format} not found")

    if Path(filename).exists():
        return FileResponse(
            path=filename,
            filename=filename.split("/")[-1],
            media_type="text/csv" if data_format == "csv" else None,
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {file_path} not found"
        )


@app.post("/members/edi")
async def post_edi_extra_data(edidata: EdiData):
    file_path = create_storage_dir()
    mmbr = MemberRoster()
    members_data = mmbr.generate(members_num=1)

    edi = EDI()
    edi_doc = edi.generate(members_data=members_data, edidata=edidata, segments_num=1)
    filename = edi.writeEDIDocument(edi_doc, path=file_path)
    if Path(filename).exists():
        return FileResponse(path=filename, filename=filename.split("/")[-1])
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {file_path} not found"
        )


@app.post("/provider_group/")
async def post_provider_group(provider_group_data: ProviderGroupData):
    filename = await create_provider_group_with_providers_and_facilities(
        provider_group_data
    )

    if Path(filename).exists():
        return FileResponse(
            path=filename, filename=filename.split("/")[-1], media_type="text/csv"
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {filename} not found"
        )


@app.post("/sponsor/")
async def post_sponsor(sponsor_data: SponsorData):
    filename = await create_sponsor_with_plan(sponsor_data)

    if Path(filename).exists():
        return FileResponse(
            path=filename, filename=filename.split("/")[-1], media_type="text/csv"
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {filename} not found"
        )


@app.post("/member/")
async def post_member(member_data: MemberData):
    filename = await create_member(member_data)

    if Path(filename).exists():
        return FileResponse(
            path=filename, filename=filename.split("/")[-1], media_type="text/csv"
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {filename} not found"
        )


@app.post("/databus/testing/")
async def get_patient_testing_data(testing_data: TestingDataModel):
    media_type = None
    s3_file_path = None

    onsite_handler = TestingData(testing_data)
    if testing_data.download_file_extension == "csv":
        filepath = onsite_handler.csv(filepath=create_storage_dir())
        media_type = "text/csv"
    elif testing_data.download_file_extension == "json":
        filepath = onsite_handler.json(filepath=create_storage_dir())
        media_type = "application/json"
    elif testing_data.download_file_extension == "jsonlike":
        filepath = onsite_handler.json_like(filepath=create_storage_dir())
        media_type = "application/octet-stream"
    else:
        return HTTPException(
            status_code=404,
            detail=f"Incorrect file extension chosen: {testing_data.download_file_extension}",
        )

    if testing_data.s3_upload:
        if testing_data.s3_file_extension == testing_data.download_file_extension:
            s3_file_path = filepath
        elif (
            testing_data.download_file_extension == "csv"
            and testing_data.s3_file_extension == "jsonlike"
        ):
            s3_file_path = convert_csv_to_jsonlike(filepath)
        elif (
            testing_data.download_file_extension == "json"
            and testing_data.s3_file_extension == "jsonlike"
        ):
            s3_file_path = convert_json_to_jsonlike(filepath)
        elif (
            testing_data.download_file_extension == "csv"
            and testing_data.s3_file_extension == "json"
        ):
            s3_file_path = convert_csv_to_json(filepath)
        else:
            s3_file_path = None
            return HTTPException(
                status_code=404,
                detail=f"File extensions usage: local-{testing_data.download_file_extension} | s3-{testing_data.s3_file_extension} is not supported",
            )
        if s3_file_path:
            onsite_handler.s3(testing_data.s3_bucket_name, s3_file_path)

    if Path(filepath).exists():
        return FileResponse(
            path=filepath, filename=filepath.split("/")[-1], media_type=media_type
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {filepath} not found"
        )


@app.get("/vaccine_patients/{entries_number}")
async def vaccine_patients(entries_number):
    filename = VaccinedPatient(entries_number).csv(filepath=create_storage_dir())

    if Path(filename).exists():
        return FileResponse(
            path=filename, filename=filename.split("/")[-1], media_type="text/csv"
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {filename} not found"
        )


@app.get("/register_vaccine_candidate/{candidates_number}")
async def register_vaccine_candidate(candidates_number):
    vaccine_candidate = VaccineCandidate("mdc")
    data_list = vaccine_candidate.generate_data(int(candidates_number))
    vaccine_candidate.register_via_api(data_list)
    filename = vaccine_candidate.save_data_to_csv(
        data_list, filepath=create_storage_dir()
    )
    if Path(filename).exists():
        return FileResponse(
            path=filename, filename=filename.split("/")[-1], media_type="text/csv"
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {filename} not found"
        )


@app.post("/databus/vaccines/")
async def get_patient_vaccine_data(vaccine_data: VaccineData):
    filename = Encounters(
        entries_number=vaccine_data.entries,
        vaccine_type=vaccine_data.vaccine_type,
        dose_number=vaccine_data.dose_number,
    ).json(filepath=create_storage_dir())
    if Path(filename).exists():
        return FileResponse(
            path=filename, filename=filename.split("/")[-1], media_type="text/json"
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {filename} not found"
        )


@app.post("/rt_eligibility/")
async def get_rt_eligibility_data(rt_eligibility: RTEligibility):
    generator = RTEligibbility(
        entries_number=rt_eligibility.members_count,
        load_type=rt_eligibility.load_type,
        optional_fields=rt_eligibility.optional_fields,
    )
    generator.generate_all_schemas()
    filename = generator.schemas_to_file(filepath=create_storage_dir())

    if Path(filename).exists():
        return FileResponse(
            path=filename, filename=filename.split("/")[-1], media_type="text/csv"
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {filename} not found"
        )


@app.post("/rt_claim_data/")
async def get_rt_claim_data(rt_claim: RTClaim):
    generator = RTClaimData(
        load_type=rt_claim.load_type,
        optional_fields=rt_claim.optional_fields,
        claim_level_record_count=rt_claim.claim_level_record_count,
        claim_line_level_record_count=rt_claim.claim_line_level_record_count,
    )
    generator.generate_all_schemas()
    filename = generator.schemas_to_file(filepath=create_storage_dir())

    if Path(filename).exists():
        return FileResponse(
            path=filename, filename=filename.split("/")[-1], media_type="text/csv"
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {filename} not found"
        )


@app.post("/rt_standard_benefit_entity_data/")
async def get_rt_eligibility_data(rt_standard_benefit_entity: RTStandardBenefitEntity):
    generator = RTStandardBenefitEntityData(
        entries_number=rt_standard_benefit_entity.members_count,
        load_type=rt_standard_benefit_entity.load_type,
        optional_fields=rt_standard_benefit_entity.optional_fields,
    )
    generator.generate_all_schemas()
    filename = generator.schemas_to_file(filepath=create_storage_dir())

    if Path(filename).exists():
        return FileResponse(
            path=filename, filename=filename.split("/")[-1], media_type="text/csv"
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {filename} not found"
        )


@app.post("/rt_plan_benefit_data/")
async def get_rt_plan_benefit_data(rt_plan_benefit: RTPlanBenefit):
    generator = RTPlanBenefitData(
        entries_number=rt_plan_benefit.members_count,
        load_type=rt_plan_benefit.load_type,
        optional_fields=rt_plan_benefit.optional_fields,
    )
    generator.generate_all_schemas()
    filename = generator.schemas_to_file(filepath=create_storage_dir())

    if Path(filename).exists():
        return FileResponse(
            path=filename, filename=filename.split("/")[-1], media_type="text/csv"
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {filename} not found"
        )


@app.post("/rt_individual_usage_benefit_data/")
async def get_rt_individual_usage_benefit_data(
    rt_individual_usage_benefit: RTIndividualUsageBenefit
):
    generator = RTIndividualUsageBenefitData(
        entries_number=rt_individual_usage_benefit.members_count,
        load_type=rt_individual_usage_benefit.load_type,
        optional_fields=rt_individual_usage_benefit.optional_fields,
    )
    generator.generate_all_schemas()
    filename = generator.schemas_to_file(filepath=create_storage_dir())

    if Path(filename).exists():
        return FileResponse(
            path=filename, filename=filename.split("/")[-1], media_type="text/csv"
        )
    else:
        raise HTTPException(
            status_code=404, detail=f"File with path: {filename} not found"
        )


def create_storage_dir():
    now = datetime.now()
    file_path = f"/tmp/data/{now.year}/{now.month}/{now.day}/"
    Path(file_path).mkdir(parents=True, exist_ok=True)
    return file_path


if __name__ == "__main__":
    """
    Start me in cli:
    uvicorn app:app --port 80 --host 0.0.0.0
    """
    uvicorn.run(app, host="0.0.0.0", port=5000)
