import datetime
from configparser import ConfigParser


def add_year(date):
    return date + datetime.timedelta(years=1)


def add_year_to_date_string(date_string):
    return add_year(formatted_date_to_datetime(date_string))


def is_string_date_le(date_string, other_date_string):
    first_date = formatted_date_to_datetime(date_string)
    second_date = formatted_date_to_datetime(other_date_string)
    return first_date <= second_date


def is_string_date_l(date_string, other_date_string):
    first_date = formatted_date_to_datetime(date_string)
    second_date = formatted_date_to_datetime(other_date_string)
    return first_date < second_date


def is_string_date_g(date_string, other_date_string):
    first_date = formatted_date_to_datetime(date_string)
    second_date = formatted_date_to_datetime(other_date_string)
    return first_date >= second_date


def is_string_date_ge(date_string, other_date_string):
    first_date = formatted_date_to_datetime(date_string)
    second_date = formatted_date_to_datetime(other_date_string)
    return first_date >= second_date


def is_string_date_eq(date_string, other_date_string):
    first_date = formatted_date_to_datetime(date_string)
    second_date = formatted_date_to_datetime(other_date_string)
    return first_date == second_date


def get_date_string_plus_year(date_string):
    return add_year_to_date_string(date_string).strftime("%Y%m%d")


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


def get_miner_values(filename="properties.ini", section="minervalues"):
    parser = ConfigParser()
    parser.read(filename)

    values = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            values[param[0]] = param[1]
    else:
        raise Exception("Section {0} doesn't extist in file {1}".format(section, filename))

    return values


def set_miner_date_value(date, filename="properties.ini", section="minervalues"):
    parser = ConfigParser()
    parser.read(filename)
    parser.set(section, "date_to_check", date)
    with open(filename, 'w') as f:
        parser.write(f)


if __name__ == "__main__":
    set_miner_date_value("19521114")
