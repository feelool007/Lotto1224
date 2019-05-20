import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

from Models import Session, History
from utils import winNumCounter


session = Session()

class StatisticsPage(wx.Panel):

    def __init__(self, parent):
        super(StatisticsPage, self).__init__(parent)
        self._init = False
        self.options = ["遞增", "遞減", "無排序"]
        self.setupUi()
        self.getData()
        self.sort()
        self.draw()
        self._init = True

    def getData(self):
        statement = session.query(History).statement
        history = pd.read_sql(statement, session.bind)
        self.rawData = history[["n01", "n02", "n03", "n04", "n05", "n06",
                                "n07", "n08", "n09", "n10", "n11", "n12"]]

    def sort(self):
        mode = self.radios.GetSelection()
        counts = [(k, v) for k, v in winNumCounter(self.rawData.values.tolist()).items()]
        if mode == 0:
            # asc
            sortedCounts = sorted(counts, key=lambda x: x[1], reverse=False)
        elif mode == 1:
            # desc
            sortedCounts = sorted(counts, key=lambda x: x[1], reverse=True)
        else:
            # not sorting
            sortedCounts = sorted(counts, key=lambda x: int(x[0]))
        self.xTicks = [x[0] for x in sortedCounts]
        self.yData = [x[1] for x in sortedCounts]

    def draw(self):
        self.x = [(x + 1) for x in range(24)]
        maxY = (int(max(self.yData) / 50) + 2) * 50
        self.yTicks = [x for x in range(0, maxY + 1, 50)]
        self.plot.bar(x=self.x, height=self.yData, tick_label=self.xTicks,
                      align="center", width=0.6)
        self.plot.set_yticks(self.yTicks)
        self.plot.set_xlabel("Counts")
        self.plot.set_ylabel("Number")
        rects = self.plot.patches
        for rect, h in zip(rects, self.yData):
            self.plot.text(rect.get_x() + rect.get_width() / 2, h + 3, h,
                           ha="center", va="bottom", rotation="vertical")

    def onUpdate(self, e):
        self.sort()
        self.plot.clear()
        self.draw()
        # call canvas.draw() to refresh ui.
        self.canvas.draw()

    def setupUi(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # widgets
        self.radios = wx.RadioBox(self, label="排序", majorDimension=1, choices=self.options,
                                  style=wx.RA_SPECIFY_ROWS)
        self.radios.Bind(wx.EVT_RADIOBOX, self.onUpdate)
        # figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.plot = self.figure.add_subplot(111)

        self.sizer.Add(self.radios, 0, wx.BOTTOM | wx.LEFT | wx.RIGHT, border=15)
        self.sizer.Add(self.canvas, 1, wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=15)

        self.SetSizer(self.sizer)
