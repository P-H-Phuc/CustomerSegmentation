# -*- coding: utf-8 -*-

# =============================================================================
#                       IMPORT MODULES FOR THIS PROJECT
# =============================================================================

def import_modules():
    # List nessary for project
    import pandas as pd
    import numpy as np
    import pandas as pd
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import seaborn as sns
    import datetime, nltk, warnings
    import matplotlib.cm as cm
    import itertools
    from pathlib import Path
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_samples, silhouette_score
    from sklearn import preprocessing, model_selection, metrics, feature_selection
    from sklearn.model_selection import GridSearchCV, learning_curve
    from sklearn.svm import SVC
    from sklearn.metrics import confusion_matrix
    from sklearn import neighbors, linear_model, svm, tree, ensemble
    from wordcloud import WordCloud, STOPWORDS
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.decomposition import PCA
    from IPython.display import display, HTML
    import plotly.graph_objs as go
    from plotly.offline import init_notebook_mode,iplot
    from termcolor import colored
    init_notebook_mode(connected=True)
    warnings.filterwarnings("ignore")
    plt.rcParams["patch.force_edgecolor"] = True
    plt.style.use('fivethirtyeight')
    mpl.rc('patch', edgecolor = 'dimgray', linewidth=1)
    # Return
    return print('\x1b[1;31;47m' + ' Modules were imported sucessfully! ' + '\x1b[0m')