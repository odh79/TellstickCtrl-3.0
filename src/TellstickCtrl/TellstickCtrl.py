import MySQLdb
import sys
import datetime
from time import mktime
import calendar
import time
import ephem
import os
import td,tdmod
import threading, Queue
import ChangeLog
from operator import itemgetter


Version = "3.0.2"
debug = 0
log = 0
count = 0
start = 1
ActionTimerExit = 0
queue = Queue.Queue(20)
logfile = "/var/log/TellstickCtrl.log"
cmd_method = "tdtool"
cmd= "/usr/bin/tdtool"
#cmd="echo >> /TellstickCtrl3.log"
CL = ChangeLog.ChangeLog()


        
if len(sys.argv) > 1:
    argv_count = 0
    for z in sys.argv :
        if argv_count == 0:
            pass
        else:
            if sys.argv[argv_count] == "debug" :
                debug = 1
            if sys.argv[argv_count] == "log" :
                log = 1
            if sys.argv[argv_count] == "td":
                cmd_method = "td"
            if sys.argv[argv_count] == "tdtool":
                cmd_method = "tdtool"                   
            if sys.argv[argv_count] == "-f" :
                number = argv_count + 1
                logfile = sys.argv[number]
            if sys.argv[argv_count] == "help":
                print("Use: TellstickCtrl.py Option " ,"Options: td or tdtool debug log help -f File -changelog -V Version")
                sys.exit()
            if sys.argv[argv_count] == "-changelog":

                for x in CL.Get() :
                    print(x);
                sys.exit()
                
            if sys.argv[argv_count] == "-V":
                print("Version " + str(Version))
                sys.exit()
        
        argv_count = argv_count + 1



class ActionTimer(threading.Thread):
    def __init__(self,queue1):
        threading.Thread.__init__(self)
        self.queue = queue
        write(self,"Thread initiated")
        
        
        
    def run(self):
        write("ActionTimer:","run started")
        while ActionTimerExit != 1:

            write("ActionTimer:", "getting data from queue")
            
            while queue.empty():
                time.sleep(5)
            
            try:
                data = queue.get(2)
            except Exception as e:
                print("Exception", e)
                write("High","ActionTimer:","Exception", e)

            write("ActionTimer:", "got data")
            write("ActionTimer:", "queue lenth:",queue.qsize())
            #cnt = 0
            #while cnt <= queue.qsize()-1:
            #    write("ActionTimer:", queue.get(cnt))
            #    cnt = cnt + 1 
            #for l in queue:
            #    write(l)
            
            sdata = data.split(",")
            if sdata[1] == "On":

                write("ActionTimer: Thread executing On")
                
                if cmd_method == "td":    
                    tdmod.SendOn(sdata[0])
                elif cmd_method == "tdtool":
                    os.system(cmd + " --on " + sdata[0])
               
                write("ActionTimer:",sdata[0],"On")
            
            elif sdata[1] == "Off":

                write("ActionTimer:","Thread executing Off")
                    
                if cmd_method == "td":  
                    tdmod.SendOff(sdata[0])
                elif cmd_method == "tdtool":
                    os.system(cmd + " --off " + sdata[0])
                
                print("ActionTimer:",sdata)
                write("ActionTimer:",sdata[0],"Off")
                   
            time.sleep(float(sdata[2])+4)           

        write("ActionTimer:",self,"Is done!")
 

def startuprun(rc_switch, gRoup, UOn, UOff):
    if int(gRoup)==1:
        group = fetch_group(rc_switch)
        #g_length = len(rc_switch)
        #queue = Queue.Queue(g_length)
        write("startup: ", "Time now:", str(datetime.datetime.fromtimestamp(int(time.time()))),"UOn", str(datetime.datetime.fromtimestamp(int(UOn))),"UOff: ", str(datetime.datetime.fromtimestamp(int(UOff))))
        if int(time.time()) > int(UOn) and int(time.time()) < int(UOff) or int(UOn) > int(UOff) and int(time.time()) > int(UOn) or int(time.time()) < int(UOn) and int(time.time()) < int(UOff) or int(time.time()) > int(UOn) and str(Off[0]) =="No" :
            for rc_s in group:
                if str(On[0]) != "No":
                   
                    write("Run once: GroupOn")   
                    while queue.full():
                        write("Queue is full", rc_s,"1")
                        time.sleep(1)
                    
                    queue.put(makeJobb(rc_s, "On", "2"))
    
        else:
            for rc_s in group:
                if str(Off[0]) != "No":
    
                    write("Run once: GroupOff")
    
                    while queue.full():
                        write("Queue is full",rc_s,"2")
                        time.sleep(1)
                        
                    queue.put(makeJobb(rc_s, "Off", "2"))
    
    else:
        if str(On[0]) != "No" :
            write("startup: ", "Time now:", str(datetime.datetime.fromtimestamp(int(time.time()))),"UOn", str(datetime.datetime.fromtimestamp(int(UOn))),"UOff: ", str(datetime.datetime.fromtimestamp(int(UOff))))
            if int(time.time()) > int(UOn) and int(time.time()) < int(UOff) or int(UOn) > int(UOff) and int(time.time()) > int(UOn) or int(time.time()) < int(UOn) and int(time.time()) < int(UOff) or int(time.time()) > int(UOn) and str(Off[0]) =="No" :
                write ("Run once: tdmod.SendOn("+rc_switch+")")
    
                while queue.full():
                    write("Queue is full",rc_switch,"3")
                    time.sleep(1)
                    
                queue.put(makeJobb(rc_switch, "On", delay))
            else:
            #if str(Off[0]) != "No":
    
                write ("Run once: tdmod.SendOff("+rc_switch+")")
    
                while queue.full():
                    write("Queue is full",rc_switch, "4")
                    time.sleep(1)
                     
                queue.put(makeJobb(rc_switch, "Off", delay))

                
    
def write(*Strings):
    if Strings[0] == "High" :
        print(str(datetime.datetime.now()) +" " + str(Strings))
        fopen = open(logfile,"a")
        Sout = str(datetime.datetime.now()) + str(Strings) + "\n"
        fopen.write(Sout)
        fopen.close()
    else :
        if debug == 1:
            print(str(datetime.datetime.now()) +" " + str(Strings))
        if log == 1:
            fopen = open(logfile,"a")
            Sout = str(datetime.datetime.now()) + str(Strings) + "\n"
            fopen.write(Sout)
            fopen.close()      

def makeJobb(switch, action, delay):
    out = str(switch + "," + action + "," + delay)    
    
    return out



def fetch_group(group):
    stri = "SELECT `rc_switches`  FROM `tellstick_groups` WHERE `Group` = \'" + group + "\'" 
    cursor.execute(stri)
    Group = cursor.fetchall()
    write ("Group:",group, ", in group: " , Group) 
    out = (Group[0][0]).split(";") 
    return out
    
def checkHM(H,M):
    #write("checkHM before:",str(H),str(M))
    if M >= 60:
        M = M - 60
        H = H + 1
    if M < 0:
        M = M + 60
        H = H - 1
    if H > 23:
        H = H - 24  
    result = [H, M]
    #write("checkHM after:",str(result))
    return result

def checkDOM(year,month,day):
    ndays = calendar.monthrange(year,month)
    nday = day + 1
    out = []
    
    if nday > ndays[1]:
        if month < 12 :
            out.append(year) 
            out.append(month + 1)
            out.append(1)
        else :
            out.append(year + 1) 
            out.append(1)
            out.append(1) 
    else :
        out.append(year)
        out.append(month)
        out.append(day)
        
        

    write("CheckDOM: Year:"  +  str(out[0]) + " " + "Month:"  + str(out[1]) + " " + "Day:" + str(out[2]))
    return out
    

def weekDay(wday):
    result = ""
    if wday == 0:
        result = "Monday"
    if wday == 1:
        result = "Tuesday"
    if wday == 2:
        result = "Wednesday"
    if wday == 3:
        result = "Thursday"
    if wday == 4:
        result = "Friday"
    if wday == 5:
        result = "Saturday"
    if wday == 6:
        result = "Sunday"
    return result

def days(days):
    p = 0
    if days[0] != "All":
        for i in days:
            if i == Wday:
                p = 1    
        if p == 1:
            write("This rule applies today")
            result = 1
        else:
            write("This rule does not apply today")
            result = 0
    else:
        write("this rule is set to all days")
        result = 1
    return result


Atimer = ActionTimer(queue)
Atimer.daemon = True
Atimer.start()
                    
# init connection to telldusd
td.init( defaultMethods = td.TELLSTICK_TURNON | td.TELLSTICK_TURNOFF ) 

#while count < 100000:
while 1 :
    write("New run: " + str(datetime.datetime.now()))
    son = 0
    soff = 0    
    now = datetime.datetime.now()   
    Ynow = now.year
    mnow = now.month
    Dnow = now.day
    Hnow = now.hour
    Mnow = now.minute
    wDay = calendar.weekday(Ynow, mnow, Dnow)
    Wday = weekDay(wDay)
    Utime = int(time.time())
    start_jobs = []


    obs = ephem.Observer()
    obs.lat = "57.8"
    obs.long = "12.06"
    sunrise = str(obs.next_rising(ephem.Sun())).split(" ")
    sunrise = sunrise[1]
    sunset = str(obs.next_setting(ephem.Sun())).split(" ")
    sunset = sunset[1]
    sunrise = sunrise.split(":")
    sunset = sunset.split(":")
    Usunrise = mktime(datetime.datetime(Ynow, mnow, Dnow, int(sunrise[0]), int(sunrise[1]), int(sunrise[2]), 109000).timetuple())
    Usunset = mktime(datetime.datetime(Ynow, mnow, Dnow, int(sunset[0]), int(sunset[1]), int(sunset[2]), 109000).timetuple())
    if int(sunset[0]) > int(03) and Usunset < Usunrise:
        YMD = checkDOM(Ynow,mnow,Dnow)
        Usunset = mktime(datetime.datetime(YMD[0], YMD[1], YMD[2], int(sunset[0]), int(sunset[1]), int(sunset[2]), 109000).timetuple())
        #Usunset = mktime(datetime.datetime(Ynow, mnow, Dnow+1, int(sunset[0]), int(sunset[1]), int(sunset[2]), 109000).timetuple())

    write("Connecting to Db")
    try:
        db = MySQLdb.connect(
                     host = "localhost",
                     db = "django_db",
                     user= "django",
                     passwd = "django"
                     )
    except Exception as e:
        #sys.exit("We cant get into the database")
        write("High" + " We cant get into the database")
        time.sleep(30)
        continue
        
        
    cursor = db.cursor()
    cursor.execute("SELECT name FROM tellstick_rc_switches")
    Switches = cursor.fetchall()
    cursor.execute("SELECT * FROM tellstick_schedule")
    result = cursor.fetchall()

 
    write("Next sunrise at: " + str(sunrise))
    write("Next sunset at:" + str(sunset))


    z = 1
    
        
    if result:
        for z in result:
            write("------------------------------------------------------------")
            
            write("------------------------------------------------------------")
            rc_switch = z[1]
            gRoup = z[2]  
            On = z[3].split(":")
            #print(On)
            Off = z[4].split(":")
            Days = z[5].split(",")
            delay = z[6]
            write("On",On)
            write("Off:", Off)
            
            
            if On[0] == "sunrise" or On[0] == "sunset":
                
                if On[0] == "sunrise":
                    write("Sunrise")
                    OnE = sunrise
                    if len(On) > 2:
                        if str(On[1]) == "+":
                            HOn = int(On[2])+int(sunrise[0])
                            MOn = int(On[3])+int(sunrise[1])
                        else:
                            HOn = int(On[2])-int(sunrise[0])
                            MOn = int(On[3])-int(sunrise[1])
                    else:
                        HOn = int(sunrise[0])
                        MOn = int(sunrise[1])
                    
                    

                else:
                    write("Sunset")
                    OnE = sunset
                    if len(On) > 2:
                        if str(On[1]) == "+":
                            HOn = int(On[2])+int(sunset[0])
                            MOn = int(On[3])+int(sunset[1])
                        else:
                            HOn = int(On[2])-int(sunset[0])
                            MOn = int(On[3])-int(sunset[1])
                    else:
                        HOn = int(sunset[0])
                        MOn = int(sunset[1])

                    
                HOn = checkHM(HOn,MOn)[0]
                MOn = checkHM(HOn,MOn)[1]
                #write("On:",On)
                
                if str(On[0]) != "No":
                    UOn = mktime(datetime.datetime(Ynow, mnow, Dnow, int(HOn), int(MOn), 00, 109000).timetuple())

                write("On contains extra info")
                write("On:",HOn,MOn) 
            else:
                if str(On[0]) != "No":
                    
                    HOn = On[0]
                    MOn = On[1]
                    UOn = mktime(datetime.datetime(Ynow, mnow, Dnow, int(On[0]), int(On[1]), 00, 109000).timetuple())
                write("No extra info on On")
                On_extra = On[0]
                 
            if Off[0] == "sunrise" or Off[0] == "sunset":
                if Off[0] == "sunrise":
                    write("Off: sunrise")
                    OffE = sunrise
                    if len(Off) > 2:
                        if str(Off[1]) == "+":
                            HOff = int(Off[2])+int(sunrise[0])
                            MOff = int(Off[3])+int(sunrise[1])
                        else:
                            HOff = int(Off[2])-int(sunrise[0])
                            MOff = int(Off[3])-int(sunrise[1])
                    else:
                        write("Off: just sunrise")
                        HOff = int(sunrise[0])
                        MOff = int(sunrise[1])
                        
                        
                    soff = 1
                    
                else:
                    write("Off: sunset")
                    OffE = sunset
                    if len(Off) > 2:
                        
                        if str(Off[1]) == "+":
                            HOff = int(Off[2])+int(sunset[0])
                            MOff = int(Off[3])+int(sunset[1])
                        else:
                            HOff = int(Off[2])-int(sunset[0])
                            MOff = int(Off[3])-int(sunset[1])
                    else:
                        write("Off: just sunset")
                        HOff = int(sunset[0])
                        MOff = int(sunset[1])
                        write("HOff: " +str(HOff) +" MOff: " +str(MOff)) 
        
                HOff = checkHM(HOff,MOff)[0]
                MOff = checkHM(HOff,MOff)[1]


                if str(Off[0]) != "No":
                    UOff = mktime(datetime.datetime(Ynow, mnow, Dnow, int(HOff), int(MOff), 00, 109000).timetuple())
                if soff != 1 and UOn > UOff:
                    Dnow = checkDOM(Ynow,mnow,Dnow)
                    UOff  = mktime(datetime.datetime(Ynow, mnow, Dnow, int(HOff), int(MOff), 00, 109000).timetuple())
                    #UOff  = mktime(datetime.datetime(Ynow, mnow, Dnow+1, int(HOff), int(MOff), 00, 109000).timetuple())
                write("Off contains extra info")
                write("Off:",HOff,MOff)
            else:
                if str(Off[0]) != "No":
                    HOff = int(Off[0])
                    MOff = int(Off[1])
                    UOff = mktime(datetime.datetime(Ynow, mnow, Dnow, int(HOff), int(MOff), 00, 109000).timetuple())
                    if str(On[0]) !="No" and UOn > UOff:
                        YMD = checkDOM(Ynow,mnow,Dnow)
                        UOff  = mktime(datetime.datetime(YMD[0], YMD[1], YMD[2], int(HOff), int(MOff), 00, 109000).timetuple())
                        #UOff  = mktime(datetime.datetime(Ynow, mnow, Dnow+1, int(Off[0]), int(Off[1]), 00, 109000).timetuple())
                write("No extra info on Off")
                Off_extra = Off[0]
                write("Off:",HOff,MOff)
                
            if soff == 1:
                if UOn > UOff:
                    On[0] = "No"
                    
                    write(On[0])
         
            
            Tnow = str(Hnow) + str(Mnow)
           
            

            Dtoday = days(Days)
            if Dtoday == 1: 
                ## Run Once when started 
                if start == 1:    
                    #write("Starting Run once when started")  
                    
                    write("Startup run starts")
                    if str(On[0]) != "No":  
                        start_jobs.append({'Rc_switch' : rc_switch, 'On' : UOn, 'Off' : UOff, 'Group' : int(gRoup)})
                    
                    
                    
                ### End Startup run
                
                if start == 0 :
                    if int(gRoup)==1:
                            group = fetch_group(rc_switch)
    
                            if int(Hnow) == int(HOn) and int(Mnow) == int(MOn) or int(Hnow) == int(HOn) and int(Mnow) == int(MOn)+1 or int(Hnow) == int(HOn) and int(Mnow) == int(MOn)+2:
                                for i in group:
                                    if str(On[0]) != "No":
    
                                        while queue.full():
                                            write("Queue is full",i, "5")
                                            time.sleep(1)
                                        queue.put(makeJobb(i, "On", delay))
    
                                        
                            if int(Hnow) == int(HOff) and int(Mnow) == int(MOff) or int(Hnow) == int(HOff) and int(Mnow) == int(MOff)+1 or int(Hnow) == int(HOff) and int(Mnow) == int(MOff)+2:
                                for i in group:
                                    if str(Off[0]) != "No":
                                        time.sleep(float(delay))
    
                                        while queue.full():
                                            write("Queue is full",i,"6")
                                            time.sleep(1)
                                            
                                        queue.put(makeJobb(i, "Off", delay))
     
                            
                    else:
                        if str(On[0]) !="No":
                            if  int(Hnow) == int(HOn) and int(Mnow) == int(MOn) or int(Hnow) == int(HOn) and int(Mnow) == int(MOn)+1 or int(Hnow) == int(HOn) and int(Mnow) == int(MOn)+2:
                                if str(On[0]) != "No":
    
                                    while queue.full():
                                        write("Queue is full",rc_switch,"7")
                                        time.sleep(1)
                                        
                                    queue.put(makeJobb(rc_switch, "On", delay))
                                    write("tdmod.SendOn(" + rc_switch +")")
    
                               
                                        
                        if str(Off[0]) !="No":
                            if  int(Hnow) == int(HOff) and int(Mnow) == int(MOff) or int(Hnow) == int(HOff) and int(Mnow) == int(MOff)+1 or int(Hnow) == int(HOff) and int(Mnow) == int(MOff)+2:
                                if str(Off[0]) != "No":
    
                                    while queue.full():
                                        write("Queue is full",rc_switch, "8")
                                        time.sleep(1)
                                        
                                    queue.put(makeJobb(rc_switch, "Off", delay))
                                    write("tdmod.SendOff("+ rc_switch+")")
    
                               
                write("Switches:" + rc_switch +" On at: " + z[3]+ " and Off at: " + z[4] + " with delay:" + delay)
    write("------------------------------------------------------------")
    
    if start == 1 and debug == 1:
        write("Startup run ends") 
    if start == 1:
        start_jobs.sort(key=itemgetter('On'))  
        for job in start_jobs:
            startuprun(job['Rc_switch'], job['Group'], job['On'], job['Off'])
            write(job)                   
    start = 0
    count = int(count)+1
    write("Going to sleep " + str(count))
    time.sleep(60)
    write("Done sleeping")
write("Waiting for threads to exit")
ActionTimerExit = 1

write("High" + "Exiting program!")
td.close()
