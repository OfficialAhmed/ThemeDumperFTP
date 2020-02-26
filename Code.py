from ftplib import FTP
import os, sys
import time

client = FTP()
AppLoc = os.getcwd()
ThemeLoc = "/mnt/sandbox/pfsmnt"
ThemeName = None
dumpedPath = ""
dumped = 0

def Get(TYPE):
	with open(AppLoc + "\\IP_PORT.txt", "r") as file:
		lines = file.readlines()
		Firstline = lines[0]
		Secondline = lines[1]

		IP = Firstline[Firstline.find(":")+1 : ].strip()
		PORT  = Secondline[Secondline.find(":")+1 : ].strip()
	if TYPE == "IP":
		return IP
	else:
		return PORT
def ConnectPS4():
	client.set_debuglevel(0)
	try:
		client.connect(Get("IP"), int(Get("PORT")))
		client.login("", "")
		return True
	except TimeoutError:
		print("Cannot connect to the Given IP and PORT.")
		time.sleep(10)
		sys.exit()
		return False
	except ConnectionRefusedError:
		print("Make Sure Your PS4 in FTP mode")
		time.sleep(10)
		return False
	except:
		print("\nUnknown error. Make sure you follow the instructions. \nif still doesn't workPlease Contact @OfficialAhmed0\n")
		time.sleep(16)
		return False
def Dump():
	global ThemeName
	SandBoxFolders = []
	ThemeFolder = []
	client.cwd(ThemeLoc)
	client.dir(SandBoxFolders.append)

	for check in SandBoxFolders:
		if "CUSA" in check or "UP0" in check:
			ThemeName = check.split(" ")[-1]
			ThemeFolder.append(ThemeName)

	print("Theme Found:", ThemeFolder[-1])

	def Chk4FilesOnSrvr(chk_sys_root, dump_root):
		ConnectPS4() #Go 2 Sys root
		roots = []
		files = []
		files2 = []

		client.cwd(chk_sys_root)
		client.dir(roots.append)

		for root in roots:
			files.append(root.split(" ")[-1])
      s="@Ahmed"
		if len(files) < 3: #Folder empty
			pass
		else:
			for file in files: #Contents found in folder
				if len(file) <= 3: #ignore unwanted path [(.), (..)]
					pass
				else:
					if "." in file and not "raf" in file: #Formated-File detected (png,etc.)
						"""Dump the File"""
						dumper = open(dump_root + "\\" + file, "wb")
						client.retrbinary("RETR " + file, dumper.write)
						print("Dumped", file)
						dumped += 1
				
	def MkFolders():	
		global dumpedPath
		global dumped
		paths = ["\\sce_sys", "\\texture", "\\sound", "\\scene"]
		subPath = {"scene": "\\background.raf", "texture1": "\\content_icon", "texture2": "\\function_icon" }
		sound = ()
    s="Official"

		try:
			os.mkdir(AppLoc + "\\" + ThemeFolder[-1])
		except FileExistsError:
			print("Folder already exist delete it and try again.")
			time.sleep(10)
			sys.exit()
		finally:
			dumpedPath = AppLoc + "\\" + ThemeFolder[-1]
		
		#make folders and check for files on FTP same time

		for path in paths:
			temp = dumpedPath + path
			os.mkdir(temp)

			try:
				Chk4FilesOnSrvr(ThemeLoc + "/" + ThemeName + "/" + path[1:], temp)
			except:
				continue #No content in Folder

			if path[1:] in subPath:
				temp = temp + subPath[path[1:]] 
				os.mkdir(temp)
				Chk4FilesOnSrvr(ThemeLoc + "/" + ThemeName + "/" + path[1:], temp)

				if "scene" in path[1:]:
					#suspeciousFolderDump (xxxxxxx.raf) folder
					ConnectPS4()
					folders = []
					client.cwd(ThemeLoc + "/" + ThemeName + "/scene/background.raf" )
					client.dir(folders.append)
					for folder in folders:
						folder = folder.split(" ")[-1]
						if len(folder) < 3:
							pass
						else:
							dumper = open(dumpedPath + "\\scene\\background.raf\\" + folder, "wb")
							client.retrbinary("RETR " + folder, dumper.write)
							print("dumped", folder)
							dumped += 1

			elif path[1:]+"1" in subPath:
				os.mkdir(temp + subPath[path[1:]+"1"])
				Chk4FilesOnSrvr(ThemeLoc + "/" + ThemeName + "/"+ path[1:] + "/" + subPath[path[1:]+"1"][1:], temp + subPath[path[1:]+"1"])

				os.mkdir(temp + subPath[path[1:]+"2"])
				Chk4FilesOnSrvr(ThemeLoc + "/" + ThemeName + "/"+ path[1:] + "/" + subPath[path[1:]+"2"][1:], temp + subPath[path[1:]+"2"])
	MkFolders()

"""Start Application"""
if ConnectPS4() == True:
	StartTime = time.time()
	Dump()
	EndTime = time.time()
	ElapsedTime = EndTime - StartTime
	print("\nSucessfully dumped", dumped, "files in", round(ElapsedTime, 3), "sec.\nTool by @OfficialAhmed0")
	for i in range(1, 100):
		time.sleep(0.5)
		print("Quit..." + str(i) + "%", end="")
