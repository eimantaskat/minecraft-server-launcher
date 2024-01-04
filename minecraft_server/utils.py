import datetime
import subprocess

import pytz


def get_timestamp():
	fmt = "%a %b %d %H:%M:%S %Z %Y"
	current_time = datetime.datetime.now()
	try:
		current_tz = pytz.timezone(str(datetime.datetime.now(
			datetime.timezone.utc).astimezone().tzinfo))
	except pytz.exceptions.UnknownTimeZoneError:
		current_tz = pytz.timezone("EET")
	return current_time.astimezone(current_tz).strftime(fmt)


def get_java_version():
	try:
		java_version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
	except FileNotFoundError:
		return False
	except subprocess.CalledProcessError:
		return False
	else:
		java_version = java_version.decode('utf-8')
		java_version = java_version.split('\n')[0]
		java_version = java_version.split(' ')[2].replace('"', '')
		return java_version