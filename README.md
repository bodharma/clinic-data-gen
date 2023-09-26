### Whoami
I am repo, which is used for test data generation.

I am just helper to the one who needs it.

### Technical info
#### Language
Python >=3.9

> Code static analysis locally and on GitHub is performed by [pre-commit](https://pre-commit.com/)


> Code static analysis locally and on GitHub is performed by [pre-commit](https://pre-commit.com/)


#### Libs
Linters:
- [black](https://black.readthedocs.io/en/stable/)
- [bandit](https://github.com/PyCQA/bandit)
- [pre-commit](https://github.com/pre-commit)

Fake data libs:
- [mimesis](https://pypi.org/project/mimesis/)
- [random](https://docs.python.org/3/library/random.html)

API servers:
- [fastapi](https://fastapi.tiangolo.com)

API requests:
- [httpx](https://www.python-httpx.org/)

Async`er:
- [asyncio](https://docs.python.org/3/library/asyncio.html)


### Installation
#### For Development
```shell
pip install -r requirements.txt
pytest .
```

#### Installing the Git Hook scripts
**Run**

`pre-commit install`

This will set up the git hook scripts and should show the following output in your terminal:

`pre-commit installed at .git/hooks/pre-commit`

Now you’ll be able to implicitly or explicitly run the hooks before each commit.

##### File explanations

- [addresses](addresses) - contains real state addresses for making vaccine candidate registration valid
- [generator_helpers](generator_helpers) - helper functions to make data generation more flexible
- [hl7](hl7) - contains schemas and generators for FHIR v4
- [templates](templates) - contains templates/scheams that are used for test data generation
- [tests](tests) - contains tests for some of generators and fastapi server
- [generate_edi.py](generate_edi.py) - generates edi files, which are used by Raghu and his team.
- [generate_onsite_data.py](generate_testing_data.py) - generates onsite data , used for Jovannie and her team and on onsite pipeline
- [generate_protobuf_data.py](generate_protobuf_data.py) - generates data for service layer api endpoints, protobuf is the same schema service(service layer) uses for storing data into DB
- [generate_raw_data.py](generate_raw_data.py) - generates different data for 1minute needs, here we store requests which are used not too often
- [generate_vaccine_registration_data.py](ragister_vaccine_candidates.py) - used to create registrations on API side for APPS team
- [app.py](app.py) - is a [fastapi](https://fastapi.tiangolo.com/tutorial/first-steps/) app, that gives us an ability to create some fake data from browser
- [api_connector.py](api_connector.py) - used to connect and preparee test data for service api endpoints

#### Docker setup
If you want to test fastapi locally, just use:
```shell
docker build -t gen .
docker run -p 80:80 gen
```

#### API Docs

Accessible on:
- swagger - [0.0.0.0/docs](0.0.0.0/docs)
- openapi - [0.0.0.0/redocs](0.0.0.0/redocs)


#### Personal access tokens

Some features required [Personal access tokens](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token), make sure it was generated in [settings](https://github.com/settings/tokens) and added in environment variables as `GHA_AUTOMATION_PAT`
