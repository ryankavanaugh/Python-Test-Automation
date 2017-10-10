import sys
import bigsuds
import requests
import time
import json
import threading
from collections import Counter, OrderedDict
import paramiko
import smtplib
import datetime

# /Users/ryankavanaugh/Desktop/Server\ Python\ Scripts/

# What is a situation number ? ? ? Oranges

# ignore updates newer than this many minutes ago.
cutoffTimeMinutes=5
# turn on debug output
debug=1
#restart servers that need it
restartServers=1
# create dictionary to store the server data [server IP, event count]
jsonData = {}
state=str(sys.argv[1])
# Grabs current time and converts it to a format we can work with, ultimately so we dont pay attention to things 5 minutes ago
cutofftime=(time.time()*1000)-(cutoffTimeMinutes*60000)
restartlist=[]


def get_active_list(pool, hostname, username, password):
    try:
        b = bigsuds.BIGIP(hostname, username, password)
    except Exception, e:
        print e
    members = b.LocalLB.Pool.get_member_v2([pool])
    status = b.LocalLB.Pool.get_member_monitor_status([pool], members)
    enabled = b.LocalLB.Pool.get_member_session_status([pool], members)
    vmList = []
    for members, status, enabled in zip(members, status, enabled):
        count = 0
        while count < len(members):
            if "MONITOR_STATUS_DOWN" not in status[count] and "SESSION_STATUS_ENABLED" in enabled[count]:
                vmList.append(members[count]["address"].replace("/Common/",""))
            count += 1
    return vmList


def get_events(state, ip):
    path = '/events_v1/api/eventReports'
    headers = {'host': state + 'tg.carsprogram.org'}
    r = requests.get('http://' + ip + path, headers=headers)
    # made changes here
    return r.content


def loadServerEvents(state, ip, returndata):
    # Grabs cars events and uses the update time: time, situation update key, update number
    try:
        response = get_events(state, ip)
        serverjson=json.loads(response)
        events={}
        counter1 = 0
        for event in serverjson:
            eventupdatetime = event['updateTime']['time']
            events[event['situationUpdateKey']['situationId']] = [event['situationUpdateKey']['updateNumber'], eventupdatetime]
        returndata[ip]=events

    except Exception, e:
        if debug: print e
        #returndata=None


def restartServer(ip):
    print "restarting server "+ip
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=james, password=Cactus321)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo reboot')
        #print ssh_stdout, ssh_stderr
    except Exception, e:
            sendEmail('ops@crc-corp.com', 'ops@crc-corp.com', state + 'TG-Event check: failed to restart server: '+ip, datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") )

    # 7777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777
    # 7777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777
        # If we use this function: make sure the IP addresses that are responding with an incorrect number are checked multiply times
        # Not to reboot more than 10 virtual machines at one time, because if you start to many at once it overloads the system and things time out
    # 7777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777
    # 7777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777777


def sendEmail(fromadd, toadd, subject, message):
    sender = fromadd
    receivers = toadd
    message = """From: {}
To: {}
Subject: {}

{}
                 """.format(fromadd, toadd, subject, message)
    try:
        smtpObj = smtplib.SMTP('10.10.2.247')
        smtpObj.sendmail(sender, receivers, message)
        print "Successfully sent email: {}".format(subject)
    except Exception, e:
        print "Error: unable to send email"


# determine which servers are active, grabs data from the load balancer
if debug: print "getting PTK IPs"
vmOnlineList = get_active_list(sys.argv[1]+'_TGEvents_V1','10.10.2.253','cragent','Cragent1!')
if debug: print "getting VC2 IPs"
vmOnlineList = vmOnlineList + get_active_list(sys.argv[1]+'_TGEvents_V1','10.2.10.1','cragent','Cragent1!')
if debug: print "getting VC3 IPs"
vmOnlineList = vmOnlineList + get_active_list(sys.argv[1]+'_TGEvents_V1','10.3.10.1','cragent','Cragent1!')


if debug: print "Querying servers..."
threads=[]
for ip in vmOnlineList:
    if debug: print "Querying " + ip + "..."
    thread = threading.Thread(target=loadServerEvents, args=(state,ip,jsonData))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
    # what does this do ? ? ?

# masterevents will be a dict of lists.  List values are update numbers from each server
masterevents={}


if debug: print "Building masterevents..." # 1 Cars ID, All Time Stamps
for ip, events in jsonData.iteritems():
    if debug: print "building from "+ ip + ", len " + str(len(events))
    if len(events) > 0: # if there is an event
        for event, update in events.iteritems(): # for cars ID, update time in this list of only these values
            if event not in masterevents:       # if that cars ID is not in the master list
                masterevents[event] = [update]  # then add the cars ID as one key to pair with the time stamps
            else:
                masterevents[event].extend([update]) # Otherwise put this time stamp with the already existing cars id
                                                     # This gives us a cars ID with all the time stamps from al the servers
                                                    # they should all be identical, but they let us know how many
                                                    # servers have this cars event, at least it seems...
staticevents = masterevents.copy() # this is a list of a cars ID with every time stamp from all servers corresponding to that cars ID


    #           7   7   7   7   7   7   7   7
    #           If the event is on at least half of the servers,
    #           to prove it is not likely part of a faulty server, then add the largest time stamp
    #           corresponding to that event to the 'masterevents' dictionary

numServers=len(vmOnlineList)

for id, event in staticevents.iteritems(): # 1 Cars ID, 1 Time Stamp
    #print id + " " + str(len(event))
    #print event
    for serverUpdateTime in event:
        # if any of the updates are after the cutoff time, set update to 0 to indicate invalid event
        # in this case the cut off time is 5 minutes ago. so we only pay attention to things that
        # happened 5 minutes or more ago, this is to try to gauge the health of all servers on the
        # same plane, and ignore slight discrepencies due to uneven updating not indicative of server health
        if serverUpdateTime[1] > cutofftime: # It looks like this may set values to 0 over and over again for a single event that doesn't work
            masterevents[id]=0                 # so for 31 servers it does this 31 times ? ? ?
            if debug: print "ignoring brand new event "+str(id)
            break
    if len(event) < (numServers / 2) and masterevents[id] != 0: # if the number of servers the event is on is less than half the servers (then it is probably wrong)
        del masterevents[id]                                    # and the masterevents id has not been set to 0 for this event, delete it
    elif masterevents[id] != 0:
        masterevents[id]=max(staticevents[id]) # adds the highest update time for the cars ID number to the dicitonary and ignores all the rest (essentially reduces the list to one time stamp per cars ID)

print masterevents

#       master events is a dictionary that is a list of Cars Ids with only the latest times associated with them

reportdata=[]
ordereddata=OrderedDict(sorted(jsonData.items()))
# ordereddata = Cars Id w/ situation number and time stamp
# masterevents = Cars Id w/ highest last update time

for ip, eventsOnIP in ordereddata.iteritems(): # goes through IP, and all events on that IP one at a time
        restart=0
        if debug: print "validating server " + ip

        for eventID, greatestTimeStamp in masterevents.iteritems():
            if greatestTimeStamp == 0:
                pass
            elif greatestTimeStamp[1] < cutofftime:
                update = greatestTimeStamp[0]
                # print 'here'
                # print update
            #event matches
            elif event in eventsOnIP and update == eventsOnIP[event][0]:
                print eventsOnIP[event][0]
                pass
            #event exists but is out of date
            elif event in eventsOnIP and update != eventsOnIP[event][0]:
                print update
                print eventsOnIP[event]
                if int(update) > int(eventsOnIP[event][0]):
                   reportdata.append(ip + ": " + event + " is stale(has:"+str(eventsOnIP[event][0])+" valid:"+str(update)+")")
                   print 'event exists but is out of date'
                   restart=1
            #event exists but is ahead (?!)
            elif event in eventsOnIP and update != eventsOnIP[event][0]:
                if int(update) < int(eventsOnIP[event][0]):
                   reportdata.append( ip + ": " + event + " is ahead(has:"+str(eventsOnIP[event][0])+" valid:"+str(update)+")" )
                   print 'event exists but is ahead'
                   restart=1
            elif event not in eventsOnIP:
               reportdata.append( ip + ": " + event + " expected but not found" )
               restart=1
               print 'event not found'
        #look only for events in

        for eventID, updateInfo in eventsOnIP.iteritems(): # Checks to see if any Cars IDs on the IP are not on the up to date list of Cars IDs (i.e. are there any discrepancies)
            #event doesn't match
            #print 'event does not match'
            if eventID not in masterevents:
               reportdata.append( ip + ": " + eventID + " returned but not found in valid response")
               restart=1
        if restart:
            restartlist.append(ip)

#            7   7   7   7   7   7   7   7
# Email function
#           7   7   7   7   7   7   7   7
# if len(reportdata)>0:
#     sendEmail('ops@crc-corp.com', 'ops@crc-corp.com', state + ' TG-Event check: Errors found.', '\n'.join(reportdata))

for ip in restartlist:
    if restartServers:
        restartServer(ip)
    else:
        if debug: print "would have restarted " + ip