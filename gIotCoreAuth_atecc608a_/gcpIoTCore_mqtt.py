import config
import ssl
from umqtt.simple import MQTTClient


def on_message(topic, message):
    print((topic,message))

def get_mqtt_client(jwt):
    """Create our MQTT client. The client_id is a unique string that identifies
    this device. For Google Cloud IoT Core, it must be in the format below."""    
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(config.google_cloud_config['project_id'], 
                                                                           config.google_cloud_config['cloud_region'], 
                                                                           config.google_cloud_config['registry_id'], 
                                                                           config.google_cloud_config['device_id'])
    print('Sending message with password {}'.format(jwt))
    client = MQTTClient(client_id.encode('utf-8'),
                        server=config.google_cloud_config['mqtt_bridge_hostname'],
                        port=config.google_cloud_config['mqtt_bridge_port'],
                        user=b'ignored',
                        password=jwt.encode('utf-8'),
                        ssl=True)
    client.set_callback(on_message)
    client.connect()
    client.subscribe('/devices/{}/config'.format(config.google_cloud_config['device_id']), 1)
    client.subscribe('/devices/{}/commands/#'.format(config.google_cloud_config['device_id']), 1)

    return client