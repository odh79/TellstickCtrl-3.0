import optparse
import td
import time



def NewName(Name):
    NameLen = len(str(Name))
    Name = str(Name)[2:NameLen-1]
    
    return Name

def getDeviceIdAndName(In):
    if (In.isdigit()):
        deviceId = int(In)
        deviceName = td.getName(int(In))
    else:
        deviceId, deviceName = td.getDeviceIdFromStr(In)

    return deviceId, deviceName

def SendOn(device):
    deviceId, deviceName = getDeviceIdAndName(device)
    resCode = td.turnOn(deviceId)
    if resCode != 0:
        res = td.getErrorString(resCode)
    else:
        res = 'Success'
    print('Turning on device:', deviceId, deviceName, '-', res)
    
def SendOff(device):

    deviceId, deviceName = getDeviceIdAndName(device)
    resCode = td.turnOff(deviceId)
    if resCode != 0:
        res = td.getErrorString(resCode)
    else:
        res = 'Success'
    print('Turning off device:', deviceId, deviceName, '-', res)


def listDevices():

    print 'Number of devices:', td.getNumberOfDevices()
    for i in range(td.getNumberOfDevices()):
        deviceId = td.getDeviceId(i)
        cmd = td.lastSentCommand(deviceId, readable = True)
        if cmd == 'DIM':
            cmd += ':' + str(td.lastSentValue(i))
        # For 3.2 Name = NewName(td.getName(deviceId))
        Name = td.getName(deviceId)
        if len(str(Name)) <= 7:
            # print("Short Name:", len(Name))
            while len(Name) < 8:
                Name = Name + " "

        #  print (deviceId, '\t', Name, '\t', cmd, '\t\t', td.methods(deviceId, readable = True))
        print deviceId, '\t', Name, '\t', cmd, '\t\t'
    print ''

    