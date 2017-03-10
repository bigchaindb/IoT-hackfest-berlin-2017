from argparse import ArgumentParser
import logging
from bigchaindb_driver import BigchainDB
from bigchaindb_driver.exceptions import NotFoundError
from time import sleep, strftime, gmtime
from transactions import create_asset, create_transfer

class BigChainDBClient:

    def init_system(self, bdb_ip, bdb_port, pub_key, pr_key):
        self.bdb = BigchainDB('http://{0}:{1}'.format(bdb_ip, bdb_port))
        self.keypair = {
            'private_key': pr_key,
            'public_key': pub_key
        }
        self.asset_data = {
            'data': {
                'asset_class': 'vehicle_telemetry',
                'asset_author': 'hackfest-berlin-2017-team'
            }
        }
        self.txids = {}
    # end init_system

    def record_data(self, bdb_conn, data, metadata, keypair, tx_id, vehicle_id):
        fulfilled_tx = None
        if tx_id != '':
            print('Transfer tx!')
            previous_tx = bdb_conn.transactions.retrieve(tx_id)
            if 'id' in previous_tx['asset']:
                asset_id = previous_tx['asset']['id']
            else:
                asset_id = previous_tx['id']

            transfer_tx = create_transfer(previous_tx, keypair['private_key'],
                                        keypair['public_key'], vehicle_id,
                                        metadata, asset_id)
            bdb_conn.transactions.send(transfer_tx.to_dict())
            fulfilled_tx = transfer_tx.to_dict()
        else:
            print('Create tx!')
            create_tx = create_asset(keypair['private_key'], keypair['public_key'],
                                    vehicle_id, data, metadata)
            bdb_conn.transactions.send(create_tx.to_dict())
            fulfilled_tx = create_tx.to_dict()
        # end if

        # verify if the tx was registered in the bigchain
        trials = 0
        while trials < 10:
            try:
                if bdb_conn.transactions.status(
                        fulfilled_tx['id']
                ).get('status') == 'valid':
                    print('Tx valid in:', trials, 'secs')
                    break
            except NotFoundError:
                trials += 1
                sleep(1)
            # end try
        # end while

        if trials == 10:
            print('Cannot connect to backend... Exiting!')
            exit(0)
        # end if
        return fulfilled_tx['id']
    # end record_data

    def send_data_to_bdb(self, telemetry_data, vehicle_id):
        tx_id = self.txids.get(vehicle_id, '')

        asset_metadata = {
            'company': 'vw',
            'financer': 'commerzbank',
            'owner': 'microsoft',
            'source': 'riddle_and_code',
            'dest': 'bdb',
            'timestamp': strftime('%Y-%m-%d_%H:%M:%S', gmtime()),
            'data': telemetry_data
        }

        # record data to bigchain
        tx_id = self.record_data(self.bdb, self.asset_data, asset_metadata, self.keypair, tx_id, vehicle_id)
        print('tx_id: ' + tx_id)
        self.txids.update({vehicle_id: tx_id})
    # end send_data_to_bdb

    def __init__(self, bdb_ip, bdb_port, public_key, private_key):
        self.bdb_ip = bdb_ip
        self.bdb_port = bdb_port
        self.public_key = public_key
        self.private_key = private_key

        self.init_system(self.bdb_ip, self.bdb_port, self.public_key, self.private_key)
    # end main
