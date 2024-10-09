import requests
from bs4 import BeautifulSoup
import pandas

sitemaps = ['https://air-com.pl/pl_productvariants_sitemap.xml',
            'https://air-com.pl/pl_productvariants10_sitemap.xml',
            'https://air-com.pl/pl_productvariants11_sitemap.xml',
            'https://air-com.pl/pl_productvariants12_sitemap.xml',
            'https://air-com.pl/pl_productvariants13_sitemap.xml',
            'https://air-com.pl/pl_productvariants14_sitemap.xml',
            'https://air-com.pl/pl_productvariants15_sitemap.xml',
            'https://air-com.pl/pl_productvariants16_sitemap.xml',
            'https://air-com.pl/pl_productvariants17_sitemap.xml',
            'https://air-com.pl/pl_productvariants18_sitemap.xml',
            'https://air-com.pl/pl_productvariants19_sitemap.xml',
            'https://air-com.pl/pl_productvariants2_sitemap.xml',
            'https://air-com.pl/pl_productvariants20_sitemap.xml',
            'https://air-com.pl/pl_productvariants21_sitemap.xml',
            'https://air-com.pl/pl_productvariants22_sitemap.xml',
            'https://air-com.pl/pl_productvariants23_sitemap.xml',
            'https://air-com.pl/pl_productvariants24_sitemap.xml',
            'https://air-com.pl/pl_productvariants25_sitemap.xml',
            'https://air-com.pl/pl_productvariants26_sitemap.xml',
            'https://air-com.pl/pl_productvariants27_sitemap.xml',
            'https://air-com.pl/pl_productvariants28_sitemap.xml',
            'https://air-com.pl/pl_productvariants29_sitemap.xml',
            'https://air-com.pl/pl_productvariants3_sitemap.xml',
            'https://air-com.pl/pl_productvariants30_sitemap.xml',
            'https://air-com.pl/pl_productvariants31_sitemap.xml',
            'https://air-com.pl/pl_productvariants32_sitemap.xml',
            'https://air-com.pl/pl_productvariants33_sitemap.xml',
            'https://air-com.pl/pl_productvariants34_sitemap.xml',
            'https://air-com.pl/pl_productvariants35_sitemap.xml',
            'https://air-com.pl/pl_productvariants36_sitemap.xml',
            'https://air-com.pl/pl_productvariants37_sitemap.xml',
            'https://air-com.pl/pl_productvariants38_sitemap.xml',
            'https://air-com.pl/pl_productvariants39_sitemap.xml',
            'https://air-com.pl/pl_productvariants4_sitemap.xml',
            'https://air-com.pl/pl_productvariants40_sitemap.xml',
            'https://air-com.pl/pl_productvariants41_sitemap.xml',
            'https://air-com.pl/pl_productvariants5_sitemap.xml',
            'https://air-com.pl/pl_productvariants6_sitemap.xml',
            'https://air-com.pl/pl_productvariants7_sitemap.xml',
            'https://air-com.pl/pl_productvariants8_sitemap.xml',
            'https://air-com.pl/pl_productvariants9_sitemap.xml',
            'https://air-com.pl/pl_products_sitemap.xml',
            'https://air-com.pl/pl_categories_sitemap.xml',
            'https://air-com.pl/pl_pages_sitemap.xml',
            'https://air-com.pl/pl_news_sitemap.xml']


def get_request(url):
    response = requests.get(url,
                            headers={
                                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
                                "cache-control": "no-cache",
                                "pragma": "no-cache",
                                "priority": "u=0, i",
                                "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
                                "sec-ch-ua-arch": "\"x86\"",
                                "sec-ch-ua-bitness": "\"64\"",
                                "sec-ch-ua-full-version": "\"127.0.6533.119\"",
                                "sec-ch-ua-full-version-list": "\"Not)A;Brand\";v=\"99.0.0.0\", \"Google Chrome\";v=\"127.0.6533.119\", \"Chromium\";v=\"127.0.6533.119\"",
                                "sec-ch-ua-mobile": "?0",
                                "sec-ch-ua-model": "\"\"",
                                "sec-ch-ua-platform": "\"Linux\"",
                                "sec-ch-ua-platform-version": "\"6.8.0\"",
                                "sec-fetch-dest": "document",
                                "sec-fetch-mode": "navigate",
                                "sec-fetch-site": "none",
                                "sec-fetch-user": "?1",
                                "upgrade-insecure-requests": "1",
                                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
                            },
                            cookies={
                                "CookieConsent": "{stamp:%27JQIkf7UP0B6BxdKr5zyQHPDoqajqAk/F7WwM15BuygszRISPfhUspw==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1728022679455%2Cregion:%27ru%27}",
                                "XSRF-TOKEN": "YpZK08voMSwobB7zqNs9wsFHRXj9yJn7RNYby9XG",
                                "_clck": "11ep28v%7C2%7Cfpq%7C0%7C1738",
                                "_clsk": "su5jvg%7C1728026486184%7C42%7C1%7Cp.clarity.ms%2Fcollect",
                                "_ga": "GA1.2.1238113704.1728022599",
                                "_gat_UA-35078555-1": "1",
                                "_gcl_au": "1.1.419109824.1728022679",
                                "_gid": "GA1.2.1367082428.1728022679",
                                "_uetsid": "6760e650821811efa0fe5fbb5a3f7dc5",
                                "_uetvid": "67611cc0821811efad50fd88763518c3",
                                "cf_clearance": "S9mOlgSAhcnKoxAKxoCXN9zaMjSdvT77AYe5HSUOXrI-1728026435-1.2.1.1-onEA3waFxvTgPkWdoGSsRWXYeYCfuu_EOfTYIZ7LTQL8LthWqaWbE8yklSM_KpoFGdut.Uni45LQnqDORzMtWlshb6CP86QFKBWga7_U_Dj_uOgqOLXuyjpzoHugs.n2kUHTxKtKI1nsB3WkqfhEPWHgk8JkgEi6cEHAP2MdEKWMVvABsoBXgJ_UuBWAi2SlcFzEU5dfgh.Hxclo5q4gVqRWMN5NneWHqOPWAsDVhnLi9MUyUMa_WlIiJrkPBNVJaUkoBM7sUw6jXM4E9orA71r5Th6GLVCffgeD5UhfwQc1PfBH3ibbmSmvNcVvYKkcPt6bdtgMQCPk7L8A9dTqqerr0oL.ALUalxnepOp6LqC2_31e3n.A83RUWlNCr42NQRYgq7TNy_MJffmKpoMvshoJk4wj_As2M7tYFKjsO0M",
                                "user_session": "eyJpdiI6ImNuTnRvcFA0MndtRnFHelFUUlVQeEE9PSIsInZhbHVlIjoiSng4UnBHczJiN2VON3JyNHVvSGN5NFIvcnhDQnpSeWJ2YSs4SDRzMnAzUVQvUlV0WVhmSGxZVkZpRUJTSHc4Z250YUFNdE5qMjk3THpZTFJ6aUF4OXZOdUNIVXJua0RoZUR6ZU00OVY2RytwSDhWT2ZZVGtnQ0x6M2VRaHNkSlIiLCJtYWMiOiIxMWRmY2Q0YmFiYWYxYTlhOGIwM2YzNDEyZDUzMWI2YzcyYmEzMmE5M2ZjNGZhOTAzYTExMGFmMjQ4MDIzYWQxIiwidGFnIjoiIn0%3D"
                            },
                            auth=(),
                            )
    return response


all_variants_link = set()

if __name__ == '__main__':
    for i in range(1, 13):
        resp = get_request(f"https://air-com.pl/k/,producent:camozzi,/{i}")
        print(resp.status_code)
        soup = BeautifulSoup(resp.content, "html.parser")
        variants_links = soup.select(".list-element-box-btns a.button")
        variants = [a["href"] for a in variants_links]
        print(len(variants))
        print(variants)
        all_variants_link.update(variants)

pandas.DataFrame(all_variants_link).to_csv(
    "/home/sana451/PycharmProjects/scrapy_parsers/air_com_pl/air_com_pl/results/variants.links.csv", index=False)
