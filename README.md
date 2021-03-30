# Examples for working with VBZ OGD for Python
## What's in this Repo?
These Python examples are intended to help you getting started with the analysis of travel time data or passenger data of Verkehrsbetriebe Zürich (VBZ), the public transport operator in the Swiss city of Zurich.
The datasets as shown below are published as Open Government Data (OGD) at the [Open Data Portal](https://data.stadt-zuerich.ch).

The R version of the examples can be found [here](https://github.com/VerkehrsbetriebeZuerich/ogd_examples_R).


Also have a look at other showcases:

- [showcases traveltimes](https://data.stadt-zuerich.ch/dataset/showcases/vbz_fahrzeiten_ogd)
at Open Data Portal
- [showcases passengerdata](https://data.stadt-zuerich.ch/dataset/showcases/vbz_fahrgastzahlen_ogd)
 at Open Data Portal

Do you want to share your output?  
Feel free to contact us via github@vbz.ch or the
[Open Data Portal contact-form](https://www.stadt-zuerich.ch/portal/de/index/ogd/kontakt.html)

For more transport data (Switzerland, not only Zurich) have a look at [opentransportdata](https://opentransportdata.swiss/de/)

## Contents
- [Dependencies](#Dependencies)
- [Use cases](#Use-cases)
- [FAQ](#FAQ)
- [Contact](#Contact)

## Dependencies

### Python
- Python (version 3.8, Community Edition)
- PyCharm (version 2020.2.3)


## Use cases

### Passengers per line/stop

**Script**

example_passengerdata.py

**Input**

In order to perform the example analysis you need to download a .csv-file containing 
passenger data ("Reisende.csv") as well as three matching tables from the [Open Data Portal](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd). There you can also find additional descriptions (in German only).

- **[REISENDE.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd/resource/38b0c1e5-1f4e-444d-975c-61a462aa8ca6)**: Main table, contains information about the number of passengers etc.  

- **[LINIE.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd/resource/463f92e0-5b20-44b3-b27f-59499e331e8d)**: Matching table, contains information about line numbers etc.  

- **[TAGTYP.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd/resource/09ffe483-19da-495e-81c6-711ae8dd49d3?inner_span=True)**: Matching table, contains information about the validation of timetables etc.  

- **[HALTESTELLEN.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd/resource/948b6347-8988-4705-9b08-45f0208a15da)**: Matching table, contains information about stops names etc.  
- **[GEFAESSGROESSE.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd/resource/718d9cb6-8daf-49d6-a5b2-687d3da78c58)**: Matching table, contains information about vehicle capacity.  


**Output**

e.g passengers per line in total for 2019 based on the input tables above as shown in the example script (data frame "pax_line_year").

Linien_Id | Linienname | Linienname_Fahrgastauskunft | pax_per_year
------------ | ------------- | ------------- | -------------
4 | 89 | 89 | 4'587'420.00
5 | 75 | 75 | 6'154'492.49
... | ... | ... | ...


### Punctuality per line

**Script**

example_traveltimedata.py

**Input**

In order to perform the example analysis you need to download a .csv-file containing travel time as well as two matching tables from the [Open Data Portal](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd). You'll also find additional descriptions there (only German at the moment)

- **[Fahrzeiten_SOLL_IST_20200809_20200815.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/resource/3029ec17-efea-44aa-9995-b8f10739aef2)**:Main table, contains actual travel time raw data (each file contains one week of data).

- **[Haltepunkt.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/resource/7b6a666e-2df8-4846-b63c-b30ab5265111)**: Matching table, contains information about the GPS position of each stop point.


- **[Haltestelle.csv](https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd/resource/7bb0405f-c009-498a-bc7c-d42bf7664e5f)**: Matching table, contains information about the full stop names.

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

**Q:** There is no data in "01_Data".  
**A:** Yes, that's right, but you'll find the data at the Open Data Portal of the City of Zurich under https://data.stadt-zuerich.ch/. Check also the links above and within the code.

**Q:** I've downloaded the datasets, but the script is still not running.  
**A:** check the path within ```wd = os.chdir("*\\01_Daten\\01_Input\\")``` at the beginning. This must refer to the directory of the downloaded files at your disc

**Q:** Where can I get more information about the datasets?  
**A:** You'll find the description of the metadata [here](https://data.stadt-zuerich.ch/dataset/vbz_fahrgastzahlen_ogd) (passenger data)
or [here](https://data.stadt-zuerich.ch/dataset/vbz_fahrzeiten_ogd) (travel time data).

**Q:** Whats the difference between stop point and stop?  
**A:** A stop (like "Bellevue") can contain several stop points or - in other words - platforms (e.g. Tramlines 2, 11, 8 towards "Bürkliplatz" or Tramlines 4, 15 towards "Helmhaus")

**Q:** Is there a possibility within the passengerdata to get information about routes (origin-destination)?  
**A:** No. The data contain only information about "number of boarding passengers" and "number of disembarking passengers" but no information about "number of persons travelling from A to B".

Something missing? Let us know your troubles during the work with the OGD/scripts from Verkehrsbetriebe Zürich! 


## Contact

Any feedback?

Feel free to contact us via
github@vbz.ch!


