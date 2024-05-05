# Resulta Technical Challenge
This repository contains an implementation of Events API according to the **ACME Sports** specification and means to test it.
## Prerequisites
 - Docker
 - GNU make
 - Python 3.10+
 - Hurl - _optional_
## HOWTO
From the root directory run:
 - `make help` to see the list of available targets
 - `make build` to build Events API and the 3rd party API stub images
 - `make up` to build and start the containers
 - `make test` Hurl tests specified in `events-api.hurl`
 - `make down` to stop the containers
## What's inside
`evens-api` is the home directory of the Events API implementation and has the following structure:
```md
events-api
├── app
│   ├── api - API routers (aka controller layer)
│   │   ├── events.py
│   │   ├── heartbeat.py
│   │   └── __init__.py
│   ├── depends.py - dependency injection file
│   ├── __init__.py
│   ├── main.py - main application class
│   ├── middlewares - custom middlewares
│   │   ├── __init__.py
│   │   └── request_logger.py
│   ├── schemas - schema classes for all object models
│   │   ├── error.py
│   │   ├── events_request.py
│   │   ├── events_response.py
│   │   ├── heartbeat_response.py
│   │   ├── __init__.py
│   │   ├── scoreboard.py
│   │   └── team_rankings.py
│   ├── service - service layer
│   │   ├── events_service.py
│   │   └── __init__.py
│   ├── settings.py - reading configuration from environment variables
│   └── utils
│       ├── exceptions - custom exception classes
│       │   └── api_exception.py
│       └── __init__.py
├── Dockerfile - Events API image specification
├── requirements.txt - Python requirements file for pip
└── tests - automated tests
    ├── conftest.py - pytest fixture for integration tests
    ├── __init__.py
    ├── test_app.py - integration test example
    ├── test_events_service.py - service unit tests
    └── test_settings.py - a copy of settings file for test purposes

```
## Links
 - [Thoughts and Considerations document](./docs/README.md) explains some key decisions made, possible shortcomings of the current implementation and ways to improve it
 - [Hurl](https://hurl.dev/) - a command line API testing tool that could be a good lightweight replacement for Postman, JMeter etc.