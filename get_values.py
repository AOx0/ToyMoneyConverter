from lxml import html
import requests


class __Money:

    def __init__(self):
        self.values: {str: float} = {}

        self.page: requests.Response = requests.get('https://www.iban.com/exchange-rates')
        self.tree: html.HtmlElement = html.fromstring(self.page.content)

        for i in range(32):
            name = str(
                self.tree.xpath(
                    f'/html/body/div[1]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[{i + 1}]/td[1]/text()')[0]
            ).replace("\t", "").replace(" ", "")
            value = float(
               self.tree.xpath(
                    f"/html/body/div[1]/div[2]/div/div[2]/div[1]/div/table/tbody/tr[{i + 1}]/td[3]/strong/text()")[0]
            )

            self.values[name] = value

        self.value_keys = tuple(self.values.keys())

    def get_names(self) -> (str, str, ...): return self.value_keys
    def get_values(self) -> {str: float}: return self.values
    def reload(self) -> None: self.__init__()


Money = __Money()
