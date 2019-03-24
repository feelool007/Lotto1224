import wx

from sql import DBHandler
from dataParser import Parser
from utils import analysis, oddAndEven, smallAndLarge
from Widgets import DeckInput

class Today(wx.Panel):
    def __init__(self, parent):
        super(Today, self).__init__(parent)
        self.deckInput = DeckInput(self)
        self.deck = self.deckInput.input.GetValue().split(",")
        self.setupUi()

    def getNewest(self):
        dbHandler = DBHandler()
        self.result = dbHandler.getNewest()

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
            oddEven = oddAndEven(result[:12])
            smallLarge = smallAndLarge(result[:12])
            result.append(oddEven)
            result.append(smallLarge)
            dbHandler.insert(result)
            radNo += 1

    def showResult(self):
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
        self.oddEvenText.SetLabel(oddAndEven(result))
        self.smallLargeText.SetLabel(smallAndLarge(result))
        self.countText.SetLabel("中了%s個號碼！！" % count)

    def onGo(self, event):
        self.showResult()

    def setupUi(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.deckInput.go.Bind(wx.EVT_BUTTON, self.onGo)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.radNoText = wx.StaticText(self, label="")
        self.radNoText.SetMinSize((85, -1))
        self.dateText = wx.StaticText(self, label="")
        self.dateText.SetMinSize((85, -1))
        hbox1.Add(self.radNoText, 0, flag=wx.EXPAND | wx.RIGHT, border=10)
        hbox1.Add(self.dateText, 0, wx.EXPAND)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.resultText = wx.StaticText(self, label="")
        hbox2.Add(self.resultText, 0, wx.EXPAND)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.oddEvenText = wx.StaticText(self, label="")
        self.oddEvenText.SetMinSize((85, -1))
        self.smallLargeText = wx.StaticText(self, label="")
        self.smallLargeText.SetMinSize((85, -1))
        hbox3.Add(self.oddEvenText, 0, flag=wx.EXPAND | wx.RIGHT, border=10)
        hbox3.Add(self.smallLargeText, 0, flag=wx.EXPAND)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.countText = wx.StaticText(self, label="")
        hbox4.Add(self.countText, 0, wx.EXPAND)

        vbox.Add(self.deckInput, 0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=15)
        vbox.Add(hbox1, 0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=15)
        vbox.Add(hbox2, 0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=15)
        vbox.Add(hbox3, 0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=15)
        vbox.Add(hbox4, 0, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=15)

        self.SetSizer(vbox)
