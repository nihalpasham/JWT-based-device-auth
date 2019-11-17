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
