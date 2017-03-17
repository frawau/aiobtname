# aiobtname

aiobtname is a Python 3/asyncio library to detect devices present using Bluetooth 
"request name" command.

Its single minded purpose is to detect "presence" using devices' MAC address. 

I could not find anything this simple anywhere so I decided to write it myself. I am aware 
of "scapy", it is a fabulous networking toolbox, but it an overkill for the use I intended.

Also most other solutions rely on external utilities ('l2ping', 'hcitool', ...) this library
is pure python, but you do need a fairly recent Linux kernel.

If this look to you as a hack, it's probably because it is.

# Installation

We are on PyPi so

     pip3 install aiobtname

or

     python3 -m pip install aiobtname
     
# Trying it out

The module can be executed with

    python3 -m aiobtname [<iface number>] <mac address> [<mac address>]

The interface number is optional, and defaults to 0. Use hciconfig to find out your
interface number, hci1 is 1 and so on....
    
# How to use

Using it is quite simple.

    1- Create a bluetooth socket:
    
            mysocket = create_bt_socket(iface)
            
               The parameter is an integer, the number associated
               with the Bluetooth adapter you want to use. Running
               "hciconfig" will list the BT adapters. For hci0, use 0 
               for hci1, use 1 and so on. If no iface is given, 0 is
               assumed
               
    2- Start the asyncio.Protocol
    
            fac=event_loop.create_connection(BTNameRequester,sock=mysocket)
            conn,btctrl = event_loop.run_until_complete(fac)
 
    3- Tell it what to do with the result
    
            btctrl.process=my_process
            
                my_process should be a function that takes 1 parameter,
                a dictionary with 2 keys:
                    mac:  the  MAC address of the answering device
                   name:  the name of the answering device
                  
                It will be called for every successful answer.
                   
    4- Send the name request
        
            btctrl.request(mac_list)
            
                The parameter is a  list of mac addresses yo be queried
                            

                
    The BTNameRequester won't stop listening until it is closed. It is the responsablitu
    of the application to manage that.
    
# Rant

This is part of AutoBuddy trying to detect presence. We wrote aioarping, a pure python library
to detect devices over the LAN using ARP Request, but this has proven to be quite unreliable
because many devices (read Smartphones, both Android and iOS) only answer the ARP request in 
the most haphazard way, even when told to keep listening to the LAN at all time. So this is meant to
complement aioarping. Note that this will not cover BLE devices, we'll have something else (aiobleprobe?) 
for that