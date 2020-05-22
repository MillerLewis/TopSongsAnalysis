import requests as r
import bs4
import os

import HelperFunctions
import properties



def get_artists_from_response(response):
    soup = bs4.BeautifulSoup(response.text, features="html.parser")
    return [ele.find('a').text for ele in soup.find_all(attrs={"class": "artist"})]


def write_artists_to_file(file_name):
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r') as f:
                lines = f.readlines()
                date_to_check = HelperFunctions.get_date_string_plus_seven(lines[-1].split(",")[0])
        except IndexError:
            date_to_check = properties.START_DATE
    else:
        date_to_check = properties.START_DATE

    with open(file_name, 'a') as f:
        response = r.get(properties.SITE_ROOT + date_to_check)
        artists = get_artists_from_response(response)

        while len(artists) != 0 and response.status_code == 200:
            print("Checking {}".format(date_to_check))
            f.write(",".join([str(date_to_check)] + artists))
            f.write("\n")
            f.flush()
            print(artists)

            date_to_check = HelperFunctions.get_date_string_plus_seven(date_to_check)
            response = r.get(properties.SITE_ROOT + date_to_check)
            artists = get_artists_from_response(r.get(properties.SITE_ROOT + date_to_check))
