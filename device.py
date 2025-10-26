import os
import random
import time
import uuid
from typing import Any, Dict, Optional

import httpx



class Device:
    def __init__(self, name: str, url: str, bind_ip: Optional[str] = None) -> None:
        self.id   = 0
        self.name = name
        self.url  = url
        self.client = self._create_client(bind_ip)

    def _create_client(self, bind_ip: Optional[str]) -> httpx.Client:
        transport = None
        if bind_ip:
            transport = httpx.HTTPTransport(local_address=(bind_ip, 0))
        return httpx.Client(transport=transport)


    def generate_data(self) -> Dict[str, Any]:
        return {               
            'name':             self.name,       
            'temperature':      round(random.uniform(35, 39), 1), 
            'heart_rate':       random.randrange(0, 120),    
            'blood_pressure':   random.randrange(5, 130),
            'respiratory_rate': random.randrange(5, 30)
        }

    def connect(self):
        while 1:
            try:
                response = self.client.get(url=f'{self.url}')

                if(response.is_success):
                    break
            except Exception as ex: 
                print(f'[{self.name}]: {ex}')
            time.sleep(1)
    

    def create_user(self):
        data = self.generate_data()
        response = self.client.post(url=f'{self.url}/users', json=data)
        self.id = int(response.json()['data']['id'])


    def update_user(self):
        data = self.generate_data()
        self.client.put(url=f'{self.url}/users/{self.id}', json=data)


    def run(self):
        self.connect()
        self.create_user()

        try:
            while 1:
                self.update_user()
                time.sleep(random.randrange(2, 6))
        except:
            self.client.delete(url=f'{self.url}/users/{self.id}')
        finally:
            self.client.close()

        


if(__name__=='__main__'):
    uid = str(os.getenv('UID', uuid.uuid4()))
    url = os.getenv('URL', 'http://localhost:8000')
    bind_ip = os.getenv('BIND_IP')
    Device(name=uid, url=url, bind_ip=bind_ip).run()
