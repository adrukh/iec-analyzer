# iec-analyzer
Analyze power consumption and production data, provided by IEC and other utility providers in Israel

## Background
Israel is moving from old electricity power meters to new ones, which support near-real-time metering of the power consumed and produced by each household. Along this change, utility providers offer discounted rates for different times of day. This raises the question - given a specific power usage profile of a household, which program / discount plan is most economic for the household? As of now, the utility providers leave this exercise to the reader.

## Purpose
The aim of this repo is to collaborate on tools that analyze the available power consumption data, and suggest the right discount plan for a household. It is currently available for households that have a new power meter installed, and are serviced by IEC or any other commercial utility provider.

The data analysis will result in output similar to the below, helping you lower your electricity bill:
```
--------------------------------------------------------------------------------
Plan                      Cost reduction
--------------------------------------------------------------------------------
night_only                6.45%
day_only                  2.26%
all_day                   7.00%
```

## Usage
Start by cloning this repo. You will need python3 installed.
```sh
git clone https://github.com/adrukh/iec-analyzer.git
cd iec-analyzer
```

### IEC
IEC allow online access to power consumption data. Download it at https://iec.co.il/consumption-info-menu/remote-reading-info. This will be a CSV file with a funny name.

Then run:
```sh
python3 analyze_iec.py path/to/your-iec-file.csv
```

### Cellcom
Cellcom do not provide their data online yet. You need to call them (*2266 or 0732989184) and ask for your data for a specific timeframe. Ask for as much as they have, and they will email you an XLSX file. [Find a way](https://csvkit.readthedocs.io/) to save it in CSV format.

Then run:
```sh
python3 analyze_cellcom.py path/to/your-cellcom-file.csv
```

## Contribute
Please feel free to suggest ideas (PRs are welcome) for more things this analysis can do!

Support for the different data formats of the various utility providers will also be appreciated.
