# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 22:02:16 2018

@author: Kamalakanta
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 21:55:07 2018

@author: Kamalakanta
"""

import nltk
import random
from nltk.corpus import movie_reviews
import matplotlib.pyplot as plot


def plot_freqdist_freq(fd,
                       max_num=None,
                       cumulative=False,
                       title='Frequency plot',
                       linewidth=2):
    """
    As of NLTK version 3.2.1, FreqDist.plot() plots the counts 
    and has no kwarg for normalising to frequency. 
    Work this around here.
    
    INPUT:
        - the FreqDist object
        - max_num: if specified, only plot up to this number of items 
          (they are already sorted descending by the FreqDist)
        - cumulative: bool (defaults to False)
        - title: the title to give the plot
        - linewidth: the width of line to use (defaults to 2)
    OUTPUT: plot the freq and return None.
    """

    tmp = fd.copy()
    norm = fd.N()
    for key in tmp.keys():
        tmp[key] = float(fd[key]) / norm

    if max_num:
        tmp.plot(max_num, cumulative=cumulative,
                 title=title, linewidth=linewidth)
    else:
        tmp.plot(cumulative=cumulative, 
                 title=title, 
                 linewidth=linewidth)

    return





all_words = []

for w in movie_reviews.words():
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

all_words.plot()
