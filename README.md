# iec-analyzer
Recommends the cheapest utility plan for your electricty bill in Israel.

## Background
Israel is moving from old electricity power meters to new ones, which support near-real-time metering of the power consumed and produced by each household. Along this change, utility providers offer discounted rates for different times of day. This raises the question - given a specific power usage profile of a household, which program / discount plan is most economic for the household? As of now, the utility providers leave this exercise to the reader.

## Purpose
The aim of this repo is to provide tools that analyze the available power consumption data, and, given the available plan details, suggest the right discount plan for the lowest electricity bill. The analysis requires data obtained from new power meters, regardless of the chosen utility provider.

After running the analysis, you should expect output similar to:
```
--------------------------------------------------------------------------------
Plan                                     Overall cost reduction
--------------------------------------------------------------------------------
20% discount between 23:00 and 7:00      8.32%
15% discount between 7:00 and 17:00      2.43%
7% discount across the entire day        7.00%
--------------------------------------------------------------------------------
```

The above example shows that the 20% during night-time discount plan is the best one for the analyzed consumption data.

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
