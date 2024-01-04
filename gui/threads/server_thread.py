import logging
import os

from PyQt5.QtCore import QProcess, pyqtSignal
import debugpy

from minecraft_server.utils import get_java_version

from .msl_thread import MslThread


logger = logging.getLogger('msl')


class Process(QProcess):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = False

    def write(self, data):
        super().write(data)

    def start(self, command):
        self.running = True
        super().start(command)

    def waitForFinished(self):
        super().waitForFinished(-1)

    def __del__(self):
        self.waitForFinished()


class ServerThread(MslThread):
    console_output = pyqtSignal(str)
    stopped = pyqtSignal()
    popup = pyqtSignal(str, str, str)

    def __init__(self, server):
        super().__init__()
        self.server = server
        self.cwd = os.path.abspath(os.path.join(self.server.server_jar, '..'))


    def _run(self):
        java_version = get_java_version()
        if not java_version:
            logger.error('JAVA is not installed')
            self.popup.emit(
                'JAVA is not installed',
                'Running Minecraft Server requires JAVA. Please install it and try to run the server again.',
                'error')
            return

        run_command = self.server.get_run_command()
        run_command = ' '.join(run_command)

        self.server_process = Process()
        self.server_process.setWorkingDirectory(self.cwd)
        self.server_process.readyReadStandardOutput.connect(self._read_process_output)
        self.server_process.readyReadStandardError.connect(self._read_process_output)
        self.server_process.start(run_command)
        logger.info(f'Starting server with command: {run_command}')
        if not self.server_process.waitForStarted():
            logger.error(f'Error starting process: {self.server_process.errorString()}')
        self.server_process.waitForFinished()
        logger.info('Server stopped')


    def send_command(self, command):
        if command == 'stop':
            self.stop()
        else:
            self.server_process.write(bytes(f'{command}\n'.encode()))
        self._read_process_output()


    def stop(self):
        self.server_process.write(b'stop\n')
        self.server_process.running = False
        
        self.stopped.emit()


    def _read_process_output(self):
        try:
            output = self.server_process.readAllStandardOutput()
            if not output:
                output = self.server_process.readAllStandardError()
        except RuntimeError:
            return
        except AttributeError:
            return

        output_str = str(output, 'utf-8')
        self.console_output.emit(output_str)
        

    @property
    def status(self):
        is_online = self.server.is_online()
        if is_online:
            return 'running'
        elif self.server_process.running:
            return 'starting'
        else:
            return 'stopped'


    @property
    def info(self):
        return self.server.get_info()