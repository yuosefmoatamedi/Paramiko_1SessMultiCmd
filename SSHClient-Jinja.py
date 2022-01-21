import re
from jinja2 import Environment, FileSystemLoader
from Lib.SSH import SSHClient
from Lib.DiskIO import DiskIOFile


class ReadWriteFile:
    @classmethod
    def DiskIOFile_init(cls, Directory, ResultFolderName):
        cls.DiskIORWFile = DiskIOFile(Directory, ResultFolderName)

    def Read_Conf(self, FileName):
        return self.DiskIORWFile.Read_Config(FileName)

    def Write_Whole_Log_Content(self, LogFileType, LogContents):
        if LogFileType == "": LogFileType = "OUTPUT"
        LogFileContent = LogContents
        LogFileExtention = ".txt"
        self.DiskIORWFile.Write_To_Log(LogFileType, LogFileContent, LogFileExtention)

    def Write_HTML_File(self, HTMLContents):
        LogFileType = "OUTPUT"
        LogFileContent = HTMLContents
        LogFileExtention = ".htm"
        self.DiskIORWFile.Write_To_Log(LogFileType, LogFileContent, LogFileExtention)


class HtmlFileMaker:
    SystemMemoryName = ["Total", "Free", "Used"]
    InterfaceDetailsLog = ""
    CPUDetailsLog = ""
    MemoryDetailsLog = ""
    CPUTempDetailsLog = ""
    PowerTempDetailsLog = ""
    SessionDetailsLog = ""
    RouteDetailsLog = ""

    def Making_HTTP_Result(self):
        file_loader = FileSystemLoader('Templates')
        env = Environment(loader=file_loader)
        template = env.get_template('Template.htm')
        HTMLOutput = template.render(InterfaceCmdExeName=CalculationFuntions().InterfaceName,
                                     InterfaceCmdExeParamName=CalculationFuntions().InterfaceParam,
                                     InterfaceCmdExeStateName=CalculationFuntions().InterfaceParamCheck,
                                     SystemCmdExeCpuUsageCPUName=CalculationFuntions().SystemCpuUsageCPUName,
                                     SystemCmdExeCpuIdlePercent=CalculationFuntions().SystemCpuUsageIdlePercent,
                                     SystemCmdExeCpuStateName=CalculationFuntions().SystemCpuUsageStateName,
                                     SystemCmdExeMemUsageMemoryName=self.SystemMemoryName,
                                     SystemCmdExeMemSizeInByte=CalculationFuntions().SystemMemorySizeInByte,
                                     SystemCmdExeMemSizeInPercent=CalculationFuntions().SystemMemorySizeInPercent,
                                     SystemCmdExeCpuTempCPUName=CalculationFuntions().SystemCpuTempCPUName,
                                     SystemCmdExeCpuTempDegree=CalculationFuntions().SystemCpuTempDegree,
                                     SystemCmdExeCpuTempState=CalculationFuntions().SystemCpuTempState,
                                     SystemCmdExePwrTempPwrName=CalculationFuntions().SystemPwrTempPwrName,
                                     SystemCmdExePwrTempDegree=CalculationFuntions().SystemPwrTempDegree,
                                     SystemCmdExePwrTempState=CalculationFuntions().SystemPwrTempState,
                                     SessionStatusCmdExeSessionName=CalculationFuntions().SessSessionName,
                                     SessionStatusCmdExeTotalSession=CalculationFuntions().SessSessionTotal,
                                     SessionStatusCmdExeSameSessions=CalculationFuntions().SessSameSessions,
                                     SessionStatusCmdExeSessionID=CalculationFuntions().SessSessionID,
                                     SessionStatusCmdExeProtocols=CalculationFuntions().SessProtocols,
                                     SessionStatusCmdExeProtocolStates=CalculationFuntions().SessProtocolStates,
                                     SessionStatusCmdExeSessionUnic=CalculationFuntions().SessSessionUnic,
                                     SessionStatusCmdExeSessionDur=CalculationFuntions().SessSessionDur,
                                     SessionStatusCmdExePolicyID=CalculationFuntions().SessPolicyID,
                                     SessionStatusCmdExeVdomNames=CalculationFuntions().SessVdomNames,
                                     RoutingCmdExeRouteName=CalculationFuntions().RoutingRouteName,
                                     RoutingCmdExeSameRouteNames=CalculationFuntions().RoutingSameRouteNames,
                                     RoutingCmdExeRouteType=CalculationFuntions().RoutingRouteType,
                                     RoutingCmdExeRouteDefaultGateway=CalculationFuntions().RoutingDefaultGateway,
                                     RoutingCmdExeRouteVdomNames=CalculationFuntions().RoutingVdomNames,
                                     InterfaceLogDetails=self.InterfaceDetailsLog,
                                     CPULogDetails=self.CPUDetailsLog,
                                     MemoryLogDetails=self.MemoryDetailsLog,
                                     CPUTemperatureLogDetails=self.CPUTempDetailsLog,
                                     PowerTemperatureLogDetails=self.PowerTempDetailsLog,
                                     SessionLogDetails=self.SessionDetailsLog,
                                     RouteLogDetails=self.RouteDetailsLog)
        ReadWriteFile().Write_HTML_File(HTMLOutput)

    def Interface_Details(self, DetailedLog):
        JumpSteps = 0
        for AnyLines in DetailedLog.splitlines():
            AnyLines = AnyLines.strip()
            if re.findall(r'--More--.*', AnyLines):
                JumpSteps += 1
            elif JumpSteps == 1:
                JumpSteps += 1
            elif JumpSteps == 2:
                JumpSteps = 0
                self.InterfaceDetailsLog += AnyLines + "<br/>\n"
            else:
                self.InterfaceDetailsLog += AnyLines + "<br/>\n"

    def CPU_Details(self, DetailedLog):
        for AnyLines in DetailedLog.splitlines():
            AnyLines = AnyLines.strip()
            self.CPUDetailsLog += AnyLines + "<br/>\n"

    def Memory_Details(self, DetailedLog):
        for AnyLines in DetailedLog.splitlines():
            AnyLines = AnyLines.strip()
            self.MemoryDetailsLog += AnyLines + "<br/>\n"

    def CPU_Temp_Details(self, DetailedLog):
        for AnyLines in DetailedLog.splitlines():
            AnyLines = AnyLines.strip()
            self.CPUTempDetailsLog += AnyLines + "<br/>\n"

    def Power_Temp_Details(self, DetailedLog):
        for AnyLines in DetailedLog.splitlines():
            AnyLines = AnyLines.strip()
            self.PowerTempDetailsLog += AnyLines + "<br/>\n"

    def Session_Details(self, DetailedLog):
        for AnyLines in DetailedLog.splitlines():
            AnyLines = AnyLines.strip()
            self.SessionDetailsLog += AnyLines + "<br/>\n"

    def Route_Details(self, DetailedLog):
        for AnyLines in DetailedLog.splitlines():
            AnyLines = AnyLines.strip()
            self.RouteDetailsLog += AnyLines + "<br/>\n"


class CalculationFuntions:
    ProtocolType = {
        "1": "ICMP",
        "6": "TCP",
        "17": "UDP",
        "132": "SCTP"
    }
    ICMPProtocolState = {
        "0": "NONE"
    }
    TCPProtocolState = {
        "0": "NONE",
        "1": "ESTABLISHED",
        "2": "SYN_SENT</div>",
        "3": "SYN & SYN/ACK",
        "4": "FIN_WAIT",
        "5": "TIME_WAIT",
        "6": "CLOSE",
        "7": "CLOSE_WAIT",
        "8": "LAST_ACK",
        "9": "LISTEN"
    }
    UDPProtocolState = {
        "0": "UDP Reply not seen",
        "1": "UDP Reply seen"
    }
    SCTPProtocolState = {
        "0": "SCTP_S_NONE",
        "1": "SCTP_S_ESTABLISHED",
        "2": "SCTP_S_CLOSED",
        "3": "SCTP_S_COOKIE_WAIT",
        "4": "SCTP_S_COOKIE_ECHOED",
        "5": "SCTP_S_SHUTDOWN_SENT",
        "6": "SCTP_S_SHUTDOWN_RECD",
        "7": "SCTP_S_SHUTDOWN_ACK_SENT",
        "8": "SCTP_S_MAX"
    }
    Username = ""
    Password = ""
    IPAddress = ""
    VdomLists = {}
    InterfaceName = []
    InterfaceParam = []
    InterfaceParamCheck = []
    SystemCpuUsageCPUName = []
    SystemCpuUsageIdlePercent = []
    SystemCpuUsageStateName = []
    SystemMemorySizeInByte = []
    SystemMemorySizeInPercent = []
    SystemCpuTempCPUName = []
    SystemCpuTempDegree = []
    SystemCpuTempState = []
    SystemPwrTempPwrName = []
    SystemPwrTempDegree = []
    SystemPwrTempState = []
    TotalSessions = ""
    SessSessionName = []
    SessSessionTotal = []
    SessSameSessions = []
    SessSessionID = []
    SessProtocols = []
    SessProtocolStates = []
    SessSessionUnic = []
    SessSessionDur = []
    SessPolicyID = []
    SessVdomNames = []
    RoutingRouteName = []
    RoutingSameRouteNames = []
    RoutingRouteType = []
    RoutingDefaultGateway = []
    RoutingVdomNames = []

    def Read_Credentials(self, CredencialCommandList):
        self.Username, self.Password, self.IPAddress = CredencialCommandList.split(',')
        if self.Username == '':
            LogType = "ERROR"
            LogFileContent = "Username field is empty"
        else:
            if self.Password == '':
                LogType = "ERROR"
                LogFileContent = "Password field is empty"
            else:
                if self.IPAddress == '':
                    LogType = "ERROR"
                    LogFileContent = "IP Address field is empty"
                else:
                    LogType = "OUTPUT"
                    LogFileContent = "Credencial is OK"
        ReadWriteFile().Write_Whole_Log_Content(LogType, LogFileContent)
        return LogType

    def VDOM_Lookuping(self, CommandResults):
        for EveryLine in CommandResults.split("\n"):
            vdomName = "".join(re.findall(r'name=[\w+-_]{0,20}/', EveryLine))
            vdomName = vdomName[5:(len(vdomName) - 1)]
            vdomIdStr = "".join(re.findall(r'index=[\d+]{0,2} ', EveryLine))
            vdomId = str(vdomIdStr[6:len(vdomIdStr) - 1])
            if vdomId != '':
                self.VdomLists[vdomId] = vdomName

    def Interface_Status(self, CommandResults, Interface, Param):
        ReadWriteFile().Write_Whole_Log_Content("", CommandResults)
        HtmlFileMaker().Interface_Details("".join(CommandResults))
        if Param == '' or Param == 'status':
            InterfaceCheck = "".join(re.findall(r'status              :.*', CommandResults))
            InterfaceCheck = "".join(re.findall(r':.*', InterfaceCheck))
            InterfaceCheck = InterfaceCheck[1:len(InterfaceCheck)]
            PARAM = 'Status'
        else:
            InterfaceCheck = "".join(re.findall(Param + ".*", CommandResults))
            InterfaceCheck = InterfaceCheck[1:len(InterfaceCheck)]
            PARAM = Param
        self.InterfaceName.append(Interface)
        self.InterfaceParam.append(PARAM)
        self.InterfaceParamCheck.append(InterfaceCheck)

    def CPU_Memory_status(self, CommandResults):
        ReadWriteFile().Write_Whole_Log_Content("", CommandResults)
        self.CPU_STATUS(CommandResults)
        self.MEM_STATUS(CommandResults)

    def CPU_STATUS(self, CommandResults):
        HtmlFileMaker().CPU_Details(CommandResults)
        # ----------Check CPU Status---------------
        CpuList = re.findall(r'CPU.*', CommandResults)
        CpuListStr = "\n".join(CpuList)
        for iCpuIdleNo in CpuListStr.split("\n"):
            CpuIdleNo = int("".join(re.findall(r'\d+', str(re.findall(r'[\d]{1,3}% idle', iCpuIdleNo)))))
            CpuName = "".join(re.findall(r'CPU.* states:', iCpuIdleNo))
            CpuNameStr = "".join(re.findall(r'CPU[\d]{0,2}', CpuName))
            if CpuIdleNo <= 30:
                CpuStatusStr = "Overload"
            else:
                CpuStatusStr = "Normal"
            self.SystemCpuUsageCPUName.append(CpuNameStr)
            self.SystemCpuUsageIdlePercent.append(str(CpuIdleNo))
            self.SystemCpuUsageStateName.append(CpuStatusStr)

    def MEM_STATUS(self, CommandResults):
        # ----------Check Memory Status---------------
        Memory = re.findall(r'Memory.*', CommandResults)
        MemoryStr = "".join(Memory)
        # ---- Total Memory --------*
        MemoryTotalInByte = re.findall(r'[\d]{1,9}', str(re.findall(r'[\d]{1,9}k total', MemoryStr)))
        MemoryTotalInByteStr = "".join(MemoryTotalInByte)
        if int(MemoryTotalInByteStr) > 1000:
            MemoryTotalInByte = int(MemoryTotalInByteStr) // 1000  # <- Keep Total Memory value in MB :: int
            MemoryTotalInByteStr = str(MemoryTotalInByte) + " MB  "  # <- Keep Total Memory value in MB :: string
        if MemoryTotalInByte > 1000:
            MemoryTotalInByte //= 1000  # <- Keep Total Memory value in GB :: int
            MemoryTotalInByteStr = str(MemoryTotalInByte) + " GB  "  # <- Keep Total Memory value in GB :: string
        # ---- Used Memory --------*
        MemoryUsedInByte = re.findall(r'[\d]{1,9}', str(re.findall(r'[\d]{1,9}k used', MemoryStr)))
        MemoryUsedInByteStr = "".join(MemoryUsedInByte)
        if int(MemoryUsedInByteStr) > 1000:
            MemoryUsedInByte = int(MemoryUsedInByteStr) // 1000  # <- Keep Used Memory value in MB :: int
            MemoryUsedInByteStr = str(MemoryUsedInByte) + " MB  "  # <- Keep Used Memory value in MB :: string
        if MemoryUsedInByte > 1000:
            MemoryUsedInByte //= 1000  # <- Keep Used Memory value in GB :: int
            MemoryUsedInByteStr = str(MemoryUsedInByte) + " GB  "  # <- Keep Used Memory value in GB :: string
        MemoryUsedInPercent = re.findall(r'[\d]{1,3}', str(re.findall(r'used \([\d]{1,3}%\)', MemoryStr)))
        MemoryUsedInPercentStr = "".join(MemoryUsedInPercent)
        # ---- Free Memory --------*
        MemoryFreeInByte = re.findall(r'[\d]{1,9}', str(re.findall(r'[\d]{1,9}k free ', MemoryStr)))
        MemoryFreeInByteStr = "".join(MemoryFreeInByte)
        if int(MemoryFreeInByteStr) > 1000:
            MemoryFreeInByte = int(MemoryFreeInByteStr) // 1000  # <- Keep Free Memory value in MB :: int
            MemoryFreeInByteStr = str(MemoryFreeInByte) + " MB  "  # <- Keep Free Memory value in MB :: string
        if MemoryFreeInByte > 1000:
            MemoryFreeInByte //= 1000  # <- Keep Free Memory value in GB :: int
            MemoryFreeInByteStr = str(MemoryFreeInByte) + " GB  "  # <- Keep Free Memory value in MB :: string
        MemoryFreeInPercent = re.findall(r'[\d]{1,3}', str(re.findall(r'free \([\d]{1,3}%\)', MemoryStr)))
        MemoryFreeInPercentStr = "".join(MemoryFreeInPercent)
        self.SystemMemorySizeInByte.extend([MemoryTotalInByteStr, MemoryFreeInByteStr, MemoryUsedInByteStr])
        self.SystemMemorySizeInPercent.extend(["", MemoryFreeInPercentStr, MemoryUsedInPercentStr])
        HtmlFileMaker().Memory_Details(MemoryStr)

    def CPU_Power_Temperature(self, CommandResults):
        ReadWriteFile().Write_Whole_Log_Content("", CommandResults)
        self.CPU_TEMP(CommandResults)
        self.PWR_TEMP(CommandResults)

    def CPU_TEMP(self, CommandResults):
        # ----------Check CPU Temperature Status---------------
        CpuTemp = re.findall(r'CPU Core.*', CommandResults)
        CpuTempLineStr = "\n".join(CpuTemp)
        for iCpuTemp in CpuTempLineStr.split("\n"):
            CpuTempNo = int("".join(re.findall(r'[\d]{1,3}', "".join(re.findall(r'value=[\d]{1,3}  ', iCpuTemp)))))
            if CpuTempNo > 87:
                StatusStr = "Too hot"
            else:
                StatusStr = "Normal"
            CpuNameStr = "".join(re.findall(r'CPU Core [\d]', iCpuTemp))
            CpuNameStr = CpuNameStr[4:len(CpuNameStr)]
            self.SystemCpuTempCPUName.append(CpuNameStr)
            self.SystemCpuTempDegree.append(str(CpuTempNo))
            self.SystemCpuTempState.append(StatusStr)
        HtmlFileMaker().CPU_Temp_Details(CpuTempLineStr)

    def PWR_TEMP(self, CommandResults):
        # ----Check Power supply Temperature--------*
        PowerSupTemp = re.findall(r'PS[\d+] Temp.*', CommandResults)
        PowerSupTempLineStr = "\n".join(PowerSupTemp)
        for iPowerSupTemp in PowerSupTempLineStr.split("\n"):
            PowerSupTempNo = int(
                "".join(re.findall(r'[\d]{0,3}', "".join(re.findall(r'value=[\d]{0,3} ', iPowerSupTemp)))))
            if PowerSupTempNo > 87:
                StatusStr = "Too hot"
            else:
                StatusStr = "Normal"
            PowerSuppNameStr = "".join(re.findall(r'PS[\d]', iPowerSupTemp))
            self.SystemPwrTempPwrName.append(PowerSuppNameStr)
            self.SystemPwrTempDegree.append(str(PowerSupTempNo))
            self.SystemPwrTempState.append(StatusStr)
        HtmlFileMaker().Power_Temp_Details(PowerSupTempLineStr)

    def Session_Status(self, SessionName, CommandResults):
        SessionUnic = ""
        LastSessionUnic = ""
        SessionID = 0
        ProtocolStates = ""

        ReadWriteFile().Write_Whole_Log_Content("", CommandResults)
        SessionLogs = "".join(CommandResults)
        self.SessSessionName.append(SessionName)
        for AnyLinesInSessionLogs in SessionLogs.split("\n"):
            if "session info" in AnyLinesInSessionLogs.lower():
                self.SessSameSessions.append(SessionName)
                # Protocol State ---------------
                Protocol = "".join(re.findall(r'proto=[\d+]{0,2}', AnyLinesInSessionLogs))
                Protocol = Protocol[6:(len(Protocol))]
                Protocols = self.ProtocolType.get(Protocol)
                self.SessProtocols.append(Protocols)
                ProtoState = "".join(re.findall(r'proto_state=[\d+]{0,2}', AnyLinesInSessionLogs))
                ProtoState = ProtoState[13:(len(ProtoState))]
                if Protocol == "1":
                    if ProtoState in self.ICMPProtocolState:
                        ProtocolStates = self.ICMPProtocolState.get(ProtoState)
                elif Protocol == "6":
                    if ProtoState in self.TCPProtocolState:
                        ProtocolStates = self.TCPProtocolState.get(ProtoState)
                elif Protocol == "17":
                    if ProtoState in self.UDPProtocolState:
                        ProtocolStates = self.UDPProtocolState.get(ProtoState)
                elif Protocol == "132":
                    if ProtoState in self.SCTPProtocolState:
                        ProtocolStates = self.SCTPProtocolState.get(ProtoState)
                self.SessProtocolStates.append(ProtocolStates)
                # Session Duration ---------------
                SessionDur = "".join(re.findall(r'duration=[\d+]{0,20}', AnyLinesInSessionLogs))
                SessionDur = "".join(re.findall(r'[\d+]{0,20}', SessionDur))
                self.SessSessionDur.append(str(SessionDur))
            if "dir=org" in AnyLinesInSessionLogs.lower():  # "hook=pre"
                # Session Uniqer ---------------
                SessionUnic = "".join(re.findall(r'dir=org act=noop [\d+\.\:\-\>]{0,100}\(', AnyLinesInSessionLogs))
                SessionUnic = SessionUnic[17:(len(SessionUnic) - 1)]
                self.SessSessionUnic.append(SessionUnic)
            if "misc=0" in AnyLinesInSessionLogs.lower():
                # Policy ID ---------------
                PolicyID = "".join(re.findall(r'policy_id=[\d+]{0,4}', AnyLinesInSessionLogs))
                PolicyID = "".join(re.findall(r'[\d+]{0,4}', PolicyID))
                self.SessPolicyID.append(PolicyID)
                # vdom Name ---------------
                VdomName = "".join(re.findall(r'vd=[\d+]{0,2}', AnyLinesInSessionLogs))
                VdomName = "".join(re.findall(r'[\d+]{0,2}', VdomName))
                if VdomName in self.VdomLists:
                    VdomNames = self.VdomLists.get(VdomName)
                    self.SessVdomNames.append(VdomNames)
                if LastSessionUnic != SessionUnic:
                    SessionID += 1
                LastSessionUnic = SessionUnic
                self.SessSessionID.append(str(SessionID))
            if "total session" in AnyLinesInSessionLogs.lower():
                TotalSession = "".join(re.findall(r'total session [\d]{0,3}', AnyLinesInSessionLogs))
                TotalSession = "".join(re.findall(r'[\d]{0,3}', TotalSession))
                self.SessSessionTotal.append(TotalSession)
        HtmlFileMaker().Session_Details(CommandResults)

    def Routing_Status(self, CommandResults, VdomName, RouteName):
        ReadWriteFile().Write_Whole_Log_Content("", CommandResults)
        HtmlFileMaker().Route_Details(CommandResults)
        self.RoutingRouteName.append(RouteName)
        RoutingType = "\n".join(re.findall(r'via.*",', CommandResults))
        for everyLine in RoutingType.splitlines():
            self.RoutingSameRouteNames.append(RouteName)
            RoutingsType = everyLine[5:len(everyLine) - 2]
            DefaultGateway = "\n".join(re.findall(r'\*.*,', CommandResults))
            DefaultGateway = DefaultGateway[2:len(DefaultGateway) - 1]
            self.RoutingRouteType.append(RoutingsType)
            self.RoutingDefaultGateway.append(DefaultGateway)
            self.RoutingVdomNames.append(VdomName)


class OpearatingFunctions:
    def __init__(self):
        self.CredencialCommandList = ""
        self.PerformanceCommandList = ""
        self.TemperatureCommandList = ""
        self.InterfaceCommandList = ""
        self.SessionCommandList = ""
        self.RouteCommandList = ""

    def SortCommands(self, SettingFile):
        for AnyLines in SettingFile.splitlines():
            AnyLines = AnyLines.strip()
            FindCommentLine = False
            if re.findall(r'#', AnyLines): FindCommentLine = True
            if AnyLines != '' and not FindCommentLine:
                key, value = AnyLines.split('(')
                key = str(key).lower()
                value = value[:-1]
                if key == "credential":
                    self.CredencialCommandList = value
                elif key == "interface":
                    self.InterfaceCommandList += value + "\n"
                elif key == "system":
                    value = str(value).lower()
                    if value == "performance":
                        self.PerformanceCommandList = value + "\n"
                    elif value == "temperature":
                        self.TemperatureCommandList = value + "\n"
                elif key == "session":
                    self.SessionCommandList += value + "\n"
                elif key == "route":
                    self.RouteCommandList += value + "\n"

    def FetchCommands(self):
        ConfigGlobal = "config global"
        ConfigVdom = "config vdom"
        DiagnoseSystemVdList = "diagnose sys vd list"
        ConfigSystemInterface = "config system interface"
        GetSystemPerformance = "get system performance status"
        ExecuteSensorList = "execute sensor list"
        ClearSessionFilter = "diagnose sys session filter clear"
        DiagnoseSessionFilter = "diagnose sys session filter "
        DiagnoseSessionList = "diagnose sys session list"
        RouterInfo = "get router info routing-table details "
        ConfigEND = "end"
        ConfigNEXT = "next"
        'global RouteName, GoNext'
        Port = 22
        DelayInterval = 0.15
        CalcFunc = CalculationFuntions()

        if self.CredencialCommandList != "":
            ConnectionResult = CalcFunc.Read_Credentials(self.CredencialCommandList)
            if ConnectionResult.upper() == "OUTPUT":
                Connection = SSHClient(CalcFunc.IPAddress, Port, CalcFunc.Username, CalcFunc.Password, DelayInterval)
                ConnectionResult = Connection.OpenConn
                if ConnectionResult.upper() == "CONNECTED":
                    ReadWriteFile().Write_Whole_Log_Content("OUTPUT", ConnectionResult)
                    Connection.CommandExec(ConfigGlobal)
                    CommandExecutionResult = Connection.CommandExec(DiagnoseSystemVdList)
                    CalcFunc.VDOM_Lookuping(CommandExecutionResult)
                    Connection.CommandExec(ConfigEND)
                    if self.InterfaceCommandList != "":
                        for AnyLinesInInterfaceCommandList in self.InterfaceCommandList.splitlines():
                            AnyLinesInInterfaceCommandList = AnyLinesInInterfaceCommandList.strip()
                            Interface, Param = AnyLinesInInterfaceCommandList.split(',')
                            Connection.CommandExec(ConfigGlobal)
                            Connection.CommandExec(ConfigSystemInterface)
                            command = "edit " + Interface
                            Connection.CommandExec(command)
                            if Param == '':
                                command = "get "
                            else:
                                command = "get | grep -i " + Param
                            CommandExecutionResult = Connection.CommandExec(command)
                            CalcFunc.Interface_Status(CommandExecutionResult, Interface, Param)
                            Connection.CommandExec(ConfigEND)
                            Connection.CommandExec(ConfigEND)
                    if self.PerformanceCommandList != "":
                        Connection.CommandExec(ConfigGlobal)
                        CommandExecutionResult = Connection.CommandExec(GetSystemPerformance)
                        CalcFunc.CPU_Memory_status(CommandExecutionResult)
                        Connection.CommandExec(ConfigEND)
                    if self.TemperatureCommandList != "":
                        Connection.CommandExec(ConfigGlobal)
                        CommandExecutionResult = Connection.CommandExec(ExecuteSensorList)
                        CalcFunc.CPU_Power_Temperature(CommandExecutionResult)
                        Connection.CommandExec(ConfigEND)
                    if self.SessionCommandList != "":
                        for AnyLinesInSessionCommandList in self.SessionCommandList.splitlines():
                            AnyLinesInSessionCommandList = AnyLinesInSessionCommandList.strip()
                            if AnyLinesInSessionCommandList != '':
                                src, dst, dstport, SessionName = AnyLinesInSessionCommandList.split(',')
                                Connection.CommandExec(ConfigGlobal)
                                Connection.CommandExec(ClearSessionFilter)
                                if src != '':
                                    command = DiagnoseSessionFilter + "src " + src
                                    Connection.CommandExec(command)
                                if dst != '':
                                    command = DiagnoseSessionFilter + "dst " + dst
                                    Connection.CommandExec(command)
                                if dstport != '':
                                    command = DiagnoseSessionFilter + "dport " + dstport
                                    Connection.CommandExec(command)
                                CommandExecutionResult = Connection.CommandExec(DiagnoseSessionList)
                                CalcFunc.Session_Status(SessionName, CommandExecutionResult)
                                Connection.CommandExec(ConfigEND)
                    if self.RouteCommandList != "":
                        for AnyLinesInRouteCommandList in self.RouteCommandList.splitlines():
                            AnyLinesInRouteCommandList = AnyLinesInRouteCommandList.strip()
                            VdomName, IPAddress, RouteName = AnyLinesInRouteCommandList.split(',')
                            Connection.CommandExec(ConfigVdom)
                            command = "edit " + VdomName
                            Connection.CommandExec(command)
                            command = RouterInfo + IPAddress
                            CommandExecutionResult = Connection.CommandExec(command)
                            CalcFunc.Routing_Status(CommandExecutionResult, VdomName, RouteName)
                            Connection.CommandExec(ConfigEND)
                    Connection.CloseConn()
                    HtmlFileMaker().Making_HTTP_Result()
                else:
                    ReadWriteFile().Write_Whole_Log_Content("ERROR", ConnectionResult)


def main():
    wrkdir = r".\\"
    ReadWriteFile().DiskIOFile_init(wrkdir, "Results")
    SettingFile = ReadWriteFile().Read_Conf("Settings.ini")
    OpFunc = OpearatingFunctions()
    OpFunc.SortCommands(SettingFile)
    OpFunc.FetchCommands()


if __name__ == "__main__":
    main()
