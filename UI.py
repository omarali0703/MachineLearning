import wx
import Utils
import knn_new as knn
import matplotlib.pyplot as plt
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

        self.figure = plt.figure()
        self.canvas = FigCanvas(panel, -1, self.figure)

        vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        panel.SetSizer(vbox)

        self.Centre()
        self.Show()
        self.Fit()

    def plot(self, year):
        y = int(year)
        k = 5
        max_year = knn.raw_data.tail(1).iloc[0]['yyyy']
        if (max_year - y) < k // 2:
            knn.k_calc_type = "FORCAST METHOD"

            n_wi = knn.calculate_knn_forcast(k, y, "winter")
            n_sp = knn.calculate_knn_forcast(k, y, "spring")
            n_su = knn.calculate_knn_forcast(k, y, "summer")
            n_au = knn.calculate_knn_forcast(k, y, "autumn")
        else:
            knn.k_calc_type = "POINTCLOUD MID METHOD"

            n_wi = knn.calculate_knn_mid(k, y, "winter")
            n_sp = knn.calculate_knn_mid(k, y, "spring")
            n_su = knn.calculate_knn_mid(k, y, "summer")
            n_au = knn.calculate_knn_mid(k, y, "autumn")

        # using the actual data from the sheet. Nothing is generated, only plotted.
        o_data = [None, None, None, None, None, None, None, None, None, None, None, None]
        if y != (max_year + 1):
            o_wi = knn.construct_season_avg(y, "winter")
            o_sp = knn.construct_season_avg(y, "spring")
            o_su = knn.construct_season_avg(y, "summer")
            o_au = knn.construct_season_avg(y, "autumn")

            o_data = [None, o_wi, None, None, o_sp, None, None, o_su, None, None, o_au, None]

        data = [None, n_wi, None, None, n_sp, None, None, n_su, None, None, n_au, None]

        ax = self.figure.add_subplot(111)
        ax.cla()
        ax.set_ylabel('Temperature (degress(c))')

        ax.set_xlabel('Season')

        predict_patch = patches.Patch(color='red', label='Predicted Value')
        actual_patch = patches.Patch(color='blue', label='Actual Value')
        fade_patch = patches.Patch(color='green', label='Fade in/out Value')

        ax.legend(handles=[predict_patch, actual_patch, fade_patch])
        ax.set_title('Prediction and Reflection for ' + year + '{'+knn.k_calc_type+'}')

        
        #TODO fix prediction for 2019

        ax.set_facecolor((0.7, 0.7, 0.7))
        ax.axis([0, 11, 0, 30])
        ax.plot(['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'], data,'rx')
        ax.plot(['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'], o_data, 'bx')

        plt.plot([1, 1], [4, 4], 'k-', lw=2)
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
