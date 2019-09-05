import requests
import json
from lxml import etree


class Spider:
    base_url = "https://asia.ensembl.org/"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "redirect_mirror=no; DYNAMIC_WIDTH=1; _ga=GA1.2.28264787.1564632522; _gid=GA1.2.1496544569.1564632522; ENSEMBL_WWW_SESSION=e67187b2a8195e570ffa0e185d917fe20ca44b7672071c1a24abc10a; ENSEMBL_SEARCH=ensembl_all; toggle_transcripts_table=open; _gat=1; ENSEMBL_WIDTH=1400",
        "Host": "asia.ensembl.org",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
    }

    def request_api(self, data):
        url = "http://127.0.0.1:8000/ssssssss"
        resp = requests.post(url=url, data=data)
        resp_data = resp.json()
        pass

    def main(self, key):
        url = "https://asia.ensembl.org/Multi/Ajax/search?"

        url_end = 'q=(+{}%5E316+AND+species%3A%22CrossSpecies%22+)+OR+(+{}%5E190+AND+species%3A%22Human%22+)+OR+(+{}%5E80+AND+species%3A%22Mouse%22+)+OR+(+{}+AND+species%3A%22Zebrafish%22+)&fq=(++(++species%3A%22CrossSpecies%22+AND+(+reference_strain%3A1+)++)++OR++(++species%3A%22Human%22+AND+(+reference_strain%3A1+)++)++OR++(++species%3A%22Mouse%22+AND+(+reference_strain%3A1+)++)++OR++(++species%3A%22Zebrafish%22+AND+(+reference_strain%3A1+)++)++)&hl=true&hl.fl=_hr&hl.fl=content&hl.fl=description&hl.fragsize=500&rows=10&start=0'

        url += url_end.format(key, key, key,key)

        resp = requests.get(url, headers=self.headers)

        # with open("preview.html", 'w') as f:
        #     f.write(resp.text)

        res_data = json.loads(resp.text)

        # print(res_data)

        # homo_sapiens/Gene/Summary?g=ENSG00000197299&db=core
        detail_end = res_data["result"]["response"]["docs"][0]["domain_url"]

        detail_url = self.base_url + detail_end  # +";r=15:90717346-90816166"

        resp_2 = requests.get(url=detail_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"})
        # with open("preview.html", 'w') as f:
        #     f.write(resp_2.text)

        html_data = etree.HTML(resp_2.text)

        # get body
        _headers = []
        headers = html_data.xpath('//*[@id="transcripts_table"]/thead/tr/th')
        for i in headers:
            _headers.append(i.xpath("text()")[0])

        # get body
        data = []
        bodys = html_data.xpath('//*[@id="transcripts_table"]/tbody/tr')
        for tr in bodys:
            _data = {}
            tds = tr.xpath('td')
            name = tds[0].xpath(".//text()")[0]
            tid = tds[1].xpath(".//text()")[0]
            bp = tds[2].xpath(".//text()")[0]
            protein = tds[3].xpath(".//text()")[0]
            tid2 = tds[4].xpath(".//text()")[0]
            biotype = tds[5].xpath('.//div[@class="coltab-text"]/text()') or tds[5].xpath('.//div[@class="coltab-text"]/span/text()')
            biotype = biotype[0]
            ccds = tds[6].xpath('.//text()')[0]
            uniprot = tds[7].xpath('..//text()')[0]
            rm = tds[8].xpath('.//text()')[0]
            flags = tds[9].xpath('span/span/text()')
            _data[_headers[0]] = name
            _data[_headers[1]] = tid
            _data[_headers[2]] = bp
            _data[_headers[3]] = protein
            _data[_headers[4]] = tid2
            _data[_headers[5]] = biotype
            _data[_headers[6]] = ccds
            _data[_headers[7]] = uniprot
            _data[_headers[8]] = rm
            _data[_headers[9]] = flags

            data.append(_data)
            print(_data)

        # save in db
        self.request_api(data)


if __name__ == '__main__':
    s = Spider()
    s.main("BLM")

