''' 
This test is designed for a simple check to see if follower drone actually follows the leader drone. 
We tested it by holding the leader drone in our hand and let the follower drone takeoff and follow the leader.
'''

'''
argv[] = [<"base" or "rover">, <base's IP>, <port number>]
'''
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import sys
import math
import socket
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from Drone import Drone
from RepeatTimer import RepeatTimer, sendMsg
from Internet import checkInternetConnection

SEND_INTERVAL = 1 
SLEEP_LENGTH = 0.5
baseDroneIP="tcp:127.0.0.1:5762"
roverDroneIP="tcp:127.0.0.1:5772"

if(len(sys.argv) <4): 
    print("Should have 3 arguments: argv[] = [<'base' or 'rover'>, <base's IP>, <port number>]")
    # python 5_simpleFollow.py base 127.0.0.1 12345
    sys.exit()

if(sys.argv[1] == "base"):
    baseDrone = Drone(baseDroneIP)
    print("=====BASE=====")
    ''' Setting up server '''
    ip = sys.argv[2]
    port = int(sys.argv[3])
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    server.listen(5)
    client, address = server.accept()
    print("Base Connection established")
    baseDrone.takeoff(25)
    sendMsgTimer = RepeatTimer(SEND_INTERVAL,sendMsg, args=(baseDrone, client,))
    sendMsgTimer.start()
    #baseDrone.takeoff(25)
    while(1):
        print("Base in while loop")
        time.sleep(1)

elif(sys.argv[1] == "rover"):
    roverDrone = Drone(roverDroneIP)
    print("=====ROVER=====")

    ''' Setting up client '''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = sys.argv[2]
    port = int(sys.argv[3])
    client.connect((ip,port))
    print("Rover Connection Established")
    roverDrone.takeoff(15)
    
    counter=0
    numInvalidMsg = 0
    ''' 
    We only want our iterations be counted when the drone actually goes to the point, 
    so only increment counter when the received message is valid. 
    numInvalidMsg is a safety measure that makes sure if the rover forever receives outdated (invalid) message, 
    we will break from the loop and land.
    '''
    #while(numInvalidMsg < 5 and counter<5):
    try:
        while True:
            print("Enter Iteration",counter)
            targetPoint = roverDrone.receiveInfo(client)
        
            if(type(targetPoint) == LocationGlobalRelative):
                targetPoint.alt = 15
                print("Received target:",targetPoint)
                roverDrone.flyToPoint(targetPoint, 3)
                counter = counter+1
                numInvalidMsg = 0
            else:
                numInvalidMsg = numInvalidMsg + 1
            time.sleep(SLEEP_LENGTH)
    except KeyboardInterrupt:
        roverDrone.land()
        roverDrone.vehicle.close()
    # Terminate program and socket 
else:
    print("Please specify which drone it is")
    