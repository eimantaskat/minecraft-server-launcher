import datetime
import pytz


def get_timestamp():
    fmt = "%a %b %d %H:%M:%S %Z %Y"
    current_time = datetime.datetime.now()
    try:
        current_tz = pytz.timezone(str(datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo))
    except pytz.exceptions.UnknownTimeZoneError:
        current_tz = pytz.timezone("EET")
    return current_time.astimezone(current_tz).strftime(fmt)


def read(path):
    properties = {}
    with open(path, 'r') as f:
        for line in f:
            if not line.startswith('#'):
                key, value = line.strip().split('=')
                properties[key] = value
    return properties


def update(filepath, new_properties):
    properties = {}
    comments = []
    with open(filepath, 'r') as f:
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
        
    with open(filepath, 'w') as f:
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

# print(read(r'C:\Users\Eimantas\Desktop\s\server.properties'))
