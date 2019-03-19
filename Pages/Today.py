import wx

from sql.dbHandler import DBHandler
from dataParser.parser import Parser
from utils.analysis import analysis
from Widgets import DeckInput

DECK = [
    "02", "03", "05", "06", "07", "10",
    "12", "15", "16", "17", "20", "23"
]

class Today(wx.Panel):
    def __init__(self, parent):
        super(Today, self).__init__(parent)
        self.deckInput = DeckInput(self)
        self.deck = self.deckInput.input.GetValue().split(",")
        self.fetchData()
        self.setupUi()

    def fetchData(self):
        dbHandler = DBHandler()
        parser = Parser()

        radNo = dbHandler.getRecent()
        if not radNo:
            radNo = 107000001
        else:
            radNo += 1
        noResultCount = 0
        while True:
            result = parser.getResult(radNo)
            if not result:
                noResultCount += 1
                radNo = (int(radNo / 1000000) + 1) * 1000000 + 1 #fetch next year's first
                if noResultCount == 2:
                    # 連2期沒結果，表示目前已經是最新
                    break
                continue
            else:
                noResultCount = 0
            count = analysis(result[:12], self.deck)
            result.append(count)
            dbHandler.insert(result)
            radNo += 1

        self.result = dbHandler.getNewest()

    def onGo(self, event):
        self.deck = self.deckInput.input.GetValue().split(",")
        dbHandler = DBHandler()
        self.result = dbHandler.getNewest()
        radNo = self.result[13]
        date = self.result[14]
        result = self.result[1:13]
        count = analysis(result, self.deck)
        self.radNoText.SetLabel(str(radNo))
        self.dateText.SetLabel(str(date))
        self.resultText.SetLabel(str(result))
        self.countText.SetLabel("中了%s個號碼！！" %count)

    def setupUi(self):
        radNo = self.result[13]
        date = self.result[14]
        result = self.result[1:13]
        count = self.result[15]

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.deckInput.go.Bind(wx.EVT_BUTTON, self.onGo)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.radNoText = wx.StaticText(self, label=str(radNo))
        self.dateText = wx.StaticText(self, label=str(date))
        hbox1.Add(self.radNoText, 0, wx.EXPAND)
        hbox1.Add(self.dateText, 0, wx.EXPAND)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.resultText = wx.StaticText(self, label=str(result))
        hbox2.Add(self.resultText, 0, wx.EXPAND)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.countText = wx.StaticText(self, label="中了%s個號碼！！" %count)
        hbox3.Add(self.countText, 0, wx.EXPAND)

        vbox.Add(self.deckInput, 0, wx.EXPAND)
        vbox.Add(hbox1, 0, wx.EXPAND)
        vbox.Add(hbox2, 0, wx.EXPAND)
        vbox.Add(hbox3, 0, wx.EXPAND)

        self.SetSizer(vbox)
