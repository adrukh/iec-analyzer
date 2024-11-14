# iec-analyzer
Analyze power consumption and production data, provided by IEC and other utility providers in Israel

## Background
Israel is moving from old electricity power meters to new ones, which support near-real-time metering of the power consumed and produced by each household. Along this change, utility providers offer discounted rates for different times of day. This raises the question - given a specific power usage profile of a household, which program / discount plan is most economic for the household? As of now, the utility providers leave this exercise to the reader.

## Purpose
The aim of this repo is to collaborate on tools that analyze the available power consumption data, and suggest the right discount plan for a household. It is currently available for households that have a new power meter installed, and are serviced by IEC or any other commercial utility provider.

## Usage
First, download your household power consumption data from IEC at https://iec.co.il/consumption-info-menu/remote-reading-info.

```
git clone https://github.com/adrukh/iec-analyzer.git
cd iec-analyzer
cp ~/Downloads/<IEC data file> iec.csv
python3 analyze_iec.py
```

## Contribute
Please feel free to suggest ideas (PRs are welcome) for more things this analysis can do!
Support for the different data formats of the various utility providers will also be appreciated.
