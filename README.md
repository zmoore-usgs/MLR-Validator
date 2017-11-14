# MLR-Validator
Validates inserts and updates to the MLR system

[![Build Status](https://travis-ci.org/USGS-CIDA/MLR-Validator.svg?branch=master)](https://travis-ci.org/USGS-CIDA/MLR-Validator)
[![Coverage Status](https://coveralls.io/repos/github/USGS-CIDA/MLR-Validator/badge.svg)](https://coveralls.io/github/USGS-CIDA/MLR-Validator)


This project has been built and tested with python 3.6.x. To build the project locally you will need
python 3 and virtualenv installed.
```bash
% virtualenv --python=python3 env
% env/bin/pip install -r requirements.txt
```
To run the tests:
```bash
env/bin/python -m unittest
```

To run the application locally execute the following:
```bash
% env/bin/python app.py
```

The swagger documentation can then be accessed at http://127.0.0.1:5000/api

Default configuration variables can be overridden be creating a .env file. For instance to turn debug on,
you will want to create an .env with the following:
```python
DEBUG = True
```
For local development, you will need to provide a JWT token to the service. This can be done through the Swagger 
documents by clicking the Authorize button and entering 'Bearer your.jwt.token'.

You can use a valid JWT token generated by another service. You will need to set it's JWT_PUBLIC_KEY to the public 
key used to generate the token, as well as the JWT_DECODE_AUDIENCE (if any) and the JWT_ALGORITHM 
(if different than RS256). If you don't want to verify the cert on this service, set AUTH_CERT_PATH to False.

Alternatively, you can generate your own token by using the python package jwt. In the python interpreter, do the following
```python
import jwt
jwt.encode({'authorities': ['one_role', 'two_role']}, 'secret', algorithm='HS256')
```

The output of this command will be the token that you can use. You will need to set JWT_SECRET_KEY to 'secret' in 
your local .env file. See http://flask-jwt-simple.readthedocs.io/en/latest/options.html for the other options that 
you can use.

The two docker files provided pull the artifact from cida.usgs.gov/artifactory. The build type and version should be specfied as
build-arg's when building the image. The argument build_type should be 'snapshots' or 'releases'. The artfact_version
should be the version of the usgs-wma-mlr-validator that you want to be used in the docker container.
The optional build argument, 'listening_port' can be specified and defaults to 7010. This port will be exposed
by the container. To build within the DOI network, use Dockerfile-DOI and place the DOI cert in '/rootcrt'.
Below is an example of how to build and run.
```bash
% docker build --build-arg artifact_version=0.1.0.dev0 --build-arg build_type=snapshots -t validator -f Dockerfile-DOI .
% docker run --publish 5000:7010 \
    --env auth_token_key_url=https://path.com/to/token_key\
    --env jwt_algorithm=HS256 \
    --env jwt_decode_audience=string_in_aud_claim_in_token \
    --env auth_cert_path=path_to_auth_cert or False if disabling SSL verification (not recommended) \
    validator
```