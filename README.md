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

### Assertiveness
I already had some concerns about the relationships between these objects but unfortunately, 
I got no answer at all after sending several emails. 
I guess he is busy on something. So, to not be blocked, I decided to go with this assumption:
- A tenant is more like a workspace which contains multiple resources.
- User can be in multiple tenants at the same time.
- Each resource is only in one single tenant.
- Each resource would have multiple files. Each file can only belong to one resource.
- User can upload files to resources in the tenant that they are in.

**🔔 NOTE**: The result of this application may not be the same as your expected result 
because I could not do confirm the requirements with you guys. 
But it will work very well with my expectation in [API Documentation section](#api-documentation) 

#### What are completed
1. 4 apis: upload, retrieve, delete, list
2. Store files in AWS S3
3. File metadata was stored in PostgreSQL 
4. API supported authentication with JWT and authorization with permission
5. Support file to expire after a certain time
6. Pagination for list api
7. Filtering by tenant_id for list api 
8. Source code in a Github repository 
9. Documentation on how to deploy the application 
10. Documentation on how to use the application 
11. Unit tests for apis, models, model managers, utils, services 
12. Deploy API to AWS EC2 
13. System design documentation including diagrams and descriptions 
14. CI/CD pipeline

#### What are not completed
1. The API should support files to be public or private => I don't really understand this requirement, want to ask but still got no answer for previous questions
2. HTTPs for deployed API => I don't have a domain to apply SSL certificate. But client still have to use HTTPS for uploading files to AWS S3

## Features at a glance
- Upload a file to the system
- Retrieve a file from the system
- Delete a file from the system
- List all files in the system

## Documentation

### Live Usage
To test the API, you can checkout this [http://18.183.204.247/api-doc](http://18.183.204.247/api-doc) and interact with the API directly on the Swagger UI.

Also, you can go to the Django admin site at [http://18.183.204.247/admin](http://18.183.204.247/admin) to manage the data such as file, resource, tenant, user, permission

Django admin credentials:
```
account/password: admin/admin
```

#### Instructions of Django admin
1. Table User is used to manage users
2. Table Tenant is used to manage tenants
3. Table Resource is used to manage resources
4. Table File is used to manage files
5. To grant permission to a specific user, go to the user detail page
   1. Go to `User permissions` field
   2. Select permission that you want to grant to the user
   3. Click `Save` button
   4. Permissions related to file are:
      1. `File management | file | Can add file` => This permission is required to upload a file
      2. `File management | file | Can view file` => This permission is required to retrieve a file and list files
      3. `File management | file | Can delete file` => This permission is required to delete a file
6. There are some existing data
    1. User: `test1/test1`. Tenant `Tenant A, Tenant B`
    2. User: `test2/test2`. Tenant `Tenant B`
    3. Tenant A has 2 resources: `Resource 1 A, Resource 2 A`
    4. Tenant B has 1 resource: `Resource 3 B` 

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

### Deployment
This project was set up to be deployed on an AWS EC2 instance using Docker and Docker Compose.

The process of deployment is automated by Github Action
1. Create a new branch for new feature
2. Push the code to the new branch
3. Create a pull request to merge the new branch to the main branch. CI will be triggered automatically, merge will be blocked if CI failed or running
4. Once the CI was successfully, dev can merge it to the main branch. CD will be triggered automatically

### System designs
Check out the [system design documentation](diagrams/system/README.md).

### Improvements
- JWT algorithm should be changed to RS256 instead of HS256 in order to be more secure and easy to scale in microservices architecture
- Use AWS ECS instead of EC2 to deploy the application
- Use AWS RDS instead of EC2 to store data

# API Documentation
1. Get access token
- Endpoint: POST `/api/v1/auth/token`
- Description: Get access token for the current user. The access token will be used to authenticate the user in the system

2. Refresh access token
- Endpoint: POST `/api/v1/auth/token/refresh`
- Description: Refresh access token for the current user. The access token will be used to authenticate the user in the system

3. List files
- Endpoint: GET `/api/v1/files`
- Description: List all files in the system that were uploaded by the current user

4. Upload a file
- Endpoint: POST `/api/v1/files`
- Upload file to a specific resource and upload to S3. System will validate if user is in the same tenant with the resource or not. If not, raise HTTP 403 error

5. Retrieve a file
- Endpoint: GET `/api/v1/files/{file_id}`
- Description: Retrieve a file by its id. If the file does not exist or was not uploaded by the current user, raise HTTP 404 error

6. Delete a file
- Endpoint: DELETE `/api/v1/files/{file_id}`
- Description: Delete a file by its id. If the file does not exist or was not uploaded by the current user, raise HTTP 404 error. 
System will also remove the file associated with the file in S3
