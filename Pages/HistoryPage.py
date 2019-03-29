import wx
import wx.grid
import pandas as pd

from Models import History, Session
from Widgets import DeckInput
from utils import analysis


session = Session()

class HistoryPage(wx.Panel):
    def __init__(self, parent):
        super(HistoryPage, self).__init__(parent)
        self.headers = [
            "id", "數字01", "數字02", "數字03", "數字04", "數字05", "數字06",
            "數字07", "數字08", "數字09", "數字10", "數字11", "數字12", "期號",
            "日期", "頭獎注數", "貳獎注數", "參獎注數", "肆獎注數", "銷售總數",
            "單雙", "大小", "對中數量"
        ]
        self.tableCols = len(self.headers)
        self.tableRows = 0
        self.history = pd.DataFrame([], columns=self.headers)
        self.deckInput = DeckInput(self)
        self.deck = self.deckInput.getValue()
        self.sortAscending = False
        self.sortIx = -1
        self._table = -1
        self.setupUi()

    def getHistoyData(self):
        statement = session.query(History).order_by(History.date.desc()).statement
        self.history = pd.read_sql(statement, session.bind)
        self.history["對中數量"] = 0
        self.history.columns = self.headers
        # df.shape: (row, col)
        self.tableRows = self.history.shape[0]

    def analysis(self):
        counts = [
            analysis(
                self.history.iloc[i, 1:13].values.tolist(),
                self.deck
            ) for i in range(self.tableRows)
        ]
        self.history["對中數量"] = counts

    def setValue(self):
        for i, h in enumerate(self.headers):
            self.grid.SetColLabelValue(i, h)

        for i in range(self.tableRows):
            for j in range(self.tableCols):
                val = self.history.iloc[i, j]
                self.grid.SetCellValue(i, j, str(val))
                self.grid.SetReadOnly(i, j)

    def onGo(self, event):
        try:
            self.grid.DeleteRows(numRows=self.tableRows)
        except:
            pass
        self.deck = self.deckInput.getValue()
        self.getHistoyData()
        self.grid.AppendRows(numRows=self.tableRows)
        self.analysis()
        self.setValue()

    def onSort(self, event):
        #event.Col: current column index
        sortBy = self.headers[event.Col]
        self.history = self.history.sort_values(by=[sortBy], ascending=self.sortAscending)
        self.setValue()
        # self.grid.SetSortingColumn(event.Col, self.sortAscending)
        self.sortAscending = not self.sortAscending
        self.sortIx = event.Col

    def setupUi(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.deckInput.go.Bind(wx.EVT_BUTTON, self.onGo)
        self.sizer.Add(self.deckInput, 0, wx.EXPAND)
        self.grid = wx.grid.Grid(self, -1)
        self.grid.CreateGrid(self.tableRows, self.tableCols)
        self.grid.Bind(wx.grid.EVT_GRID_COL_SORT, self.onSort)
        self.sizer.Add(self.grid, 1, wx.EXPAND)
        self.setValue()

        self.SetSizer(self.sizer)
