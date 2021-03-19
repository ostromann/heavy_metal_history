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
import networkx as nx
import itertools
from heapq import nlargest

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


DATASET = os.path.abspath(__file__ + "/../../") + '/data/proc_MA_1k_albums.csv'

def load_data(dataset):
    """
    Loads a dataset as Pandas DataFrame. Inputs can be either a filepath to a csv, a Pandas DataFrame or None.
    If None the dataset indicate in global constant is loaded.

    Parameters
    ----------

    dataset : Name of the input csv file or pandas dataframe

    Returns:
    ----------

    Dataframe
    """
    
    # Load data
    assert dataset is None or isinstance(dataset, str) or isinstance(dataset, pd.DataFrame), "'dataset' must be None, str or pandas DataFrame"
    if isinstance(dataset, pd.DataFrame):
        df = dataset
    elif dataset is not None:
        df = pd.read_csv(dataset)
    else:
        df = pd.read_csv(DATASET)
    return df


def artist_barplot(min_albums=5, n_artists=30, metric='MA_score', file_name='./images/artist_bar.svg'):
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

    The pandas Series used to produce the image
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


def prune_and_group(threshold=5, dataset=None):
    """
    Preprocess the dataset with grouping and pruning.

    Parameters
    ----------

    threshold: pruning value, all artist entries with album value < threshold will be removed

    dataset : Name of the input csv file or pandas dataframe

    Returns:
    ----------

    Return the grouped and pruned dataset.
    """

    # Load data
    df = load_data(dataset)

    
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

    dataset : Name of the input csv file or pandas dataframe

    image_name : Name of the output image (or None to not save)

    Returns
    ----------

    The output image as a PIL Image object
    """

    # Load data
    df = load_data(dataset)
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


def generate_tag_cooccurrence_list_from_df(df):
    """
    Generate a list of cooccurring tags per album from a dataframe.

    Parameters
    ----------

    df: dataframe used to generate the list

    Returns
    ----------

    List of cooccurring tags per album.
    """
    tags_df = df[['tags']].dropna(axis=0)
    tags = tags_df['tags'].values
    tag_cooccurrence_list = []
    for tag in tags:
        tag_cooccurrence_list.append(eval(tag))
    return tag_cooccurrence_list

def generate_unique_tag_from_list(tag_list):
    """
    Generate a list of unique tags.

    Parameters
    ----------

    tag_list : list of tags per album.

    Returns
    ----------

    List of unique tags.
    """
    # Assert tag_list is a list of lists
    assert isinstance(tag_list, list), "'tag_list' is not of type list."
    assert all(isinstance(x, list) for x in tag_list), "'tag_list' is not a list of lists."

    # Get List of unique tags in list of lists
    unique_tags = list(set(list(itertools.chain.from_iterable(tag_list))))
    return unique_tags

def generate_tag_network(tag_cooccurrence_list, tags):
    """
    Generate a nextwork from tags and their coocurrences.
    Each node resembles a tag. Each edge resembles a coocurrence of two tags.
    Node weight resembles number of occurrences of a tag.
    Edge weight resembles number of cooccurrences of two tags.

    Parameters
    ----------

    tag_cooccurrence_list : list of cooccurring tags.

    tags : list of unique tags.

    Returns
    ----------

    Graph of tags
    """
    G = nx.Graph()
    G.add_nodes_from(tags) #create a node for each tag
    nx.set_node_attributes(G, 1,'weight')

    for d in tag_cooccurrence_list:
        # Increase node weight
        for n in d:
            G.nodes[n]['weight'] += 1

            # Draw Edges (or increase weight if already present)
            if len(d) >= 2:
                for comb in itertools.combinations(d, 2):
                    u = comb[0]
                    v = comb[1]
                    if G.has_edge(u, v):
                        G[u][v]['weight'] += 1
                    else:
                        G.add_edge(u, v, weight=1)
    return G


def filter_tag_graph(g, n_top_tags, attribute='weight'):
    """
    Filter graph for the n top tags according to chosen attribute.

    Parameters
    ----------

    g : Input graph of tags

    n_top_tags : Number of top tags to filter

    attribute : The node attribute to filter on

    Returns
    ----------

    Subgraph filtered for top tags
    """
    assert isinstance(g, nx.Graph), "'g' must be an undirected Graph (nx.Graph)"
    node_dict = nx.get_node_attributes(g, attribute)
    top_node_keys = nlargest(n_top_tags, node_dict, key = node_dict.get)    
    
    return g.subgraph(top_node_keys)

def tag_graph(n_tags=18, dataset=None, file_name='./images/tag_graph.svg'):    
    """
    Visualize coocurrences of tags in the dataframe.

    Parameters
    ----------

    num_albums : Number of top albums to use (by playcount)

    n_tags : Number of tags used in the visualisation

    dataset : Name of the input csv file or pandas dataframe

    image_name : Name of the output image (or None to not save)

    Returns
    ----------

    Matplotlib figure of the tag graph.
    """
    # Load data
    df = load_data(dataset)

    tag_cooccurrence_list = generate_tag_cooccurrence_list_from_df(df)
    unique_tags = generate_unique_tag_from_list(tag_cooccurrence_list)
    G = generate_tag_network(tag_cooccurrence_list, unique_tags)
    G = filter_tag_graph(G, n_top_tags=n_tags)

    n_weights = nx.get_node_attributes(G, 'weight')
    edges,e_weights = zip(*nx.get_edge_attributes(G,'weight').items())    

    # Plot constants for tag graph
    FIG_SIZE = (12,10)

    X_OFFSET = 1.1
    Y_OFFSET = 1.25 # y-axis offset needs to be larger so labels have enough space
    X_LIMIT = [-2,2]
    Y_LIMIT = [-1.5,2]
    IMG_EXTENT = X_LIMIT + Y_LIMIT

    NODE_SIZE = 7
    NODE_COLOR = 'white'
    SHADOW_NODE_SIZE = 10
    SHADOW_NODE_COLOR = '#333333'

    EDGE_WIDTH= 1.0
    EDGE_WIDTH_LOG_BASE = 3 # Base 10 was too extreme, base 2 too small
    EDGE_COLOR = 'white'

    LABEL_FONT_COLOR = 'white'
    LABEL_FONT_WEIGHT = 'bold'

    TITLE_TEXT = 'Heavy Metal Genre Relations'
    TITLE_X_POS = -1.2
    TITLE_Y_POS = 1.5
    TITLE_FONT_SIZE = 28
    TITLE_FONT_COLOR = 'white'

    BACKGROUND_IMAGE_FILE = "assets/coal_bg_crop.jpg"

    # Create figure
    plt.figure(1,figsize=FIG_SIZE) 
    ax = plt.axes()
    img = plt.imread(BACKGROUND_IMAGE_FILE)
    ax.imshow(img, extent=IMG_EXTENT)
    pos = nx.circular_layout(G)
    pos_outer = {}
    for k, v in pos.items():
        pos_outer[k] = (v[0]*(X_OFFSET), v[1]*(Y_OFFSET))

    nx.draw_networkx(G, pos, nodelist=n_weights.keys(), node_size=[v * SHADOW_NODE_SIZE for v in n_weights.values()], node_color=SHADOW_NODE_COLOR, edge_color=EDGE_COLOR, width=[math.log(v, EDGE_WIDTH_LOG_BASE) * EDGE_WIDTH for v in e_weights], with_labels=False)
    nx.draw_networkx_nodes(G, pos, nodelist=n_weights.keys(), node_size=[v * NODE_SIZE for v in n_weights.values()], node_color=NODE_COLOR)
    nx.draw_networkx_labels(G, pos_outer, font_color=LABEL_FONT_COLOR, font_weight=LABEL_FONT_WEIGHT)
    plt.xlim(X_LIMIT)
    plt.ylim(Y_LIMIT)

    ax.text(TITLE_X_POS, TITLE_Y_POS, TITLE_TEXT, size=TITLE_FONT_SIZE, color=TITLE_FONT_COLOR)
    
    fig = plt.gcf()
    if file_name is not None:
        dir_name = os.path.dirname(file_name)
        if dir_name != '' and not os.path.exists(dir_name):
            os.makedirs(dir_name)
        plt.savefig(file_name)
    plt.close("all")

    return fig






