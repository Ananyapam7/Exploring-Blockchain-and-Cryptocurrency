# Man-in-the-middle(MITM) Attack

A Man-in-the-Middle (MITM) attack occurs when a communication between two systems is intercepted by an outside entity. This can happen with in any network or any form of online communication, such as email, social media, web surfing, online banking etc.
The common goal of an attack is to steal personal information, is to gain login credentials, account details and credit card numbers or digital resource.

In a network, computers use the IP Address to communicate with other devices, however, in reality, the communication happens over the MAC Address. ARP is used to find out the MAC Address of a particular device whose IP address is known. For instance, a device wants to communicate with the other device on the network, then the sending device uses ARP to find the MAC Address of the device that it wants to communicate with. ARP involves two steps to find the MAC address:

1. The sending device sends an ARP Request containing the IP Address of the device it wants to communicate with. This request is broadcasted meaning every device in the network will receive this but only the device with the intended IP address will respond.
2. After receiving the broadcast message, the device with the IP address equal to the IP address in the message will send an ARP Response containing its MAC Adress to the sender.

# What is ARP Spoofing?

ARP spoofing is a Man In The Middle (MITM) attack in which the attacker sends forged ARP Messages. This allows the attacker to pretend as a legitimate user as it links the attacker machine’s MAC Address to the legitimate IP Address. Once the MAC Address has been linked the attacker will now receive the messages intended for the legitimate IP Address. Furthermore, ARP Spoofing allows the attacker to intercept, modify, and drop the incoming messages.

ARP Spoofing is only possible on 32-bit IP Addresses (IPv4) and not on IPv6.However, it is widely used because most of the internet still works on IPv4.

# Why is ARP Spoofing possible?

ARP was designed for security. There are two reasons why ARP spoofing is possible.

1. The machines in a network accept ARP Responses even if they haven’t sent an ARP Request.
2. The machines trust these ARP Responses without any verification

# What is a Packet Sniffer?
A packet sniffer is a tool that is used to monitor networks and to diagnose any network problems. Packet sniffers log network traffic on a network interface that they have access to. It can see every packet that flows to and from an interface.

In this I have implimented a MITM attack where wrote I Python script on (ARP Spoofing) that allows us to become a Man In The Middle and then the goal of the packet sniffer is to capture the victim’s network traffic and extract the visited URLs and credentials.

