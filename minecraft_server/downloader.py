import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
from .msl_exceptions import exceptions
from .version import verify_version


def download_server_jar(version, download_location):
    """
    Downloads the Minecraft server JAR file for the selected version
    """
    file_name = f"server-{version}.jar"

    # Create the download_location directory if it does not exist
    os.makedirs(download_location, exist_ok=True)

    # URL of the website
    url = f"https://mcversions.net/download/{version}"

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
            f"The download url for minecraft server {version} does not exist")

    download_url = download_url['href']

    # Get the binary content of the fileand set the stream to True
    jar = requests.get(download_url, stream=True)

    # Get the total size of the file
    total_size = int(jar.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte

    file_path = os.path.join(download_location, file_name)

    # Initialize the progress bar
    t = tqdm(total=total_size, unit="iB", unit_scale=True,
             unit_divisor=1024, desc=f"Downloading {version}")
    # Open the file to write
    with open(file_path, "wb") as f:
        for data in jar.iter_content(block_size):
            # Update the progress bar
            t.update(len(data))
            f.write(data)
    t.close()

    if total_size != 0 and t.n != total_size:
        raise exceptions.FileDownloadError(
            f"An error occured while downloading {file_name} file")
    else:
        verify_version(file_path, version)
    
    return file_path
