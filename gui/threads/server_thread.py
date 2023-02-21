from PyQt5.QtCore import QProcess, pyqtSignal
from .msl_thread import MslThread
import os


class Process(QProcess):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __del__(self):
        self.waitForFinished()
        print("Process deleted")


class ServerThread(MslThread):
    console_output = pyqtSignal(str)
    stopped = pyqtSignal()

    def __init__(self, server):
        super().__init__()
        self.server = server
        self.cwd = os.path.abspath(os.path.join(self.server.server_jar, ".."))


    def _run(self):
        run_command = self.server.get_run_command()
        run_command = ' '.join(run_command)
        print("CWD:", self.cwd)
        self.server_process = Process()
        self.server_process.setWorkingDirectory(self.cwd)
        self.server_process.readyReadStandardOutput.connect(self._read_process_output)
        self.server_process.readyReadStandardError.connect(self._read_process_output)
        self.server_process.start(run_command)
        print("Process started:", run_command)
        if not self.server_process.waitForStarted():
            print("Error starting process:", self.server_process.errorString())
        self.server_process.waitForFinished()
        print("Process finished")


    def send_command(self, command):
        if command == 'stop':
            self.stop()
        else:
            self.server_process.write(f'{command}\n'.encode())


    def stop(self):
        self.server_process.write(b'stop\n')
        self.server_process.waitForBytesWritten()
        self.server_process.waitForFinished()
        self.stopped.emit()
        self._read_process_output()
        del self.server_process


    def _read_process_output(self):
        try:
            output = self.server_process.readAllStandardOutput()
            if not output:
                output = self.server_process.readAllStandardError()
        except RuntimeError:
            return

        output_str = str(output, 'utf-8')
        self.console_output.emit(output_str)
