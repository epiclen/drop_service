#!/bin/python

import os
import time
import sys
import logging

cmd=os.popen("pwd").read().split("\n")[0]
logging.basicConfig(filename='/var/log/down_service.log', filemode="w", level=logging.DEBUG)

arglist=sys.argv

#check interval -i
interval=1

#limit load -l
request_load=8

#limit memory available -m
request_memory=2

#kill count -c
kill_count=5

for i in range(0,len(arglist)):
  if(arglist[i]=="-i"):
    interval=arglist[i+1]
    i+=1
  elif (arglist[i]=="-l"):
    request_load=arglist[i+1]
    i+=1
  elif (arglist[i]=="-m"):
    request_memory=arglist[i+1]
    i+=1
  elif (arglist[i]=="-c"):
    kill_count=arglist[i+1]
    i+=1

#list load top 10
def cpu10():
  loadtoplist=os.popen("ps aux|awk '{print $3 \"    \" $2}'|sort -k 1 -r|awk 'NR=="+kill_count+" || NR <"+kill_count+"{print $2 }'").read().split("\n")[:-1]
  logging.info(os.popen("ps aux|awk '{print $3 \"    \" $2 \"    \" $1}'|sort -k 1 -r|awk 'NR=="+kill_count+" || NR <"+kill_count+"{print $3\" \" $2\" \" $1}'").read())
  return loadtoplist

#list memory top 10
def memory10():
  memorytoplist=os.popen("ps aux|awk '{print $4 \"    \" $2}'|sort -k 1 -r|awk 'NR=="+kill_count+" || NR <"+kill_count+"{print $2 }'").read().split("\n")[:-1]
  logging.info(os.popen("ps aux|awk '{print $4 \"    \" $2 \"    \" $1}'|sort -k 1 -r|awk 'NR=="+kill_count+" || NR <"+kill_count+"{print $3\" \"$2\" \"$1}'").read())
  return memorytoplist

#check load
def checkload():
  load=os.popen("uptime|awk '{print $10}'|sed -n 's#,##gp'").read().split("\n")[0]
  return load

#check memory
def checkmemory():
  usage=os.popen("free -h|awk 'NR==2{print $7}'|sed -n 's#G##gp'").read().split("\n")[0]
  return usage

#clean pid
def cleanload():
  logging.info("clean load")
  loadlist=cpu10()
  for i in range(0,int(kill_count)):
    logging.info("kill "+loadlist[i])

#clean memory
def cleanmemory():
  logging.info("clean memory");
  memorylist=memory10()  
  for i in range(0,int(kill_count)):
    logging.info("kill "+memorylist[i])

load=0
memory_available=100

while True:
  load=float(checkload())
  memory_available=float(checkmemory())
  
  now_date=os.popen("date").read().split("\n")[0]
  logging.info("\n")
  logging.info("-----------------------------------------------------------------------------------")
  logging.info("date:"+now_date)
  logging.info("now load:"+str(load))
  logging.info("now memory available:"+str(memory_available))

  if (load >float(request_load)):
    cleanload()
  if (memory_available<float(request_memory)):
    cleanmemory()

  logging.info("-----------------------------------------------------------------------------------")
  time.sleep(int(interval))
