#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# This application is simply a python only Bluetooth Name Request 
# It is meant to be used for presence detection using devices MAC addresses
# 
# Copyright (c) 2017 François Wautier
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE

import socket, asyncio
from struct import pack, unpack


#A little bit of HCI
HCI_COMMAND = 0x01
HCI_EVENT = 0x04

CMD_NAME_REQUEST = 0x1904 #mixing the OGF in with that HCI shift


def create_bt_socket(interface=0):
    exceptions = []
    sock = None
    try:
        sock = socket.socket(family=socket.AF_BLUETOOTH,
                             type=socket.SOCK_RAW,
                             proto=socket.BTPROTO_HCI)
        sock.setblocking(False)
        sock.setsockopt(socket.SOL_HCI, socket.HCI_FILTER, pack("IIIh2x", 0xffffffff,0xffffffff,0xffffffff,0)) #type mask, event mask, event mask, opcode
        try:
            sock.bind((interface,))
        except OSError as exc:
            exc = OSError(
                    exc.errno, 'error while attempting to bind on '
                    'interface {!r}: {}'.format(
                        interface, exc.strerror))
            exceptions.append(exc)
    except OSError as exc:
        if sock is not None:
            sock.close()
        exceptions.append(exc)
    except:
        if sock is not None:
            sock.close()
        raise
    if len(exceptions) == 1:
        raise exceptions[0]
    elif len(exceptions) > 1:
        model = str(exceptions[0])
        if all(str(exc) == model for exc in exceptions):
            raise exceptions[0]
        raise OSError('Multiple exceptions: {}'.format(
            ', '.join(str(exc) for exc in exceptions)))
    return sock

###########

class BTNameRequester(asyncio.Protocol):
    '''Protocol handling the requests'''
    def __init__(self):
        self.transport = None
        self.smac = None
        self.sip = None
        self.process = self.default_process
    
    def connection_made(self, transport):
        self.transport = transport
            
    def connection_lost(self, exc):
        super().connection_lost(exc)
        
    def request(self, mac_addr):
        """Send Name request, mac_addr is a list of mac addresses"""
        for addr in mac_addr:
            self.send_name_request(addr)
       
    
        
    def send_name_request(self,mac_addr):
        '''Sending ARP request for given IP'''

        # make the frame :
        frame = [
            ### HCI header###
            # Destination MAC address  :
            pack('!B', HCI_COMMAND),
            pack('!H', CMD_NAME_REQUEST),
            #Length... we know it's 10
            pack('!B',0x0a),
            #MAC address
            int(mac_addr.replace(":",""),16).to_bytes(6,"little"),
            #Repeat
            pack('!B',0x02),
            pack('!B',0x00),
            pack('!B',0x00),
            pack('!B',0x00)
        ]
        
        self.transport.write(b''.join(frame)) # Sending
        
    def data_received(self, packet):
        resu=unpack("ssss",packet[:4])
        if resu[0]==b'\x04' and resu[1]==b'\x07' and resu[3]==b'\x00': #Essentially a successful answer
            raw_mac = packet[4:10]
            mac = ':'.join(a + b for a, b in list(zip(*[iter(raw_mac.hex())]*2))[::-1])
            name=packet[10:].strip(b'\x00').decode()
            self.process({"mac":mac,"name":name})
    
    def default_process(self,data):
        pass
    
