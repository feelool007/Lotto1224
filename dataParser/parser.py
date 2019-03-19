import requests
from bs4 import BeautifulSoup

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

    def getResult(self, radNo):
        self._payload["Lotto1224Control_history$txtNO"] = radNo
        res = requests.post(url, data=self._payload)
        soup = BeautifulSoup(res.text, "html.parser")
        noResult = soup.find(id="Lotto1224Control_history_Label1").text == "查無資料"
        if noResult:
            print("%s no result" %radNo)
            return False
        result = []
        date = soup.find(id="Lotto1224Control_history_dlQuery_Lotto1224_DDate_0").text
        resultByOrder = soup.find("td", text="開出大小").parent
        for i in range(12):
            number = resultByOrder.find_all(id="Lotto1224Control_history_dlQuery_No%s_0" % (i + 1))[1].text
            result.append(number)
        result.append(radNo)
        result.append(date)
        print("%s parse successfully." %radNo)
        return result
