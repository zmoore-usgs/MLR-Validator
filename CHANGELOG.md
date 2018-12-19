# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

[Unreleased]

### Security
- cschroedl@usgs.gov - Upgraded `requests` and `cryptography` to address security vulnerability https://nvd.nist.gov/vuln/detail/CVE-2018-18074

### Updated
- kmschoep@usgs.gov - remove land net validation
- updated flask version due to CVE https://nvd.nist.gov/vuln/detail/CVE-2018-1000656

## [0.7.0] - 2018-09-10
### Updated
- kmschoep@usgs.gov - Updated reference lists for 2018 winter, spring, summer.

## [0.6.0] 2018-08-23
### Updated
- isuftin@usgs.gov - Updated the version constraint for pyca/cryptography due to
CVE https://nvd.nist.gov/vuln/detail/CVE-2018-10903

### Added
- Dockerfile Healthcheck

### Removed
- Dockerfile
- Dockerfile-DOI
- gunicorn_config.py

## [0.5.0] - 2017-11-20
### Added
- GET endpoint /version to show the current version and artifact name
- Authentication for /validators/add and /validators/update endpoint
- HTTPS Support

## [0.4.0] - 2017-11-01
### Removed
- Removed POST endpoint /validators/

### Changed
- Refactored to implement cross field error and warning validations without using Cerberus.
- Disabled site type validations until we can regenerate the resource file

### Added
- POST endpoint /validators/add. Expects a payload containing a ddotLocation and existingLocation json object.
- POST endpoint /validators/update. Expects a payload containing a ddotLocation and existingLocation json object.
- Duplicate site check for /validators/add.
- Tests which test the ErrorValidator and WarningValidator without mocking any external resources
- Site type transition checks


## [0.3.0] - 2017-10-11

### Added
- Reference list error and warning validations
- Site type cross field checks
- Cross field validations

## 0.2.0 - 2017-10-04

## Added
- POST endpoint /validators
- Implement single field validations
- Swagger docs endpoint /api

[Unreleased]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.5.0...master
[0.5.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.4.0...MLR-Validator-0.5.0
[0.4.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.3.0...MLR-Validator-0.4.0
[0.3.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.2.0...MLR-Validator-0.3.0
