import wx

from Pages import TodayPage, HistoryPage


class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi()
        self.Show()

    def setupUi(self):
        # Set pages
        self.nb = wx.Notebook(self)
        todayPage = TodayPage(self.nb)
        historyPage = HistoryPage(self.nb)
        self.nb.AddPage(todayPage, "今日對獎")
        self.nb.AddPage(historyPage, "歷史資料")

        # 外觀設置
        self.SetSize((800, 600))
        self.SetTitle("Lotto1224")
        self.Centre()

        todayPage.fetchData()
        todayPage.showResult()