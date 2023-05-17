# Resola challenge
This repository contains the solution for the Resola challenge including the system design and the code.

## Problem
As a user, I want to be able to upload files to a system, so that I can retrieve them later.
Each file must be uploaded by authorized user and it should be associated with a particular resource

Look at the requirements [link](https://gist.github.com/evert0n/d86eec2e5dfc5ac2c55db3b0c39950a9). I see there are 4 main objects in this system
- User
- Tenant
- Resource
- File

I already had some concerns about the relationships between these objects but unfortunately, 
I got no answer at all after sending several emails. 
I guess he is busy on something. So, to not be blocked, I decided to go with this assumption:
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

### Live Usage
TODO AFTER DEPLOY TO AWS

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
- [JWT](#) for authentication

### Installation on local machine
#### Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

- This guidance has been tested on MacOS only

#### Steps
1. Clone the repository
```shell
git clone git@github.com:vanhiepdam/resola.git

cd resola
```

2. Create a `.env` file in the root directory of the project and fill in the environment variables
```shell
cp .env.example .env
vim .env

SECRET_KEY=3a677a%h+t_*kwr)
DEBUG=true
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://localhost:8000
DATABASE_NAME=resola
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME=YOUR_AWS_STORAGE_BUCKET_NAME
```

3. Build the docker image
```shell
make build
```

4. Run the docker container
```shell
make up
```

5. Checkout the backend server at [http://localhost:8000](http://localhost:8000)

6. Meanwhile spawning up the backend server, it already create a super admin for you by default. To login into the admin site, you can use the following credentials:
```
account/password: admin/admin
```

### API Documentation
After deploying successfully, you can access the API documentation at [http://localhost:8000/api-doc](http://localhost:8000/api-doc)

1. List files
- Endpoint: GET `/api/v1/files`
- Description: List all files in the system that were uploaded by the current user

2. Upload a file
- Endpoint: POST `/api/v1/files`
- Upload file to a specific resource and upload to S3. System will validate if user is in the same tenant with the resource or not. If not, raise HTTP 403 error

4. Retrieve a file
- Endpoint: GET `/api/v1/files/{file_id}`
- Description: Retrieve a file by its id. If the file does not exist or was not uploaded by the current user, raise HTTP 404 error

5. Delete a file
- Endpoint: DELETE `/api/v1/files/{file_id}`
- Description: Delete a file by its id. If the file does not exist or was not uploaded by the current user, raise HTTP 404 error. 
System will also remove the file associated with the file in S3

### Deployment
This project was set up to be deployed on an AWS EC2 instance using Docker and Docker Compose.

The process of deployment is automated by Github Action
1. Create a new branch for new feature
2. Push the code to the new branch
3. Create a pull request to merge the new branch to the main branch. CI will be triggered automatically
4. After the pull request is approved, merge it to the main branch. CD will be triggered automatically

### System designs
Check out the [system design documentation](diagrams/system/README.md).

### Testing
1. Open shell terminal in the backend docker container
```shell
docker exec -it /bin/sh app
```

2. Run test
```shell
pytest
```
