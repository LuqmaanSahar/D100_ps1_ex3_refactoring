# %%
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt


# %%
# Reading data from a csv file
# You can read data from a CSV file using the `read_csv` function. By default, it assumes that the fields are comma-separated.

# We're going to be looking at some cyclist data from Montréal. Here's the [original page](http://donnees.ville.montreal.qc.ca/dataset/velos-comptage) (in French), but it's already included in this repository. We're using the data from 2012.

# This dataset is a list of how many people were on 7 different bike paths in Montreal, each day.

broken_df = pd.read_csv("../data/bikes.csv", encoding="ISO-8859-1")
broken_df.head()

# %%
# Reading data from a csv file using Polars using 'eager' mode
pl_broken_df = pl.read_csv("../data/bikes.csv", encoding="ISO-8859-1")
pl_broken_df.head()

# We can use pl.scan_csv to load in 'lazy' mode, but it expects utf8 encoding only.
# %%
# Look at the first 3 rows
broken_df[:3]
# %%
# the Polars DataFrame has the same index
pl_broken_df[:3]

# %%
# You'll notice that this is totally broken! `read_csv` has a bunch of options that will let us fix that, though. Here we'll

# * Change the column separator to a `;`
# * Set the encoding to `'latin1'` (the default is `'utf8'`)
# * Parse the dates in the 'Date' column
# * Tell it that our dates have the day first instead of the month first
# * Set the index to be the 'Date' column

fixed_df = pd.read_csv(
    "../data/bikes.csv",
    sep=";",
    encoding="latin1",
    parse_dates=["Date"],
    dayfirst=True,
    index_col="Date",
)
fixed_df[:3]

# %%
# same thing, but using polars

pl_fixed_df = pl.read_csv(
    "../data/bikes.csv",
    separator=";",              # identical to 'sep'
    encoding="latin1",
    try_parse_dates=True        # automatically parses dates
).sort("Date")                  # Polars does not have an 'index_col' equivalent. Instead, we can sort by the date.
pl_fixed_df[:3]


# %%
# Selecting a column
# When you read a CSV, you get a kind of object called a `DataFrame`, which is made up of rows and columns. You get columns out of a DataFrame the same way you get elements out of a dictionary.

# Here's an example:
fixed_df["Berri 1"]

# %%
# We can use the same syntax for a Polars DataFrame
pl_fixed_df["Berri 1"]


# %%
# Plotting is quite easy in Pandas
fixed_df["Berri 1"].plot()

# %%
# Polars DataFrames do not have built in visualisation methods

# We could convert to a pandas dataframe to take advantage of the '.plot' method

# If it's a one-off plot, we can use matplotlib instead

plt.plot(pl_fixed_df["Berri 1"])


# %%
# We can also plot all the columns just as easily. We'll make it a little bigger, too.
# You can see that it's more squished together, but all the bike paths behave basically the same -- if it's a bad day for cyclists, it's a bad day everywhere.

fixed_df.plot(figsize=(15, 10))

# %%

#  Polars DataFrames are not integrated with Matplotlib or Seaborn, so we need to manually plot each line ourselves

x = pl_fixed_df["Date"].to_numpy()              # obtain the x-axis variable
y = pl_fixed_df.drop("Date").to_numpy()         # obtain the array of other variables
columns = pl_fixed_df.drop("Date").columns      # obtain column names to create the legend

fig, ax = plt.subplots(figsize=(15, 8))         # set up the figure
for i, col_name in enumerate(columns):          # plot each column in the y array
    ax.plot(x, y[:, i], label=col_name)

plt.legend()
ax.set(xlabel="Date")

# TL;DR Pandas DataFrames are still much more convenient for creating data visualisations