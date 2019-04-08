#Import Libraries
import os, sys, re, time, requests
from datetime import datetime

#Libraries Necessary for rrunning script in Django Environment
sys.path.append('/home/pi/Documents/Netscan')
import setup
from home.models import setting as settings
from home.models import device as dev_model

#Check if command line argument for scanning interface was added correctly
try:
    interface = sys.argv[1]
    if("wlan0" not in interface and "eth0" not in interface):
        sys.exit('Invalid Interface!')
except:
    sys.exit("Please pass in a valid interface [eth0 / wlan0]")

#Create Device Class
class device:
       def __init__(self, device):
        #Set attributes.
        self.ip = device[0]
        self.mac = device[1]
        self.up = "0 Days 0:0:0"
        self.down = 0
        
        #Use only the first Mac returned by arp-scan
        regex = re.compile("(?:[0-9a-fA-F]:?){12}")
        self.mac = re.findall(regex, device[1])[0]
        
        #Macvendors API takes a URL with the MAC appended at the end.
        api_url = 'https://macvendors.co/api/vendorname/' + device[1]
        vendor = str(requests.get(api_url).content).split("'")[1]
        self.name = vendor
    
#Scan function which performs the network scan and returns a list of devices. Each device is an instantiation of the "device" class.
def scan():
    #Create an empty list for each Device Class.
    device_list_class = []
    
    #Run the command, put the output into device_list, and turn it into a 2d array with names, ips, and macs.
    command = "sudo arp-scan -l -I " + interface
    device_list = os.popen(command).read()
    device_list = device_list.split('\n')
    regex = re.compile("\d{1,3}\.")
    device_list = [string for string in device_list if re.match(regex, string)]
    for i, d in enumerate(device_list):
        device_list[i] = d.split('\t')
    
    #If the device is not a duplicate, create a device objects for each new device and return the list.
    for d in device_list:
        if "(DUP:" not in d[2]: 
                device_list_class.append(device(d))
    return device_list_class

#Function which takes a device class and adds it into the database
def	add_device(d):
    dev_model.objects.create(device=d.name, ip=d.ip, mac=d.mac, uptime=d.up, down_flag=d.down, first_ping=datetime.now(), notification=False)

#Check if the scanned device exists in the database. If it does and the IP's do not match, delete the old entry from the database.
#Returns a list of devices that do not exist in the database.
def remove_existing_devices(devs):
    non_existent_devices = []
    for d in devs:
        try:
            obj = dev_model.objects.get(mac=d.mac)
            if(obj.ip != d.ip):
                obj.delete()
                non_existent_devices.append(d)
        except:
            non_existent_devices.append(d)
            
    return non_existent_devices

def check_new_devices():
    #Get all new devices
    new_devices = remove_existing_devices(scan())

    #For each device in the devices list, add it to the Database.
    for d in new_devices:
        add_device(d)
