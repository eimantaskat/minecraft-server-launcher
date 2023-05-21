import json
import hashlib
import os
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# from minecraft_server.msl_exceptions import IncorrectServerVersion

IncorrectServerVersion = Exception


VERSION_MANIFEST_URL = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
MAX_WORKERS = os.cpu_count()
MAX_RETRIES = 3


def merge_dicts(dict1, dict2):
	merged = {}
	for key in dict1.keys() | dict2.keys():
		if key in dict1 and key in dict2:
			merged[key] = {**dict1[key], **dict2[key]}
		elif key in dict1:
			merged[key] = dict1[key]
		else:
			merged[key] = dict2[key]

	return merged


class VersionManager:
	def __init__(self) -> None:
		pass

	@staticmethod
	def get_version(jar_file):
		"""
		Get the version name of the server from the version.json file inside the JAR file

		:param jar_file: Path to the JAR file

		:return: The version name
		"""
		# Extract version.json file from the downloaded JAR file
		try:
			with zipfile.ZipFile(jar_file, 'r') as zip_ref:
				version_json = zip_ref.read('version.json')
				# Load version.json as a dictionary
				version_name = json.loads(version_json)
				version_name = version_name["name"]
		except zipfile.BadZipFile:
			version_name = "File corrupted"

		return version_name


	@staticmethod
	def get_version_id(jar_file):
		"""
		Get the version ID of the server from the version.json file inside the JAR file

		:param jar_file: Path to the JAR file

		:return: The version ID
		"""
		# Extract version.json file from the downloaded JAR file
		try:
			with zipfile.ZipFile(jar_file, 'r') as zip_ref:
				version_json = zip_ref.read('version.json')
				# Load version.json as a dictionary
				version_id = json.loads(version_json)
				version_id = version_id["id"]
		except zipfile.BadZipFile:
			version_id = "File corrupted"

		return version_id


	@staticmethod
	def verify_version(jar_file, expected_version):
		"""
		Verify that the version of given JAR file matches the expected version

		:param jar_file: Path to the JAR file
		:param expected_version: Expected version

		:raises IncorrectServerVersion: If the version of the JAR file does not match the expected version
		"""
		version = VersionManager.get_version_id(jar_file)

		# Check the version number in the version.json file
		if version != expected_version:
			raise IncorrectServerVersion(
				f"Incorrect {jar_file} version. Expected {expected_version}, got {version}")


	@staticmethod
	def read_versions_file(versions_file):
		"""
		Read the versions file and return the contents as a dictionary

		:param versions_file: Path to the versions file

		:return: The contents of the versions file as a dictionary
		"""
		versions = {}
		if os.path.isfile(versions_file):
			with open(versions_file, 'r') as f:
				try:
					versions = json.load(f)
				except json.JSONDecodeError:
					pass
		return versions


	@staticmethod
	def get_existing_versions(versions_file):
		"""
		Get version IDs from the versions file

		:param versions_file: Path to the versions file

		:return: List of version IDs
		"""
		versions = VersionManager.read_versions_file(versions_file)
		return VersionManager.get_version_ids(versions)


	@staticmethod
	def get_version_ids(manifest):
		"""
		Get version IDs from the version manifest

		:param manifest: Version manifest

		:return: List of version IDs
		"""
		versions = manifest.get('versions')
		if versions is not None:
			return [version['id'] for version in versions]
		
		categories = ['release', 'snapshot', 'old_beta', 'old_alpha']
		ids = []
		for category in categories:
			ids.extend(manifest.get(category, {}).keys())
		return ids


	@staticmethod
	def get_version_manifest():
		"""
		Yoink the version manifest from Mojang

		:return: Version manifest
		"""
		for _ in range(MAX_RETRIES):
			try:
				response = requests.get(VERSION_MANIFEST_URL)
				response.raise_for_status()
				return response.json()
			except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
				print(f"Error retrieving version manifest: {e}. Retrying...")
				time.sleep(5)
		raise Exception(f"Unable to retrieve version manifest after {MAX_RETRIES} retries.")


	@staticmethod
	def get_version_data(url):
		"""
		Get version data from the given URL

		:param url: URL to get version data from

		:return: Version data
		"""
		for _ in range(MAX_RETRIES):
			try:
				response = requests.get(url)
				response.raise_for_status()
				return response.json()
			except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
				print(f"Error retrieving version data for {url}: {e}. Retrying...")
				time.sleep(5)
		raise Exception(f"Unable to retrieve version data for {url} after {MAX_RETRIES} retries.")


	@staticmethod
	def get_versions(version_manifest, versions_to_update):
		"""
		Get version data for the given versions

		:param version_manifest: Version manifest
		:param versions_to_update: List of versions to update

		:return: Dictionary of versions
		"""
		versions = {
			'latest': version_manifest['latest'],
			'release': {},
			'snapshot': {},
			'old_beta': {},
			'old_alpha': {},
		}
		with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
			futures = {}
			for version in version_manifest['versions']:
				if version['id'] in versions_to_update:
					url = version['url']
					futures[executor.submit(VersionManager.get_version_data, url)] = version

			for future in as_completed(futures):
				version_data, version = future.result(), futures[future]
				version_type, version_id = version['type'], version['id']
				download_info = version_data.get('downloads', {}).get('server')
				version_dict = versions[version_type].setdefault(version_id, {})
				version_dict.update({
					'time': version['time'],
					'releaseTime': version['releaseTime'],
				})
				if download_info is not None:
					version_dict['download'] = download_info['url']
					version_dict['sha1'] = download_info['sha1']
		return versions


	@staticmethod
	def update_cached_versions(versions_file):
		"""
		Update the cached versions file

		:param versions_file: Path to the versions file

		:return: None
		"""
		print("Updating cached versions...")
		cached_versions = VersionManager.get_existing_versions(versions_file)
		version_manifest = VersionManager.get_version_manifest()
		version_ids = VersionManager.get_version_ids(version_manifest)
		versions_to_update = [version_id for version_id in version_ids if version_id not in cached_versions]
		print(f"Updating {len(versions_to_update)} versions...")
		versions = VersionManager.get_versions(version_manifest, versions_to_update)
		current_versions = VersionManager.read_versions_file(versions_file)
		updated_versions = merge_dicts(current_versions, versions)
		with open(versions_file, 'w') as f:
			json.dump(updated_versions, f)
			print(f"Updated cached versions in {versions_file}")


	@staticmethod
	def get_minecraft_versions(versions_file, type='release'):
		"""
		Get a list of Minecraft versions

		:param versions_file: Path to the versions file
		:param type: Type of versions to get (release, snapshot, old_beta, old_alpha)

		:return: List of Minecraft versions
		"""
		versions = VersionManager.read_versions_file(versions_file)
		if versions == {}:
			VersionManager.update_cached_versions(versions_file)
			versions = VersionManager.read_versions_file(versions_file)
		if type in versions:
			return versions['release'].keys()
		else:
			raise Exception(f"Invalid version type: {type}. Valid types are: release, snapshot, old_beta, old_alpha")


	@staticmethod
	def verify_sha1(file, sha1):
		print(f"Verifying {file}...")
		hash = hashlib.sha1()

		with open(file, 'rb') as file:
			chunk = 0
			while chunk != b'':
				chunk = file.read(1024)
				hash.update(chunk)

		# TODO: This is only for testing
		hexdigest = hash.hexdigest()
		if hexdigest != sha1:
			print(f"Verification failed. Expected {sha1}, got {hexdigest}")
			return False
		else:
			print("Verification successful")
			return True
