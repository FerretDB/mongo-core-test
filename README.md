# MongoDB Core Compatibilty Test

In this scenario, we are performing a MongoDB API test aimed at verifying compatibility, reliability, and performance across different implementations of the MongoDB document model. It's important to note that our focus is on the core product itself, and we are not evaluating or testing specific cloud providers. The purpose of this test is to validate the behavior of the MongoDB API when interacting with various MongoDB clones, taking into consideration potential differences in their underlying architecture or features.

## Prerequisites:
* Install [Git](https://git-scm.com/downloads)
* Install [Docker](https://www.docker.com/products/docker-desktop/)
* Download [Mongo 5.0.26 client](https://www.mongodb.com/try/download/community) to your preferred bin folder
* Install pymongo: `pip3 install pymongo`

## Instructions

#### Clone Repos
* `git clone https://github.com/mongodb-developer/mongo-core-test.git`
* `cd mongo-core-test`
* `git clone https://github.com/mongodb/mongo.git`

#### Run Tests
* Edit [run.py](run.py) "User Variables"
* `python3 run.py [5 or 7]`

## Optional Instructions To Create Test Environment
#### Use [MongoDB 5.0.26](https://www.mongodb.com/try/download/community) Docker Container:
  * `docker compose -f mongo5.yml up -d`

#### Use [MongoDB 7.0.7](https://www.mongodb.com/try/download/community) Docker Container:
  * `docker compose -f mongo7.yml up -d`

#### Use [MaxScale 23.08.4](https://mariadb.com/kb/en/mariadb-maxscale-2308-nosql-protocol-module/) Docker Container:
* `docker compose -f maxscale.yml up -d`

#### Use [FerretDB 1.20.1](https://www.ferretdb.com) Docker Container:
* `docker compose -f ferret.yml up -d`

## Compatibilty Results By MongoDB Version
| Product Tested | MongoDB 5.x | MongoDB 7.x | Works with [Compass](https://www.mongodb.com/products/tools/compass) |
| :------ | :--:| :--:| :--: |
| MongoDB 5.0.26 | 100% | 96.73% | :heavy_check_mark: |
| MongoDB 7.0.7 | 100% | 100% | :heavy_check_mark: |
| SingleStore Kai™ | 38.96% | 37.02% | :heavy_check_mark: |
| FerretDB 1.20.1 | 37.83% | 36.60% | :x: |
| MariaDB MaxScale 23.08.4 | 33.88% | 33.03% | :x: |