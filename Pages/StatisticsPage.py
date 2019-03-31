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
        self.setupUi()
        self.draw()

    def draw(self):
        self._sequence = ["n01", "n02", "n03", "n04", "n05", "n06",
                          "n07", "n08", "n09", "n10", "n11", "n12"]
        self._tickLabel = ["%02d" %(x + 1) for x in range(24)]
        self._x = [(x + 1) for x in range(24)]
        statement = session.query(History).statement
        history = pd.read_sql(statement, session.bind)
        allDecks = history[self._sequence]
        counts = winNumCounter(allDecks.values.tolist())
        self._height = [counts[n] for n in self._tickLabel]
        maxY = (int(max(self._height) / 50) + 1) * 50
        self._yLabels = [x for x in range(maxY + 1) if x % 50 == 0]
        self.plot.bar(x=self._x, height=self._height, tick_label=self._tickLabel,
                      align="center", width=0.6)
        self.plot.set_yticks(self._yLabels)
        rects = self.plot.patches
        for rect, h in zip(rects, self._height):
            self.plot.text(rect.get_x() + rect.get_width() / 2, h + 3, h,
                           ha="center", va="bottom", rotation="vertical")

    def setupUi(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.figure = Figure()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.plot = self.figure.add_subplot(111)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
