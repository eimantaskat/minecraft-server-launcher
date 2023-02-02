from .msl_thread import MslThread
from minecraft_server import exceptions, verify_version
from PyQt5.QtCore import pyqtSignal
import os
import requests
from bs4 import BeautifulSoup


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
        self.download_location = download_location

    def _run(self):
        file_name = f"server-{self.jar_version}.jar"

        # Create the download_location directory if it does not exist
        os.makedirs(self.download_location, exist_ok=True)

        # URL of the website
        url = f"https://mcversions.net/download/{self.jar_version}"

        # Send a GET request to the website
        response = requests.get(url)

        # Check if the response is ok
        if response.status_code != 200:
            raise exceptions.InvalidResponseStatusError(
                f"{url} responded with {response.status_code} {response.reason}")

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the server JAR file URL
        download_url = soup.find("a", string="Download Server Jar")

        # Check if the download URL exists
        if download_url is None:
            raise exceptions.DownloadUrlDoesNotExistError(
                f"The download url for minecraft server {self.jar_version} does not exist")

        download_url = download_url['href']

        # Get the binary content of the file and set the stream to True
        ok = False
        while not ok:
            try:
                jar = requests.get(download_url, stream=True)
                ok = True
            except requests.exceptions.ConnectionError: # TODO
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

        if total_size != 0 and os.path.getsize(file_path) != total_size:
            raise exceptions.FileDownloadError(
                f"An error occured while downloading {file_name} file")
        else:
            verify_version(file_path, self.jar_version)
        
        self.download_finished.emit()
