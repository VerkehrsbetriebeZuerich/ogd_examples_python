# How to get started with travel time data from Verkehrsbetriebe Zürich (VBZ) available on the open data platform of the City of Zurich. 
#     This guide is based on the example dataset for 2020: https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2020.
#     There you can also find further explanations (only in German).
#     Update: These datasets are no longer maintained on Open Data Zurich. Travel times of VBZ in the planned vs. actual comparison after 29.07.2023, can be found in the open data 
#     catalog on opentransportdata.swiss at https://opentransportdata.swiss/en/dataset/istdaten.
# Author: Verkehrsbetriebe Zürich (Y. Neuenschwander)

# Load packages
from pathlib import Path
import pandas as pd

# suppress scientific notation from pandas results
pd.options.display.float_format = "{:.4f}".format

# Define where the ogd-data is to find on your disk
path_to_data = Path(r".../data")

# Load the data
# You will find the datasets here:
# https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2020

# Matching tables
df_stop_point = pd.read_csv(path_to_data / "haltepunkt.csv", sep=",")
df_stop = pd.read_csv(path_to_data / "haltestelle.csv", sep=",")

# Load table "fahrzeiten": the travel time data is stored there
df_travel_time = pd.read_csv(path_to_data / "fahrzeiten_soll_ist_20200809_20200815.csv", sep=",")

# Matching
# In order to get the full stops information, you need to match df_travel_time with df_stop_point and df_stop

# match df_travel_time with the stop points from df_stop_point according to the departure stop point
# ("from"; german: "von")
traveltime_stpoint_from = pd.merge(df_travel_time,df_stop_point,how="left",
    left_on=["halt_punkt_id_von","halt_punkt_diva_von","halt_id_von"],
    right_on=["halt_punkt_id","halt_punkt_diva","halt_id"]
)

# adjust variables names
traveltime_stpoint_from.rename(columns=
                               {'GPS_Latitude': 'GPS_Latitude_von', 
                                'GPS_Longitude': 'GPS_Longitude_von',
                                'GPS_Bearing': 'GPS_Bearing_von', 
                                'halt_punkt_ist_aktiv': 'halt_punkt_ist_aktiv_von'},
                                inplace=True)

# match df_travel_time with the stop points from df_stop_point according to the destination stop point
# ("to"; german: "nach")
traveltime_stpoint = pd.merge(
    traveltime_stpoint_from,
    df_stop_point,
    how="left",
    left_on=["halt_punkt_id_nach","halt_punkt_diva_nach","halt_id_nach"],
    right_on=["halt_punkt_id","halt_punkt_diva","halt_id"]
)

# adjust variables names
traveltime_stpoint.rename(columns=
                          {'GPS_Latitude': 'GPS_Latitude_nach', 
                           'GPS_Longitude': 'GPS_Longitude_nach',
                            'GPS_Bearing': 'GPS_Bearing_nach', 
                           'halt_punkt_ist_aktiv': 'halt_punkt_ist_aktiv_nach'},
                            inplace=True)


# match traveltime_stpoint with the stop names from df_stop according to the stop point of departure
# ("from"; german: "von")
traveltime_stpoint_st_from = pd.merge(
    traveltime_stpoint,
    df_stop,
    how="left",
    left_on=["halt_id_von","halt_diva_von","halt_kurz_von1"],
    right_on=["halt_id","halt_diva","halt_kurz"]
)

# adjust variables names
traveltime_stpoint_st_from.rename(columns=
                                  {'halt_lang': 'halt_lang_von',
                                   'halt_ist_aktiv': 'halt_ist_aktiv_von'},
                                    inplace=True)

# Drop unnecessary columns from traveltime_stpoint_st_from as is it causing a problem later
traveltime_stpoint_st_from = traveltime_stpoint_st_from.drop(columns=["halt_id_x"])

# match traveltime_stpoint_st_from with the stop names from df_stop according to the destination stop point
# ("to"; german: "nach")
traveltime_stpoint_st = pd.merge(
    traveltime_stpoint_st_from,
    df_stop,
    how="left",
    left_on=["halt_id_nach","halt_diva_nach","halt_kurz_nach1"],
    right_on=["halt_id","halt_diva","halt_kurz"]
)

# adjust variables names
traveltime_stpoint_st.rename(columns={'halt_lang': 'halt_lang_nach', 
                                      'halt_ist_aktiv': 'halt_ist_aktiv_nach'},
                                       inplace=True)

# Calculate the punctuality per line
#     According to the punctuality definition of VBZ, a ride is considered on time (punctual) when the actual arrival time at the stop
#     does not exceed the scheduled arrival time by more than 2 minutes (otherwise defined as "delayed") or the actual
#     departure at a stop does not happen more than 1 minute earlier than the scheduled departure (otherwise defined as
#     "too early")

# first calculate the difference between actual ("ist") and scheduled ("soll") arrival ("an") / departure ("ab")
#     and then assign the punctuality categories accordingly
traveltime_stpoint_st['punct_cat'] = traveltime_stpoint_st.apply(lambda x:
                                            'delay' if x["ist_an_nach1"] - x["soll_an_nach"] >= 120 else 'too early'
                                            if x["ist_ab_nach"] - x["soll_ab_nach"]<= -60 else "punctual", axis=1)

# count the occurrences per line of each category
count_punct_cat = traveltime_stpoint_st.groupby(['linie', 'punct_cat']).size().rename('count')

# calculate the proportions
percent_punct = 100 * (count_punct_cat / count_punct_cat.groupby(level=0).sum())

# transform to data frame and name percentage column
punctuality = percent_punct.to_frame(name='percent')

# add count column to punctuality
punctuality = pd.merge(count_punct_cat,
                       punctuality,
                       how="left",
                       left_on=["linie","punct_cat"],
                       right_on=["linie","punct_cat"])

