# %%
import pandas as pd
import matplotlib.pyplot as plt
import polars as pl

# %%
# We're going to use a new dataset here, to demonstrate how to deal with larger datasets. This is a subset of the of 311 service requests from [NYC Open Data](https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9).
# because of mixed types we specify dtype to prevent any errors
complaints = pd.read_csv("data/311-service-requests.csv", dtype="unicode")
complaints.head()

# %%
# TODO: rewrite the above using the polars library and call the data frame pl_complaints
# Hint: we need the dtype argument reading all columns in as strings above in Pandas due to the zip code column containing NaNs as "NA" and some zip codes containing a dash like 1234-456
# you cannot exactly do the same in Polars but you can read about some other solutions here:
# see a discussion about dtype argument here: https://github.com/pola-rs/polars/issues/8230

pl_complaints = pl.read_csv("data/311-service-requests.csv", infer_schema_length=0)

print(pl_complaints.head())

# %%
# Selecting columns:
complaints["Complaint Type"]

# %%
# TODO: rewrite the above using the polars library
complaint_type_col = pl_complaints.select(pl.col("Complaint Type"))

# %%
# Get the first 5 rows of a dataframe
complaints[:5]

# %%
# TODO: rewrite the above using the polars library
first_five_rows = pl_complaints.head(5)
# %%
# Combine these to get the first 5 rows of a column:
complaints["Complaint Type"][:5]

# %%
# TODO: rewrite the above using the polars library
first_five_complaint_type_A = pl_complaints.select(pl.col("Complaint Type")).head(5)

# %%
# Selecting multiple columns
complaints[["Complaint Type", "Borough"]]

# %%
# TODO: rewrite the above using the polars library
selected_cols = pl_complaints.select(pl.col("Complaint Type"),pl.col("Borough"))
# %%
# What's the most common complaint type?
complaint_counts = complaints["Complaint Type"].value_counts()
complaint_counts[:10]

# %%
# TODO: rewrite the above using the polars library
complaint_counts_pl = (
    pl_complaints
    .group_by("Complaint Type")
    .agg(pl.len().alias("count"))
    .sort("count", descending=True)
)
top_10_complaints = complaint_counts_pl.head(10)
# %%
# Plot the top 10 most common complaints
complaint_counts[:10].plot(kind="bar")
plt.title("Top 10 Complaint Types")
plt.xlabel("Complaint Type")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# %%
# TODO: please do the same with Polars
fig, ax = plt.subplots()

ax.bar(
    x=top_10_complaints["Complaint Type"],
    height=top_10_complaints["count"],
)
ax.set_xlabel("Complaint Type")
ax.set_ylabel("Count")
plt.title("Top 10 Complaint Types")
plt.xticks(rotation=45, ha="right")
plt.tight_layout(pad=1.5) 
plt.show()