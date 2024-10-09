import requests


def get_price_by_sku(sku: str):
    response = requests.get(f"https://www.schmalz.com/de-de/product-permissions?sku={sku}",
                            headers={
                                "accept": "application/json, text/javascript, */*; q=0.01",
                                "accept-language": "en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7",
                                "cache-control": "no-cache",
                                "pragma": "no-cache",
                                "priority": "u=0, i",
                                "referer": "https://www.schmalz.com/de-de/vakuumtechnik-fuer-die-automation/vakuum-komponenten/vakuum-sauggreifer/zubehoer-vakuum-sauggreifer/saugereinsaetze-spi-fuer-spb2-305924/10.01.06.04044/",
                                "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
                                "sec-ch-ua-mobile": "?0",
                                "sec-ch-ua-platform": "\"Linux\"",
                                "sec-fetch-dest": "empty",
                                "sec-fetch-mode": "cors",
                                "sec-fetch-site": "same-origin",
                                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                                "x-requested-with": "XMLHttpRequest"
                            },
                            cookies={
                                "AWSALB": "tGO2iDj7rHTQXEp8pk1CdI1peuzrejGbFzhuCQmIRusodD5A8XIvqAReYn6+GBjS80VR1fVIC0nTJqqH5ZQegtNEaO8NqKGEoF4fcnTpDFI1wMtFiVVf9Ac6kTeq",
                                "AWSALBCORS": "tGO2iDj7rHTQXEp8pk1CdI1peuzrejGbFzhuCQmIRusodD5A8XIvqAReYn6+GBjS80VR1fVIC0nTJqqH5ZQegtNEaO8NqKGEoF4fcnTpDFI1wMtFiVVf9Ac6kTeq",
                                "AWSELB": "E97BF37114DC14F0AEB705612B29CF3F419B2BFF25D43631D3B1C9B9BD85111F0FFB83163FB61F484404597DA1F3B411DD66ED14092FF07038EF70EBF5D28FC4CA384C8708CDE678430BEA35DE1C27FD5E5336BEA8",
                                "JSESSIONID": "E83AD63007860BF02A4BE35177B66038",
                                "OAuth_Token_Request_State": "61c68f02-e0be-4044-9491-2ea88ec21546",
                                "_clck": "11aqexd%7C2%7Cfpn%7C0%7C1735",
                                "_clsk": "hxrfnn%7C1727770774284%7C10%7C1%7Cp.clarity.ms%2Fcollect",
                                "_uetsid": "c01184a07fc711ef9bb09714495b5495",
                                "_uetvid": "c0119ae07fc711ef9ae6652693cba2ca",
                                "channelKeyCookie": "web-DE",
                                "cmsSiteIdCookie": "de-de",
                                "cmsSiteIdCookieOrigin": "Deutschland",
                                "countrySelector": "DE",
                                "localeCookie": "de",
                                "loggedIn": "true"
                            },
                            auth=(),
                            )
    return response.json()["price"].replace("€", "")


print(
    get_price_by_sku("10.01.06.04044")
)
