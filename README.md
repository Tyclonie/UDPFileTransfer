# UDP File Transfer
- This is PRE-RELEASE and is currently not fully functional and is feature limited!
- FTP (File Transfer Protocol) uses the TCP protocol to tranfer files within a network. I present to you a program which uses the UDP protocol to transfer files across networks.

## How to use
- Run main.py and setup a server on your server by selecting option 1, you will need a client to complete the setup so start a client on another device by selecting option 2. Complete the instructions displayed on the screen, but enter the port on the server first!
- If you need a second client to be able to connect to the server at a different time, you can go into the first client, go to /opt/client_data and open the text file named as the servers IP address you used to connect. Copy the salt (the contents of the text file) and run the main.py on the client you want to setup, select option 3 and follow the steps on screen.

### As a side note and a few warnings
- The use of this potentially isn't necessary but saw it as a cool little project to work on as I had urges to program.
- Please not the application may not be very secure. With it being password protected with a salt generated for each server/client and hashed using bcrypt, the file transfer is not encrypted as of yet (if I add it). So file snooping may be easy with packet sniffers.
