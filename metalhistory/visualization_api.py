"""
Class allowing some nice visualization of heavy metal data
"""

from .data_query_functions import LastFM

# visualization libraries
import numpy as np
import pandas as pd
import os
import squarify
import ast
import math
import requests
from PIL import Image

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


DATASET = os.path.abspath(__file__ + "/../../") + '/data/proc_MA_1k_albums_not_cumulative.csv'


def artist_barplot(min_albums=5, n_artists=30, metric='MA_score', file_name='./images/artist_bar.jpg'):
    """
    Visualize a histogram plot with artists statistics based on the MA score.

    Parameters
    ----------

    min_albums: Min number of album published by the considered artists

    n_artists: Max number of the artists considered in the plot

    metric: Metric used to evaluate the entries [listeners, playcount, MA_score]

    file_name: Name of the output file

    Returns:
    ----------

    Return the image with average, max and min scores and the dataset used for the plotting.
    """

    artist_df = prune_and_group(min_albums)

    # manipulate DF to retain useful statistics for the plot
    artist_description = artist_df.describe()
    # prune the dataset from the not considered metrics
    all_metrics = ['listeners', 'playcount', 'MA_score']
    all_metrics.remove(metric)
    artist_description.drop(all_metrics, axis=1, level=0, inplace=True)
    artist_description.drop(['count', 'std', '25%', '50%', '75%'], axis=1, level=1, inplace=True)
    artist_sorted = artist_description.sort_values(by=(metric, "mean"), ascending=False)
    # drop upper level in columns names
    output_df = artist_sorted.copy()
    artist_sorted.columns = artist_sorted.columns.droplevel()
    # keep the requested number of artists
    # note that n_artists is higher than the size of the dataframe, no exception is raised
    artist_sorted = artist_sorted.head(n_artists)

    img = plt.figure(figsize=(900,300))
    artist_sorted.plot.bar()
    plt.xticks(rotation=70)
    plt.title("Statistics on artists with at least " + str(min_albums) + " albums.")
    plt.xlabel("")
    plt.ylabel("Metric: " + metric)
    plt.tight_layout()

    if file_name is not None:
        dir_name = os.path.dirname(file_name)
        if dir_name != '' and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        plt.savefig(file_name)
    plt.close("all")

    return img, output_df


def artist_cloud(min_albums=5, words_limit=20, metric='MA_score', file_name='./images/artist_cloud.svg'):
    """
    Visualize a world cloud with artist names.

    Parameters
    ----------

    min_albums: Min number of album published by the considered artists

    words_limit: Max number of the artists considered in the word cloud

    metric: Metric used to evaluate the entries [listeners, playcount, MA_score]

    file_name: Name of the output file

    Returns:
    ----------

    The dataframe used to produce the image
    """

    artist_df = prune_and_group(min_albums)

    artist_df = artist_df.mean().sort_values(by=metric, ascending=False)[metric]
    # elaborate data
    if metric == 'listeners':
        artist_df = artist_df.div(1e+05)
    elif metric == 'playcount':
        artist_df = artist_df.div(1e+06)
    artist_df = artist_df.round(2)

    artist_df = artist_df.head(words_limit)

    # create and generate a word cloud image
    txt_path = generate_text_from_df(artist_df)
    generate_word_cloud(words_limit, txt_path, file_name)

    return artist_df


def prune_and_group(threshold=5):
    """
    Preprocess the dataset with grouping and pruning.

    Parameters
    ----------

    threshold: pruning value, all artist entries with album value < threshold will be removed

    Returns:
    ----------

    Return the grouped and pruned dataset.
    """

    try:
        df = pd.read_csv(DATASET)
    except FileNotFoundError:
        print("The specified file could not be loaded.")
    
    # consider only relevant index
    df = df[['MA_artist', 'MA_album', 'listeners', 'playcount', 'MA_score']]
    # group dataset by artist
    df_grouped = df.groupby('MA_artist')
    # sort artist by album count
    df_sorted = df_grouped.count().sort_values(by='MA_album', ascending=False)
    # save the dataframe with discarded artists
    discarded = df_sorted.drop(df_sorted[df_sorted['MA_album'] >= threshold].index)
    for artist in discarded.index:
        df = df.drop(df_grouped.get_group(artist).index)

    return df.groupby('MA_artist')


def generate_text_from_df(df, file_name='./images/artist_cloud.txt'):
    """
    Generate a textfile froma dataframe to use in the word cloud.

    Parameters
    ----------

    df: dataframe used to generate the file

    file_name: Name of the output file

    Returns:
    ----------

    Path to the file so it's easy to locate it.
    """

    # the dataframe is indexed with the artists names that we need to access
    index_obj = df.index
    index_list = []

    # erase the file if it exists
    out_file = open(file_name, 'w')
    out_file.write("")

    for name in index_obj:
        # replace space with tabs so that artists names with multiple words are counted as a single entity
        index_list.append(name.replace(' ', '_'))
        count = round(float(df.loc[name]))
        # create a file.txt containing artists names repeated N times where N is the number of published albums
        out_file = open(file_name, 'a')
        for i in range(count):
            out_file.write(index_list[-1] + " ")

    return file_name


def generate_word_cloud(words=1, txt_file='./images/artist_cloud.txt', figure_name='./images/artist_cloud.svg'):
    """
    Generate the word cloud out of a txt file.

    Parameters
    ----------

    words: Number of words in the could

    txt_file: Path of the file containing the text used to generate the word cloud

    figure_name: Name of the output figure
    """

    out_file = open(txt_file, 'r')
    contents = out_file.read()
    wordcloud = WordCloud(collocations=False, max_words=words).generate(contents)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(figure_name)

    if figure_name is not None:
        dir_name = os.path.dirname(figure_name)
        if dir_name != '' and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        plt.savefig(figure_name)
    plt.close("all")


def album_covers(num_albums=100, width=1280, height=720, dataset=None,
                 image_name='./images/album_covers.jpg'):
    """
    Visualize a wordcloud but use album covers instead of names.

    Parameters
    ----------

    num_albums : Number of top albums to use (by playcount)

    width : Width of the output image

    height : Height of the output image

    dataset : Name of the input csv file

    image_name : Name of the output image (or None to not save)

    Returns
    ----------

    The output image as a PIL Image object
    """

    # Load data
    if dataset is not None:
        df = pd.read_csv(dataset)
    else:
        df = pd.read_csv(DATASET)
    df = df[['artist', 'album', 'playcount', 'image']]
    df = df.sort_values('playcount', ascending=False)
    if num_albums is not None:
        df = df.head(num_albums)

    # Format image URLs
    def format_image_str(s):
        # TODO: get the largest image in case some image sizes are not present
        s = s.replace('"', "'")
        s = ast.literal_eval(s)
        return s[-1]['#text']
    df['image'] = df.apply(lambda row: format_image_str(row['image']), axis=1)

    # Compute album cover positions using squarify
    values = list(df['playcount'])
    values = squarify.normalize_sizes(values, height, width)
    rects = squarify.squarify(values, 0., 0., height, width)

    # Compute integer values for slicing
    for rect in rects:
        rect['x1'] = max(0, math.floor(rect['x']))
        rect['y1'] = max(0, math.floor(rect['y']))
        rect['x2'] = min(height, math.ceil(rect['x'] + rect['dx']))
        rect['y2'] = min(width,  math.ceil(rect['y'] + rect['dy']))

    # Create the image
    img = np.zeros((height, width, 3), np.uint8)
    for i, url in enumerate(df['image']):
        rect = rects[i]
        im = Image.open(requests.get(url, stream=True).raw)
        im = im.convert('RGB')
        im = im.resize((rect['y2']-rect['y1'], rect['x2']-rect['x1']))
        im = np.asarray(im)
        img[rect['x1']:rect['x2'], rect['y1']:rect['y2'], :] = im

    # Save and return the image
    img = Image.fromarray(img)
    if image_name is not None:
        dir_name = os.path.dirname(image_name)
        if dir_name != '' and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        img.save(image_name)
    return img
