# Examples for working with VBZ OGD for Python
## What's in this Repo?
These Python examples are intended to help you getting started with the analysis of travel time data or passenger data of Verkehrsbetriebe Zürich (VBZ), the public transport operator in the Swiss city of Zurich.
The datasets as shown below are published as Open Government Data (OGD) at the [Open Data Portal](https://data.stadt-zuerich.ch).

The R version of the examples can be found [here](https://github.com/VerkehrsbetriebeZuerich/ogd_examples_R).


Also have a look at [showcases](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd#showcase).

Do you want to share your output?  
Feel free to contact us via github@vbz.ch or the
[Open Data Portal contact-form](https://www.stadt-zuerich.ch/portal/de/index/ogd/kontakt.html).

For additional transportation data covering Switzerland (not just Zurich), take a look at [opentransportdata](https://opentransportdata.swiss).

## Contents
- [Dependencies](#Dependencies)
- [Use cases](#Use-cases)
- [FAQ](#FAQ)
- [Contact](#Contact)

## Dependencies

### Python
- Python (version 3.11)

## Use cases

### Passengers per line/stop

**Script**

example_passengerdata.py

**Input**

In order to perform the example analysis, you need to download a .csv-file containing 
passenger data ("Reisende.csv") as well as three matching tables from the [Open Data Portal](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd). There you can also find additional descriptions (in German only).

- **[REISENDE.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd/resource/38b0c1e5-1f4e-444d-975c-61a462aa8ca6)**: Main table, contains information about the number of passengers etc.  

- **[LINIE.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd/resource/463f92e0-5b20-44b3-b27f-59499e331e8d)**: Matching table, contains information about line numbers etc.  

- **[TAGTYP.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd/resource/09ffe483-19da-495e-81c6-711ae8dd49d3?inner_span=True)**: Matching table, contains information about the validation of timetables etc.  

- **[HALTESTELLEN.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd/resource/948b6347-8988-4705-9b08-45f0208a15da)**: Matching table, contains information about stops names etc.  
- **[GEFAESSGROESSE.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd/resource/718d9cb6-8daf-49d6-a5b2-687d3da78c58)**: Matching table, contains information about vehicle capacity.  


**Output**

e.g passengers per line in total for 2019 based on the input tables above as shown in the example script (data frame "pax_line_year"):

Linien_Id | Linienname | Linienname_Fahrgastauskunft | pax_per_year
------------ | ------------- | ------------- | -------------
4 | 89 | 89 | 4'587'420.00
5 | 75 | 75 | 6'154'492.49
... | ... | ... | ...


### Punctuality per line

**Script**

example_traveltimedata.py

**Input**

In order to perform the example analysis you need to download a .csv-file containing travel time as well as two matching tables from the [Open Data Portal](https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2020). You'll also find additional descriptions there (in German only).

- **Fahrzeiten_SOLL_IST_YYYYMMDD_YYYYMMDD.csv**: Main table, contains actual travel time raw data (each file contains one week of data).

- **Haltepunkt.csv**: Matching table, contains information about the GPS position of each stop point.

- **Haltestelle.csv**: Matching table, contains information about the full stop names.

**Output**

e.g percentage of the punctuality per line for 2019 based on the input tables above as shown in the example script (data frame "punctuality").

According to the punctuality definition of VBZ, a ride is considered on time (punctual) when the actual arrival time at the stop
does not exceed the scheduled arrival time by more than 2 minutes (otherwise defined as "delayed") or the actual
departure at a stop does not happen more than 1 minute earlier than the scheduled departure (otherwise defined as
"too early").

line | punctual | too early | delayed
------------ | ------------- | ------------- | -------------
2 | 95.61179 | 	2.66941139 | 1.718800
3 | 95.60730 | 2.52430229 | 1.868402
... | ... | ... | ...


## FAQ

**Q:** There is no data in the folder "data" <br>
**A:** That’s correct. The data is not included in this repository. You can find it on the Open Data Portal of the City of Zurich at https://data.stadt-zuerich.ch/. <br>
Be sure to check the links provided above and within the code for further guidance.

**Q:** I’ve downloaded the datasets, but the script still isn’t running.<br>
**A:** Please check the path specified in ``path_to_data = Path(r".../data")``. Ensure it points to the directory where the downloaded files are stored on your hard drive.

**Q:** Where can I get more information about the datasets?<br>
**A:** You can find metadata descriptions at the following links:
- [Passenger data](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd)
- [Travel time data, e.g. for 2020](https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd_2020)

**Q:** What’s the difference between a stop point and a stop?<br>
**A:** A stop (e.g., "Bellevue") can include several stop points, which are essentially platforms. For instance:
- Tram lines 2, 11, and 8 heading towards "Bürkliplatz"
- Tram lines 4 and 15 heading towards "Helmhaus"<br>

Each platform is considered a separate stop point.

**Q:** Is it possible to derive route information (origin-destination) from the passenger data?<br>
**A:** No, the data only provides information about the number of boarding passengers and the number of disembarking passengers. It does not include details about the number of people traveling between specific locations (A to B).<br>

If anything is unclear or missing, feel free to let us know about any challenges you encounter while working with the OGD datasets or scripts provided by Verkehrsbetriebe Zürich!

## Contact

Any feedback?

Feel free to contact us via github@vbz.ch!


