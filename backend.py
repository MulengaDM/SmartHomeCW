from tkinter import *

class SmartDevice():
    """
    This class is the parent that includes the defaults for any smart device, including the power status, and the ability to toggle the
    power status. aswell as the empty variable for the name of a device.
    """
    def __init__(self):
        self.switchedOn = False
        self.name = None
        self.widgets = {}
    def toggleSwitch(self):
        """
        This method turns the Device on or off.
        """
        if self.switchedOn == False:
            self.switchedOn = True
        else:
            self.switchedOn = False
    def getDeviceStatus(self):
        """
        this method returns whether or not the device is on.
        """
        if self.switchedOn == True:
            return "On"
        else: 
            return "Off"

    def getDeviceName(self):
        """
        This returns the device name.
        """
        return self.name
    def setUpText(self, frame, index, device):
        """
        This function creates the text box and inserts the devices information, given the frame and index of said deivce.
        """
        deviceText = Text(frame, height=1, pady=20)
        deviceLabel = "{}.".format(index+1) + str(device)
        deviceText.insert("1.0", deviceLabel)
        deviceText.pack(side=LEFT, expand=False, fill="both")
        self.widgets["textBox"] = deviceText
    def setUpConfig(self, frame):
        """
        This function creates the button to configure the options of the current device.
        """
        configBtn = Button(frame, text="Configure")
        configBtn.pack(side=LEFT, expand=True, fill="both")
        self.widgets["configButton"] = configBtn

    def setUpToggle(self, frame):
        """
        This function creates the button to toggle the current device.
        """
        deviceBtn = Button(frame, text="Toggle this")
        deviceBtn.pack(side=LEFT, expand=True, fill="both")
        self.widgets["toggleButton"] = deviceBtn
    def getWidgets(self):
        """
        This function retruns the dictionary contain the widgets connected to the device.
        """
        return self.widgets

class SmartPlug(SmartDevice):
    """
    This creates a Smart plug object that is by default turned off and has a default of zero consumption rate.
    """
    def __init__(self):
        super().__init__()
        self.consumptionRate = 0
        self.name = "Smart Plug"
    def setConsumptionRate(self, rate):
        """
        This method sets the consumption rate of the plug.
        """
        if 0 <= rate <= 150:
            self.consumptionRate = rate
        else:
            return(print("Invalid consumption rate entered!"))
    def getConsumptionRate(self):
        """
        This method returns the consumption rate of the plug.
        """
        return self.consumptionRate
    def __str__(self):
        if self.switchedOn == True:
            status = "ON"
        else:
            status = "OFF"
        output = "Smart plug: {} | Consumption rate: {}".format(status, self.consumptionRate)
        return output

class SmartWashingMachine(SmartDevice):
    """
    This creates a Smart washing machine obejct. 
    The object contains whether it is on or off and a wash  mode. 
    The available wash modes are Daily wash, Quick wash, Eco.
    """
    def __init__(self):
        super().__init__()
        self.washMode_list = ["Daily wash", "Quick wash", "Eco"]
        self.washMode = "Daily wash"
        self.name = "Smart Washing Machine"
    def setWashMode(self, mode):
        """
        This sets the wash mode of the device, only accepts "Daily wash", "Quick wash" or "Eco".
        """
        if mode in self.washMode_list:
            self.washMode = mode
        else:
            return(print("Invalid wash mode entered!"))
    def getWashMode(self):
        """
        This returns the current wash mode of the device.
        """
        return self.washMode
    def getWashOptions(self):
        """
        This returns a list of the options for this device.
        """
        return self.washMode_list
    def __str__(self):
        if self.switchedOn == True:
            status = "ON"
        else:
            status = "OFF"
        output = "Washing machine: {} | Wash mode: {}".format(status, self.washMode)
        return output

class SmartHome():
    """
    This creates a smart home object in which a group of devices can be stored.
    """
    def __init__(self):
        self.devices = []
    def getDevices(self):
        """
        this returns a group of all the devices in the smart home object.    
        """
        return self.devices
    def getDeviceAt(self, index):
        """
        This retruns the specific device at a certain index in the smart home object.
        """
        return self.devices[index]
    def addDevice(self, device):
        """
        This adds a device to the smart home object.
        """
        self.devices.append(device)
    def toggleSwitch(self, index):
        """
        This turns the device at a certain index on or off.
        """
        self.devices[index].toggleSwitch()
    def turnOnAll(self):
        """
        This turns on all the devices inside a smart home object.
        """
        for device in self.devices:
            if device.getDeviceStatus() == "Off":
                device.toggleSwitch()
    def turnOffAll(self):
        """
        This turns off all the devices inside a smart home object.
        """
        for device in self.devices:
            if device.getDeviceStatus() == "On":
                device.toggleSwitch()
    def deleteDeviceAt(self, index):
        """
        This command deletes a device from the smart home object given the index of said device.
        """
        del self.devices[index]
    def getIndex(self, device):
        """
        This command returns the index of a given device in the smart home.
        """
        if device in self.devices:
            return self.devices.index(device)
        else:
            print("Entered device not in smart home")
    def __str__(self):
        output = "Your smart home contains:\n"
        for i in range(len(self.devices)):
            output += "{}\n".format(self.devices[i])
        return output
    def countTotalOn(self):
        """
        This command returns a count of the total smart devices that are currently turned on.
        """
        count = 0
        for device in self.devices:
            if device.getDeviceStatus() == "On":
                count += 1
        return count
    def displayTotalOn(self, frame):
        """
        This command calculates the total number of devices that are on and displays the total that are on.
        """
        count = 0
        for device in self.devices:
            if device.getDeviceStatus() == "On":
                count += 1
        self.totalOnLabel = Label(frame, text="Total activated: {}".format(count), font=("Arial", 16), pady=15)
        self.totalOnLabel.pack(fill="both", expand=TRUE)
    def updateTotalOn(self, count):
        """
        This command updates the total on label to the inputted count.
        """
        self.totalOnLabel.configure(text="Total activated: {}".format(count))


