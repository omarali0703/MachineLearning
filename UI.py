import wx
import Utils
import kNN as knn
import matplotlib.patches as patches

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas

class win(wx.Frame) :
    def __init__(self, parent, title):

        super(win, self).__init__(parent, title=title, size=(1200, 600))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.btn = wx.Button(panel, 1, "Forcast")
        vbox.Add(self.btn, 0, wx.ALIGN_LEFT)
        self.btn.Bind(wx.EVT_BUTTON, self.OnClicked)

        self.figure = knn.plt.figure()
        self.canvas = FigCanvas(panel, -1, self.figure)

        vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        panel.SetSizer(vbox)

        self.Centre()
        self.Show()
        self.Fit()

    def plot(self, year):
        y = int(year)

        n_wi = knn.knn.calculate_data_from_date(knn, 5, knn.da, "winter", y)
        n_sp = knn.knn.calculate_data_from_date(knn, 5, knn.da, "spring", y)
        n_su = knn.knn.calculate_data_from_date(knn, 5, knn.da, "summer", y)
        n_au = knn.knn.calculate_data_from_date(knn, 5, knn.da, "autumn", y)

        # using the actual data from the sheet. Nothing is generated, only plotted.
        o_wi = Utils.construct_season_dataframe_no_fill(knn.da, "winter")
        o_sp = Utils.construct_season_dataframe_no_fill(knn.da, "spring")
        o_su = Utils.construct_season_dataframe_no_fill(knn.da, "summer")
        o_au = Utils.construct_season_dataframe_no_fill(knn.da, "autumn")

        oldwi = o_wi.loc[o_wi['yyyy'] == int(year)]['maxC']
        oldsp = o_sp.loc[o_sp['yyyy'] == int(year)]['maxC']
        oldsu = o_su.loc[o_su['yyyy'] == int(year)]['maxC']
        oldau = o_au.loc[o_au['yyyy'] == int(year)]['maxC']

        data = [None, n_wi, None, None, n_sp, None, None, n_su, None, None, n_au, None]
        o_data = [None, oldwi, None, None, oldsp, None, None, oldsu, None, None, oldau, None]

        ax = self.figure.add_subplot(111)
        ax.cla()
        ax.set_ylabel('Temperature (degress(c))')

        ax.set_xlabel('Season')

        predict_patch = patches.Patch(color='red', label='Predicted Value')
        actual_patch = patches.Patch(color='blue', label='Actual Value')
        fade_patch = patches.Patch(color='green', label='Fade in/out Value')

        ax.legend(handles=[predict_patch, actual_patch, fade_patch])
        ax.set_title('Prediction and Reflection for ' + year)

        
        #TODO fix prediction for 2019

        ax.set_facecolor((0.7, 0.7, 0.7))
        ax.axis([0, 11, 0, 30])
        ax.plot(['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'], data,'rx')
        ax.plot(['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'], o_data, 'bx')

        fade_wi = knn.knn.calculate_fade_points(knn, 5, knn.da, "winter", int(year))
        fade_sp = knn.knn.calculate_fade_points(knn, 5, knn.da, "spring", int(year))
        fade_su = knn.knn.calculate_fade_points(knn, 5, knn.da, "summer", int(year))
        fade_au = knn.knn.calculate_fade_points(knn, 5, knn.da, "autumn", int(year))

        for i in range(3):
            ax.plot(fade_sp.iloc[i]['mm'], fade_sp.iloc[i]['temp'], 'gx')
            ax.plot(fade_su.iloc[i]['mm'], fade_su.iloc[i]['temp'], 'gx')
            ax.plot(fade_au.iloc[i]['mm'], fade_au.iloc[i]['temp'], 'gx')
        # Exemption for winter
        ax.plot(0, fade_wi.iloc[0]['temp'], 'gx')
        ax.plot(1, fade_wi.iloc[1]['temp'], 'gx')
        ax.plot(2, fade_wi.iloc[2]['temp'], 'gx')

        self.canvas.draw()

    def OnClicked(self, event):
        check_date = wx.TextEntryDialog(None, 'enter date')
        check_date.ShowModal()
        date = check_date.GetValue()

        btn = event.GetEventObject().GetLabel()
        self.plot(date)
        

app = wx.App()
win(None, 'Predicting Seasonal Transitions')
app.MainLoop()
