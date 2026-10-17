# Họ và tên: Nguyễn Trung Hiếu
# Mã số sinh viên: 202418898
from datetime import datetime, timedelta
import sys
from abc import ABC, abstractmethod
DeviceStatus = ("Available", "Borrowed", "UnderMaintenance")
Late_returning = []
class Device(ABC):
    def __init__(self, deviceid, name, year_into_use, cost, state, borrowlimit):
        if name == None or deviceid == None:
            print("Error: No blank name allowed.")
            sys.exit()
        if not cost>0:
            print("Error: The cost must be positive.")
            sys.exit()
        if year_into_use>int(datetime.now().year):
            print("Error: Unsuitable year into usage detected.")
            sys.exit()
        global DeviceStatus
        if not state in DeviceStatus:
            print("Error: Device state should either be available or borrowed or under maintenance")
            sys.exit()
        if not isinstance(borrowlimit, int) or borrowlimit<0:
            print("Error: Invalid borrow limit!")
            return None
        
        self.deviceid = deviceid
        self.name = name
        self.year_into_use = year_into_use
        self.state = state
        self.borrowlimit = borrowlimit
        @abstractmethod
        def MaintenanceCost(self):
            pass

        def Info(self):
            print(f"Device ID: {self.deviceid}")
            print(f"Device name:{self.name}")
            print(f"Device was first used in{self.year_into_use}")
            print(f"Device cost:{self.cost}")
            print(f"Device state:{self.state}")
            print(f"Borrow limit:{self.borrowlimit}")

class ACRemoteControl(Device):
    def __init__(self, deviceid, name, year_into_use, cost, state, borrowlimit):
        if deviceid == None or name == None:
            print("Error: No blank device ID or name allowed.")
            sys.exit()
        if not cost>0:
            print("Error: The cost must be positive.")
            sys.exit()
        if year_into_use>int(datetime.now().year):
            print("Error: Unsuitable year into usage detected.")
            sys.exit()
        global DeviceStatus
        if not state in DeviceStatus:
            print("Error: Device state should either be available or borrowed or under maintenance")
            sys.exit()
        if not isinstance(borrowlimit, int) or borrowlimit<0:
            print("Error: Invalid borrow limit!")
            return None

        super().__init__(deviceid, name, year_into_use, cost, state, borrowlimit)
        
    def MaintenanceCost(self):
        if int(datetime.now().year)-self.year_into_use>5:
            return 0.04*self.cost
        else:
            return 0.025*self.cost

class Micro(Device):
    def __init__(self, deviceid, name, year_into_use, cost, state, borrowlimit, Requires_Cable):
        if deviceid == None or name == None:
            print("Error: No blank device ID or name allowed.")
            sys.exit()
        if not cost>0:
            print("Error: The cost must be positive.")
            sys.exit()
        if year_into_use>int(datetime.now().year):
            print("Error: Unsuitable year into usage detected.")
            sys.exit()
        global DeviceStatus
        if not state in DeviceStatus:
            print("Error: Device state should either be available or borrowed or under maintenance")
            sys.exit()
        if not isinstance(Requires_Cable, bool):
            print("Error: Requires_Cable should either be True or False only")
            sys.exit()
        if not isinstance(borrowlimit, int) or borrowlimit<0:
            print("Error: Invalid borrow limit!")
            return None
        
        super().__init__(deviceid, name, year_into_use, cost, state, borrowlimit)
        self.Requires_Cable = Requires_Cable
        self.Maintain = 0.05*cost
    def MaintenanceCost(self):
        if int(datetime.now().year)-self.year_into_use>5:
            self.Maintain += 0.025*self.cost
        return self.Maintain
    
    def Info(self):
        print(f"Device ID: {self.deviceid}")
        print(f"Device name:{self.name}")
        print(f"Device was first used in{self.year_into_use}")
        print(f"Device cost:{self.cost}")
        print(f"Device state:{self.state}")
        print(f"Borrow limit:{self.borrowlimit}")
        print(f"Does it require cable? - {str(self.Requires_Cable)}")

class ProjectorRemoteControl(Device):
    def __init__(self, deviceid, name, year_into_use, cost, state, borrowlimit):
        if deviceid == None or name == None:
            print("Error: No blank device ID or name allowed.")
            sys.exit()
        if not cost>0:
            print("Error: The cost must be positive.")
            sys.exit()
        if year_into_use>datetime.now().year:
            print("Error: Unsuitable year into usage detected.")
            sys.exit()
        global DeviceStatus
        if not state in DeviceStatus:
            print("Error: Device state should either be available or borrowed or under maintenance")
            sys.exit()
        if not isinstance(borrowlimit, int) or borrowlimit<0:
            print("Error: Invalid borrow limit!")
            return None

        super().__init__(deviceid, name, year_into_use, cost, state, borrowlimit)
    
    def MaintenanceCost(self):
        if int(datetime.now().year)-self.year_into_use>5:
            return 0.03*self.cost
        else:
            return 0.02*self.cost

class ClassRoom:
    def __init__(self, roomid, name, capacity, devices_inside):
        if roomid == None or name == None:
            print("Error, room ID and room name cannot be blank!")
            sys.exit()
        if capacity<0 or type(capacity) is not int:
            print("Error, the capacity of the room must be a non-negative integer!")
            sys.exit()
        for i in range(0, len(devices_inside)-1, 1):
            if devices_inside[i] == None:
                print("Error: No null devices allowed!")
                return None
            for j in range(i+1, len(devices_inside)-1, 1):
                if devices_inside[j].deviceid == devices_inside[j].deviceid:
                    print("Error, you cannot have 2 devices with the same ID!")
                    return None

        self.roomid = roomid
        self.roomname = name
        self.capacity = capacity
        self.devices_inside = []
        for i in devices_inside:
            self.devices_inside.append(i)

    def addDevice(self, device):
        for i in self.devices_inside:
            if i.deviceid == device.deviceid:
                print("Error: ID already exists!")
                return None

        self.devices_inside.append(device)

    def removeDevice(self, deviceid):
        for i in self.devices_inside:
            if i.deviceid == deviceid:
                self.devices_inside.remove(i)
                return None

        print("Error, no device with device id found.")

    def FindDevice(self, deviceid):
        for i in self.devices_inside:
            if i.deviceid == deviceid:
                print("Device found! Device statistics:")
                print(f"{i.Info()}")
                return None
        
        print("Error, no device with device id found.")

    def CalculateAnnualMaintenanceCost(self):
        totalcost = 0
        for i in self.devices_inside:
            totalcost += i.MaintenanceCost()    
        return totalcost  

    def GetDevicesRequiringMaintenance(self):
        AllDevices = []
        for i in self.devices_inside:
            if i.state == "UnderMaintenance" or int(datetime.strftime("%Y"))-i.year_into_use>5:
                AllDevices.append(i)

        return AllDevices

class Lecturer:
    def __init__(self, id, name):
        if id == None or isinstance(id, str) == False or name == None or isinstance(name, str) == False:
            print("Error, id and name must be strings and cant be empty!")
            return None

        self.id = id
        self.name = name
        self.maxdevices = 3

class TeachingAssistant:
    def __init__(self, id, name):
        if id == None or isinstance(id, str) == False or name == None or isinstance(name, str) == False:
            print("Error, id must be a string and cant be empty!")
            return None

        self.id = id
        self.name = name
        self.maxdevices = 2

class BorrowItem:
    def __init__(self, device, borrow_date, fromPeriod, toPeriod):
        if device == None:
            print("Error, devices cannot be null")
            return None
        if not isinstance(borrow_date, str):
            print("Error, the borrow date should be date and time")
        if not toPeriod > fromPeriod or not isinstance(fromPeriod, int) or not isinstance(toPeriod, int):
            print("Error, toPeriod must be behind fromPeriod and both values must be integers")

        self.device = device
        self.borrow_date = borrow_date
        self.fromPeriod = fromPeriod
        self.toPeriod = toPeriod
        self.return_date = None
        self.isreturned = False


class BorrowingSlip:
    def __init__(self, slipid, borrower, teachingroom, borrowed_date, items_list):
        if slipid == None or not isinstance(slipid, str):
            print("Error, invalid slip id!")
            return None
    
        if not (isinstance(borrower, TeachingAssistant) or isinstance(borrower, Lecturer)) or borrower == None:
            print("Error, invalid borrower!")
            return None
        if teachingroom == None or not isinstance(teachingroom, str):
            print("Error, invalid teahcing room")
            return None
        if len(items_list)>borrower.maxdevices:
            print("Error. Too many devices!")
            return None
        for i in range(0, len(items_list)-1, 1):
            if not isinstance(items_list[i], BorrowItem):
                print("Error, unsuitable item detected!")
                return None
            for j in range(i+1, len(items_list)-1, 1):
                if items_list[j].device.deviceid == items_list[i].device.deviceid:
                    print("Error, duplicated device IDs!")
                    return None

        self.slipid = slipid
        self.borrower = borrower
        self.teachingroom = teachingroom
        self.borrowed_date = borrowed_date
        self.items_list = []
        for i in items_list:
            self.items_list.append(i)

    def AddDevice(self, device, borrowDays):
        if device == None or not isinstance(device, Device):
            print("Error, invalid device!")
            return None

        if not borrowDays>0 or not isinstance(borrowDays, int):
            print("Error, invalid borrow days!")
            return None

        for i in self.items_list:
            if i.device == device:
                print("Device is already here!")
                return None

        if len(self.items_list) == self.borrower.maxdevices:
            print("Borrower has reached borrow items limit!")
            return None

        if not device.state == "Available":
            print("The device must be available!")
            return None

        if borrowDays>device.borrowlimit:
            print("Error: Borrow days exceeds borrow limits!")
            return None

        device.state = "Borrowed"
        self.items_list.append(BorrowItem(device, self.borrowed_date, 1, 5))
        self.items_list[-1].return_date = datetime.strptime(self.borrowed_date, "%d-%m-%Y") + timedelta(days=borrowDays)

    def ReturnDevice(self, deviceid, returnedDate):
        for i in self.items_list:
            if i.device.deviceid == deviceid:
                if i.isreturned == True:
                    print("Device is already returned!") 
                    return None
                if datetime.strptime(returnedDate, "%d-%m-%Y") < datetime.strptime(i.borrow_date, "%d-%m-%Y"):
                    print("Invalid return date!")
                    return None

                i.device.state = "Available"
                if datetime.strptime(returnedDate, "%d-%m-%Y") > i.return_date:
                    Late_returning.append([self.slipid, deviceid])
                self.items_list.remove(i)
                return None

        print("Device not found!")
        return None



def main():
    L1 = Lecturer("L01", "Ivo")
    PJ1 = ProjectorRemoteControl("PJ01", "Projector X-1", 2015, 520000, "Available", 5)
    AC1 = ACRemoteControl("AC01", "LG Inverter", 2018, 450000, "Available", 5)
    M1 = Micro("M01", "Super-Loud mic", 2009, 1100000, "Available", 21, False)
    S1 = BorrowingSlip("S01", L1, "Math Class", "22-12-2023", [])
    S1.AddDevice(M1, 2)
    S1.AddDevice(M1, 2)
    S1.AddDevice(PJ1, 2)
    S1.ReturnDevice("PJ01", "23-12-2023")
    S1.ReturnDevice("M01", "21-12-2023")
    AC2 = ACRemoteControl("AC02", "Hyper AC", 2021, 9000000, "UnderMaintenance", 14)
    PJ2 = ProjectorRemoteControl("PJ02", "Projector X", 2022, 15000000, "Available", 30)
    S1.AddDevice(AC2, 10)
    S1.AddDevice(PJ2, 45)
    S1.ReturnDevice("PJ02", "25-12-2023")
if __name__ == '__main__':
    main()

        

        