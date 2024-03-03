import time
import telnetlib
from telnetlib import Telnet
import time
import Config

#This file contains commands to measure the memory usage


#COMMANDS:

#'XYZ' is a name of processes
cmd_RES = """
top -b -n 5 -U 20006 | grep "XYZ" | awk '{$1=$2=$3=$4=$5=$7=$8=$9=$10=$11=$12=$13=$14=""; print $0}' | awk -F " " '{TotalMEM=TotalMEM+$1} {AverageMEM=TotalMEM/5} END{print AverageMEM}'
"""
#'XYZ' is a name of processes
cmd_CPU = """
top -b -n 5 -U 20006 | grep "XYZ" | awk '{$1=$2=$3=$4=$5=$6=$8=$9=$10=$11=$12=$13=$14=""; print $0}' | awk -F " " '{TotalCPU=TotalCPU+$1} {AverageCPU=TotalCPU/5} END{print AverageCPU}'
"""
cmd_GFX = """
cat /proc/brcm/core | grep -E "GFX" | awk '{$1=$2=$3=$4=$5=$6=""; print $0}' | awk '{$3=""; print $0}'
"""
cmd_MAIN = """
cat /proc/brcm/core | grep -E "MAIN" | awk '{$1=$2=$3=$4=$5=$6=""; print $0}' | awk '{$3=""; print $0}'
"""
cmd_MemAvailable = """
cat /proc/meminfo | grep 'MemAvailable:' | awk '{$1=$3=""; print $0/1024}' | awk '{$2=""; print $0}'
"""
cmd_MemFree = """
cat /proc/meminfo | grep 'MemFree:' | awk '{$1=$3=""; print $0/1024}' | awk '{$2=""; print $0}'
"""
cmd_PSS = """
procrank 2>&1 | grep "WPE" | awk '{ Pss+=$4/1024} END {print Pss}'
"""
cmd_USS = """
procrank 2>&1 | grep "WPE" | awk '{ Uss+=$5/1024} END {print Uss}'
"""


#Define variables and starting points
def start_results():
    
    result_GFX = '0% 0%'
    result_MAIN = '0% 0%'
    result_RES = 0
    result_CPU = -1
    result_MemAvailable = 0
    result_MemFree = 0
    result_PSS = 0
    result_USS = 0
    
    # Returning the results as a tuple
    return result_GFX, result_MAIN, result_RES, result_CPU, result_MemAvailable, result_MemFree, result_PSS, result_USS
    

#Measure memory usage
def MemoryTest():
    start_results()

    time.sleep(29)

    tn = Telnet(Config.IP)
    time.sleep(0.5)
    tn.write(b'root\n')
    time.sleep(0.5)
    tn.write(cmd_GFX.encode() + b'\r\n')
    tn.read_until(b"""0}'\r\n""")
    time.sleep(2)
    result_GFX = tn.read_until(b'#').decode().rstrip(('# \r\n'))
    print("GFX ", result_GFX)
    tn.write(b'exit\n')

    time.sleep(1)

    tn = Telnet(Config.IP)
    time.sleep(0.5)
    tn.write(b'root\n')
    time.sleep(0.5)
    tn.write(cmd_MAIN.encode() + b'\r\n')
    tn.read_until(b"""0}'\r\n""")
    time.sleep(2)
    result_MAIN = tn.read_until(b'#').decode().rstrip(('# \r\n'))
    print("MAIN ",result_MAIN)
    tn.write(b'exit\n')

    time.sleep(1)

    tn = Telnet(Config.IP)
    time.sleep(0.5)
    tn.write(b'root\n')
    time.sleep(0.5)
    tn.write(cmd_RES.encode() + b'\r\n')
    tn.read_until(b"""AverageMEM}'\r\n""")
    time.sleep(2)
    result_RES = tn.read_until(b'#').decode().rstrip(('# \r\n'))
    print("RES ",result_RES)
    tn.write(b'exit\n')

    time.sleep(1)

    tn = Telnet(Config.IP)
    time.sleep(0.5)
    tn.write(b'root\n')
    time.sleep(0.5)
    tn.write(cmd_CPU.encode() + b'\r\n')
    tn.read_until(b"""AverageCPU}'\r\n""")
    time.sleep(2)
    result_CPU = tn.read_until(b'#').decode().rstrip(('# \r\n'))
    print("CPU ",result_CPU)
    tn.write(b'exit\n')

    time.sleep(1)

    tn =Telnet(Config.IP)
    time.sleep(0.5)
    tn.write(b'root\n')
    time.sleep(0.5)
    tn.write(cmd_MemAvailable.encode() + b'\r\n')
    tn.read_until(b"""$0}'\r\n""")
    time.sleep(2)
    result_MemAvailable = tn.read_until(b'#').decode().rstrip(('# \r\n'))
    print("MemAvailable ",result_MemAvailable)
    tn.write(b'exit\n')

    time.sleep(1)

    tn =Telnet(Config.IP)
    time.sleep(0.5)
    tn.write(b'root\n')
    time.sleep(0.5)
    tn.write(cmd_MemFree.encode() + b'\r\n')
    tn.read_until(b"""$0}'\r\n""")
    time.sleep(2)
    result_MemFree = tn.read_until(b'#').decode().rstrip(('# \r\n'))
    print("MemFree ",result_MemFree)
    tn.write(b'exit\n')

    time.sleep(1)

    tn = telnetlib.Telnet(Config.IP)
    time.sleep(0.5)
    tn.write(b'root' + b"\n")
    time.sleep(0.5)
    tn.write(cmd_PSS.encode() + b'\r\n')
    tn.read_until(b"""Pss}'\r\n""")
    time.sleep(6)
    result_PSS = tn.read_until(b'#').decode().rstrip(('# \r\n'))
    print("PSS ",result_PSS)

    time.sleep(1)

    tn = telnetlib.Telnet(Config.IP)
    time.sleep(0.5)
    tn.write(b'root' + b"\n")
    time.sleep(0.5)
    tn.write(cmd_USS.encode() + b'\r\n')
    tn.read_until(b"""Uss}'\r\n""")
    time.sleep(6)
    result_USS= tn.read_until(b'#').decode().rstrip(('# \r\n'))
    print("USS ",result_USS)
    time.sleep(1)

    return result_GFX, result_MAIN, result_RES, result_CPU, result_MemAvailable, result_MemFree, result_PSS, result_USS




    
