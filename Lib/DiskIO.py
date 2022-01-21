import time
import os


class DiskIOFile:
    NewPath = ""

    def __init__(self, Directory, ResultFolderName):
        self.WorkingDirectory = Directory
        self.ResultFolderName = ResultFolderName
        self.LocalTime = time.localtime()
        self.TimeStamp = time.strftime('%b-%d-%Y_%H-%M', self.LocalTime)
        self.Create_New_Directory()

    def Read_Config(self, FileName):
        try:
            ReadConfigLines = open(self.WorkingDirectory + FileName, "r")
            if ReadConfigLines.mode == 'r':
                # contents = read_settings.read()
                ConfigLines = ReadConfigLines.read()
            ReadConfigLines.close()
            # lines = contents.splitlines()
        except FileNotFoundError:
            self.Write_To_Log("ERROR", "Setting File not found: %s", ".log")
        return ConfigLines

    def Write_To_Log(self, Result, LogFileContent, LogFileExtention):
        if Result.upper() == "ERROR":
            LogFileName = "Error Log - "
        elif Result.upper() == "OUTPUT":
            LogFileName = "Log - "
        LogWriter = open(self.NewPath + r'\\' + LogFileName + LogFileExtention, "a+")
        LogWriter.write(LogFileContent)
        LogWriter.close()

    def Create_New_Directory(self):
        self.NewPath = os.path.join(self.WorkingDirectory, self.ResultFolderName + " " + self.TimeStamp)
        if not os.path.exists(self.NewPath):
            os.makedirs(self.NewPath)
