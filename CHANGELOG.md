# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.14.0] - 2019-03-01
## Changed
- standardize error reponse
- update restplus to 0.12.1

## [0.13.0] - 2019-02-14
## Added
- instructions in Readme to connect the validator with mlr-local-dev setup

## Changed
- fixed leftover error reporting bug

## [0.12.0] - 2019-02-05
### Changed
- fixed siteTypeCode SS or FA bug

## [0.11.0] - 2019-01-31
### Added
- Disallow left padding

### Changed
- Validation for creates or updates, force user to change site type if they're attempting to update SS or FA
- Let timezone be 6 chars
- Update pyyaml to 4.21b.

## [0.10.0] - 2018-11-27
### Added
- minlength of siteNumber validation
- Disallow siteTypeCode SS or FA to be created 

### Changed
- site type code checks to warnings instead of fatal errors
- strip right padding before ref list comparison

## [0.9.0] - 2018-10-24
### Security
- cschroedl@usgs.gov - Upgraded `requests` and `cryptography` to address security vulnerability https://nvd.nist.gov/vuln/detail/CVE-2018-18074

## Changed
-  Made secondaryUseOfSiteCode and tertiaryUseOfSiteCode optional on GW type sites.

### Removed
- requirement to define secondary and tertiary site use codes for groundwater secondary site types.

## [0.8.0] - 2018-9-13
### Changed
- kmschoep@usgs.gov - remove land net validation
- updated flask version due to CVE https://nvd.nist.gov/vuln/detail/CVE-2018-1000656

## [0.7.0] - 2018-09-10
### Changed
- kmschoep@usgs.gov - Updated reference lists for 2018 winter, spring, summer.

## [0.6.0] 2018-08-23
### Changed
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
[0.14.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.13.0...MLR-Validator-0.14.0
[0.13.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.12.0...MLR-Validator-0.13.0
[0.12.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.11.0...MLR-Validator-0.12.0
[0.11.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.10.0...MLR-Validator-0.11.0
[0.10.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.9.0...MLR-Validator-0.10.0
[0.9.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.8.0...MLR-Validator-0.9.0
[0.8.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.7.0...MLR-Validator-0.8.0
[0.7.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.6.0...MLR-Validator-0.7.0
[0.6.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.5.0...MLR-Validator-0.6.0
[0.5.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.4.0...MLR-Validator-0.5.0
[0.4.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.3.0...MLR-Validator-0.4.0
[0.3.0]: https://github.com/USGS-CIDA/MLR-Validator/compare/MLR-Validator-0.2.0...MLR-Validator-0.3.0
