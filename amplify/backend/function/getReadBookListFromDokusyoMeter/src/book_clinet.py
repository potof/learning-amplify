# coding: UTF-8
import time
import requests
import re
from bs4 import BeautifulSoup

class DokusyoMeter:

    def __init__(self, user, password):
        self.user = user
        self.password = password


    def scrap_readbooks(self):

        url_base = "https://bookmeter.com"
        url_login = "https://bookmeter.com/login"
        login_info = {
            "session[email_address]": self.user,
            "session[password]": self.password,
            "utf8": "✓",
            "session[keep]": "0"
        }

        # authenticity_tokenの取得
        session = requests.session()
        r = session.get(url_login)
        soup = BeautifulSoup(r.text, "lxml")
        auth_token = soup.find(attrs={'name': 'authenticity_token'}).get('value')
        login_info['authenticity_token'] = auth_token

        # login
        res = session.post(url_login, data=login_info)
        res.raise_for_status()

        # 本棚ページへ移動する
        user_id = "117579" # TODO: ID 自動取得（home のプロフィールへのリンクから ID から取得可能）
        booklist_url = url_base + "/users/" + user_id + "/books/read?display_type=list"
        res = session.get(booklist_url)
        res.raise_for_status
        soup = BeautifulSoup(res.text, "lxml")

        # 画面下部のページネーションの最後のリンクを最終ページとして取得する
        lastpage_href = soup.find_all("a", class_="bm-pagination__link")[-1].get("href")
        lastpage = int(re.findall(r".*page=(.*)", lastpage_href)[0])

        # 本棚ページに移動して読んだ本を取得する
        books_list = []
        for current_pagination in range(1, lastpage+1):
            # サーバ負荷を考慮して 5 sec 待機
            time.sleep(5)

            url = booklist_url + "&page=" + str(current_pagination)
            res = session.get(url)
            res.raise_for_status
            soup = BeautifulSoup(res.text, "lxml")

            # 読んだ本の取得
            books_s = soup.select("li.group__book")
            for b in books_s:
                t = b.find("div", class_="detail__title").find("a").string
                d = b.find("div", class_="detail__date").string
                a = b.find("ul", class_="detail__authors").find("a").string
                p = b.find("div", class_="detail__page").string

                l = {
                    "title" : t,
                    "readDate" : d,
                    "author" : a,
                    "page" : p
                }
                books_list.append(l)
        return books_list 



