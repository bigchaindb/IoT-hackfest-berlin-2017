# BigChainDB IoT Hub Feeder

The feeder receives the device messages from IoT Hub, using an AMQP link to the Event Hubs endpoint. It then feeds them to BigChainDB using the Python driver.

The Docker image has all the necessary pre-requisites, i.e. Qpid Proton with Python3 bindings and the BigChainDB driver.

```
docker build -t bcdbhackfest:feeder .
```

Run the feeder:

```
docker run --rm -it -v %CD%:/app bcdbhackfest:feeder python3 feeder.py
```

The BigChainDB connection parameters are hardcoded in `feeder.py`.

```
BigChainDBClient('bcdbhack.westeurope.cloudapp.azure.com', 9984, 'F911cpKsZTP3Fxzx243mJqUh15CtGDTRuVBaw5xnvGXh', '6H6g4c6fwc5MCDMT4cmTgDDuij9Yhr6FXVJ7G2sMoztJ')
```
