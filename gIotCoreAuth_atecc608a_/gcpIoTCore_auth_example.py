import machine
from machine import Pin
import esp32, utime
import gcpIoTCore_mqtt
import wifi, create_token
import config
import ujson
from cryptoauthlib.device import ATECCX08A

# Instantiate the cryptoauth device. Mine is already personalized i.e. configured to my requirements.
# with an ECC private key in slot 2 of the device's data zone. This is what I will be using to sign my jwts. 
device = ATECCX08A()
# print(device)

led_pin = machine.Pin(config.device_config['led_pin'], Pin.OUT) #built-in LED pin
led_pin.value(0)

wifi.connect()
create_token.set_time()
jwt = create_token.create_token(config.google_cloud_config['project_id'], 
                                config.jwt_config['token_ttl'],
                                device,
                                config.atecc608a_dzone_slot['slot'])
client = gcpIoTCore_mqtt.get_mqtt_client(jwt)

for _ in range(20):
    message = {
        "device_id": config.google_cloud_config['device_id'],
        "temp": esp32.raw_temperature()
    }
    print("publishing message " + str(ujson.dumps(message)))
    led_pin.value(1)
    mqtt_topic ='/devices/{}/{}'.format(config.google_cloud_config['device_id'], 'events')
    client.publish(mqtt_topic.encode('utf-8'), ujson.dumps(message).encode('utf-8'))

    #client.check_msg() # Check for new messages on subscription
    # We can use the built-in led in the esp32 to give us some visual clues when publishing to IoT Core. 
    # On == publishing
    # Off == not publishing
    utime.sleep(2)  # Delay for 2 seconds
    led_pin.value(0)
    utime.sleep(2)