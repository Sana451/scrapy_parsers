import requests


def post_article_for_url(article):
    response = requests.post("https://www.comitronic-bti.de/de/recherche",
                             data=f'front_recherche%5B_rech%5D={article}&front_recherche%5B_token%5D=a73044fa926c4aa0a8f48e.dTQZsau6itXr3OuATj78HXnSslDAKNDJ74TzDXDHg38.H35og8Lfp6OFt7_LeE2UUDHrgzSmHISZquOSWhuRzTctAnHY5v3QhdyXgA',
                             headers={
                                 "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                                 "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
                                 "cache-control": "no-cache",
                                 "content-type": "application/x-www-form-urlencoded",
                                 "origin": "https://www.comitronic-bti.de",
                                 "pragma": "no-cache",
                                 "priority": "u=0, i",
                                 "referer": "https://www.comitronic-bti.de/de/recherche",
                                 "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
                                 "sec-ch-ua-mobile": "?0",
                                 "sec-ch-ua-platform": "\"Linux\"",
                                 "sec-fetch-dest": "document",
                                 "sec-fetch-mode": "navigate",
                                 "sec-fetch-site": "same-origin",
                                 "sec-fetch-user": "?1",
                                 "upgrade-insecure-requests": "1",
                                 "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
                             },
                             cookies={
                                 "PHPSESSID": "33n2ju4uioogtdmr590bgs4mr5",
                                 "TawkConnectionTime": "0",
                                 "panier_session_id": "4eba472e1be28a93c440d69fee298a7c",
                                 "tarteaucitron": "!gtag=true!googletagmanager=true!tawkto=true",
                                 "twk_idm_key": "GNR-E1yoqCLgbD_ur3sx1",
                                 "twk_uuid_58b5745b97fbd80a94f1367e": "%7B%22uuid%22%3A%221.92P6lVYFyy1vcsKO4l9PDK2OWEpHcXWlOT7zyyGbt8Yqqb0EbqqisRPHwA8LkhXBoBTA5WWsZCyiiDNtkQsiVr8ONggljxlWBpeiOCTp5FBZnJ7YMsAZbPOqpFZ9%22%2C%22version%22%3A3%2C%22domain%22%3A%22comitronic-bti.de%22%2C%22ts%22%3A1727867085663%7D"
                             },
                             auth=(),
                             )
    return response.content


res = post_article_for_url("7SSR24V")
print(res)
f = open("1.html", "w")
f.write(str(res))
f.close()
