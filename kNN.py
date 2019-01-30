import pandas as pd
import matplotlib.pyplot as plt
import Utils as utils
from operator import itemgetter

# reading data
#da = utils.combine_data()
da = pd.read_csv('rawdata/heathrowRawData.csv')


class knn:
    def __init__(self,  *args, **kw):
        pd.set_option('display.max_rows', 2000)
        plt.rcParams['figure.figsize'] = (10.0, 5.0)
        #self.write_to_file(5, 2013)
        #self.plot()

    def calculate_data(self, data, season):
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

    def calculate_data_from_date(self, k, data, season, date):
        d = utils.construct_season_dataframe_no_fill(data, season)
        print(season)
        set_size = 5
        set = []
        for i in range(set_size):
            index = date - 1948

            new_k = round(k/2) - i
            if date >= 2016:
                new_k = i + 1

            dic = {
                "ma": d[["maxC"]].values[index - new_k][0],
                "yyyy": d[["yyyy"]].values[index - new_k][0]
            }
            set.append(dic)

        mean = 0

        for i in range(k):
            mean += set[i]['ma']

        mean = mean / set_size
        print(set)
        return mean

    def calculate_fade_points(self, k, data, season, year):
        fade_set = pd.DataFrame()
        month_series = utils.get_data_from_season(season, utils.get_data_from_year(data, year))[['mm']]

        for i in range(k):
            y_d = utils.get_data_from_year(data, year - i)
            d = utils.get_data_from_season(season, y_d)
            ad = d[['maxC', 'minC']].mean(axis=1)
            m = ad.to_frame().reset_index().drop(['index'], axis=1)
            fade_set = pd.concat([fade_set, m], axis=1)
            new_avg = fade_set.mean(axis=1)

        final_df = pd.concat([month_series.reset_index().drop(['index'], axis=1), new_avg], axis=1)
        final_df.columns=['mm', 'temp']

        return final_df

knn()
