# Final Project for the Course on Cyber-Physical Systems and IoT Security

The objective of this project is to implement the authentication protocol as described in
the provided reference paper. As well as that, we aim to provide an implementation of Secure Vaults, a storage
capability for keys.

The authentication protocol in use is a modulation of a three-way handshake protocol,
whereby both client and server challenge each other to provide means to authenticate
both parties.

1. At first the IoT device sends its device ID and session ID to the server. The device
ID is known by the server and validated.
2. If it is accepted, the server generates a random number r1 and a challenge C1 and
sends both to the client.
3. The client generates a key k1 from the keys in the challenge C1, random values
t1, r2 and a challenge C2, ensuring that C1 ̸ = C2. It then encrypts r1||t1||{C2, r2}
under k1 and sends it to the server.
4. In the next step the server verifies the client’s message by generating the key k1
from the keys in the challenge C1 themselves. With k1 it decrypts the message
and reviews whether r1 is in the message.
5. If r1 is incorrect, the server aborts. Otherwise it generates a random value t2 and
a new key k2, which is based on the challenge C2. The server then sends r2||t2
encrypted under k2 ⊕ t1 to the client.
6. Next the client generates k2 itself and decrypts the message. It checks whether r2
in the message is correct. If it is incorrect the client aborts.
7. In the end both the client and the server generate the session key t by computing
t1 ⊕ t2