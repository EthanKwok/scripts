
# -*- coding: utf-8 -*-

# Title: collectlog
# Version: v0.2
# Last-Modified: 04-17-2014
# Author: Ethan.Guo, guozhiqiang@qiyi.com

import subprocess
from datetime import datetime
import sys, re, os, platform

LOGFOLDER = ""
IP = ""
TIMEFORMAT = "%Y_%m_%d_%H_%M_%S"

def checkEnv():
    if not "Windows-7" in platform.platform():
        print "Can support Win7 only for now, please contact Ethan for more details"
        sys.exit()

def getTime():
    return datetime.now().strftime(TIMEFORMAT)

def getConnection():
    global IP
    IP = raw_input("Please provide the IP address of your device then press ENTER to continue\r\n")
    if not IP:
        print "Invalid IP address, script's gonna stop!"
        sys.exit()
    p = subprocess.Popen(("adb connect %s" %(IP)).split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = p.communicate("\n")
    m = re.search(r"(connected){1}", stdout)
    if not m:
        print "Connect to the IP failed, script's gonna stop!"
        sys.exit()

def createFolder():
    global LOGFOLDER
    LOGFOLDER = os.sep.join([os.environ['USERPROFILE'], "Desktop", getTime()])
    try:
        os.mkdir(LOGFOLDER)
    except OSError:
        print "Folder %s exists already, gonna re-use it." %(LOGFOLDER)

def writeLog():
    global LOGFOLDER, IP
    print "Start collecting logs..."
    p = subprocess.Popen(("adb -s %s logcat -v time" %(IP + ":5555")).split(), shell=False, stdout=subprocess.PIPE)
    while True:
        f = open(os.sep.join([LOGFOLDER, ("logcat_" + getTime() + ".log")]), 'wb')
        while True:
            f.write(p.stdout.readline())
            if f.tell() >= 5242880:
                f.close()
                break

if __name__ == "__main__":
    checkEnv()
    getConnection()
    createFolder()
    writeLog()