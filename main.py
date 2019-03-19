import pandas as pd
import wx

from MainWindow.MainWindow import MainWindow

from sql.dbHandler import DBHandler
from dataParser.parser import Parser
from utils.analysis import analysis

DECK = [
    "02", "03", "05", "06", "07", "10",
    "12", "15", "16", "17", "20", "23"
]

if __name__ == "__main__":
    app = wx.App()
    window = MainWindow(None)
    app.MainLoop()