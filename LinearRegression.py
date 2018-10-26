import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (20.0, 10.0)

#reading data
d = pd.read_csv('shRawData.csv')

def get_data_from_year(year):
    return d.loc[lambda d: d.get('yyyy') == year, :]

def get_data_from_season(season, year_data):
   seasons = {
       'winter': year_data.loc[lambda year_data: year_data.get('mm').between(1, 3, inclusive=True), :],
       'spring': year_data.loc[lambda year_data: year_data.get('mm').between(4, 6, inclusive=True), :],
       'summer': year_data.loc[lambda year_data: year_data.get('mm').between(7, 9, inclusive=True), :],
       'autumn': year_data.loc[lambda year_data: year_data.get('mm').between(10, 12, inclusive=True), :]
   }

   return seasons.get(season)

def get_average_season_temperature(season_data):
    return season_data["maxC"].mean()

def construct_season_dataframe(season):
    df = []

    for i in range(1855, 2001):
        mC = get_average_season_temperature(get_data_from_season(season, get_data_from_year(str(i))))

        d = {
            "maxC": mC,
            "yyyy": i

        }
        # This gets rid of anomalies that can have an effect on the overall regression line

        average_season_temp = get_average_season_temperature(get_data_from_season(season, get_data_from_year(str(i))))

        if season == "autumn":
            if average_season_temp > 15.5 and average_season_temp < 17.5 :
                df.append(d)

        if season == "summer":
            if average_season_temp > 15:
                df.append(d)

        if season == "autumn":
            if average_season_temp > 7:
                df.append(d)

        if season == "winter":
            if average_season_temp > 1 and average_season_temp < 11: #Removing data that isn't in main cluster
                df.append(d)


    df = pd.DataFrame(df)

    return df

#print(get_data_from_season("winter", get_data_from_year('1975')))
#print(construct_season_dataframe("winter"))

data = construct_season_dataframe("autumn") # use for different seasons
##data = pd.read_csv('shRawData.csv')
data.head()

#changes these back
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
b0 = mean_y - (b1 * mean_x)  #calculating the coefficients

print(b1, b0)

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

#print(r2*100)

plt.title("Predicting the transition of seasons")
line = plt.plot(x, y, color='#00FF00', label='regression Line')
plt.scatter(X, Y, c='#FF0000', label='Scatter Plot')

plt.xlabel('year')
plt.ylabel('Temperature (c)')

new_y = b0 + b1 * 1960 #change back to 2001
print(r2, new_y, new_y + (new_y * r2))

# THESE VALUES SHOULD BE BASED ON WHAT THE AVERAGE TEMP WAS FOR EACH SEASON MOST RECENTLY
# Win (Temperature should be between 2 - 7)   (DEC JAN FEB)
# Spr (Temperature should be between 7 - 15)  (MAR APR MAY)
# Sum (Temperature should be between 17 - 30) (JUN JULY AUG)
# Aut (Temperature should be between 15 - 20) (SEP OCT NOV)

plt.legend()
plt.show()
