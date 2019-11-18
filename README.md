# Commoditizing security for 'all connected-devices' - especially low-cost connected-anything.

**Context** - Evaluate how you could **vastly** improve security in any IoT project with 0.50$. 

When you think about embedded-device security, pretty much most if not all requirements (i.e. use-cases) depend on some kind of crypto. Ex:
  1. You need a **unique** device identity to securely - **'authenticate your device'**
  2. You need to make sure the code on your device is what you expect it to be - **'firmware validation aka secure boot'**
  3. You need to know that people can't make (illegitimate) copies of your devices - **'anti-cloning or counterfeit protection'**
  4. You don't want someone stealing your IP (when in the field or the supply-chain) - **'IP protection'**
  5. You want a secure way to distribute updates or communicate with a cloud backend - **'secure FOTA or connectivity'**

# The problem:
  - All of the above ultimately depends on the secrecy/safety of a **cryptographic root of trust** (i.e. a private key + crypto constructs/algorithms). Ok great, so all you have to do is protect your keys and use standards-based crypto - how hard can that be? -right

Turns out this is a non-trivial affair, requiring a solution that addresses several categories of issues such as
  - **Expertise**: Crypto based **device-security** is hard 
  - **Price**: I've a **5$ connected thing** and an HSM to secure it is **more work and money** than I'm willing to put in for the ROI
  - **Agility**: It adds significantly to my dev timeframe and I need to be the first to market. 
  - **Good enough security**: The concept of **good enough security** - leading to things like key/certs being stored in SW (in the clear), a compromised chain of trust, an unsecured debug port or a custom SW crypto implementations susceptible to side-channel attacks.
  - **Complex ecosystem**: With a myriad number of **silicon + firmware vendors, micro-architectures, security technologies, open source offerings, cloud platforms, and a heterogenous supply-chain** comprising OEMs, contract manufacturers etc, this problem can easily get compounded, making it increasingly difficult to **secure** a mix of devices.

# The way forward: a usable answer
'Expertise' is what you need to clearly understand the nitty gritties of addressing the above issue-categories but in general, all other classes of issues are attributable to a much tinier knowledge-gap i.e. an understanding of available security options - cryptoprocessors - you can call them TPMs, secure elements, emv chips or custom ones like apple's T2 chip that you cant buy etc. To elaborate  

 - **Price:** Secure crypto processors/chips/accelerators are cheap (cost just a few cents) and most come with certifiable protection for key-storage and crypto-processing capabilities. 
 - **Agility:** Crypto-chips are available in a variety of configurations, from add-ons or isolated external modules to fully integrated secure crytpo co-processors boards. So, it doesn’t matter if it’s a greenfield or brownfield project, you can still have the best of security. 
 - **Good enough security:** No need to make anymore assumptions here -just use the right features for the requirement. Any crypto processor worth the its name addresses most (or all) of basic security use-cases. **Although you still need an expert to do this not throw overloaded app developers at it.**
 - **Complexity:** Most commercially available crypto-chips are independent modules with no micro-architectural or hardware specific dependencies. They are pretty much MCU or MPU agnostic. All you need is a serial interface (largely) to get started. Supply-chain risks can be plugged as you can now handover pre-provisioned crypto-elements to anyone without the worrying about compromise/leakage.
 
**In short with the right expertise, crypto-processors can be a cheap, flexible, highly secure and proven piece of technology - i.e. a commodity that accelerate dev timescales and remove complexity no matter the device.**

# Crypto-processing: **lets get down to the reason this repo exists**

![The tiny but versatile atecc608a cryptoauthentication device from microchip](https://github.com/nihalpasham/micropython_w_atecc608a_googleIotCoreAuth/blob/master/atecc608a_pic_LI%20(2).jpg)

That brings us to the topic of this repo. The atecc608a crypto-processor. This repo will help demo a typical IoT security use-case like secure device authentication to show that price, agility, complexity are not the problems: 
  - Esp32 uses espressif's xtensa micro-architecture (not ARM or intel)
  - micropython firmware is pure python for microcontrollers
  - atecc608a - i2c enabled crypto-processor with a common criteria - JIL high rating 
  - Google cloud - authenticating with google's IoT Core using jwt standard (can easily be extended to TLS mutual auth or other forms of custom auth options supported by iot cloud providers like aws, azure etc.)

# The set-up:
  - An ESP32 board running micropython
  - A Jupyter Notebook for flashing and debugging your code via the repl
  - The ATECC608A Crypto Authentication device (from microchip) to generate and store a (ECC) private key (which **never leaves** the cryptochip)
  - A micropython module (i.e. driver) for the ATECC608A Crypto Authentication device - https://github.com/dmazzella/ucryptoauthlib
  - **You'll also need the EspressIf binary toolchain and SDK to build micropython firmware (esp32 port) i.e. some micropython modules (atecc608a driver, mqtt) will need to be frozen into the firmware else you'll run into out of memory issues.** 
  
# Demo: Secure device authentication with Google IoT Core (Esp32 + micropython + atecc608a)
  1. Step 1 starts with personlization of your crypto element i.e. the atecc608a needs to be configured for your needs. (Note -There's a whole bunch of things the chip can do for you. This is where the 'expertise' comes in but that's beyond the scope of this little demo). 
  2. For our demo - all you need to do is generate and store an (ECC) private key onboard the cryptochip. Although, the datasheet for atecc608a isn't available (its under NDA). You could still use its predecessor's datasheet (atecc508a) to do this. - http://ww1.microchip.com/downloads/en/DeviceDoc/20005927A.pdf
  3. Once you've configured your crypto-chip. It should ideally be permanently locked down i.e. no-one can, not even you can access the private-keys or sensitive data directly. **You do this wrong and you end up 0.50$ short.**
  4. Set up Google IoT Core on your GCP account with a registry, add a device to it. Refer to Google IoT Core's getting started guide for this. 
  4. Retrieve the associated public-key from the chip and upload a PEM formatted version of it to your Google cloud account. Use the pubkey_format.py script to do this. Google has a nice little guide for how to upload and tie your key to an device - https://cloud.google.com/iot/docs/how-tos/devices
  5. From hereon - just follows usage steps. 
 
# Usage:

![Wiring up an ESP32 with a ATECC608a crypto-processor](https://github.com/nihalpasham/micropython_w_atecc608a_googleIotCoreAuth/blob/master/wiredup_atecc608a.jpg)

Simply clone the repository and follow these steps
  - Wire up the sensors and board as shown in the picture. I'm have a fancy expansion board (from microchip) for my atecc608a but you can get a basic breakout board (adafruit has one) with a single i2c interface.
  - Flash the firmware onto the board and copy all scripts contained in the repo onto micropython's filesystem.
  - Use jupyter notebooks to connect to the esp32's serial port (included jupyter notebook for guidance)
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
  - Run the gcpIoTCore_auth_example.py script to generate a signed token and authenticate with google IoT Core and publish some telemetry data. If all goes well, you should see a blue led flashing on your esp32.
  - Assuming everything's tied up right, you should now be able to see test **telemetry data** showing up in your GCP account. 
  - You could also look at the logs for **mqtt messages**. Should see something like this.
  
  ![MQTT logs from GCP](https://github.com/nihalpasham/micropython_w_atecc608a_googleIotCoreAuth/blob/master/google_cloud_mqtt_logs_LI.jpg)


