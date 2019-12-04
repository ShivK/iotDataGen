#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import json
import os
import copy

import configparser
from string import Template
from datetime import date, datetime, timedelta

import Getter
import Util as ut

NUM_COPIES = "num_copies"
MSG_TEMPLATE = "message_template"
DEV_TYPE = "type"


def read_device_types(config):
    configDir = config['Devices'].get('configDir')
    deviceFile = configDir + "/" + config['Devices'].get('Devices')
    #Open the Device file and get the definitions
    with open(deviceFile) as data_file:
        devA = json.loads(data_file.read());

    numDevA = [0] * len(devA); # number of copies of each device type
    devMsgTempA = [] #output message template coresponding  to the device type
    #Init numCopies and output message templates 
    for i in range(len(devA)):
        numDevA[i] = devA[i][NUM_COPIES];
        if devA[i][DEV_TYPE] == "complex":
            devMsgTempA.append(read_template(configDir + "/" + devA[i][MSG_TEMPLATE]))
        else:
            devMsgTempA.append("")

    return devA,numDevA,devMsgTempA

def read_template(fname):
    with open(fname) as data_file:
        dfile = json.load(data_file);
    #convert to string
    tstr = json.dumps(dfile);
    return tstr
    
def gen_Device_rec(dev,numDev,msgTemplate,tm):
    resA = []  # records generated for each copy of a device type
    
    #For numDev generate deviceId
    for i in range(numDev):
        srec = ""
        #generate data
        rec = Getter.genData(dev,i,tm);
        #recA[i] = copy.deepcopy(rec)
        
        if dev[DEV_TYPE] == "complex":
            tstr = json.dumps(msgTemplate);
            s = Template(tstr)
            sstr = s.safe_substitute(rec)
            sstr = sstr.replace("\"<","")
            sstr = sstr.replace("\\","")
            sstr = sstr.replace(">\"","")
            sstr = sstr.replace("\"{","{")
            sstr = sstr.replace("}\"","}")
            rec = sstr
        else:
            rec = json.dumps(rec);

        #print("rec 2",rec)
        resA.append(rec)

    return resA

'''
function gen_Device_records
  This generates Device records
  Input: config: the config properties object
             outFile: the output file name
             tm : start time in datetime format
'''    
def gen_Device_records(config,outFile,tm):
    npc = config['OutputSection']

    num_records = 0
    nr = npc.get('totalRecords','0')
    if nr.isdigit():
        num_records = int(nr)
    else:
        print ("Total number of records in the Config file not numeric or it is zero")
        
    if nr == 0:
        print ("Total number of records is not specified or it is zero")

    #Read DeviceTypes
    devA,numDevA,devMsgTempA = read_device_types(config);

    timeA = [tm] * 2; 
    #prevRecDev = [] * len(devA) #keep track of prev Rec (values generated per device type)

    with open(outFile, 'w') as ofile:
        
        #For numRecords
        for numRec in range(num_records):
            #generate record for each device type
            for i in range(len(devA)):
                #Time is per device type (in datetime format)
                #interval is seconds (int)
                recA = gen_Device_rec(devA[i],numDevA[i],devMsgTempA[i],timeA[i]);

                #Increment time
                samplingType = devA[i]["sampling"]["type"]
                samplingInterval = devA[i]["sampling"]["interval"]

                if samplingType == "fixed":
                    timeA[i] =ut.add_seconds(timeA[i],samplingInterval)
                elif samplingType == 'random':
                    n = ut.gen_number(1,samplingInterval)
                    timeA[i] = ut.add_seconds(timeA[i],n)

                #Write to file (streaming)
                for rec in recA:
                    #ofile.write(rec  + os.linesep);      
                    #use the foll
                    ofile.write(rec + "\n");


#Date validation routine
def val_date(date_str,fieldname,format):
    try:
        datetime.strptime(date_str,format)
        return 0
    except ValueError:
        print ("Config property {} is not in the correct data format, should be MM/DD/YYYY".format(fieldname))
        exit(0)

#Read Config file
def readConfig(fname):
    config = configparser.ConfigParser()
    r = config.read(fname)
    if (len(r) == 0):
        print ("Could not read the config file - please enter a valid config file");
        exit(0)

    npc = config['OutputSection']
    outDir = npc.get("outDir","output");
    #if outDir does not exist create it
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    outFile = npc.get("outFile","outfile.jsonl");
    outFile = outDir + "/" + outFile;
    totRec = npc.get("totalRecords","10");
    d_date = '01/01/2018'
    nr = npc.get('iotDateFrom',d_date)
    if nr == "":
        nr = d_date
    val_date(nr,'iotDateFrom','%m/%d/%Y')
    date_from = nr

    d_time = '00/00/00'
    nr = npc.get('iotTimeFrom',d_time)
    if nr == "":
        nr = d_time
    val_date(nr,'iotTimeFrom',"%H/%M/%S")
    time_from = nr

    return config,outFile,date_from,time_from,totRec


def datagenIOT(fname):
    print("Using configuration file {}".format(fname));

    config,outFile,iotDateFrom,iotTimeFrom,totRec = readConfig(fname)
    stA = iotDateFrom.split("/")
    tA= iotTimeFrom.split("/")
    t = datetime(int(stA[2]),int(stA[1]),int(stA[0]),int(tA[0]),int(tA[1]),int(tA[2]))

    gen_Device_records(config,outFile,t);
    print("Generated {} sets of records to {}".format(totRec,outFile))
    
    return



#Entry into the DataGenIOT CLI command
#Current usage is 'DataGenIOT <configfile>'
if __name__ == '__main__':
    if len(sys.argv) == 2:
        fname = sys.argv[1].strip()
        #num_yrs = sys.argv[2].strip()
        datagenIOT(fname)
    else:
        print("Usage: DataGenIOT <config filename>")
        print("Example: DataGenIOT iot-1.properties")


