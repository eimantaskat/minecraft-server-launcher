from .msl_thread import MslThread
import os
import subprocess


class ServerThread(MslThread):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.cwd = os.path.abspath(os.path.join(self.server.server_jar, ".."))

    def _run(self):
        run_command = self.server.get_run_command()
        print(run_command)
        self.server_process = subprocess.Popen(run_command, stdin=subprocess.PIPE, shell=True, cwd=self.cwd)
        self.server_process.wait()

    def send_command(self, command):
        self.server_process.communicate(input=f'{command}\n'.encode())

    def stop(self):
        self.server_process.communicate(b'stop\n')
