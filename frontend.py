from backend import *
from tkinter import *

home = SmartHome()
mainWin = Tk()
widgetTypes = ["textBox", "configButton", "toggleButton"]

def setUpHome():
    """
    This sets up the specified smart home.
    """
    plug1 = SmartPlug()
    plug2 = SmartPlug()
    plug3 = SmartPlug()
    washer1 = SmartWashingMachine()
    washer2 = SmartWashingMachine()
    deviceList = [plug1, plug2, plug3, washer1, washer2]
    for device in deviceList:
        home.addDevice(device)

def rowSetUp(device, row, index):
    """
    This function takes a device from the smart home and sets up the graphics and buttons options for said device.
    """
    device.setUpText(row[0], index, device)

    device.setUpToggle(row[1])
    toggleBtn = device.getWidgets()[widgetTypes[2]]
    toggleBtn.configure(command=lambda device=device: toggleDevice(device))

    device.setUpConfig(row[2])
    configBtn = device.getWidgets()[widgetTypes[1]]
    configBtn.configure(command=lambda device=device: configWindow(device))

def setUpMainWin():
    """
    This sets up and designs the main window of the app. It is where everything to do with the window is initialised.
    """
    numOfDevices = len(home.getDevices())
    mainWin.title("Smart Home")
    mainWin.resizable(False, False)
    mainWin.grid_columnconfigure((0), uniform="uniform", weight=3)
    
    frames = []
    for row in range(numOfDevices+4):
        mainWin.rowconfigure(row, weight=1)
        framesRow = []
        for col in range(3):
            frame = Frame(mainWin)
            frame.grid_propagate(0)
            frame.grid(row=row, column=col, sticky=NSEW)
            framesRow.append(frame)
        frames.append(framesRow)
    
    home.displayTotalOn((frames[numOfDevices+3])[0])

    titleWin = Label((frames[0])[0], text="Smart Home", font=('Arial', 20, 'bold'))
    titleWin.pack(expand=True, fill="both")

    turnOnAllBtn = Button((frames[1])[0], text="Turn all off", command=lambda: turnOffAllDevices(), pady=5)
    turnOnAllBtn.pack(fill=BOTH, expand=True)

    turnOffAllBtn = Button((frames[2])[0], text="Turn all on", command=lambda: turnOnAllDevices(), pady=5)
    turnOffAllBtn.pack(fill=BOTH, expand=True)

    for row in range(3, numOfDevices+3):
        index = row-3
        frameList = frames[row]
        device = home.getDeviceAt(index)
        rowSetUp(device, frameList, index)
 
    deleteDeviceBtn = Button((frames[numOfDevices+3])[1], text="Delete Devices", command=lambda: deleteDevice(frames))
    deleteDeviceBtn.pack(side=LEFT, expand=True, fill="both")

    addDeviceBtn = Button((frames[numOfDevices+3])[2], text="Add Device", command=lambda: addDevice(frames))
    addDeviceBtn.pack(side=LEFT, expand=True, fill="both")

    mainWin.mainloop()

def turnOffAllDevices():
    """
    This turns off all the devices in the smart devices in a smart home and updates the main window.
    """
    home.turnOffAll()
    for index in range(len(home.getDevices())):
        device = home.getDeviceAt(index)
        newDevice = "{}.".format(index+1) + str(device)
        textBox = device.getWidgets()[widgetTypes[0]]
        textBox.delete("1.0", "end")
        textBox.insert("1.0", newDevice)
    totalOnDevices = home.countTotalOn()
    home.updateTotalOn(totalOnDevices)

def turnOnAllDevices():
    """
    This turns on all the devices in the smart devices in a smart home and updates the main window.
    """
    home.turnOnAll()
    for index in range(len(home.getDevices())):
        device = home.getDeviceAt(index)
        newDevice = "{}.".format(index+1) + str(device)
        textBox = device.getWidgets()[widgetTypes[0]]
        textBox.delete("1.0", "end")
        textBox.insert("1.0", newDevice)
    totalOnDevices = home.countTotalOn()
    home.updateTotalOn(totalOnDevices)

def toggleDevice(device):
    """
    This turns a specific device at the specified index on/off.
    """
    index = home.getIndex(device)
    device.toggleSwitch()
    newDevice = "{}.".format(index+1) + str(device)
    textBox = device.getWidgets()[widgetTypes[0]]
    textBox.delete("1.0", "end")
    textBox.insert("1.0", newDevice)
    totalOnDevices = home.countTotalOn()
    home.updateTotalOn(totalOnDevices)
            
def configWindow(device):
    """
    This opens a top level window to give the user an opportunity to edit the options of the given device and updates the window
    to reflect those changes.
    """
    index = home.getIndex(device)
    configWin = Toplevel()
    configWin.geometry("400x150")
    configWin.resizable(False, False)
    configWin.transient(mainWin)
    configWin.grab_set()

    deviceName = device.getDeviceName()
    configWin.title("Configure {}".format(deviceName))

    def changeWasherOption():
        """
        This gives the user an opportunity to change the option of their smart washing machine if that is the device selected.
        """
        options = device.getWashOptions()
        start_option = StringVar(configWin)
        start_option.set("{}".format(options[0]))
        dropmenu = OptionMenu(configWin,start_option, *options)
        dropmenu.pack()
        def getChoice():
            """
            This gets the chosen option from the option menu widget. and destroys the top level window.
            """
            option_choice = start_option.get()
            device.setWashMode(option_choice)
            newDevice = "{}.".format(index+1) + str(device)
            washer = device.getWidgets()[widgetTypes[0]]
            washer.delete("1.0", "end")
            washer.insert("1.0", newDevice)
            configWin.destroy()
        doneBtn = Button(configWin, text="Done", font=("Arial", 15, 'bold'), command=getChoice)
        doneBtn.pack()
    
    def changePlugOption():
        """
        This gives the user an opportunity to change the consumption rate of the smart plug device selected from the smart home.
        """
        consumptionSlider = Scale(configWin, from_=0, to=150, orient=HORIZONTAL, length=380, tickinterval=10)
        consumptionSlider.grid(row=0, sticky=W+E)
        def getConsumtion():
            """
            This gets the chosen consumption rate of the selected smart plug device from the smart home.
            """
            rate = consumptionSlider.get()
            device.setConsumptionRate(rate)
            newDevice = "{}.".format(index+1) + str(device)
            plug = device.getWidgets()[widgetTypes[0]]
            plug.delete("1.0", "end")
            plug.insert("1.0", newDevice)
            configWin.destroy()
        doneBtn = Button(configWin, text="Done", font=("Arial", 15, 'bold'), command=getConsumtion)
        doneBtn.grid(row=1)

    commandKey = {
        "Smart Plug" : changePlugOption,
        "Smart Washing Machine" : changeWasherOption
    }
    commandKey[deviceName]()


def deleteDevice(frames):
    """
    This command deletes a device selected by the user from an option menu if there is still a device in the smart home and updates the window
    to reflect the users choice.
    """
    if len(home.getDevices()) > 0:
        configWin = Toplevel()
        configWin.geometry("400x100")
        configWin.resizable(False, False)
        configWin.title("Delete Device")
        configWin.rowconfigure((0,1), uniform="uniform", weight=1)
        configWin.columnconfigure((0), uniform="uniform", weight=2)
        configWin.transient(mainWin)
        configWin.grab_set()

        insrtuctionTxt = Text(configWin)
        insrtuctionTxt.insert("1.0", """
Please select a device to delete:""")
        insrtuctionTxt.grid(row=0, column=0, sticky=N+S+E+W)

        deviceNames = []
        for index in range(len(home.getDevices())):
            name = "{}.".format(index+1) + (home.getDeviceAt(index)).getDeviceName()
            deviceNames.append(name)
        start_option = StringVar(configWin)
        start_option.set("{}".format(deviceNames[0]))
        selction = OptionMenu(configWin, start_option, *deviceNames)
        selction.grid(row=0, column=1, sticky=N+S+E)

        def getDeleteChoice():
            """
            This command gets the device chosen from the smart home and deletes from the smart home.
            """
            choice = start_option.get()
            choiceIndex = int(choice[0])-1
            configWin.destroy()
            deleteSelection(choiceIndex, frames)
        doneBtn = Button(configWin, text="Done", font=30, command=getDeleteChoice)
        doneBtn.grid(row=1, columnspan=2, sticky=N+S+W+E)
    else:
        configWin = Toplevel()
        configWin.transient(mainWin)
        configWin.grab_set()
        messageLabel = Label(configWin, text="No more devices to delete!", font=("Arial", 24, "bold"))
        messageLabel.pack()
        cancelBtn = Button(configWin, text="Cancel", command=configWin.destroy)
        cancelBtn.pack()

    
def deleteSelection(index, frames):
    """
    this command identifies the chosen device to be deleted and updates the main window after destroying the top level 
    window.
    """
    home.deleteDeviceAt(index)
    refreshMainWinDel(frames, index+3)
    orderNum = 1
    for smartD in home.getDevices():
        textBox = (smartD.getWidgets())[widgetTypes[0]]
        textCurrent = textBox.get("1.0", END)
        newText = textCurrent[2:]
        newDevice = "{}.".format(orderNum) + newText
        orderNum += 1
        textBox.delete("1.0", "end")
        textBox.insert("1.0", newDevice)
    totalOnDevices = home.countTotalOn()
    home.updateTotalOn(totalOnDevices)

def refreshMainWinDel(frames, rowToDelete):
    """
    This command takes the row of the data that needs to be deleted and removes all frames from that row on the window
    and moves all subsequent rows and frames up one row to fill the empty space.
    """
    for index, row in enumerate(frames):
        col = 0
        for frame in row:
            if index == rowToDelete:
                for widgets in frame.winfo_children():
                    widgets.destroy()
                frame.destroy()
            elif index > rowToDelete:
                frame.grid_remove()
                frame.grid(row=index-1, column=col)
                col += 1
    del frames[rowToDelete]

def addDevice(frames):
    """
    This command opens a top level window where the user can accept the type of device to be added to the smart home object 
    and updates the window accordingly.
    """
    numOfDevices = len(home.getDevices())
    configWin = Toplevel()
    configWin.geometry("400x200")
    configWin.resizable(False, False)
    configWin.title("Delete Device")
    configWin.rowconfigure((0,1,2), uniform="uniform", weight=1)
    configWin.columnconfigure(0, uniform="uniform", weight=1)
    configWin.transient(mainWin)
    configWin.grab_set()

    instructionTxt = Text(configWin)
    instructionTxt.insert("1.0", "Please select a device from below to add:")
    instructionTxt.grid(row=0, column=0)

    deviceTypes = ["Smart Plug", "Smart Washing Machine"]
    start_option = StringVar(configWin)
    start_option.set("{}".format(deviceTypes[0]))
    selction = OptionMenu(configWin, start_option, *deviceTypes)
    selction.grid(row=1)

    def addDeviceCommand():
        """
        This calls the function that needs to be run when the add device button is called and include the needed variables to run
        the function.
        """
        addDeviceProcess(start_option.get(), numOfDevices, frames)
        configWin.destroy()
    doneBtn = Button(configWin, text="Done", command=addDeviceCommand)
    doneBtn.grid(row=2, sticky=N+W+S+E)

def addDeviceProcess(selection, numOfDevices, frames):
    """
    This identifies the device chosen by the user and add said dvice to the smart home object and updates the main window after destroying the
    top level window.
    """
    devices = {
        "Smart Plug": SmartPlug,
        "Smart Washing Machine": SmartWashingMachine
        }
    choice = devices[selection]()
    home.addDevice(choice)
    lastRow = frames[numOfDevices+3]
    newRow = []
    for index, frame in enumerate(lastRow):
        frame.grid_remove()
        newFrame = Frame(mainWin)
        newFrame.grid(row=numOfDevices+3, column=index, sticky=NSEW)
        newRow.append(newFrame)
        frame.grid(row=numOfDevices+4, column=index, sticky=NSEW)
    frames.insert(numOfDevices+3, newRow)
    rowSetUp(choice, newRow, numOfDevices)
    
def main():
    """
    This is the main function that runs all the above code.
    """
    setUpHome()
    setUpMainWin()

main()
