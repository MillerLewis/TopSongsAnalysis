import datetime


def add_seven_days(date):
    return date + datetime.timedelta(days=7)


def formatted_date_to_datetime(date_string):
    return datetime.datetime.strptime(date_string, "%Y%m%d")


def add_seven_to_date_string(date_string):
    return add_seven_days(formatted_date_to_datetime(date_string))


def get_date_string_plus_seven(date_string):
    return add_seven_to_date_string(date_string).strftime("%Y%m%d")


def load_properties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"')
                props[key] = value
    return props
