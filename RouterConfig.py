import re
import os
class BGPData:
	#BGP data class
	asnum = 0
	neighbors = []
	def __init__(self, asnum):
		self.asnum = asnum
	def addneighbor(self, neighbor, remoteas):
		self.neighbors.append((neighbor, remoteas))
	def getneighbors(self):
		return self.neighbors

def nlflood(nls=30):
	#Used to keep the feel of a clean terminal, clears away the last prompt.
	print("\n"*nls)

def subnettowildcard(subnet):
	wildcard = []
	for x in subnet.split("."):
		wildcard.append(str(255-int(x)))
	return ".".join(wildcard)

def validateip(ip):
	return re.fullmatch(ifvalid,interface)

def networkaddress(ip, subnet):
	network = []
	for i, j in enumerate(ip.split(".")):
		network.append( str( int(j) & int(subnet.split(".")[i] ) ) )
	return ".".join(network)

def generate():
	os.makedirs(os.getcwd() + "\\configs")
	with open("configs/" + hostname + "-config.txt", "w") as f:
		#CONFIGURE DEFAULTS ====================================
		f.write("enable\nconfig t\n") #Elevation to router config
		f.write("hostname " + hostname + "\n")
		f.write("no ip domain-lookup\n")
		if (privexec != ""):
			f.write("enable secret " + privexec + "\n")
		if (linepass != ""): #Setup VTY pass, if there is one
			f.write("line vty 0 15\n")
			f.write("password " + linepass + "\n")
			f.write("login\n")
			f.write("exit\n")
		f.write("line con 0\n")
		f.write("logging sync\n")
		if (linepass != ""): #Setup console pass, if there is one
			f.write("password " + linepass + "\n")
			f.write("login\n")
		f.write("exit\n")
		for i, j in interfaces.items(): #Configure interfaces
			ipadd, smask = j
			f.write("interface " + i + "\n")
			f.write("ip add " + ipadd + " " + smask + "\n")
			f.write("no sh\n")
		#CONFIGURE ROUTING =====================================
		if (routingmodelkup[routingmode] == "RIPv2"): # RIPv2 =========================
			f.write("router rip\nversion 2\n")
			if (not autosum):
				f.write("no auto-summary\n")
			for i in routinginterfaces:
				ip, subnet = interfaces[i]
				f.write("network " + ip + "\n")
			for i in passiveinterfaces:
				if (i in routinginterfaces):
					f.write("passive-interface " + i + "\n")
		elif (routingmodelkup[routingmode] == "EIGRP"): #EIGRP ========================
			f.write("router eigrp " + str(asnum) + "\n")
			if (not autosum):
				f.write("no auto-summary\n")
			for i in routinginterfaces:
				ip, subnet = interfaces[i]
				f.write("network " + ip + " " + subnettowildcard(subnet) + "\n")
			for i in passiveinterfaces:
				f.write("passive-interface " + i + "\n")
			f.write("exit\n")
		elif (routingmodelkup[routingmode] == "OSPF"): #OSPF =========================
			f.write("router ospf " + str(asnum) + "\n")
			for i in routinginterfaces:
				ip, subnet = interfaces[i]
				f.write("network " + networkaddress(ip,subnet) + " " + subnettowildcard(subnet) + " area 0\n")
			for i in passiveinterfaces:
				f.write("passive-interface " + i + "\n")
		elif (routingmodelkup[routingmode] == "BGP"): #BGP ===========================
			f.write("router bgp " + str(bgp.asnum) + "\n")
			for i in bgp.getNeighbors():
				f.write("neighbor " + i[0] + " remote-as " + i[1] + "\n")
			for i in routinginterfaces:
				ip, subnet = interfaces[i]
				f.write("network " + networkaddress(ip,subnet) + " mask " + subnet + "\n")
			f.write("address-family ipv4 unicast\n")
			f.write("exit\n")
		f.write("exit\n") #De-escalate to Config 
# MAIN LOGIC ==============================================================================================================
while True:		
	print("======================")
	print("RouterMacro v1.5")
	print("======================\n")
	routingmodelkup = ["None", "RIPv2", "EIGRP", "OSPF", "BGP"]
	routingmode = 0
	routinginterfaces = []
	passiveinterfaces = []
	asnum = 1
	autosum = False
	hostname = input("Router Hostname: ")
	privexec = input("Priviledged EXEC password (Leave blank for none): ")
	linepass = input("Line password (Leave blank for none): ")
	interfaces = {}
	ifvalid = r"[SsFfGgLl]\d/\d(/\d|)|lo\d"
	ipvalid = r"^(?:(?:[01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.){3}(?:[01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
	while True:
		nlflood()
		print("\nMAIN ==========================")
		print("0: Exit")
		print("1: Configure interface")
		print("2: Print interfaces")
		print("3: Routing [" + routingmodelkup[routingmode] + "]")
		print("4: Delete Interface")
		print("5: Generate config!")
		inp = input("> ")
		if (inp == "0"):
			break
	#------------------------------------ INTERFACE CONFIGURATION -----------------------------------
		elif (inp == "1"):
			while True:
				interface = input("Interface: ")
				if(re.fullmatch(ifvalid,interface) and not interface in interfaces):
					break
				else:
					print("## Possible error: " + ("<invalid interface>", "<duplicate interface>")[interface in interfaces])
					break
			while True:
				ip = input("IP [cancel]: ")
				if (ip == ""):
					break
				if (re.fullmatch(ipvalid, ip)):
					break
				else:
					print("There was an error in your IP address. Please recheck")
			while (ip != ""):
				subnet = input("Subnet [/24]: ")
				if (subnet == ""):
					subnet = "255.255.255.0"
				if (re.match(ipvalid, subnet)):
					break
				else:
					print("There was an error in your subnet. Please recheck")
			if(ip != ""):
				interfaces[interface] = (ip, subnet)

	#-------------------------------------- INTERFACE LIST -----------------------------
		elif (inp == "2"):
			nlflood()
			print("\nINTERFACES ==================")
			for i, j in interfaces.items():
				print(str(i) + ": " + str(j))
			if (interfaces == {}):
				print("No interfaces configured")
			print("=============================")
			input("Enter to continue...")



	#-------------------------------------- ROUTING ------------------------------------
		elif (inp == "3"):
			while (True):
				nlflood()
				print("\nROUTING =======================")
				print("0: Exit")
				print("1: Select routing mode [Current: " + routingmodelkup[routingmode] + "]")
				print("2: Enable routing of all interfaces")
				print("3: Select interfaces to route")
				print("4: Display routed interfaces")
				print("5: Set passive interfaces")
				print("6: Toggle Auto-Summary [" + ("OFF", "ON")[autosum] + "]")
				inp = input("> ")
				if (inp == "0"): #Quit
					break
				elif (inp == "1"): #Routing Mode
					while True:
						nlflood()
						print("\nMODES =========================")
						for i, j in enumerate(routingmodelkup):
							print(str(i) + ": " + j)
						inp = input("[Cancel] > ")
						if (int(inp) < len(routingmodelkup) and int(inp) >= 0):
							routingmode = int(inp)
							if (routingmodelkup[routingmode] == "BGP"): # Specific BGP Configuration
								nlflood()
								inp = input("AS Number (0-65535) > ")
								bgp = BGPData(int(inp))
								print("Neigbor relationships are required.\nHit enter without typing anything to finish adding neighbors")
								while True:
									neighborIP = input("Neighbor IP > ")
									if (neighborIP == ""):
										break
									remoteAS = input("Remote AS > ")
									if (remoteAS == ""):
										break
									bgp.addNeighbor(neighborIP, remoteAS)
							break
						elif (inp == ""):
							break
				elif (inp == "2"): #Enable all interfaces 
					nlflood()
					for i, j in enumerate(interfaces.keys()):
						if (not j in routinginterfaces):
							routinginterfaces.append(j)
					print("All interfaces enabled for routing!")
					input("Enter to continue...")
				elif (inp == "3"): #Select interfaces to route
					while (True):
						nlflood()
						print("0: Exit")
						for i, j in enumerate(interfaces.keys()):
							print(str(i+1) + ": " + j + " [" + ("OFF", "ON")[j in routinginterfaces] + "]") #Print "id: interface [On | Off]" for each interface
						inp = int(input("> "))
						if (inp == 0):
							break
						if (list(interfaces.keys())[inp-1] in routinginterfaces):
							#Exists, disable
							del routinginterfaces[routinginterfaces.index(list(interfaces.keys())[inp-1])]
						else:
							#Does not exist, enable
							routinginterfaces.append(list(interfaces.keys())[inp-1])
				elif (inp == "4"): #Display Routed
					nlflood()
					print("ROUTED INTERFACES =========================")
					for i, j in enumerate(interfaces.keys()):
						print(str(i+1) + ": " + j + " [" + ("OFF", "ON")[j in routinginterfaces] + "]" + ("", " [Passive]")[j in passiveinterfaces])
					print("===========================================")
					input("Enter to continue...")

				elif (inp == "5"): #Set Passives
					while (True):
						nlflood()
						print("0: Exit")
						for i, j in enumerate(interfaces.keys()):
							print(str(i+1) + ": " + j + " [" + ("Active", "Passive")[j in passiveinterfaces] + "]") #Print "id: interface [Active | Off]" for each interface
						inp = int(input("> "))
						if (inp == 0):
							break
						if (list(interfaces.keys())[inp-1] in passiveinterfaces):
							#Exists, disable
							del passiveinterfaces[passiveinterfaces.index(list(interfaces.keys())[inp-1])]
						else:
							#Does not exist, enable
							passiveinterfaces.append(list(interfaces.keys())[inp-1])
					autosum = not autosum
	#--------------------------------------- DELETE --------------------------------------
		elif (inp == "4"):
			while True:
				nlflood()
				print("\nDELETE ==================")
				print("0: Exit")
				for i in range(len(interfaces.items())):
					print(str(i+1) + ": " + list(interfaces.keys())[i] + " [" + interfaces[list(interfaces.keys())[i]][0] + " - " + interfaces[list(interfaces.keys())[i]][1] + "]") #Strictly pythonic code only here sir 
				inp = input("> ")
				if (inp == "0"):
					break
				if (list(interfaces.keys())[int(inp)-1] in interfaces):
					#Exists, disable
					del interfaces[list(interfaces.keys())[int(inp)-1]]
	#-------------------------------------- GENERATE -------------------------------------
		elif (inp == "5"):
			generate()
			print("Finished!")
			inprepeat = input("Generate another configuration? [y/N]: ")
			break
	if (inprepeat.lower() == "y"):
		nlflood()
		continue
	else:
		break