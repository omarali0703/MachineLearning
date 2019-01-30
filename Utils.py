import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_data_from_year(d, year):
    return d.loc[d['yyyy'] == int(year)]

def get_month_data(d, year, mm):
    return get_data_from_year(d, year).loc[get_data_from_year(d, year)[mm]]

def get_data_from_season(season, year_data):
   seasons = {
       'winter': year_data.loc[year_data['mm'].isin([12, 1, 2])], # Talk about this error in the design on the software (and about grabbing the wrong december var)
       'spring': year_data.loc[year_data['mm'].isin([3, 4, 5])],
       'summer': year_data.loc[year_data['mm'].isin([6, 7, 8])],
       'autumn': year_data.loc[year_data['mm'].isin([9, 10, 11])]

   }
   #print(seasons.get('winter'))

   return seasons.get(season)

def get_average_season_temperature(season_data):
    return (season_data["maxC"].mean() + season_data["minC"].mean())*0.5

def construct_season_dataframe(da, season): # Already calculates the average even though its called max.
    df = []

    for i in range(1949, 2019):#1949 instead of 1948 To make sure that when we grab the winter from the year before.

        mC = get_average_season_temperature(
            get_data_from_season(season, get_data_from_year(da, str(i))))

        d = {
            "maxC": mC,
            "yyyy": i
        }
        # Fill in data using kNN where k = 8

        before3 = get_average_season_temperature(
            get_data_from_season(season, get_data_from_year(da, str(i - 3))))

        before2 = get_average_season_temperature(
            get_data_from_season(season, get_data_from_year(da, str(i - 2))))

        before1 = get_average_season_temperature(
            get_data_from_season(season, get_data_from_year(da, str(i - 1))))

        after1 = get_average_season_temperature(
            get_data_from_season(season, get_data_from_year(da, str(i + 1))))

        after2 = get_average_season_temperature(
            get_data_from_season(season, get_data_from_year(da, str(i + 2))))

        after3 = get_average_season_temperature(
            get_data_from_season(season, get_data_from_year(da, str(i + 3))))

        after4 = get_average_season_temperature(
            get_data_from_season(season, get_data_from_year(da, str(i + 4))))

        fill = {
            "maxC": (before3 + before2 + before1 + mC + after1 + after2 + after3 + after4) / 8,
            "yyyy": i + 0.5
        }
        # This gets rid of anomalies that can have an effect on the overall regression line
        diff = after1 - mC

        #if abs(diff) < 0.2:
        df.append(d)

        if not(np.isnan(fill.get('maxC'))):
            df.append(fill)

    df = pd.DataFrame(df)

    return df
def construct_season_dataframe_no_fill(da, season): # constructs without filled in averages
    df = []

    for i in range(1948, 2019):

        mC = get_average_season_temperature(
            get_data_from_season(season, get_data_from_year(da, str(i))))

        d = { #make sure decembers is from last year.
            "maxC": mC,
            "yyyy": i
        }

        #if abs(diff) < 0.2:
        df.append(d)
    df = pd.DataFrame(df)
    return df

def write_to_file(data):
    f = open("out.txt", "w+")
    f.write(str(data))