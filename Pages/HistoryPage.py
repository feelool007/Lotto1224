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
        self.sortCol = 14
        self.setupUi()

    def getHistoyData(self):
        statement = session.query(History).statement
        self.history = pd.read_sql(statement, session.bind)
        self.history["對中數量"] = 0
        self.history.columns = self.headers
        # df.shape: (row, col)
        self.tableRows = self.history.shape[0]

    def analysis(self):
        # 計算對中數量
        counts = [
            analysis(
                self.history.iloc[i, 1:13].values.tolist(),
                self.deck
            ) for i in range(self.tableRows)
        ]
        self.history["對中數量"] = counts

    def setValue(self):
        # 產生表格
        indicator = "↑" if self.sortAscending else "↓"
        for i, h in enumerate(self.headers):
            if i == self.sortCol:
                self.grid.SetColLabelValue(i, h + "  " + indicator)
            else:
                self.grid.SetColLabelValue(i, h)

        for i in range(self.tableRows):
            for j in range(self.tableCols):
                val = self.history.iloc[i, j]
                self.grid.SetCellValue(i, j, str(val))
                self.grid.SetReadOnly(i, j)

    def onGo(self, event):
        # 查詢歷史資料
        try:
            self.grid.DeleteRows(numRows=self.tableRows)
        except:
            pass
        self.deck = self.deckInput.getValue()
        self.getHistoyData()
        self.grid.AppendRows(numRows=self.tableRows)
        self.analysis()
        self.sortData()
        self.setValue()

    def sortData(self):
        # 排序
        sortBy = self.headers[self.sortCol]
        self.history = self.history.sort_values(by=[sortBy], ascending=self.sortAscending)

    def onSort(self, event):
        # 觸發排序
        #event.Col: sorting column index
        if event.Col == self.sortCol:
            self.sortAscending = not self.sortAscending
        self.sortCol = event.Col
        self.sortData()
        self.setValue()

    def setupUi(self):
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.deckInput.go.Bind(wx.EVT_BUTTON, self.onGo)
        self.sizer.Add(self.deckInput, 0, flag=wx.EXPAND | wx.BOTTOM | wx.LEFT, border=15)
        self.grid = wx.grid.Grid(self, -1)
        self.grid.CreateGrid(self.tableRows, self.tableCols)
        self.grid.Bind(wx.grid.EVT_GRID_COL_SORT, self.onSort)
        self.sizer.Add(self.grid, 1, flag=wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=15)
        self.setValue()

        self.SetSizer(self.sizer)
