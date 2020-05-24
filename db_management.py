import psycopg2
from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section {0} not found in the {1} file".format(section, filename))

    return db


def get_db_conn_cursor():
    params = config()
    print("Connecting to db")
    conn = psycopg2.connect(**params)

    cur = conn.cursor()
    return conn, cur


def add_date_row(artist, song, date, cur=None):
    # Date of format yyyymmdd
    # Artists of format John Doe, Jane Doe
    sql = """INSERT INTO weeks(artist, date, song)
                VALUES (%(artist)s, %(date)s, %(song)s)"""

    if cur is None:
        conn, cur = get_db_conn_cursor()

    print("Adding row for date {date} and artists {artist} and song {song}".format(date=date,
                                                                   artist=truncate_string(artist, 20),
                                                                   song=truncate_string(song, 20)))
    cur.execute(sql, {"artist": artist, "song": song, "date": date})


def add_date_rows(artists_and_songs, date, cur=None):
    # Date of format yyyymmdd
    # Artists_and_songs of format [[John Doe, song_1], [Jane Doe, song_2]]
    for artist_and_song in artists_and_songs:

        add_date_row(artist_and_song[0], artist_and_song[1], date, cur=cur)


def close_connections(conn, cur):
    print("Closing connection to db.")
    conn.close()
    cur.close()


def truncate_string(s, max_length):
    return s if len(s) <= max_length else s[:max_length] + " ..."


def list2pgarray(l):
    return '{' + ', '.join(l) + '}'


if __name__ == "__main__":
    conn, cur = get_db_conn_cursor()
    # add_date_rows(['John Doe', 'Jane Doe'], '20200523', cur=cur)
    add_date_row('John Doe', 'Song1', '20200523', cur=cur)
    conn.commit()
    close_connections(conn, cur)
