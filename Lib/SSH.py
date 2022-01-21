import re
import time
from Lib import paramiko


class SSHClient(object):
    client = None

    def __init__(self, Address, Port, Username, Password, CommandDelay):
        self.Address = Address
        self.Port = Port
        self.Username = Username
        self.Password = Password
        self.CommandDelay = CommandDelay

    @property
    def OpenConn(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.Address, self.Port, username=self.Username, password=self.Password)
            transport = self.client.get_transport()
            self.client = transport.open_session()
            # set up for interactive mode, multiple commands - pty
            self.client.get_pty()
            self.client.invoke_shell()
            # keep session active with parameters while class is initialized
            self.client.keep_this = self.client
            SSHConnectingResult = "Connected"
        except paramiko.AuthenticationException:
            SSHConnectingResult = "Authentication failed, please verify your credentials: %s"
        except paramiko.BadHostKeyException as badHostKeyException:
            SSHConnectingResult = "Unable to verify server's host key: %s" % badHostKeyException
        except paramiko.SSHException as sshException:
            SSHConnectingResult = "Unable to establish SSH connection: %s" % sshException
        except Exception as e:
            SSHConnectingResult = str(e.args)
        return SSHConnectingResult

    def CommandExec(self, Command):
        # send command over to the switch
        self.client.send(Command + '\n')

        # initialize the data received from switch
        data = self.client.recv(1).decode('utf-8')

        while True:
            # read from socket, if there is data to be read
            if self.client.recv_ready():
                # keep reading 512 bytes of data from socket
                data += self.client.recv(9999).decode('utf-8')
            # grab current last line from collected socket, subject to
            # keep changing as more data flows in
            current_last_line = data.splitlines()[-1].strip()
            # check if there are spaces in the line, skip if so
            # print(current_last_line)
            if current_last_line.endswith('#'):
                print(data)
                break
            # password prompt
            elif current_last_line.endswith(':'):
                break
            elif "".join(re.findall(r'--More--', current_last_line)):
                self.client.send(' ')
            # minor delay to allow cpu some breathing room
            time.sleep(self.CommandDelay)
        return data

    def CloseConn(self):
        """ close ssh session
        closes the current session so that there are no hanging ssh threads """
        self.client.close()
