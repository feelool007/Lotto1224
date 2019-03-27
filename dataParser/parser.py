import requests
from bs4 import BeautifulSoup
from typing import Union

from Models import History
from utils import parseInt


url = "http://www.taiwanlottery.com.tw/lotto/Lotto1224/history.aspx"

class Parser(object):
    def __init__(self):
        self._payload = {
            "Lotto1224Control_history$DropDownList1": 12,
            "Lotto1224Control_history$chk": "radNO",
            "Lotto1224Control_history$btnSubmit": "查詢"
        }
        self._getViewState()

    def _getViewState(self):
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        __VIEWSTATE = soup.find(id="__VIEWSTATE")["value"]
        __VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")["value"]
        __EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")["value"]
        self._payload["__VIEWSTATE"] = __VIEWSTATE
        self._payload["__VIEWSTATEGENERATOR"] = __VIEWSTATEGENERATOR
        self._payload["__EVENTVALIDATION"] = __EVENTVALIDATION

    def getResult(self, radNo) -> Union[History,bool]:
        result = History()

        self._payload["Lotto1224Control_history$txtNO"] = radNo
        res = requests.post(url, data=self._payload)
        soup = BeautifulSoup(res.text, "html.parser")
        noResult = soup.find(id="Lotto1224Control_history_Label1").text == "查無資料"
        if noResult:
            print("%s no result" %radNo)
            return False

        date = soup.find(id="Lotto1224Control_history_dlQuery_Lotto1224_DDate_0").text
        resultByOrder = soup.find("td", text="開出大小").parent
        result.n01 = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No1_0")[1].text
        result.n02 = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No2_0")[1].text
        result.n03 = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No3_0")[1].text
        result.n04 = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No4_0")[1].text
        result.n05 = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No5_0")[1].text
        result.n06 = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No6_0")[1].text
        result.n07 = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No7_0")[1].text
        result.n08 = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No8_0")[1].text
        result.n09 = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No9_0")[1].text
        result.n10 = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No10_0")[1].text
        result.n11 = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No11_0")[1].text
        result.n12 = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No12_0")[1].text
        result.firstPrize = parseInt(soup.find(id="Lotto1224Control_history_dlQuery_Lotto1224_CategA2_0").text)
        result.secondPrize = parseInt(soup.find(id="Lotto1224Control_history_dlQuery_Lotto1224_CategB2_0").text)
        result.thirdPrize = parseInt(soup.find(id="Lotto1224Control_history_dlQuery_Lotto1224_CategC2_0").text)
        result.forthPrize = parseInt(soup.find(id="Lotto1224Control_history_dlQuery_Lotto1224_CategD2_0").text)
        # 銷售總量：銷售總金額 / 50
        result.totalAmount = parseInt(soup.find(id="Lotto1224Control_history_dlQuery_Lotto1224_TotalAmount_0").text) / 50
        result.radno = radNo
        result.date = date
        print("%s parse successfully." %radNo)

        return result
