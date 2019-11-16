
# Configuration File
device_config = {
  'led_pin': 2
}

atecc608a_dzone_slot = {
  'slot': 2
}

google_cloud_config = {
    'project_id':'stoked-axle-258910',
    'cloud_region':'asia-east1',
    'registry_id':'secure_device_auth',
    'device_id':'esp32_w_atecc608a',
    'mqtt_bridge_hostname':'mqtt.googleapis.com',
    'mqtt_bridge_port':8883
}

jwt_config = {
    'algorithm':'ES256',
    'token_ttl': 43200, #12 hours
    # We're using the ATECC608A to perform the ECDSA operation here. We dont need the private-key setting.
    'private_key':'null'
}
