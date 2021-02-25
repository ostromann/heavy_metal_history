# The History of Heavy Metal

In this project we will gather statistics from LastFM and Spotify to analyse and visualise the most influencial Heavy Metal albums in history.


## Motivation
This projects aims to demonstrate good software engineering practices (versioning, testing, refactoring).

## Table of Contents
- Getting started
  - [Install](#install)
  - [Usage](#usage)
- Development Notes
    - [Commit Convention](#commit-convention)
    - [Workpackages](#workpackages)
    - [Data Collection](#data-collection)
- FAQ
    - [Do I need an API key?](#Do-I-need-an-API-key?)
    - [What counts as Heavy Metal?](#What-counts-as-Heavy-Metal?)


# Getting started

## Install
Install instructions go here.

## Usage
Run test routines with:
```bash
pytest -s tests/test_query_api.py
```
from the `metalhistory` directory.
The `-s` option will output to screen any `print()` statement.

# Development Notes

## Commit Convention

In general we follow the <a href="https://www.conventionalcommits.org/en/v1.0.0/ ">Conventional Commits 1.0.0</a>.
We use the following commit types:
feat, fix, docs, test


## Workpackages

Keep track of this project's development on this <a href="https://trello.com/b/Ixw63lN3/history-of-heavy-metal">Trello board</a>.

## Datasets
Currently we have two lists of input data:


[./data/artists_unfiltered.csv](./data/artists_unfiltered.csv) which contains a list of artists that have released at least 1 album that could be tagged as a subgenre of metal (See [What counts as Heavy Metal?](#What-counts-as-Heavy-Metal?)). This means that album tags should be checked before including all albums of an artist.

[./data/MetalArchives_top_10000_albums.csv](./data/MetalArchives_top_10000_albums.csv) which contains the a list of 10,000 albums and their respective artists that received the highest Metascores on <a href="https://www.metal-archives.com/">Encyclopedia Metallum: The Metal Archives</a>


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




