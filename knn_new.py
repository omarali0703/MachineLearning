import wx
import matplotlib.patches as patches
import pandas as pd
import numpy as np

raw_data = pd.read_csv('rawdata/heathrowRawData.csv')
k_calc_type = ""

def construct_df(raw):
    data = raw_data
    raw_data['avg'] = raw_data[['maxC']].mean(axis=1)   # NOT USING AVERAGE ANYMORE, WANT TO GET AS WARM AS IT COULD BE.
                                                        # THIS IS BECAUSE IT AS MORE IMPACT ON AGRIC. (WANT TO PREPARE
                                                        # FOR THE WORST.
    return data

def construct_year_data(df, year):
    return df.loc[df['yyyy'] == year]

def get_month_data(year, mm): #10oC
    df = construct_df(raw_data)
    year_data = construct_year_data(df, year)
    temp = year_data.loc[df['mm'] == mm].iloc[0]['avg']

    return temp

def mean(arr):
    length = len(arr)
    sum = 0
    for i in arr :
        sum += i
    return sum / length

def construct_season_avg(year, season):
    seasons = {
        "winter": mean([get_month_data(year-1, 12),get_month_data(year, 1),get_month_data(year, 2)]),
        "spring": mean([get_month_data(year, 3), get_month_data(year, 4), get_month_data(year, 5)]),
        "summer": mean([get_month_data(year, 6), get_month_data(year, 7), get_month_data(year, 8)]),
        "autumn": mean([get_month_data(year, 9), get_month_data(year, 10), get_month_data(year, 11)]),
    }

    return seasons.get(season) #gets actual value

def calculate_knn_mid(k, year, season):
    k_side = k // 2
    k_range=[]
    for i in range(k):
        if i != k_side:
            k_range.append(construct_season_avg(year + (i - k_side), season))

    return mean(k_range) #gets predicted value

def calculate_knn_forcast(k, year, season): #calc future values
    k_range=[]
    for i in range(k):
        k_range.append(construct_season_avg(year - (k-i), season))

    return mean(k_range) #gets predicted value


def plot(month_data_arr, month_prediction_arr):
    pass

#print(get_month_data(2019, 1))

#print(construct_season_avg(2000, "winter")) #OG DATA
#print(calculate_knn_forcast(5, 2019, "summer")) #PRED DATA

