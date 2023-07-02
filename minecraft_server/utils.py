import datetime

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