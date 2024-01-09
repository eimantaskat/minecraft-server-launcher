import logging
import time
import os

from PyQt5.QtCore import QProcess, pyqtSignal

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
    help_output = pyqtSignal(str)
    console_output = pyqtSignal(str)
    stopped = pyqtSignal()
    popup = pyqtSignal(str, str, str)

    def __init__(self, server):
        super().__init__()
        self.server = server
        self.cwd = os.path.abspath(os.path.join(self.server.server_jar, '..'))

        self._waiting_for_help = False

    def _run(self):
        java_version = get_java_version()
        if not java_version:
            logger.error('Java is not installed')
            self.popup.emit(
                'Java is not installed',
                'Running Minecraft Server requires Java. Please install it and try to run the server again.',
                'warning')
            return

        logger.info(f'Using Java version {java_version}')

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

        process_id = self.server_process.processId()
        logger.info(f'Server started with PID {process_id}')
        self.server_process.waitForFinished()
        logger.info('Server stopped')

    def send_command(self, command):
        if command == 'stop':
            self.stop()
        else:
            self.server_process.write(bytes(f'{command}\n'.encode()))

    def stop(self):
        self.server_process.write(b'stop\n')
        self.server_process.running = False
        
        self.stopped.emit()

    def _read_process_output(self):
        if self._waiting_for_help:
            time.sleep(0.1)

        try:
            output = self.server_process.readAllStandardOutput()
            if not output:
                output = self.server_process.readAllStandardError()
        except RuntimeError:
            return
        except AttributeError:
            return

        output_str = str(output, 'utf-8')
        if self._waiting_for_help:
            self.help_output.emit(output_str)
            self._waiting_for_help = False
        else:
            self.console_output.emit(output_str)

        # This might read the wrong output but I dont give a fuck
        # The worst that could happen is auto-completion not working and some server output missing
        if 'For help, type "help"' in output_str:
            self.server_process.write(bytes(f'help\n'.encode()))
            self._waiting_for_help = True
        
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
