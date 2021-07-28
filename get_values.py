from lxml import html
import requests


class __Money:

    def __init__(self):
        self.__values: {str: float} = {}

        self.__page: requests.Response = requests.get('https://www.iban.com/exchange-rates')
        self.__tree: html.HtmlElement = html.fromstring(self.__page.content)

        for i in range(32):
            name = str(
                self.__tree.xpath(
                    f'/html/body/div[1]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[{i + 1}]/td[1]/text()')[0]
            ).replace("\t", "").replace(" ", "")
            value = float(
               self.__tree.xpath(
                    f"/html/body/div[1]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[{i + 1}]/td[3]/strong/text()")[0]
            )

            self.__values[name] = value

        self.__value_keys = tuple(self.__values.keys())

    def get_names(self) -> (str, str, ...): return self.__value_keys
    def get_values(self) -> {str: float}: return self.__values
    def reload(self) -> None: self.__init__()


Money = __Money()
