import time
import requests
from amazon.api import AmazonAPI
from lxml import etree

from utils import SpidersToolBox
from settings import AMAZON_ACCESS_KEY, AMAZON_ASSOC_TAG, AMAZON_SECRET_KEY


class AmazonApi(SpidersToolBox, AmazonAPI):
    def __init__(self):
        super(AmazonApi, self).__init__()
        self.responsegroup = "Images,ItemAttributes,Offers"
        self.amazon = AmazonAPI(
            AMAZON_ACCESS_KEY,
            AMAZON_SECRET_KEY,
            AMAZON_ASSOC_TAG,
            region="CN",
            ErrorHandler=self.error_handler
        )
        self.sql = """
                    select stcode from crawl.amazon_base_information201907
                    where barcode=%s;
                    """  # and stock is not false and crawl_state != 3

    def error_handler(self, error):
        ex = error['exception']
        if ex.code == 503:
            time.sleep(1)
            return True

    def func1(self, stcode):
        url = "https://www.amazon.cn/dp/{}".format(stcode)
        response = requests.get(url, headers={"User-Agent": self.user_agent})
        # html_data = etree.HTML(response.content.decode())

        with open("sss.html", "w", encoding="utf-8") as f:
            f.write(response.text)

    def func2(self, stcode):
        try:
            products = self.amazon.lookup(
                IdType="ASIN",
                ItemId=stcode,
                ResponseGroup=self.responsegroup
            )
            a, b = products.price_and_currency
        except Exception as e:
            self.logger.debug(e)
        else:
            print(a)
            print(b)

    def main(self, barcode):
        sql = self.sql
        self.conn.execute(sql, (barcode,))
        res = self.conn.fetchone()

        self.func1(res[0])


if __name__ == '__main__':
    ss = AmazonApi()
    ss.main("987987987")

