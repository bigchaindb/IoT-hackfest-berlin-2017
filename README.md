# IoT-hackfest-berlin-2017
Code for the IoT+ BigchainDb + MSFT + VW PoC at the hackfest in Berlin held from 28 Feb to 03 Mar 2017



## Steps to deploy the PoC
```
NOTE: You may have to use different the public and private keys than those 
used below.
```

#### Run RethinkDB
```
docker run \
--detach \
--name=rethinkdb \
--publish=172.17.0.1:28015:28015 \
--publish=172.17.0.1:8080:8080 \
--restart=always \
--volume "$HOME/bigchaindb_docker:/data" \
rethinkdb:2.3
```
To check the logs: `docker logs -f rethinkdb`


#### Configure BigchainDB to use the RethinkDB backend
Note: You do not need to do this step if you have done this already

```
docker run \
--interactive \
--rm \
--tty \
--volume "$HOME/bigchaindb_docker:/data" \
bigchaindb/bigchaindb \
-y configure \
rethinkdb
```
Change the `database.host` param in `~/bigchaindb_docker/.bigchaindb` file 
from `localhost` to `172.17.0.1`


#### Run BigchainDB
```
docker run \
--detach \
--name=bigchaindb \
--publish=172.17.0.1:9984:9984 \
--restart=always \
--volume=$HOME/bigchaindb_docker:/data \
bigchaindb/bigchaindb \
start
```
To check the logs: `docker logs -f bigchaindb`


#### Build and run nginx
```
cd IoT-hackfest-berlin-2017/bdb-web-api/nginx
docker build -t bdb-nginx .
docker run \
--detach \
--name=bdb-nginx \
--publish=80:80 \
--restart=always \
bdb-nginx
```
To check the logs: `docker logs -f bdb-nginx`


#### (Optional) Add the Lungo Tavolo products to bigchaindb
```
cd IoT-hackfest-berlin-2017/bdb-web-api/lungo_tavolo
python3 lungo_tavolo.py \
--bdb-ip localhost \
--bdb-port 80 \
--public-key F911cpKsZTP3Fxzx243mJqUh15CtGDTRuVBaw5xnvGXh \
--private-key 6H6g4c6fwc5MCDMT4cmTgDDuij9Yhr6FXVJ7G2sMoztJ \
--file ["Product Data Lungo Tavolo - Skirt.csv" |
        "Product Data Lungo Tavolo - Top.csv"   |
        "Product Data Lungo Tavolo - Pants.csv" ]
```
Note the transaction id for each product. We will need them later.


#### Run Lungo Tavolo UI
Use the transaction id in the code, as this is hardcoded for the PoC.
```
cd IoT-hackfest-berlin-2017/front-end/lt
docker build -t hackfest-lt .
docker run \
--detach \
--name=hackfest-lt \
--publish=172.17.0.1:8002:8002 \
--restart=always \
hackfest-lt
```
To check the logs: `docker logs -f hackfest-lt`


#### Run VW Fin Services UI
```
cd IoT-hackfest-berlin-2017/front-end/vw
docker build -t hackfest-vw .
docker run \
--detach \
--name=hackfest-vw \
--publish=172.17.0.1:8001:8001 \
--restart=always \
hackfest-vw
```
To check the logs: `docker logs -f hackfest-vw`


#### Run VW Web API Server
##### Microsoft module
```
cd IoT-hackfest-berlin-2017/vw-web-api
docker build -t vw-web-api .
docker run \
--detach \
--name=vw-web \
--publish=5000:5000 \
--restart=always \
vw-web-api
```

##### BigchainDB module - TODO(Krish/Thomas)
```
cd IoT-hackfest-berlin-2017/bdb-web-api/vw
docker build -t vw-backend-api .
docker run \
--detach \
--name=vw-backend-api \
--publish=5000:5000 \
--restart=always \
vw-web-api

```

