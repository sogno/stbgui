# -*- coding: utf-8 -*-
import sys, os, time
from Tools.HardwareInfo import HardwareInfo

def getVersionString():
	return getImageVersionString()

def getImageVersionString():
	try:
		if os.path.isfile('/var/lib/opkg/status'):
			st = os.stat('/var/lib/opkg/status')
		else:
			st = os.stat('/usr/lib/ipkg/status')
		tm = time.localtime(st.st_mtime)
		if tm.tm_year >= 2011:
			return time.strftime("%Y-%m-%d %H:%M:%S", tm)
	except:
		pass
	return _("unavailable")

def getEnigmaVersionString():
	import enigma
	enigma_version = enigma.getEnigmaVersionString()
	if '-(no branch)' in enigma_version:
		enigma_version = enigma_version [:-12]
	return enigma_version

def getGStreamerVersionString():
	import enigma
	return enigma.getGStreamerVersionString()

def getKernelVersionString():
	try:
		f = open("/proc/version","r")
		kernelversion = f.read().split(' ', 4)[2].split('-',2)[0]
		f.close()
		return kernelversion
	except:
		return _("unknown")

def getDriverBuildDateString():
	try:
		file = open("/proc/stb/info/buildate", "r")
		model = file.readline().strip()
		file.close()
		return model
	except IOError:
		string = getDriverDate()
		year = string[0:4]
		month = string[4:6]
		day = string[6:8]
		driversdate = '-'.join((year, month, day))	  
		return driversdate
	      
def getDriversVersionString():
	try:
		if (os.path.isfile("/proc/stb/info/boxtype") and os.path.isfile("/proc/stb/info/buildate")):
			  if ((open("/proc/stb/info/chipset").read().strip()) == "7405"):
			    return open("/proc/stb/info/chipset").read().strip() + "-" + open("/proc/stb/info/buildate").read().strip()
			  else:
			    return open("/proc/stb/info/chipset").read().strip() + "-" + open("/proc/stb/info/version").read().strip()
	except:
		pass
	return "Unavailable"  
      
def getHardwareTypeString():                                                    
	try:
		if (os.path.isfile("/proc/stb/info/boxtype") and os.path.isfile("/proc/stb/info/buildate")): 
			return open("/proc/stb/info/boxtype").read().strip().upper()
		if os.path.isfile("/proc/stb/info/boxtype"):                            
			return open("/proc/stb/info/boxtype").read().strip().upper() + " (" + open("/proc/stb/info/board_revision").read().strip() + "-" + open("/proc/stb/info/version").read().strip() + ")"
		if os.path.isfile("/proc/stb/info/vumodel"):                            
			return "VU+" + open("/proc/stb/info/vumodel").read().strip().upper() + "(" + open("/proc/stb/info/version").read().strip().upper() + ")" 
		if os.path.isfile("/proc/stb/info/model"):                              
			return open("/proc/stb/info/model").read().strip().upper()      
	except:
		pass
	return "Unavailable" 

def getImageTypeString():
	try:
		return open("/etc/issue").readlines()[-2].capitalize().strip()[:-6]
	except:
		return _("undefined")

def getCPUInfoString():
	try:
		cpu_count = 0
		for line in open("/proc/cpuinfo").readlines():
			line = [x.strip() for x in line.strip().split(":")]
			if line[0] == "system type":
				processor = line[1].split()[0]
			if line[0] == "cpu MHz":
				cpu_speed = "%1.0f" % float(line[1])
				cpu_count += 1
		if os.path.isfile('/proc/stb/fp/temp_sensor_avs'):
			temperature = open("/proc/stb/fp/temp_sensor_avs").readline().replace('\n','')
			return "%s %s MHz (%s) %s°C" % (processor, cpu_speed, ngettext("%d core", "%d cores", cpu_count) % cpu_count, temperature)
		return "%s %s MHz (%s)" % (processor, cpu_speed, ngettext("%d core", "%d cores", cpu_count) % cpu_count)
	except:
		return _("undefined")

def getDriverInstalledDate():
	try:
		from glob import glob
		driver = [x.split("-")[-2:-1][0][-8:] for x in open(glob("/var/lib/opkg/info/*-dvb-modules-*.control")[0], "r") if x.startswith("Version:")][0]
		return  "%s-%s-%s" % (driver[:4], driver[4:6], driver[6:])
	except:
		return _("unknown")

def getChipSetString():
	try:
		f = open('/proc/stb/info/chipset', 'r')
		chipset = f.read()
		f.close()
		return chipset.replace('\n','')
	except IOError:
		return "unavailable"

def getCPUString():
	try:
		file = open('/proc/cpuinfo', 'r')
		lines = file.readlines()
		for x in lines:
			splitted = x.split(': ')
			if len(splitted) > 1:
				splitted[1] = splitted[1].replace('\n','')
				if splitted[0].startswith("system type"):
					system = splitted[1].split(' ')[0]
		file.close()
		return system 
	except IOError:
		return "unavailable"

def getCpuCoresString():
	try:
		file = open('/proc/cpuinfo', 'r')
		lines = file.readlines()
		for x in lines:
			splitted = x.split(': ')
			if len(splitted) > 1:
				splitted[1] = splitted[1].replace('\n','')
				if splitted[0].startswith("processor"):
					if int(splitted[1]) > 0:
						cores = 2
					else:
						cores = 1
		file.close()
		return cores
	except IOError:
		return "unavailable"

def getMicomVersionString():
	try:
		f = open('/proc/stb/info/version', 'r')
		micom = f.read()
		f.close()
		return micom.replace('\n','')
	except IOError:
		return "unavailable"
	      
# For modules that do "from About import about"
about = sys.modules[__name__]
