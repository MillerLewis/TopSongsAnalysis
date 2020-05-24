import pandas as pd
import HelperFunctions
from sqlalchemy import create_engine

import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

alchemy_engine = create_engine("postgresql://postgres:1234@localhost:5432/TopMusic")
conn = alchemy_engine.connect()

print("Fetching data...")
df = pd.read_sql("""SELECT *
                    FROM weeks""", conn)

df = df.sort_values(by=["date"])

cum_count_df = pd.DataFrame(df.groupby(by=["artist"]).cumcount(), columns=["cumCount"])
cum_count_df["cumCount"] += 1

grouped_and_count_df = pd.DataFrame(df.loc[:, "artist"].groupby(by=df.loc[:, "artist"]).count())
grouped_and_count_df.columns = ["count"]
grouped_and_count_df = grouped_and_count_df.reset_index()

top_10_artists = grouped_and_count_df.sort_values(by="count", ascending=False)[:10]
joined_with_cum_count_df = df.join(cum_count_df)

cum_count_with_artists = joined_with_cum_count_df.loc[joined_with_cum_count_df["artist"].isin(top_10_artists["artist"])]

for artist in top_10_artists["artist"]:
    print("Plotting artist {}".format(artist))
    artist_df = cum_count_with_artists[cum_count_with_artists["artist"] == artist]
    plt.plot(artist_df["date"], artist_df["cumCount"], label=artist)

plt.legend(loc="upper left")
plt.show()