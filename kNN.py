import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Utils as utils
from operator import itemgetter

# reading data
#da = utils.combine_data()
da = pd.read_csv('rawdata/oxfordRawData.csv')

def setup():
    pd.set_option('display.max_rows', 2000)
    plt.rcParams['figure.figsize'] = (10.0, 5.0)


def calculate_data(data, season):
    d = utils.construct_season_dataframe_no_fill(data, season)
    set_size = 5
    k = 3
    set = []
    for i in range(set_size):
        dic = {
            "ma": d[["maxC"]].values[d[["maxC"]].size - 1 - i][0],
            "yyyy": d[["yyyy"]].values[d[["yyyy"]].size - 1 - i][0]
        }
        set.append(dic)

    new_set = sorted(set, key=itemgetter('yyyy'))
    mean = 0

    for i in range(k):
        mean += new_set[k]['ma']

    mean = mean / k
    return mean


def calculate_data_from_date(k, data, season, date):
    d = utils.construct_season_dataframe_no_fill(data, season)

    set_size = 5
    set = []
    for i in range(set_size):
        index = date - 1948

        new_k = round(k/2) - i
        if date > 2018:
            new_k = i

        dic = {
            "ma": d[["maxC"]].values[index-1 - new_k][0],
            "yyyy": d[["yyyy"]].values[index-1 - new_k][0]
        }
        set.append(dic)

    mean = 0

    for i in range(k):
        mean += set[i]['ma']

    mean = mean / k
    print(set)
    return mean


def plot():
    new_win = calculate_data_from_date(5, da, "winter", 2019)
    new_spr = calculate_data_from_date(5, da, "spring", 2019)
    new_sum = calculate_data_from_date(5, da, "summer", 2019)
    new_aut = calculate_data_from_date(5, da, "autumn", 2019)
    
    new_plot_frame = []
    new_plot = {
        "winter": new_win,
        "spring": new_spr,
        "summer": new_sum,
        "autumn": new_aut
    }
    print(new_win, new_spr, new_sum, new_aut)
    new_plot_frame.append(new_plot)
    new_plot_frame = pd.DataFrame(new_plot_frame)
    plt.axis([0, 12, 0, 40])
    plt.plot(['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'], [0, new_win, 0, 0, new_spr, 0, 0, new_sum, 0, 0, new_aut, 0], 'ro')
    plt.ylabel('Temperature (degress(c))')
    plt.xlabel('Season')

    plt.legend
    plt.show()

setup()
plot()
#print(calculate_data_from_date(5, da, "winter", 2018))