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
cutOffTimeMinutes=5
cutOffTime=(time.time()*1000)-(cutOffTimeMinutes*60000)
restartServers=1
jsonData = {}
state=str(sys.argv[1])

finalList = {}
newList = {}
masterList ={}
counter = 0
totalCount = 0
eventNumbers = []
mostCommonEventCounter = 0
discrepancyCounter = 0

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
    return r.content


def loadServerEvents(state, ip, returndata):
    try:
        response = get_events(state, ip)
        serverjson=json.loads(response)
        events={}
        for event in serverjson:
            eventupdatetime = event['updateTime']['time']
            events[event['situationUpdateKey']['situationId']] = [event['situationUpdateKey']['updateNumber'], eventupdatetime]
        returndata[ip]=events
    except Exception, e:
        if debug: print e


def restartServer(ip):
    print "restarting server "+ip
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=USERNAME, password=USERPASS)
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('sudo reboot')
    except Exception, e:
            sendEmail('ryan.kavanaugh@crc-corp.com', 'ryan.kavanaugh@crc-corp.com', state + 'TG-Event check: failed to restart server: '+ip, datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y") )

def sendEmail(fromadd, toadd, subject, message):
    sender = fromadd
    receivers = toadd
    message = """From: {} To: {} Subject: {} {}
                 """.format(fromadd, toadd, subject, message)
    try:
        smtpObj = smtplib.SMTP('10.10.2.247')
        smtpObj.sendmail(sender, receivers, message)
        print "Successfully sent email: {}".format(subject)
    except Exception, e:
        print "Error: unable to send email"

def Most_Common(lst):
    data = Counter(lst)
    return data.most_common(1)[0][0]


print "getting PTK IPs"
vmOnlineList = get_active_list(sys.argv[1] + '_TGEvents_V1', '10.10.2.253', 'cragent', 'Cragent1!')
print "getting VC2 IPs"
vmOnlineList = vmOnlineList + get_active_list(sys.argv[1] + '_TGEvents_V1', '10.2.10.1', 'cragent', 'Cragent1!')
print "getting VC3 IPs"
vmOnlineList = vmOnlineList + get_active_list(sys.argv[1] + '_TGEvents_V1', '10.3.10.1', 'cragent', 'Cragent1!')

print "Querying servers..."
threads = []
serverCount = len(vmOnlineList)


# This is where the program really begins
#   We get all events that are from before 5 minutes ago. We then comb through the list, find the most commmon number,
#   confirm it occurs more than 50% of the time, then find any odd men out and restart the corresponding server

for ip in vmOnlineList:
    print "Querying " + ip + "..."
    thread = threading.Thread(target=loadServerEvents, args=(state,ip,jsonData))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

for ip, events in jsonData.iteritems():
    for id in events:
        if events[id][1] > cutOffTime:
            counter += 1
        else:
            totalCount +=1
    finalList[ip] = totalCount
    totalCount = 0
print

# Create list of event numbers from dictionary of -> ips : number of events in ip
for ip in finalList:
    eventNumbers.append(finalList[ip])

mostCommonEventsNumber = Most_Common(eventNumbers)

# Compare each event count to most common event count and get a total of how many servers have this event count number
for ip in finalList:
    if finalList[ip] == mostCommonEventsNumber:
        #print finalList[ip]
        mostCommonEventCounter += 1

if mostCommonEventsNumber > (serverCount/2):
    for ip in finalList:
         if finalList[ip] != mostCommonEventsNumber:
             print ip
             print finalList[ip]
             restartServer(ip)
