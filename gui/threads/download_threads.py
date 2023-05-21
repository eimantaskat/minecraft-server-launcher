from gui.threads.msl_thread import MslThread
from minecraft_server import exceptions, VersionManager
from PyQt5.QtCore import pyqtSignal
import os
import requests
import json
import hashlib


def get_jar_versions(versions_file) -> list:
	with open(versions_file, "r") as f:
		return json.load(f)


class DownloadThread(MslThread):
	download_finished = pyqtSignal()
	increment_progress_bar_value = pyqtSignal(int)
	set_maximum_progress_bar_value = pyqtSignal(int)
	set_progress_bar_description = pyqtSignal(str)
	reset_progress_bar = pyqtSignal()
	show_progress_bar = pyqtSignal()


	def __init__(self, jar_version, download_location):
		super().__init__()
		self.jar_version = jar_version
		self.download_location = os.path.expandvars(download_location)


	def _run(self):
		versions_file = os.path.join(os.path.abspath(os.path.join(self.download_location ,"../..")), "versions.json")

		available_versions = get_jar_versions(versions_file)

		if self.jar_version in available_versions['release'].keys():
			version_data = available_versions['release'][self.jar_version]
		elif self.jar_version in available_versions['snapshot'].keys():
			version_data = available_versions['snapshot'][self.jar_version]
		elif self.jar_version in available_versions['old_alpha'].keys():
			version_data = available_versions['old_alpha'][self.jar_version]
		elif self.jar_version in available_versions['old_beta'].keys():
			version_data = available_versions['old_beta'][self.jar_version]
		else:
			raise Exception(f"Version {self.jar_version} does not exist")
		
		file_name = f"server-{self.jar_version}.jar"
		download_url = version_data['download']
		sha1 = version_data['sha1']

		# Get the binary content of the file and set the stream to True
		ok = False
		while not ok:
			try:
				jar = requests.get(download_url, stream=True)
				ok = True
			except requests.exceptions.ConnectionError:  # TODO
				pass

		# Get the total size of the file
		total_size = int(jar.headers.get("content-length", 0))
		block_size = 1024  # 1 Kibibyte

		file_path = os.path.join(self.download_location, file_name)

		self.reset_progress_bar.emit()
		self.set_maximum_progress_bar_value.emit(total_size)
		self.set_progress_bar_description.emit(f"Downloading {file_name}")
		self.show_progress_bar.emit()

		# Open the file to write
		with open(file_path, "wb") as f:
			for data in jar.iter_content(block_size):
				# Update the progress bar
				self.increment_progress_bar_value.emit(len(data))
				f.write(data)

		if total_size != 0 and os.path.getsize(file_path) != total_size \
				or not VersionManager.verify_sha1(file_path, sha1):
			raise exceptions.FileDownloadError(
				f"An error occured while downloading {file_name} file")
		else:
			VersionManager.verify_version(file_path, self.jar_version)

		self.download_finished.emit()

	def stop(self):
		self.terminate() # TODO
