import wx

DECK = [
    "02", "03", "05", "06", "07", "10",
    "12", "15", "16", "17", "20", "23"
]

class DeckInput(wx.Panel):
    def __init__(self, parent):
        super(DeckInput, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.input = wx.TextCtrl(self)
        self.input.SetValue(",".join(DECK))
        self.go = wx.Button(self, wx.ID_EXECUTE, "對獎")

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(self.input, 4, wx.EXPAND)
        self.hbox.Add(self.go, 0, wx.EXPAND)

        self.SetSizer(self.hbox)