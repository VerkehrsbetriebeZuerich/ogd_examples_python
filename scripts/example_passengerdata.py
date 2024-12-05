# How to get started with passenger data by Verkehrsbetriebe
#     Zürich (VBZ) from the open data platform of the City of Zurich
#     https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd
#     There you can also find further explanations (only in German)
# Author: Verkehrsbetriebe Zürich (Y. Neuenschwander)

# Load packages
from pathlib import Path
import pandas as pd

# suppress scientific notation from pandas results
pd.options.display.float_format = "{:.4f}".format

# Define where the ogd-data is to find on your disk
path_to_data = Path(r".../data")

# Load the data 
# You will find the datasets at
# https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd

# Load matching tables
df_stops = pd.read_csv(path_to_data / "HALTESTELLEN.csv", sep=";")
df_day_type = pd.read_csv(path_to_data / "TAGTYP.csv", sep=";")
df_lines = pd.read_csv(path_to_data / "LINIE.csv", sep=";")
df_vehicle_capacities = pd.read_csv(path_to_data / "GEFAESSGROESSE.csv", sep=";")

# Load table "REISENDE": the passenger data is stored there
df_count = pd.read_csv(path_to_data / "REISENDE.csv", sep=";")

# Matching
# In order to get the complete main passengers table, you need to match REISENDE with HALTESTELLEN, TAGTYP and LINIE

# first drop the column "Linienname" from REISENDE
df_count = df_count.drop("Linienname", axis=1)

# match df_count with df_stops according to the stops ids (= "Haltestellen_Id")
reisende_haltestellen = pd.merge(
    df_count,
    df_stops,
    how="left",
    left_on=["Haltestellen_Id"],
    right_on=["Haltestellen_Id"],
)

# match reisende_haltestellen with df_day_type according to the id of the day type (= "Tagtyp_Id")
reisende_haltestellen_tagtyp = pd.merge(
    reisende_haltestellen,
    df_day_type,
    how="left",
    left_on=["Tagtyp_Id"],
    right_on=["Tagtyp_Id"],
)

# match reisende_haltestellen_tagtyp with df_lines according to the line ids (= "Linien_Id")
reisende_haltestellen_tagtyp_linie = pd.merge(
    reisende_haltestellen_tagtyp,
    df_lines,
    how="left",
    left_on=["Linien_Id"],
    right_on=["Linien_Id"],
)

# match reisende_haltestellen_tagtyp_linie with df_vehicle_capacities according to the id of the scheduled trip
# (= "Plan_Fahrt_Id")
reisende_full = pd.merge(
    reisende_haltestellen_tagtyp_linie,
    df_vehicle_capacities,
    how="left",
    left_on=["Plan_Fahrt_Id"],
    right_on=["Plan_Fahrt_Id"],
)


# Example Analyses

# Passengers per line
# hint: "Linien_Id" (= lines ids) is only unique within one year.
# Use "Linienname" (= lines names) to compare lines between years

# passengers per line per year
# group by Linien_Id etc., multiply Einsteiger (= passengers getting into the vehicle) with Tage_DTV
# (= extrapolation factor for the whole year) and calculate the sum
pax_line_year = (
    reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"])[
        ["Einsteiger", "Tage_DTV"]
    ]
    .prod(axis=1)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_year")
    .round(0)
)


# passengers per
# - average Monday-Friday work day (DWV)
# - average Monday-Sunday day (DTV)
# - average Saturday (Sa)
# - average Sunday (So)
# - average Saturday night (Sa_n)
# - average Sunday night (So_n)
einsteiger_tage_dtv = (
    reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"])[
        ["Einsteiger", "Tage_DTV"]
    ]
    .prod(axis=1)
    .div(365)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_DTV")
    .round(0)
)

einsteiger_tage_dwv = (
    reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"])[
        ["Einsteiger", "Tage_DWV"]
    ]
    .prod(axis=1)
    .div(251)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_DWV")
    .round(0)
)

einsteiger_tage_sa = (
    reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"])[
        ["Einsteiger", "Tage_SA"]
    ]
    .prod(axis=1)
    .div(52)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_Sa")
    .round(0)
)

einsteiger_tage_so = (
    reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"])[
        ["Einsteiger", "Tage_SO"]
    ]
    .prod(axis=1)
    .div(62)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_So")
    .round(0)
)


einsteiger_tage_sa_n = (
    reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"])[
        ["Einsteiger", "Tage_SA_N"]
    ]
    .prod(axis=1)
    .div(52)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_Sa_N")
    .round(0)
)

einsteiger_tage_so_n = (
    reisende_full.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"])[
        ["Einsteiger", "Tage_SO_N"]
    ]
    .prod(axis=1)
    .div(52)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_So_N")
    .round(0)
)

# merge the day type data frames to a list
pax_line_year_day_type = [
    df.set_index(["Linien_Id", "Linienname", "Linienname_Fahrgastauskunft"])
    for df in [
        einsteiger_tage_dtv,
        einsteiger_tage_dwv,
        einsteiger_tage_sa,
        einsteiger_tage_so,
        einsteiger_tage_sa_n,
        einsteiger_tage_so_n,
    ]
]

# concatenate the list on columns to a data frame
pax_line_year_day_type = pd.concat(pax_line_year_day_type, axis=1).reset_index()


# Passengers per stop
# hint: "Haltestellen_Id" (= stops ids) is only unique within one year.
# Use "Haltestellennummer" (= stops numbers) to compare lines between years.
# Haltestellennummer" is more stable and unique within all published datasets.

# passengers per stop per year
# group by Haltestellen_Id etc., multiply Einsteiger (= passengers getting into the vehicle) with Tage_DTV
# (= extrapolation factor for the whole year) and calculate the sum
pax_stop_year = (
    reisende_full.set_index(
        ["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]
    )[["Einsteiger", "Tage_DTV"]]
    .prod(axis=1)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_year")
    .round(0)
)

# passengers per:
# - average Monday-Friday work day (DWV)
# - average Monday-Sunday day (DTV)
# - average Saturday (Sa)
# - average Sunday (So)
# - average Saturday night (Sa_n)
# - average Sunday night (So_n)
einsteiger_stops_tage_dtv = (
    reisende_full.set_index(
        ["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]
    )[["Einsteiger", "Tage_DTV"]]
    .prod(axis=1)
    .div(365)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_DTV")
    .round(0)
)

einsteiger_stops_tage_dwv = (
    reisende_full.set_index(
        ["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]
    )[["Einsteiger", "Tage_DWV"]]
    .prod(axis=1)
    .div(251)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_DWV")
    .round(0)
)

einsteiger_stops_tage_sa = (
    reisende_full.set_index(
        ["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]
    )[["Einsteiger", "Tage_SA"]]
    .prod(axis=1)
    .div(52)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_Sa")
    .round(0)
)

einsteiger_stops_tage_so = (
    reisende_full.set_index(
        ["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]
    )[["Einsteiger", "Tage_SO"]]
    .prod(axis=1)
    .div(62)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_So")
    .round(0)
)


einsteiger_stops_tage_sa_n = (
    reisende_full.set_index(
        ["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]
    )[["Einsteiger", "Tage_SA_N"]]
    .prod(axis=1)
    .div(52)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_Sa_N")
    .round(0)
)

einsteiger_stops_tage_so_n = (
    reisende_full.set_index(
        ["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"]
    )[["Einsteiger", "Tage_SO_N"]]
    .prod(axis=1)
    .div(52)
    .groupby(level=[0, 1, 2])
    .sum()
    .reset_index(name="pax_per_So_N")
    .round(0)
)

# merge the day type data frames to a list
pax_stops_year_day_type = [
    df.set_index(["Haltestellen_Id", "Haltestellennummer", "Haltestellenlangname"])
    for df in [
        einsteiger_stops_tage_dtv,
        einsteiger_stops_tage_dwv,
        einsteiger_stops_tage_sa,
        einsteiger_stops_tage_so,
        einsteiger_stops_tage_sa_n,
        einsteiger_stops_tage_so_n,
    ]
]

# concatenate the list on columns to a data frame
pax_stops_year_day_type = pd.concat(pax_stops_year_day_type, axis=1).reset_index()

