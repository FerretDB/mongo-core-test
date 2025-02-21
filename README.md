# MongoDB Compatibilty Test

In this scenario, we are performing a MongoDB API test aimed at verifying compatibility, reliability, and performance across different implementations of the MongoDB document model. It's important to note that our focus is on the core product itself, and we are not evaluating or testing specific cloud providers. The purpose of this test is to validate the behavior of the MongoDB API when interacting with various MongoDB clones, taking into consideration potential differences in their underlying architecture or features.

## Prerequisites:
* Install [Git](https://git-scm.com/downloads)
* Install [Docker](https://www.docker.com/products/docker-desktop/)
* Download [Mongo 5.0.30 client](https://www.mongodb.com/try/download/community) to your preferred bin folder
* Install pymongo: `pip3 install pymongo`

## Instructions

#### Clone Repos
* `git clone https://github.com/mongodb-developer/mongo-core-test.git`
* `cd mongo-core-test`
* `git clone https://github.com/mongodb/mongo.git`

#### Run Tests
* Edit [run.py](run.py) "User Variables"
* `python3 run.py [5, 7 or 8]`

## Optional Instructions To Create Test Environment
#### Use [MongoDB 5.0.30](https://www.mongodb.com/try/download/community) Docker Container:
  * `docker compose -f mongo5.yml up -d`

#### Use [MongoDB 7.0.11](https://www.mongodb.com/try/download/community) Docker Container:
  * `docker compose -f mongo7.yml up -d`

#### Use [MongoDB 8.0.4](https://www.mongodb.com/try/download/community) Docker Container:
  * `docker compose -f mongo8.yml up -d`  

#### Use [MariaDB MaxScale](https://mariadb.com/downloads/community/maxscale/) Docker Container:
  * `docker compose -f maxscale.yml up -d`

#### Use [FerretDB 1.24](https://www.ferretdb.com) Docker Container:
  * `docker compose -f ferret.yml up -d`

## Compatibilty Results By MongoDB Version
| Product Tested | vs MongoDB 5.x | vs MongoDB 7.x | vs MongodB 8.x | Works with [Compass](https://www.mongodb.com/products/tools/compass) |
| :------ | :--:| :--:| :--: | :--: |
| MongoDB 5 | 100% | 96.01% | 94.39% | :heavy_check_mark: |
| MongoDB 7 | 100% | 100% | 98.20% | :heavy_check_mark: |
| MongoDB 8 | 100% | 100% | 100% | :heavy_check_mark: |
| [Oracle 23ai](https://docs.oracle.com/en/database/oracle/mongodb-api/mgapi/overview-oracle-database-api-mongodb.html) | 33.73% | 32.70% | 32.13% | :heavy_check_mark: |
| [SingleStore Kai](https://www.singlestore.com/kai/) | 46.96% | 45.85% | N/A | :heavy_check_mark: |
| [FerretDB 1.24](https://docs.ferretdb.io/) | 37.42% | 36.34% | 34.60% | :x: |
| [MaxScale 25.01.1](https://mariadb.com/kb/en/mariadb-maxscale-2501-maxscale-2501-nosql-protocol-module/) | 35.18% | 33.88% | 33.40% | :x: |