import os
import json
import win32api
import glob
import sys
import shutil

class mp3FileTransfer:
    def __init__(self, music_folder, **kwargs):
        self.idFileName   = "mp3ID.jito"
        self.musicFolder  = music_folder
        self.mp3Files_musicFolder = []
        self.mp3Files_musicFolderNoID = []
        self.mp3Files_targetFolder = []
        self.targetFolder = ''

        #Define target folder
        if ("targetFolder" in kwargs):
            self.targetFolder = kwargs['targetFolder']
        else:  #Find the device with the ID-file 
            drives                     = self.listAllDrives()
            activeDrive                = self.findDriveWithIdFile(drives)
            idFilePath                 = activeDrive + self.idFileName 
            self.targetFolder          = activeDrive + self.getTargetFolderFromIdFile(idFilePath)


        self.mp3Files_musicFolder  = self.getListofMp3files(self.musicFolder)
        i = 0
        for filename in self.mp3Files_musicFolder:
            self.mp3Files_musicFolderNoID.append(filename.split('#',1)[1])
            i = i+1

        self.mp3Files_targetFolder = self.getListofMp3files(self.targetFolder)
        
    def listAllDrives(self):
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        return drives
    
    def findDriveWithIdFile(self, driveToSearch):
        for drive in driveToSearch:
            pathToSearch = drive + self.idFileName
            if os.path.isfile(pathToSearch):
                return drive
        
        return ''
    
    def getTargetFolderFromIdFile(self, idFilePath):
        targetFolder = ""
        if idFilePath != '':
            with open(idFilePath) as json_data:
                idData = json.load(json_data)
                json_data.close()
            
            targetFolder = idData["TargetFolder"]
        return targetFolder

    def getListofMp3files(self, folder):
        fileNames = []
        fullPaths = glob.glob(folder + "\\" + "*.mp3")
        for path in fullPaths:
            fileNames.append(path.split('\\')[-1])
        return fileNames

    def deleteMp3NotInList(self):
        for fileStr in self.mp3Files_targetFolder:
            fileStr_noPath = fileStr.split('\\')[-1]       
            if not fileStr_noPath in self.mp3Files_musicFolderNoID:
                filePath = self.targetFolder + '\\' + fileStr
                print("Deleting " + filePath)
                os.remove(filePath)
        self.mp3Files_targetFolder = self.getListofMp3files(self.targetFolder)
    
    def transferMp3Files_and_rename(self):
        Nfiles = len(self.mp3Files_musicFolderNoID)
        print('Files to transfer ' + str(Nfiles) + '...\n')
        i = 0
        for fileStr in self.mp3Files_musicFolderNoID:
            print( '#' + str(i+1) + '/' + str(Nfiles) )
            if not fileStr in self.mp3Files_targetFolder:
                src_file = self.musicFolder + '\\' + self.mp3Files_musicFolder[i]
                trg_file = self.targetFolder + '\\' + fileStr 
                print("Copying \"" + src_file + "\" to \"" + trg_file + "\"")
                shutil.copyfile(src_file, trg_file)
            else:
                print( fileStr + ' already exist --- skipping')
            i = i + 1

    def startFileTransfer(self):
        print("-- DELETE FILES START-- \n")
        self.deleteMp3NotInList()
        print(" ")
        print("-- TRANSFER START -- \n")
        self.transferMp3Files_and_rename()
        print(" ")
        print("-- TRANSFER COMPLETED -- \n")
        return  self.mp3Files_musicFolder  

