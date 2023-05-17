# Resola challenge
This repository contains the solution for the Resola challenge including the system design and the code.

## Problem
TODO

My Assumptions:
- A tenant is more like a workspace which contains multiple resources.
- User can be in multiple tenants at the same time.
- Each resource is only in one single tenant.
- Each resource would have multiple files. Each file can only belong to one resource.
- User can upload files to resources in the tenant that they are in.


## Features at a glance
- Upload a file to the system
- Retrieve a file from the system
- Delete a file from the system
- List all files in the system

## Documentation

### Introduction
- [python-3.10](https://www.python.org/) for building backend application
- [Django 4.2.1](https://www.djangoproject.com/) for building web application
- [django-rest-framework 3.14.0](https://www.django-rest-framework.org/) for building RESTful API
- [django-storages 1.13.2](https://django-storages.readthedocs.io/en/latest/) for managing file in cloud storage
- [PostgreSQL 14.8]() for storing data
- [pytest]() for testing
- [Docker](https://www.docker.com/) for containerization and deployment
- [poetry](https://python-poetry.org/) for dependency management
- [Makefile](#) for automating tasks and centralizing commands
- [Flake8](#) for linting
- [Black](#) for formatting
- [isort](#) for sorting imports
- [mypy](#) for type checking
- [safety](#) for checking security vulnerabilities in dependencies
- [Github Action](#) for CI/CD
- [Domain Design Driven (DDD)](#) for designing the Django apps

### Installation
TODO

### Usage
TODO
Test api
Deploy on local
Run test
Run seeds

### API Documentation
TODO

### System designs
Check out the [system design documentation](diagrams/system/README.md).