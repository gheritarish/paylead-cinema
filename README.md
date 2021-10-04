# paylead-cinema
This repository contains an answer to the technical test for PayLead.

## Purpose
The objective of this repository is to contain a solution answering to the following problematic: we want some statistics on French theaters, and we want to get them from a UNIX shell running a Python script.

The code contained in this repository answers to the following questions:

* How to download the data (zip archive) and extract the file we are interested in?
* How to analyze the data to get:
  * The number of theaters in a city, knowing the name of the city
  * The *n* biggest networks of theaters, given an argument *n*
  * A quick analysis of a network, with the biggest theaters (numbers of screens and seats), and the number of theaters with 3D projection
  * The number of theaters in a department, given the department code (*e.g.* 75 for Paris, 2A for Corse du Sud).

## How does it work?
This tool has two different parts: a scrapping part, and an analysis part.

### Scrapping
This part works as follow: we know the URL of the website from which we want to get the data. The objective is to find, on this page, the URL of the file to download.

For that, we will get all the URL that are present on this site, and find the one that matches a pre-defined regex.

Then, we download the corresponding file: this operation takes a few minutes.

Once the data is downloaded, we analyze the content of the zip archive to find the geojson file, that we can extract.

### Analysis
Once the data is downloaded and extracted, we can analyze it.

To do so, the geojson file is loaded as a `GeoDataFrame`, on which are made the different analysis we want.

Each of those analysis calls a function that will specifically get the informations we want, so we can stay with short functions that we can test and maintain easily.

## Install
To install this tool, the first step is to clone this repository.

Then, the `./install.sh` script will create an environment and install all dependencies for the project, so you can execute the script. **It will fail if you don't run this first!**

The last installation step is to run the following command: `./cinema_osm.py --mode initialize`. This will download the data in the zip file `./cinema_geojson.zip`.

Once this has been downloaded, the different analysis can be run with `./cinema_osm.py --mode analyze`, as developed in the next part.

## Input
The analyze mode of this script accepts several different arguments:

* `--theatersintown (str)`: the string given to this argument is the name of the town from which we want to know the number of theaters.
* `--biggestnetworks (int)`: the integer given to this argument is the number of networks from which we want to get informations. Those networks are sorted from the biggest to the smallest.
* `--analyzenetwork (str)`: the name of the network from which we want to get a quick analysis.
* `--theatersindepartment (str)`: the code of the department of which we want to know the number of theaters.

## Output
Each of those modes will give a different output. Here are some examples:

### Number of theaters in a town
`$ ./cinema_osm.py --mode analyze --theatersintown Paris`:

`There are 90 theaters in Paris.`

### The three biggest networks
`$ ./cinema_osm.py --mode analyze --biggestnetworks 3`:

```
Pathé Gaumont: 68 theaters.
CGR cinémas: 64 theaters.
UGC: 49 theaters.
```

### Analysis of the UGC network
`$ ./cinema_osm.py --mode analyze --analyzenetwork UGC`:

```
Network: UGC:

Highest number of screens: 22 at UGC Ciné Cité Strasbourg

Biggest theater: 5412 seats at UGC Ciné Cité Strasbourg

8 3D theaters in this network.
```

### Number of theaters in Corse du Sud
`$ ./cinema_osm.py --mode analyze --theatersindepartment 2A`:

`There are 9 theaters in department 2A`

## Tests
Tests for this code were written with pytest. There are a total of 13 tests, focused on the analysis part and the scrapping part.
