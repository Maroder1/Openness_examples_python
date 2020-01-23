


import clr
clr.AddReference('C:\\Program Files\\Siemens\\Automation\\Portal V16\PublicAPI\\V16\\Siemens.Engineering.dll')
from System.IO import DirectoryInfo, FileInfo
import Siemens.Engineering as tia
import Siemens.Engineering.HW.Features as hwf
import Siemens.Engineering.Compiler as comp
import os


# 
# # Starting TIA and creating project
# 


#Starting TIA with UI, also possible to start without ui
print ('Starting TIA with UI')
mytia = tia.TiaPortal(tia.TiaPortalMode.WithUserInterface)




# Alternative code to connect to an allready running instance (uncomment to use)

processes = tia.TiaPortal.GetProcesses() # Making a list of all running processes
print (processes)
#process = processes[0]                   # Just taking the first process as an example
#mytia = process.Attach()
#myproject = mytia.Projects[0]




# Creating a new project. Using try/except in case project allready exists

project_path = DirectoryInfo ('C:\\Jonas\\TIA')
project_name = 'PythonTest'
try:
    myproject = mytia.Projects.Create(project_path, project_name)
except Exception as e:
    print (e)

#
# # Adding HW to the project
#


#Adding the main components

print ('Creating PLC1')
PLC1_mlfb = 'OrderNumber:6ES7 513-1AL02-0AB0/V2.6'
PLC1 = myproject.Devices.CreateWithItem(PLC1_mlfb, 'PLC1', 'PLC1')


print ('Creating IOnode1')
IOnode1_mlfb = 'OrderNumber:6ES7 155-6AU01-0BN0/V4.1'
IOnode1 = myproject.Devices.CreateWithItem(IOnode1_mlfb, 'IOnode1', 'IOnode1')


print ('Creating HMI1')
HMI1_mlfb = 'OrderNumber:6AV2 124-0GC01-0AX0/15.1.0.0'
HMI1 = myproject.Devices.CreateWithItem(HMI1_mlfb, 'HM1', None)

#ToDo Add start screen to avoid compilation error fo the HMI



# Adding IO cards to the PLC and IO station
# This is basic to show how it works, use loops with checks (CanPlugNew) to see if the slot is available
# CanPlugnew is not mandatory, but usefull in real code

if (PLC1.DeviceItems[0].CanPlugNew('OrderNumber:6ES7 521-1BL00-0AB0/V2.1','IO1',2)): 
    PLC1.DeviceItems[0].PlugNew('OrderNumber:6ES7 521-1BL00-0AB0/V2.1','IO1', 2)

    
if (IOnode1.DeviceItems[0].CanPlugNew('OrderNumber:6ES7 131-6BH01-0BA0/V0.0','IO1',1)):
    IOnode1.DeviceItems[0].PlugNew('OrderNumber:6ES7 131-6BH01-0BA0/V0.0','IO1', 1)



#
# # Creating network, iosytem and setting IP adresses
# 


#creating a list of all found network interfaces on all stations in the station list
n_interfaces = []
for device in myproject.Devices:
    device_item_aggregation = device.DeviceItems[1].DeviceItems
    for deviceitem in device_item_aggregation:
        network_service = tia.IEngineeringServiceProvider(deviceitem).GetService[hwf.NetworkInterface]()
        if type(network_service) is hwf.NetworkInterface:
            n_interfaces.append(network_service)




# Assigning an IP to each item in the list (dirty code, but to demonstrate how theAPI works)

n_interfaces[0].Nodes[0].SetAttribute('Address','192.168.0.130')
n_interfaces[1].Nodes[0].SetAttribute('Address','192.168.0.131')
n_interfaces[2].Nodes[0].SetAttribute('Address','192.168.0.132')



# Creating subnet and IO system on the first item in the list
# Connects to subnet for remaining devices, if IO device it gets assigned to the IO system
for n in n_interfaces:
    if n_interfaces.index(n) == 0:
        subnet = n_interfaces[0].Nodes[0].CreateAndConnectToSubnet("Profinet")
        ioSystem = n_interfaces[0].IoControllers[0].CreateIoSystem("PNIO");
    else:
        n_interfaces[n_interfaces.index(n)].Nodes[0].ConnectToSubnet(subnet)
        if (n_interfaces[n_interfaces.index(n)].IoConnectors.Count) >> 0:
            n_interfaces[n_interfaces.index(n)].IoConnectors[0].ConnectToIoSystem(ioSystem);



#
# # Compiling HW & SW
# 



# Defining method to recursively print error messages
def print_comp(messages):
    for msg in messages:
        print(f'Path: {msg.Path}')
        print(f'DateTime: {msg.DateTime}')
        print(f'State: {msg.State}')
        print(f'Description: {msg.Description}')
        print(f'Warning Count: {msg.WarningCount}')
        print(f'Error Count: {msg.ErrorCount}\n')
        print_comp(msg.Messages)
    
# Compiling all devices
for device in myproject.Devices:
    compile_service =  device.GetService[comp.ICompilable]()
    result = compile_service.Compile()
                
    #Printing results from compiler
    print(f'State: {result.State}')
    print(f'Warning Count: {result.WarningCount}')
    print(f'Error Count: {result.ErrorCount}')
    print_comp(result.Messages)   

        


#
# # Option to compile SW only
# 



# Defining method to recursively print error messages
def print_comp(messages):
    for msg in messages:
        print(f'Path: {msg.Path}')
        print(f'DateTime: {msg.DateTime}')
        print(f'State: {msg.State}')
        print(f'Description: {msg.Description}')
        print(f'Warning Count: {msg.WarningCount}')
        print(f'Error Count: {msg.ErrorCount}\n')
        print_comp(msg.Messages)
    
#compiling all sw in all devices
for device in myproject.Devices:
    device_item_aggregation = device.DeviceItems
    for deviceitem in device_item_aggregation:   
            software_container = tia.IEngineeringServiceProvider(deviceitem).GetService[hwf.SoftwareContainer]()
            if (software_container != None):
                print(f'compiling: {deviceitem.Name}')
                software_base = software_container.Software
                
                compile_service =  software_base.GetService[comp.ICompilable]()
                result = compile_service.Compile()
                
                #Printing results from compiler
                print(f'State: {result.State}')
                print(f'Warning Count: {result.WarningCount}')
                print(f'Error Count: {result.ErrorCount}')
                print_comp(result.Messages)   



#
# # Exporting 
#     


#Optional code to remove xml files that may allready exist on your computer
try:
    os.remove('C:\\Jonas\\TIA\\exports\\dummy.xml')
except OSError:
    pass
try:
    os.remove('C:\\Jonas\\TIA\\exports\\Main.xml')
except OSError:
    pass


# exporting "main" from PLC1

#export_path = FileInfo ('C:\\Jonas\\TIA\\exports\\Main.xml')
software_container = tia.IEngineeringServiceProvider(PLC1.DeviceItems[1]).GetService[hwf.SoftwareContainer]()
software_base = software_container.Software
plc_block = software_base.BlockGroup.Blocks.Find("Main")
plc_block.Export(FileInfo('C:\\Jonas\\TIA\\exports\\Main.xml'), tia.ExportOptions.WithDefaults)

# Exporting tagtable from PLC1
tag_table_group = software_base.TagTableGroup
#creating a dummy table to export
tagtable = tag_table_group.TagTables.Create("dummy")
tagtable = tag_table_group.TagTables.Find("dummy")
tagtable.Export(FileInfo('C:\\Jonas\\TIA\\exports\\dummy.xml'), tia.ExportOptions.WithDefaults)


#deleting block and tag table in project 
plc_block.Delete()
tagtable.Delete()


#
# # Importing
# 



# Importing the xml files back in to the project
tag_table_group.TagTables.Import(FileInfo('C:\\Jonas\\TIA\\exports\\dummy.xml'), tia.ImportOptions.Override)
software_base.BlockGroup.Blocks.Import(FileInfo('C:\\Jonas\\TIA\\exports\\Main.xml'), tia.ImportOptions.Override)




myproject.Save()




#myproject.Close()




#mytia.Dispose()

