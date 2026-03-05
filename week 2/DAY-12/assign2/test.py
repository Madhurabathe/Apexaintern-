import pandas as pd

# load dataset
df = pd.read_csv("booking_hotel.csv")

# set your budget
budget = 200,000

# filter hotels under budget
budget_hotels = df[df["price"] <= budget]

# filter hotels suitable for family (example column)
family_hotels = budget_hotels[budget_hotels["amenities"].str.contains("family", case=False, na=False)]

# sort by rating (highest first)
best_hotels = family_hotels.sort_values(by="rating", ascending=False)

# show top 10 hotels
print(best_hotels[["hotel_name","location","price","rating"]].head(10))