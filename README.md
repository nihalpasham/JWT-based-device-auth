# Commoditizing security - for 'connected-devices'  

**Context** - Evaluate how you could **vastly** improve security in any IoT project with 0.50$. 

When you think about embedded-device security, pretty much most if not all requirements (i.e. use-cases) depend on some kind of crypto. Ex:
  1. You need a **unique** device identity to securely -**authenticate your device**
  2. You need make sure the code on your device is what you expect it to be -**firmware validation aka secure boot**
  3. You need to know that people cant make (illegitimate) copies of your devices -**anti-cloning or counterfeit protection**
  4. You don't want someone to stealing your IP (when in the field or the supply-chain) -**IP protection**
  5. You want a secure way to distribute updates or communicate with a cloud backend -**secure FOTA or connectivity**

# The problem:
  - All of the above ultimately depend on the secrecy/safety of a **cryptographic root of trust** (i.e. a private key + crypto constructs/algorithms) . So, all you have to do is protect your keys and use standards based crypto - how hard can that be? -right

Turns out this is a non-trivial problem, requiring a solution that addresses 5 categories of issues
  - **Expertise**: Crypto based **device-security** is hard 
  - **Price**: I've a **5$ connected thing**. An HSM is **more work** than I'm willing to put in for the ROI
  - **Agility**: It adds significantly to my dev timeframe and I need to be the first to market. 
  - **Assumptions**: The concept of **good enough security** - leading to things like key/certs being stored in SW (in the clear), a compromised chain of trust or an unsecured debug port.
  - **Fragmented ecosystem**: With a myriad number of silicon, firmware vendors, open source components and cloud platforms, and heterogenous supply chain comprising OEMs, contract manufacturers, this problem can easily be compounded becomes increasingly difficult to manage security for a heterogenous mix of devices.

# Not really,  
Barring 'expertise' all other classes of issues are attributable to a lack of understanding of  the current security landscape and the available options. To elaborate  

 - **Price:** secure crypto processors/chips/accelerators are cheap ( cost a few cents), some with certifiable protection for key-storage and crypto processing
 - **Agility:** crypto-chips are available in a variety of configuration,  from fully isolated external modules to  integrated boards with secure co-processors. In short it doesn’t matter if it’s a greenfield or brownfield project or if its micro
 - **Assumptions:** 
 - **Fragmentation:** 

That brings us to the case in point. The atecc608a 

**Benefits:**
With an external HW add-on or brownfield deployments
There are no hw dependencies 
Cloud agnostic works with any 

# The set-up:
  - An ESP32 board running micropython
  - A Jupyter Notebook for flashing and debugging your code via the repl
  - The ATECC608A Crypto Authentication device (from microchip) to generate and store a (ECC) private key (which **never leaves** the cryptochip)
  - A micropython module (i.e. driver) for the ATECC608A Crypto Authentication device - https://github.com/dmazzella/ucryptoauthlib
  - **You'll also need the EspressIf binary toolchain and SDK to build micropython firmware (esp32 port) i.e. some micropython modules (atecc608a driver, mqtt) will need to be frozen into the firmware else you'll run into memory constraints. 
  
# The Steps:
  1. Generate and store a (ECC) private key onboard the cryptochip 
 

# Usage:

Simply clone the repository and follow these steps
  - Wire up the sensors and board as shown in the picture. 
  - Flash the code onto the board - you'll probably
