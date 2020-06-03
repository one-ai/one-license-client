import requests
import random
import _thread
import time
import os


class OneLicenceClient:
    def __init__(self, config):
        self.server_url = config['server_url']
        self.product_id = config['product_id']
        self.version_id = config['version_id']
        self.license_id = config['license_id']
        self.api_counter = 0
        self.sync_retry_counter = 0
        self.clientConnectionId = random.randint(1, 10000000)
        self.consumeUrl = self.server_url + '/products/{}/versions/{}/licenses/{}/consume'.format(
            self.product_id, self.version_id, self.license_id)
        self.activate()
        _thread.start_new_thread(self.sync_at_interval, (self,))

    def activate(self):
        """
        Activate instance
        """
        print('- Activating instance license...')
        response = requests.put(url=self.consumeUrl, json={
                                'type': 'activate',
                                'clientConnectionId': self.clientConnectionId
                                })
        status = response.status_code
        data = response.json()
        self.config = data

        if status == 200:
            print('- Delaying activation for : ' +
                  str(self.config['activationDelay']) + 's')
            time.sleep(self.config['activationDelay'])
            print('- Instance license activated successfully!')
            return
        else:
            raise Exception(data)

    def sync(self):
        """
        Sync client and server
        """
        print('- Consuming single API count')
        response = requests.put(url=self.consumeUrl, json={
                                'type': 'sync',
                                'clientConnectionId': self.clientConnectionId,
                                'apiCallCounter': self.api_counter
                                })
        status = response.status_code
        data = response.json()
        self.config = data

        if status == 200:
            print('- Sync successful')
            print()
            self.sync_retry_counter = 0
            self.api_counter = 0
            return
        else:
            print('- Failed to sync')
            raise Exception(data)

    def consume(self):
        """
        Consume single API call
        """
        print('- Consuming single API count')
        self.api_counter += 1
        response = requests.put(url=self.consumeUrl, json={
                                'type': 'sync',
                                'clientConnectionId': self.clientConnectionId,
                                'apiCallCounter': self.api_counter
                                })
        status = response.status_code
        data = response.json()
        self.config = data

        if status == 200:
            print('- Single API count consumption successful')
            print()
            self.sync_retry_counter = 0
            self.api_counter = 0
            return
        else:
            print('- Failed to consume single API count')
            raise Exception(data)

    def sync_at_interval(self, license):
        try:
            while True:
                print('- Started periodic license syncing')
                if self.config['syncTrigger'] == 'AFTER_INTERVAL':
                    # For intervalled syncing
                    max_retries = self.config['maxSyncRetries']
                    sync_interval = self.config['syncInterval']
                    interval_bw_retries = sync_interval//max_retries
                    print('- Type : SYNC AFTER INTERVAL')
                    print('- Max retries : ' + str(max_retries))
                    print('- Current retry counter : ' +
                          str(self.sync_retry_counter))
                    print('- Sync interval : ' + str(sync_interval) + 's')
                    print('- Interval between retries : ' +
                          str(interval_bw_retries))

                    if(self.sync_retry_counter >= max_retries):
                        raise Exception('- Max sync retries limit reached.')

                    try:
                        self.sync()
                        print('- Periodic license sync successful')
                        print()
                        time.sleep(interval_bw_retries)
                    except Exception as err:
                        print('- Sync at interval error!')
                        print('- Retrying sync after: ' +
                              str(interval_bw_retries) + 's')
                        self.sync_retry_counter += 1
                        print()
                        time.sleep(interval_bw_retries)
                else:
                    # For per call syncing
                    try:
                        print('- Type : SYNC AT EVERY CALL')
                        print('- Max retries : Infinite')
                        print('- Current retry counter : ' +
                              str(self.sync_retry_counter))
                        print('- Sync interval : 60s')
                        self.sync()
                        print('- Periodic license sync successful')
                        print()
                        time.sleep(60)
                    except Exception as err:
                        print('- Sync at interval error!')
                        print('- Retrying sync after: 60s')
                        self.sync_retry_counter += 1
                        print()
                        time.sleep(60)

        except Exception as err:
            print('- Periodic syncing error')
            print(err)
            print('- Crashing due to licensing error')
            os._exit(1)


# Example usage
l = OneLicenceClient({
    "server_url": "http://localhost:4000/api/v1",
    "product_id": "5edb10fecc150913cb7640f6",
    "version_id": "5edb1105cc150913cb7640f7",
    "license_id": "5edb1264cc150913cb7640f8",
})


l.consume()
while True:
    pass
