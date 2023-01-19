import zipfile
import json
import requests
from .msl_exceptions import IncorrectServerVersion

def get_version(file):
    # Extract version.json file from the downloaded JAR file
    with zipfile.ZipFile(file, 'r') as zip_ref:
        version_json = zip_ref.read('version.json')

    # Load version.json as a dictionary
    version_data = json.loads(version_json)

    return version_data["id"]

def get_version_id(file):
    # Extract version.json file from the downloaded JAR file
    with zipfile.ZipFile(file, 'r') as zip_ref:
        version_json = zip_ref.read('version.json')

    # Load version.json as a dictionary
    version_data = json.loads(version_json)

    return version_data['world_version']


def verify_version(file, expected_version):
    version = get_version(file)

    # Check the version number in the version.json file
    if version != expected_version:
        raise IncorrectServerVersion(
            f"Incorrect {file} version. Expected {expected_version}, got {version}")


def filter_list_dicts(data, key, value):
    """
    Filters a list of dictionaries by a selected key-value pair.
    """
    filtered_data = [d for d in data if d[key] == value]
    return filtered_data


def get_minecraft_versions(release=True):
    # URL of the version manifest
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

    # Retrieve the JSON data from the URL
    response = requests.get(url)

    # Parse the JSON data
    data = json.loads(response.text)

    # Extract the version information from the JSON data
    versions = data["versions"]

    if release:
        versions = filter_list_dicts(versions, "type", "release")

    # Keep only version keys in returned dict
    versions = [version["id"] for version in versions]
    return versions
