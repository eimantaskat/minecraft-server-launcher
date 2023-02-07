import datetime
import pytz
import os


def get_timestamp():
    fmt = "%a %b %d %H:%M:%S %Z %Y"
    current_time = datetime.datetime.now()
    try:
        current_tz = pytz.timezone(str(datetime.datetime.now(
            datetime.timezone.utc).astimezone().tzinfo))
    except pytz.exceptions.UnknownTimeZoneError:
        current_tz = pytz.timezone("EET")
    return current_time.astimezone(current_tz).strftime(fmt)


def read(path):
    path = os.path.join(path, 'server.properties')
    properties = {}
    with open(path, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                key, value = line.strip().split('=')
                properties[key] = value
    return properties


def update(path, new_properties):
    path = os.path.join(path, 'server.properties')
    properties = {}
    comments = []
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('#'):
                if "#" in line and ":" in line:
                    comments.append(f"#{get_timestamp()}\n")
                else:
                    comments.append(line)
            else:
                key, value = line.strip().split('=')
                properties[key] = value

    for key, value in new_properties.items():
        properties[key] = value

    with open(path, 'w') as f:
        for comment in comments:
            f.write(comment)
        for key, value in properties.items():
            f.write(key + '=' + value + '\n')


def stringify(properties: dict):
    for key, value in properties.items():
        if key != 'motd':
            properties[key] = str(value).lower()
        else:
            properties[key] = str(value)
    return properties


def create(path, properties: dict):
    path = os.path.join(path, 'server.properties')
    comments = ["#Minecraft server properties"]
    comments.append(f"#{get_timestamp()}\n")
    with open(path, 'w') as f:
        for comment in comments:
            f.write(comment)
        for key, value in properties.items():
            f.write(key + '=' + value + '\n')
