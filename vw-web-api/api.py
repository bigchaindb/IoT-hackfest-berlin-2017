from flask import Flask
from flask_restful import Resource, Api

import base58
import hashlib
import urllib.request
import json

app = Flask(__name__)
api = Api(app)

# Valid vehicle ids - currently there's only data for '001'
Vehicles = {
    '001': {},
    '002': {}
}

# BigChainDB endpoint configuraton
Database = {
    "Host": "bcdbhack.westeurope.cloudapp.azure.com",
    "Port": 9984
}

def abort_if_vehicle_doesnt_exist(vehicle_id):
    if vehicle_id not in Vehicles:
        abort(404, message="Vehicle {0} doesn't exist".format(vehicle_id))

# Generate the correct public key for vehicle id
def generateVehicleKey(vehicle_id):
    return base58.b58encode(hashlib.sha256(vehicle_id.encode()).digest())

# This retrieves all BigchainDB entries of msgType 'getTrips'
class TripList(Resource):
     def get(self, vehicle_id):
        abort_if_vehicle_doesnt_exist(vehicle_id)
        VehicleKey = generateVehicleKey(vehicle_id)

        # result set
        metadata = []

        print("----------------Vehicle Key -------------------------")
        print(VehicleKey)

        # get all transactions for the public key
        print("----------------get all transactions for the public key -------------------------")
        webUrl = urllib.request.urlopen("http://{0}:{1}/api/v1/outputs?public_key={2}".format(Database["Host"], Database["Port"], VehicleKey))
        data = webUrl.read()
        encoding = webUrl.info().get_content_charset('utf-8')
        json_object = json.loads(data.decode(encoding))
        print(json_object)

        # get the asset it for one transaction 
        print("----------------get the asset it for one transaction -------------------------")
        transaction_id = json_object[0].split('/')[2]
        print(transaction_id)

        webUrl = urllib.request.urlopen("http://{0}:{1}/api/v1/transactions/{2}".format(Database["Host"], Database["Port"], transaction_id))
        data = webUrl.read()
        encoding = webUrl.info().get_content_charset('utf-8')
        json_object = json.loads(data.decode(encoding))
        #print(json_object)

        # get all the data for an asset
        print("----------------get all the data for an asset-------------------------")
        if json_object['operation'] == 'CREATE':
            asset_id = transaction_id
        else:
            asset_id = json_object['asset']['id']
        #print(transaction_id)

        webUrl = urllib.request.urlopen("http://{0}:{1}/api/v1/transactions?asset_id={2}".format(Database["Host"], Database["Port"], asset_id))
        data = webUrl.read()
        encoding = webUrl.info().get_content_charset('utf-8')
        json_object = json.loads(data.decode(encoding))
        #print(json_object)

        # filter the metadata
        print("----------------filter the metadata-------------------------")
        for index in range(len(json_object)):
            try:
                rawData = json_object[index]['metadata']['data']
                jsRawData = json.loads(rawData)

                # since we have some legacy data in it just use the correct one
                if 'vehicleId' in jsRawData and jsRawData['msgType'] == 'getTrips':
                    print('element added to result set')
                    metadata.append(jsRawData)
            except:
                print("Unexpected error:")

        print(metadata)

        # CORS response headers needed to avoid errors
        # TODO: when used in production ensure this is properly updated
        return metadata, 200, {'Access-Control-Allow-Origin':'*', 'Access-Control-Request-Headers':'*'}

api.add_resource(TripList, '/trips/<string:vehicle_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
