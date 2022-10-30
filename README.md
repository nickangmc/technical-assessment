# Technical Assessment Attempt

This application contains Django/Python with MySQL, Redis & Celery all running in Docker.

## Overview of the solution

- Designed to meet the assessment requirements

  1. Django, Python is used as the backend code.
  1. MySQL is used as the database.
  1. Included unit tests for the API endpoints.
  1. Created APIs based on the 3 scenarios required.

- Use of Docker & Docker compose for the app stack

  For ease of setup, development, & deployment if needed. Live-reload/Hot module reload (HMR) is supported during development for this docker stack setup as well. The template production docker compose configuration can be found in `production.yml` file, it is however not ready yet to be used for any production purposes based on the requirements in this assessment.

- Use of Django REST Framework (DRF)

  [Django REST Framework](https://www.django-rest-framework.org/) (DRF) is used on top of Django to create REST APIs. DRF simplifies the API development by providing useful abstractions (e.g. serializers, viewsets, etc.) to reduce code complexities and redundancy.

  Though there might be some learning curves for newcomers from other frameworks/languages.

## Files & Folders structure

- `envs/`: Contains the environment variables for all environments (e.g. _local, staging & etc._).
- `assessment/`: Contains all backend application logic (e.g. _Django apps, models, test & etc._).
- `compose/`: Contains docker & docker compose related files (e.g. _Dockerfile_)
- `config/`: Contains `settings.py` for different environments, routes/urls config, & the web server config - `wsgi.py`.
- `requirements/`: Contains the lists of package dependencies for different environments.
- `local.yml`, `production.yml`: Docker compose config files for different environements.

The main API logic/functions created for this assessment are contained in the folder here:

- `assessment/items/`

  - `api/`: Contains the functions that handle API requests.

    - `serializers.py`: Contains serializers to help with input validation, response serialization, & object create/update logic. More information on the functions of `serializers` can be found on [DRF guides](https://www.django-rest-framework.org/api-guide/serializers/).
    - `views.py`: Acts as the controllers for the API in this `item` app/module.

  - `migrations/`: Contains all the migration files for this `item` app/module.
  - `tests/`: Contains all the unit tests for this `item` module.
  - `models.py`: Defines all the models in this module.
  - `conftest.py`: Defines the common fixtures/functions for unit tests in this module.

## API endpoints

- `POST /api/items/` - Scenario/Task #1
- `GET /api/items/` - Scenario/Task #2
- `GET /api/items/category/` - Scenario/Task #3

## Local development & setup instructions

Make sure you already have Docker & Docker Compose installed in your terminal.

### Initial setup

Build the Docker stack:

```
$ docker compose -f local.yml build
```

### Run the app stack

```
$ docker compose -f local.yml up
```

You might need to wait awhile for Django to complete the initial migrations (on first launch only). Otherwise, use the following command if you want to run the initial migrations manually:

```
$ docker compose -f local.yml run --rm django python manage.py migrate
```

### Run tests with pytest

```
$ docker compose -f local.yml run --rm django pytest
```

### Check test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```
$ docker compose -f local.yml run --rm django coverage run -m pytest
$ docker compose -f local.yml run --rm django coverage html
$ open htmlcov/index.html
```

### Credits

This project is initialized using [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django). Therefore, it comes with many useful features (e.g. user authentication), even though some are not needed in this project. As a result, it closely follows best practices/standards outlined by Cookiecutter in project structure (e.g. `.envs/` & `config/`) and docker configuration.
