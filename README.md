# Computer_Networks

I. Multi-Node Chatroom & RPS Game Engine

This project is a functional, multi-user application built using Python Sockets. Developed as a final task for a Computer Networks course, it demonstrates real-time data transmission and application-layer logic.


II. Core Features

1. Real-Time Chat: Enables multiple clients to connect to a central server and broadcast messages to all connected peers.

2. Integrated Mini-Game: Includes a built-in Rock Paper Scissors (RPS) game option, allowing users to challenge and play against other connected players in real-time.

3. Hardware Versatility: The system can be deployed on a single local machine for testing or distributed across a network using hardware like a Raspberry Pi.

4. Socket Management: Handled via Server.py (broadcasting and connection handling) and Client.py (individual player interface).


III. Network Analysis (Wireshark)

To verify the protocol's performance, We used Wireshark to capture and analyze the TCP/IP traffic:

Trace File: Final Task testrun.pcapng contains the packet-level capture of the chat and game session.

Verification: Confirms successful 3-way handshakes and the efficient transmission of game-state data segments.


IV. Credits

1. Anirudh Gopishankar

2. Yohan Amaratunga
