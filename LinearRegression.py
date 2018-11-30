import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Utils as utils

def setup():
    pd.set_option('display.max_rows', 2000)
    plt.rcParams['figure.figsize'] = (10.0, 5.0)

# reading data
da = pd.read_csv('rawdata/heathrowRawData.csv')

season = "summer"

def produce_data(season, yyyy):
    data = utils.construct_season_dataframe(da, season) # use for different seasons
    # data = pd.read_csv('shRawData.csv')
    data.head()

    X = data['yyyy'].values
    Y = data['maxC'].values

    mean_x = np.mean(X)
    mean_y = np.mean(Y)

    m = len(X)

    numer = 0
    denom = 0

    for i in range(m):
        numer += (X[i] - mean_x) * (Y[i]-mean_y)
        denom += (X[i] - mean_x)**2

    b1 = numer/denom
    b0 = mean_y - (b1 * mean_x)  # calculating the coefficients

    max_x = np.max(X)
    min_x = np.min(X)

    x = np.linspace(min_x, max_x, 1000)
    y = b0 + b1 * x

    ss_t = 0
    ss_r = 0

    for i in range(m):
        y_pred = b0 + b1 * X[i]
        ss_t += (Y[i] - mean_y) ** 2
        ss_r += (Y[i] - y_pred) ** 2

    r2 = 1 - (ss_r / ss_t)

    # print(r2*100)

    plt.title("Predicting the transition of seasons: " + season.upper())
    plt.plot(x, y, color='#0000FF', label='regression Line')
    plt.scatter(X, Y, c='#FF0000', label='Scatter Plot')

    plt.xlabel('year')
    plt.ylabel('Temperature (c)')

    new_y = b0 + b1 * yyyy
    print(r2, new_y*r2, season)
    return new_y * r2
# THESE VALUES SHOULD BE BASED ON WHAT THE AVERAGE TEMP WAS FOR EACH SEASON MOST RECENTLY
# Win (Temperature should be between 2 - 7)   (DEC JAN FEB)
# Spr (Temperature should be between 7 - 15)  (MAR APR MAY)
# Sum (Temperature should be between 17 - 30) (JUN JULY AUG)
# Aut (Temperature should be between 15 - 20) (SEP OCT NOV)

def predict_next():
    new_winter = produce_data("winter", 2018)
    new_spring = produce_data("spring", 2018)
    new_summer = produce_data("summer", 2018)
    new_autumn = produce_data("autumn", 2018)

    new_plot_frame=[]

    new_plot = {
        "winter": new_winter,
        "spring": new_spring,
        "summer": new_summer,
        "autumn": new_autumn
    }

    new_plot_frame.append(new_plot)
    new_plot_frame = pd.DataFrame(new_plot_frame)

    #plt.axis([0, 3, 0, 40])
    # the predicted weather
    #plt.plot(['Winter', 'Spring', 'Summer', 'Autumn'], [new_winter, new_spring, new_summer, new_autumn], 'ro')
    #plt.ylabel('Temperature (degrees (c)' )
    #plt.xlabel('Season')

    # Perhaps have this as one model and make another with data from average date from area?

    # Talk about how using the fixed dates of the seasons can tell you how long the seasons are "overstepping"
    print(new_plot)
    print(new_winter, new_spring, new_summer, new_autumn)
    plt.legend()
    plt.show()

setup()
predict_next()