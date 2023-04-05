import pandas as pd

class DataIngestor:

    def __init__(self):
        pass

    def load_file(self, path, format):
        if format == 'pickle':
            return pd.read_pickle(path)
        elif format == 'csv':
            return pd.read_csv(path)
        elif format == 'xlsx':
            return pd.read_excel(path)
        else:
            return 'Apoligies, but this format has not been implemented yet.'
        
    def save_file(self, df, path, format):
        if format == 'pickle':
            return df.to_pickle(path)
        elif format == 'csv':
            return df.to_csv(path)
        elif format == 'xlsx':
            return df.to_excel(path)
        else:
            return 'Apoligies, but this format has not been implemented yet.'
        
<<<<<<< HEAD
'''save imageimport matplotlib.pyplot as plt
import pandas as pd
from pandas.table.plotting import table # EDIT: see deprecation warnings below

ax = plt.subplot(111, frame_on=False) # no visible frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis

table(ax, df)  # where df is your data frame

plt.savefig('mytable.png')
###############
load image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
image_path = "D:/foto's/fbshare.png"
image = mpimg.imread(image_path)
plt.imshow(image)
plt.show()'''
=======
    def load_to_list(self, path, col, format):

        if format == 'pickle':
            df = pd.read_pickle(path)
            return df.iloc[:, col]
        elif format == 'csv':
            df = pd.read_csv(path)
            return df.iloc[:, col]
        elif format == 'xlsx':
            df = pd.read_excel(path)
            return df.iloc[:, col]
        else:
            return 'Apoligies, but this format has not been implemented yet.'
        
>>>>>>> carlo
