# Strong device authentication for 'all connected-devices' (at 0.50$)

**The goal- Evaluate JWT based authentication schemes fo IoT projects.** 

A typical IoT use-case - 'Securely' connect an IoT node (such as an ESP32, nRF, Rpi etc.) to the Cloud. Well, at first glance one might think, it's a fairly simple ask but in practice that couldn't be further from the truth.

If the plan is to simply connect a device, that's easy. The tricky part is securing that connection. The cost of securing a connected-device as well as the complexity to implement and maintain a high level of security can be a huge undertaking, especially when the vast majority of the internet relies on 'PKI technology' standards to establish trust, identity and confidentiality over the internet.

1. For starters, we'll need to generate cryptographic keys to provision digital certificates and a Certificate Authority to sign those certificates (which in itself needs to be protected with the highest level of care.)
2. Next, the cost of burning keys/certificates into a device is a balance between dollar amounts (and finding an appropriate ODM), and the risk of credentials being compromised (copied) during manufacture. So, most of the time we end up storing them in firmware.
3. After you're done with the first two, you'll need to use something like mutual-TLS to fully secure the communication link, which means a bloated TLS stack on the device and a larger memory footprint than anticipated. These resource demands increase after you integrate Online Certificate Status Protocol (OCSP for the broker), which requires additional (memory-consuming) keys and (CPU-consuming) requests.
4. And let's say you managed to put together all of the above, cryptographic keys are extremely difficult, if not impossible to store securely in the firmware.

For scenarios such as the above, there are other ways to establish trust, identity. What follows is a solution that can serve as a good alternative to the above 

- **Use a secure element:** With Microchip's ATECC608a for example, the private key is generated by the secure element itself, not an external party (CA). The chip uses a random number generator to create the key, making it virtually impossible to derive. The private key never leaves the chip, ever. Using the private key, the chip will be able to generate a public key that can be signed by the chosen CA of the company.
- **Using a JWT for authentication:** Using TLS is perfect for securing the communication between the device and the cloud, but the authentication stack is not ideal for IoT. The stack required for mutual authentication is large in size and has a downside: it needs to be aware of where the keys are stored. The TLS stack needs to know what secure element is used and how to communicate with it. An OpenSSL stack will assume the keys are stored in a file system and need to be modified to access the secure element. This requires development and testing that has to be done again at each update of the stack. With TLS 1.3 coming up, it is likely that this work will have to happen several times, which is a cost for the company. The company can use a TLS stack that is already compatible with the secure element, like WolfSSL, but there is a licensing cost involved that adds to the cost of the device. Google Cloud IoT is using a very common JWT (JSON Web Token) to authenticate the device instead of relying on the mutual authentication of a TLS stack.

Here's how it works:

1. The device will establish a secure connection to the global cloud endpoint for Cloud IoT Core (mqtt.googleapis.com) using TLS, but instead of triggering the mutual authentication it will generate a very simple JWT, sign it with its private key and pass it as a password.
2. The ATECC608 offers a simple interface to sign the device JWT securely without ever exposing the private key.
3. The JWT is received by Google Cloud IoT, the public key for the device is retrieved and used to verify the JWT signature.
4. If valid, the mutual authentication is effectively established.
5. The JWT validation can be set by the customer but never exceeds 24 hours, making it very ephemeral.

![Device Auth Workflow with Google IoT Core](https://www.digikey.com/-/media/Images/Article%20Library/TechZone%20Articles/2019/January/An%20Easier%20Solution%20for%20Securely%20Connecting%20IoT%20Devices%20to%20the%20Cloud/article-2019january-an-easier-solution-fig3_fullsize.jpg?la=en&ts=8b232885-9269-4021-87cf-3e83c5409c48)

We've put together a PoC showcase. What's interesting is that this solution is **completely agnostic to the type of 'Host MCU' and 'firmware' (OS or bare metal)** running on it. Note - this is just a PoC (not intended for production use).

![The tiny but versatile atecc608a cryptoauthentication device from microchip](https://github.com/nihalpasham/micropython_w_atecc608a_googleIotCoreAuth/blob/master/atecc608a_pic_LI%20(2).jpg)

# The set-up:
  - An ESP32 board running micropython
  - A Jupyter Notebook for flashing and debugging your code via the repl
  - The ATECC608A Crypto Authentication device (from microchip) to generate and store a (ECC) private key (which **never leaves** the cryptochip)
  - A micropython module (i.e. driver) for the ATECC608A Crypto Authentication device - https://github.com/dmazzella/ucryptoauthlib
  - **You'll also need the Espressif binary toolchain and SDK to build micropython firmware (esp32 port) i.e. some micropython modules (atecc608a driver, mqtt) will need to be frozen into the firmware else you'll run into out of memory issues.** 
  

**Demo: Secure device authentication with Google IoT Core (ESP32 + Micropython + ATECC608a)**
1. The first step starts with personalizing the secure element i.e. the atecc608a needs to be configured for your needs. (Note -There's a whole bunch of things the chip can do for you. This is where the 'expertise' comes in but that's beyond the scope of this little demo).
2. For our demo - all you need to do is generate and store an (ECC) private key onboard the cryptochip. Although, the datasheet for atecc608a isn't available (its under NDA). You could still use its predecessor's datasheet (atecc508a) to do this. - http://ww1.microchip.com/downloads/en/DeviceDoc/20005927A.pdf
3. Once you've configured your crypto-chip. It should ideally be permanently locked down i.e. no-one can, not even you can access the private-keys or sensitive data directly. You do this wrong and you end up 0.50$ short.
4. Set up Google IoT Core on your GCP account with a registry, add a device to it. Refer to Google IoT Core's getting started guide for this.
5. Retrieve the associated public-key from the chip and upload a PEM formatted version of it to your Google cloud account. Use the pubkey_format.py script to do this. Google has a nice little guide for how to upload and tie your key to an device - https://cloud.google.com/iot/docs/how-tos/devices
6. From hereon - just follows usage steps.
 
# Usage:

![Wiring up an ESP32 with a ATECC608a crypto-processor](https://github.com/nihalpasham/micropython_w_atecc608a_googleIotCoreAuth/blob/master/wiredup_atecc608a.jpg)

Simply clone the repository and follow these steps
  - Wire up the sensors and board as shown in the picture. I'm have a fancy expansion board (from microchip) for my atecc608a but you can get a basic breakout board (adafruit has one) with a single i2c interface.
  - Flash the firmware onto the board and copy all scripts contained in the repo onto micropython's filesystem.
  - Use jupyter notebooks to connect to the esp32's serial port (`included jupyter notebook` for guidance)
  - Test to see if your board can see the atecc608a on its i2c bus. If yes, move on to the next steps
  ```python
  
      import machine
      
      i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=133000)
      print('Scan i2c bus...')

      addresses = i2c.scan()

      if len(addresses) == 0:
        print("No i2c device !")
      else:
        print('i2c devices found:',len(addresses))
        for device in addresses:  
          print("Decimal address: ",device," | Hexa address: ",hex(device))
       
      Scan i2c bus...
      i2c devices found: 1
      Decimal address:  96  | Hexa address:  0x60
      
  ```
  - Make sure your board is connected to a local wifi-hotspot before you start.
  - Run the gcpIoTCore_auth_example.py script to generate a signed token and authenticate with google IoT Core and publish some telemetry data. If all goes well, you should see a blue led flashing on your esp32. ***click on the video link below***
  
   [![Flashing blue led on the esp32.](https://img.youtube.com/vi/VYf0L76V8uE/maxresdefault.jpg)](https://youtu.be/VYf0L76V8uE) 
  
  - Assuming everything's tied up right, you should now be able to see test **telemetry data** showing up in your GCP account. 
  
  ![Raw MQTT Telemetry data being published to GCP upon successful authentication.](https://github.com/nihalpasham/micropython_w_atecc608a_googleIotCoreAuth/blob/master/telemetry_raw_mqtt_messages.png)
  
  - You could also look at the logs for **mqtt messages**. Should see something like this.
  
  ![MQTT logs from GCP](https://github.com/nihalpasham/micropython_w_atecc608a_googleIotCoreAuth/blob/master/google_cloud_mqtt_logs_LI.jpg)

# Notes:

  - Having made dedicated HW based crypto-processing sound like the next best thing to sliced bread, let me just say that there is no such thing. You still need defense in depth and the expertise to get all of this right but nonetheless this is a pretty good starting point. 
  - For example - most crypto-chips dont offer much in the way of 'runtime code isolation' security (not that you need it in most low-powered connected IoT projects) but if that's something on your list of security needs, you should probably look at other options like Cortex-M trustzone etc.  

##### Footnote: Sales pitch part, skippable if you want to save 30 secs of your life but if you're looking to solve any of the above use-cases or grappling with similar security requirements (like TPMs, Cortez-M Trustzone), please feel free to get in touch or drop a tweet at @npashi. 
