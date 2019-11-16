

def connect():
    import network

    station = network.WLAN(network.STA_IF)
    if station.isconnected == True:
        print("Already connected")
        return
    
    station.active(True)
    # Try to connect to WiFi access point
    print("Connecting...")
    station.connect(<<SSID>>, <<password>>)

    while station.isconnected() == False:
        pass
 
    print("Connection successful")
    

def disconnect():
    import network

    station = network.WLAN(network.STA_IF)
    station.disconnect()
    station.active(False)