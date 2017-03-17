import sys,asyncio
import aiobtname

if len(sys.argv) <= 1:
    print("Error: Usage is {} [adapter nb] <mac address> [<mac address>]".format(sys.argv[0]))
    sys.exit(-1)

def my_process(data):
    print ("Heard from MAC:      {} {}".format(data["mac"],data["name"]))
    print()
    
mac_list=[]
try:
    mydev=int(sys.argv[1])
    if len(sys.argv) <= 2:
        print("Error: Usage is {} [adapter nb] <mac address> [<mac address>]".format(sys.argv[0]))
        sys.exit(-1)
    for x in sys.argv[2:]:
        mac_list.append(x)
except:
    mydev=0
    for x in sys.argv[1:]:
        mac_list.append(x)


event_loop = asyncio.get_event_loop()

#First create and configure a raw socket
mysocket = aiobtname.create_bt_socket(mydev)

#create a connection with the raw socket
fac=event_loop.create_connection(aiobtname.BTNameRequester,sock=mysocket)
#Start it
conn,btctrl = event_loop.run_until_complete(fac)
#Attach your processing 
btctrl.process=my_process
#Probe
btctrl.request(mac_list)
try:
    # event_loop.run_until_complete(coro)
    event_loop.run_forever()
except KeyboardInterrupt:
    print('keyboard interrupt')
finally:
    print('closing event loop')
    conn.close()
    event_loop.close()