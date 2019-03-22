import wx

from MainWindow import MainWindow

if __name__ == "__main__":
    app = wx.App()
    window = MainWindow(None)
    app.MainLoop()