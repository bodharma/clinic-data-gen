import pytest
from httpx import AsyncClient, ASGITransport
from app import app
from flaky import flaky

max_runs = 2
base_url = "http://localhost"


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.get("/")
    assert resp.status_code == 200


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
async def test_create_csv():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.get(
            "/members/csv/?members_num=1&relationships=false&segments=1"
        )
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/csv" in resp.headers["content-type"]


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
async def test_create_edi():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.get(
            "/members/edi/?members_num=1&relationships=false&segments=1"
        )
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/plain" in resp.headers["content-type"]


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
async def test_create_edi_with_specified_data():
    data = {
        "claim": {
            "diagnosis_code": "TEST_diagnose",
            "service_code": "TEST_service",
            "procedure_code": "TEST_procedure",
            "service_price": 111.1,
            "procedure_price": 888.9,
        },
        "subscriber": {
            "group_id": "TEST_group",
            "first_name": "TEST_first",
            "last_name": "TEST_last",
            "member_number": "TEST_member_number",
        },
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.post(
            "/members/edi?segments_num=1&members_num=1&relationships=false", json=data
        )
        # TODO: here we need add input, output data assertion, to verify data is valid
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/plain" in resp.headers["content-type"]


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
async def test_create_edi_with_empty_data():
    data = {}
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.post(
            "/members/edi?segments_num=1&members_num=1&relationships=false", json=data
        )
        # TODO: here we need add input, output data assertion, to verify data is valid
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/plain" in resp.headers["content-type"]


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        pytest.param({"provider_group_count": 1}),
        pytest.param(
            {"provider_group_count": 1, "facilities_count": 1, "providers_count": 1}
        ),
        pytest.param({"provider_group_count": 1}),
        pytest.param(
            {"provider_group_count": 1, "facilities_count": 1, "providers_count": 1}
        ),
    ],
)
async def test_create_provider_group(data):
    # TODO: add mock not to be dependent on some other service
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.post("/provider_group/", json=data)
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/csv" in resp.headers["content-type"]


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {"sponsors_count": 1},
        {"sponsors_count": 1, "plans_count": 1},
        {"sponsors_count": 1},
        {"sponsors_count": 1, "plans_count": 1},
    ],
)
async def test_create_sponsor(data):
    # TODO: add mock not to be dependent on some other service
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.post("/sponsor/", json=data)
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/csv" in resp.headers["content-type"]


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
@pytest.mark.parametrize("data", [{"members_count": 1}])
async def test_create_member(data):
    # TODO: add mock not to be dependent on some other service
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.post("/member/", json=data)
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/csv" in resp.headers["content-type"]


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {"entries": 1, "download_file_extension": "csv"},
        {"entries": 1, "download_file_extension": "json"},
        {"entries": 1, "download_file_extension": "jsonlike"},
        {
            "entries": 1,
            "download_file_extension": "jsonlike",
            "banana_email": True,
            "patient_last_name": "Vlob",
            "patient_first_name": "Lob",
            "patient_dob": "20010101",
            "patient_phone": "+1986573617581",
            "patient_email": "banana@banana.com",
        },
    ],
)
async def test_create_onsite_data(data):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.post("/databus/testing/", json=data)
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    if data["download_file_extension"] == "jsonlike":
        assert "application/octet-stream" in resp.headers["content-type"]
    else:
        assert data["download_file_extension"] in resp.headers["content-type"]
    # TODO: add checking if response data equal to request data


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
async def test_create_vaccine_patient_data():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.get("/vaccine_patients/1")
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/csv" in resp.headers["content-type"]


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
async def test_create_databus_data():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.post(
            "/databus/vaccines/",
            json={"entries": 10, "dose_number": 1, "vaccine_type": "Pfizer"},
        )
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/json" in resp.headers["content-type"]


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {"members_count": 1, "load_type": "F", "optional_fields": True},
        {"members_count": 5, "load_type": "F", "optional_fields": False},
        {"members_count": 10, "load_type": "I", "optional_fields": True},
        {"members_count": 15, "load_type": "I", "optional_fields": False},
    ],
)
async def test_rt_eligibility_data(data):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.post("/rt_eligibility/", json=data)
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/csv" in resp.headers["content-type"]


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {
            "load_type": "F",
            "optional_fields": False,
            "claim_level_record_count": 1,
            "claim_line_level_record_count": 0,
        },
        {
            "load_type": "F",
            "optional_fields": False,
            "claim_level_record_count": 5,
            "claim_line_level_record_count": 0,
        },
        {
            "load_type": "F",
            "optional_fields": False,
            "claim_level_record_count": 5,
            "claim_line_level_record_count": 5,
        },
        {
            "load_type": "I",
            "optional_fields": False,
            "claim_level_record_count": 1,
            "claim_line_level_record_count": 0,
        },
        {
            "load_type": "I",
            "optional_fields": False,
            "claim_level_record_count": 5,
            "claim_line_level_record_count": 0,
        },
        {
            "load_type": "I",
            "optional_fields": False,
            "claim_level_record_count": 5,
            "claim_line_level_record_count": 5,
        },
        {
            "load_type": "F",
            "optional_fields": True,
            "claim_level_record_count": 1,
            "claim_line_level_record_count": 0,
        },
        {
            "load_type": "F",
            "optional_fields": True,
            "claim_level_record_count": 5,
            "claim_line_level_record_count": 0,
        },
        {
            "load_type": "F",
            "optional_fields": True,
            "claim_level_record_count": 5,
            "claim_line_level_record_count": 5,
        },
        {
            "load_type": "I",
            "optional_fields": True,
            "claim_level_record_count": 1,
            "claim_line_level_record_count": 0,
        },
        {
            "load_type": "I",
            "optional_fields": True,
            "claim_level_record_count": 5,
            "claim_line_level_record_count": 0,
        },
        {
            "load_type": "I",
            "optional_fields": True,
            "claim_level_record_count": 5,
            "claim_line_level_record_count": 5,
        },
    ],
)
async def test_rt_claim_data(data):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.post("/rt_claim_data/", json=data)
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/csv" in resp.headers["content-type"]
    assert (
        len(resp.text.split("\n"))
        == data["claim_level_record_count"] * 2
        + data["claim_line_level_record_count"] * 2 * data["claim_level_record_count"]
        + 3
    )


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {"members_count": 1, "load_type": "F", "optional_fields": True},
        {"members_count": 5, "load_type": "F", "optional_fields": True},
        {"members_count": 1, "load_type": "H", "optional_fields": True},
        {"members_count": 5, "load_type": "H", "optional_fields": True},
        {"members_count": 1, "load_type": "F", "optional_fields": False},
        {"members_count": 5, "load_type": "F", "optional_fields": False},
        {"members_count": 1, "load_type": "H", "optional_fields": False},
        {"members_count": 5, "load_type": "H", "optional_fields": False},
    ],
)
async def test_rt_eligibility_data(data):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.post("/rt_plan_benefit_data/", json=data)
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/csv" in resp.headers["content-type"]
    assert data["members_count"] + 3 == len(resp.text.split("\n"))


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {"members_count": 1, "load_type": "F", "optional_fields": True},
        {"members_count": 5, "load_type": "F", "optional_fields": True},
        {"members_count": 1, "load_type": "I", "optional_fields": True},
        {"members_count": 5, "load_type": "I", "optional_fields": True},
        {"members_count": 1, "load_type": "F", "optional_fields": False},
        {"members_count": 5, "load_type": "F", "optional_fields": False},
        {"members_count": 1, "load_type": "I", "optional_fields": False},
        {"members_count": 5, "load_type": "I", "optional_fields": False},
    ],
)
async def test_rt_individual_usage_benefit_data(data):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.post("/rt_individual_usage_benefit_data/", json=data)
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/csv" in resp.headers["content-type"]
    assert data["members_count"] + 3 == len(resp.text.split("\n"))


@flaky(max_runs=max_runs)
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "data",
    [
        {"members_count": 1, "load_type": "F", "optional_fields": True},
        {"members_count": 5, "load_type": "F", "optional_fields": True},
        {"members_count": 1, "load_type": "H", "optional_fields": True},
        {"members_count": 5, "load_type": "H", "optional_fields": True},
        {"members_count": 1, "load_type": "F", "optional_fields": False},
        {"members_count": 5, "load_type": "F", "optional_fields": False},
        {"members_count": 1, "load_type": "H", "optional_fields": False},
        {"members_count": 5, "load_type": "H", "optional_fields": False},
    ],
)
async def test_rt_plan_benefit_data(data):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as ac:
        resp = await ac.post("/rt_standard_benefit_entity_data/", json=data)
    assert (
        resp.status_code == 200
    ), f"Assertion error: status code: {resp.status_code} | content: {resp.content}"
    assert "text/csv" in resp.headers["content-type"]
    assert data["members_count"] + 3 == len(resp.text.split("\n"))
