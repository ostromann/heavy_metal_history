# The History of Heavy Metal

In this project we will gather statistics from LastFM and Spotify to analyse and visualise the most influencial Heavy Metal albums in history.

![CI](https://github.com/ostromann/heavy_metal_history/blob/master/.github/workflows/python-package/badge.svg)


## Motivation
This projects aims to demonstrate good software engineering practices (versioning, testing, refactoring).

## Table of Contents
- [Getting started](#getting-started)
  - [Install](#install)
  - [Usage](#usage)
  - [Testing](#testing)
  - [Folder structure](#folder-structure)
- [Development Notes](#development-notes)
  - [Commit Convention](#commit-convention)
  - [Branch Convention](#branch-convention)
  - [Workpackages](#workpackages)
  - [Datasets](#datasets)
  - [Data Collection](#data-collection)
- [FAQ](#faq)
  - [Do I need an API key?](#Do-I-need-an-API-key?)
  - [What counts as Heavy Metal?](#What-counts-as-Heavy-Metal?)


# Getting started

## Install
It is possible to install and run our code both with and without a conda environment. See both options below.

### With a Conda environment
To use with conda simply run the following commands. An environment will be created with the name `spotify`, so make sure that there does not already exist an environment with that name.
```bash
git clone https://github.com/ostromann/heavy_metal_history.git
cd heavy_metal_history
conda env create -f environment.yml
conda activate metalhistory
```

### Without a Conda environment
If you want to install the repository not in a Conda-based environment, simply clone the repository, then run the following commands:
```bash
cd heavy_metal_history
pip3 install -r requirements.txt
```
Note to run
```bash
python3 -m venv /path/to/new/virtual/environment
```
if you want to create a virtual environment before installing the required packages.

## Usage
The code in this repository can be devided into two groups of functions, namely data retrieval/pre-processing and visualization. We provide two jupyter notebooks to demonstrate the usage of these functions.

To get familiar with the data retrieval/pre-processing, run:
```bash
jupyter notebook 0-preprocessing.ipynb
```
This uses the functions in `metalhistory/data_query_functions.py` to create a csv file of pre-processed data. We do not recommend running this for a large number of album entries as it takes a long time. We have instead included the pre-processed csv file in the repository.

To see how to do some visualizations, run:
```bash
jupyter notebook 1-visualizations.ipynb
```
This notebook uses the functions in `metalhistory/visualization_api.py` to visualize the pre-processed data in different ways.

It is also possible to view these notebooks in a browser by navigating to e.g. <a href="https://github.com/ostromann/heavy_metal_history/blob/master/1-visualizations.ipynb">1-visualizations.ipynb</a>.


## Testing
Run test routines with:
```bash
pytest -s
```
from the root directory. This command will execute all the test routines contained in the `tests` folder.
The `-s` option will output to screen any `print()` statement. To run singular test routines, execute:
```bash
pytest -s metalhistory/tests/test_query_api.py
```
to test the data query functions, and
```bash
pytest -s metalhistory/tests/test_visualization_api.py
```
to test the visualization functions.


## Folder structure
We use the following folder structure in this project:
- `heavy_metal_history`, root of repository (includes notebooks)
  - `data`, raw and pre-processed data
  - `images`, generated visualizations and other images
  - `metalhistory`, source code
    - `tests`


# Development Notes

## Commit Convention

In general we follow the <a href="https://www.conventionalcommits.org/en/v1.0.0/ ">Conventional Commits 1.0.0</a>.
We use the following commit types:
feat, fix, docs, test


## Branch Convention

We draw some inspiration from <a href="https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow">Gitflow</a> and use two permanent branches, namely *master* and *stable*. For each new feature we create a new temporary branch of master named *type/scope* where *type* is one of feature/fix/doc or similar, and *scope* is a brief name for the feature. The name is written in small letters and words are separated by hyphen (-). An example branch name is *feature/word-cloud-visualization*.

When enough features have been implemented for a release, we merge the master branch with the stable branch and increment the release version.


## Workpackages

Keep track of this project's development on this <a href="https://trello.com/b/Ixw63lN3/history-of-heavy-metal">Trello board</a>.

## Datasets
Currently we have two lists of input data:


[./data/artists_unfiltered.csv](./data/artists_unfiltered.csv) which contains a list of artists that have released at least 1 album that could be tagged as a subgenre of metal (See [What counts as Heavy Metal?](#What-counts-as-Heavy-Metal?)). This means that album tags should be checked before including all albums of an artist.

[./data/MA_10k_albums.csv](./data/MA_10k_albums.csv) which contains the a list of 10,000 albums and their respective artists that received the highest Metascores on <a href="https://www.metal-archives.com/">Encyclopedia Metallum: The Metal Archives</a>.



Additionally, we have one preprocessed dataset that is ready for data analysis and visualizations: 

[./data/proc_MA_1k_albums.csv](./data/proc_MA_1k_albums.csv) contains the first 1,000 albums of [./data/MA_10k_albums.csv](./data/MA_10k_albums.csv) with added information like listeners, playcounts, tags, urls, images etc.


## Data Collection

The data will be collected using <a href="https://developer.spotify.com/documentation/web-api/">Spotify's Web API</a> and  <a href="https://www.last.fm/api">LastFM's Web API</a>.

The following features and limitations were already identified in the two APIs:

Spotify's Web API:
- doesn't show playcounts
- release years are often wrong (due to re-masters, special editions etc.)
- gives only a popularity score measured against the most popular artists in general

LastFM's API:
- shows playcounts and number of listeners
- many different versions of the same album appear
- release years are often wrong, too

To get the right release years we'd perhaps need to use another API (Wikipedia?) or use some other approach (like take the lowest ever mentioned release year of an album on Last FM)




# FAQ
## Do I need an API key?
Right now you will need a personal API key for both Spotify's Web API and LastFM's Web API. Both are free but require registration (see <a href="https://developer.spotify.com/documentation/general/guides/app-settings/">Spotify Authentication</a> and <a href="https://www.last.fm/api/authentication">LastFM Authentication</a>).

## What counts as Heavy Metal?

To give a broad overview of the genre all of the following subgenres of Heavy Metal are considered (taken from <a href="https://en.wikipedia.org/wiki/Heavy_metal_genres">
Wikipedia</a> and extended by some sub Wikipedia sites. Can still be extended):

<ul style="list-style-type:none;">
        <li><details><summary>Alternative metal</summary>
        <p>
            <ul>
                <li>Funk metal</li>
                <li>Nu metal</li>
                <li>Rap metal</li>
            </ul>
        </p>
        </details></li>
        <li>Avant-garde metal</li>
        <li><details><summary>Black metal</summary>
        <p>
            <ul>
                <li>Ambient black metal</li>
                <li>Blackened heavy metal</li>
                <li>Blackened screamo</li>
                <li>Blackgaze</li>
                <li>Black'n'Roll</li>
                <li>Depressive suicidal black metal</li>
                <li>NSBM</li>
                <li>Post-black metal</li>
                <li>Red and Anarchist black metal</li>
                <li>Symphonic black metal</li>
                <li>Viking metal</li>
                <li>War metal</li>
            </ul>
        </p>
        </details></li>
        <li><details><summary>Christian metal</summary>
        <p>
            <ul>
                <li>Unblack metal</li>
            </ul>
        </p>
        </details></li>
        <li><details><summary>Crust punk</summary>
        <p>
            <ul>
                <li>Blackened crust</li>
            </ul>
        </p>
        </details></li>
        <li><details><summary>Death metal</summary>
        <p>
            <ul>
                <li>Blackened death metal</li>
                <li>Death 'n' roll</li>
                <li>Melodic death metal</li>
                <li>Technical death metal</li>
                <li>Symphonic death metal</li>
            </ul>
        </p>
        </details></li>
        <li><details><summary>Doom metal</summary>
        <p>
            <ul>
                <li>Death-doom</li>
                <li>Drone metal</li>
                <li>Funeral doom</li>
                <li>Sludge metal</li>
                <li>Stoner metal</li>
            </ul>
        </p>
        </details></li>
        <li>Extreme metal</li>
        <li><details><summary>Folk metal</summary>
        <p>
            <ul>
                <li>Celtic metal</li>
                <li>Pirate metal</li>
                <li>Pagan metal</li>
            </ul>
        </p>
        </details></li>
        <li><details><summary>Glam metal</summary>
         <p>
            <ul>
                <li>Hair metal</li>
                <li>Pop metal</li>
            </ul>
        </p></details></li>
        <li>Gothic metal</li> 
        <li><details><summary>Grindcore</summary>
        <p>
            <ul>
                <li>Deathgrind</li>
                <li>Goregrind</li>
                <li>Pornogrind</li>
                <li>Electrogrind</li>
            </ul>
        </p>
        </details></li>
        <li>Grunge</li>
        <li><details><summary>Industrial metal</summary>
        <p>
            <ul>
                <li>Industrial death metal</li>
                <li>Industrial black metal</li>
            </ul>
        </p>
        </details></li>
        <li>Kawaii metal</li>
        <li>Latin metal</li>
        <li><details><summary>Metalcore</summary>
        <p>
            <ul>
                <li>Melodic metal</li>
                <li>Deathcore</li>
                <li>Mathcore</li>
                <li>Electronicore</li>
                <li>Synthcore</li>
                <li>Trancecore</li>
                <li>Nu metalcore</li>
                <li>Nu metal revival</li>
                <li>New nu metal</li>
                <li>Progressive metalcore</li>
                <li>Technical metalcore</li>
                <li>Ambient metalcore</li>
            </ul>
        </p>
        </details></li>
        <li>Neoclassical metal / Shred metal</li>
        <li>Neue Deutsche Härte</li>
        <li>Post-metal</li>
        <li>Power metal</li>
        <li><details><summary>Progressive metal</summary>
        <p>
            <ul>
                <li>Djent</li>
                <li>Space metal</li>
            </ul>
        </p>
        </details></li>
        <li>Speed metal</li>
        <li>Symphonic metal</li>
        <li><details><summary>Thrash metal</summary>
        <p>
            <ul>
                <li>Crossover thrash</li>
                <li>Groove metal</li>
                <li>Teutonic thrash metal</li>
            </ul>
        </p>
        </details></li>
        <li><details><summary>Traditional heavy metal</summary>
        <p>
            <ul>
                <li>New wave of British heavy metal (NWOBHM)</li>
                <li>New wave of American heavy metal (NWOAHM)</li>
                <li>New wave of traditional heavy metal (NWOTHM)</li>
            </ul>
        </p>
        </details></li>
</ul>




