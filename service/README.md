# PSD-status service

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Flask Application and API to monitor information systems.

## Table of Contents

<!-- toc -->
- [Requirements for Development](#requirements-for-development-1)
- [Getting Started](#getting-started-1)
  - [Configuring the Environment](#configuring-the-environment-1)
  - [Setup Steps](#setup-steps-1)
- [Running](#running-1)
- [Testing](#testing-1)
  - [Testing Requirements](#testing-requirements)
  - [Running Tests](#running-tests)
- [Routes](#routes)
- [Scheduled Jobs](#scheduled-jobs)
- [Miscellaneous](#miscellaneous)
  - [Type Checking](#type-checking)

<!-- tocstop -->

### Requirements for Development

The following tools are required for development:

- python (use pyenv or something similar to install the python version specified in the `Pipfile`)
- MySQL (recommended 5.7, if using later versions you may need some schema tweaks)

### Getting Started

#### Configuring the Environment

Non-sensitive environment variables can be stored in the `.flaskenv` file. These will be read
by the `python-dotenv` library when the app is run. Here you can specify the database connection information.

#### Setup Steps

- Use pyenv or something similar to install the version of python
  defined in the `Pipfile`:

      brew install pyenv
      pyenv install <python_version>

- Use pipenv to install the required python packages for the application and development:

      pipenv install --dev

- Create the schema and tables:

      Enter a local mysql session and paste the contents of `app/db/schema.sql`
      You may also want to create the default test schema at this point which can be done by running
      `CREATE DATABASE psd_status_test;`

- Setup dummy data:

      We recommend you setup dummy data using the `dummy_data.py` script
      This can be achieved by running this from the service folder:

      pipenv shell
      
      python3 ./dummmy_data.py


### Running

1. Enter the python virtual environment using:

       pipenv shell

1. Run the app using:

       flask run

`Note:` The default login is admin/admin


### Testing

#### Testing Requirements

Verify the credentials for the required databases in the test settings file `tests/conftest`.
You may need to create a schema such as `psd_status_test`.
Flask SQL-Alchemy handles the creation of the tables and data during testing run time.

#### Running Tests

A wrapper is provided with pipenv (look in the Pipfile's `[scripts]` block for more information):

    pipenv run test

## Routes

The service has the following routes:

|     Endpoint                         |     Methods     |     Rule                                        |
| ------------------------------------ | --------------- | ----------------------------------------------- |
| login                                | POST            | `/login`                                        |
| monitors                             | GET             | `/monitors`                                     |
| monitor                              | POST            | `/monitor`                                      |
| protocols                            | GET             | `/protocols`                                    |
| http_records                         | GET             | `/http_records?monitor_ids="1,2,3"`             |

## Scheduled Jobs

This service utilises flask-apscheduler to run asynchronous background jobs in order to monitor multiple
information systems without interfeering with one another.
For development purposes the scheduled jobs monitor public websites so an internet connection is needed.
`In the future` the jobs will be stubbed so real websites dont need to be used and development can be done
without internet access.

## Miscellaneous

### Formatting and lint

Formatting and linting is done with black and flake8, to run them, execute:

        pipenv run black .
        pipenv run flake8
