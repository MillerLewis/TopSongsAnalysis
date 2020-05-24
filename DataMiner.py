import requests as r
import bs4

import db_management
import psycopg2

import HelperFunctions


def get_artists_from_soup(soup):
    return [ele.find('a').text for ele in soup.find_all(attrs={"class": "artist"})]


def get_song_from_soup(soup):
    return [ele.find('a').text for ele in soup.find_all(attrs={"class": "title"})]


def create_soup_from_response(response):
    return bs4.BeautifulSoup(response.text, features="html.parser")


def write_artists_to_db():
    conn = None

    try:
        conn, cur = db_management.get_db_conn_cursor()

        date_to_check = HelperFunctions.get_miner_values()["date_to_check"]
        site_root = HelperFunctions.get_miner_values()["site_root"]

        response = r.get(site_root + date_to_check)
        soup = create_soup_from_response(response)
        artists = get_artists_from_soup(soup)
        songs = get_song_from_soup(soup)

        while len(artists) != 0 and response.status_code == 200:
            db_management.add_date_rows(zip(artists, songs), date_to_check, cur=cur)
            print("Checked {}".format(date_to_check))
            conn.commit()
            HelperFunctions.set_miner_date_value(date_to_check)

            date_to_check = HelperFunctions.get_date_string_plus_seven(date_to_check)

            response = r.get(HelperFunctions.get_miner_values()["site_root"] + date_to_check)
            soup = create_soup_from_response((r.get(site_root + date_to_check)))

            artists = get_artists_from_soup(soup)
            songs = get_song_from_soup(soup)

        if response.status_code != 200:
            print("Got a non-200 error..")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)

    finally:
        if conn is not None:
            conn.close()


write_artists_to_db()
