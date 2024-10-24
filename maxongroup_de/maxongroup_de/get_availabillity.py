import requests
from bs4 import BeautifulSoup

cookies = {
    'JSESSIONID': 'Y2-2062f923-6441-466d-8603-ad8e2d7b90c3.node3',
    # 'TS01c7a627': '01245915d7fb980b837dd4223549ea1d2a955f6ef29aa96f0338b074563831dedd3f098bd3c0be989f77c0aa8784ccaf4e211cf91af4408fb491ab2e19c590d013ba8687cb',
    # '_gcl_au': '1.1.901293010.1728657623',
    # '_ga': 'GA1.2.1595138255.1728657624',
    # '_gid': 'GA1.2.1699274773.1728657624',
    # 'hubspotutk': '11228325cf7623f9cb12bf87e47727a8',
    # '__hssrc': '1',
    # '_et_coid': '90733702604c03e769b992d4869c3531',
    # 'isSdEnabled': 'true',
    # '__hstc': '227576258.11228325cf7623f9cb12bf87e47727a8.1728657624227.1728800471033.1728805844742.5',
    # 'RT': '"z=1&dm=maxongroup.de&si=6pg1qki9rvd&ss=m24u44wt&sl=0&tt=0"',
    # 'TS01a5dca8': '01245915d7969581984e1f8fa8762a7361aa63ef01c5a65f16387d371ca3238a8919689678d5f17e5bf849261892fa1757881b36bd',
}

headers = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,ru-RU;q=0.7',
    # 'Cache-Control': 'no-cache',
    # 'Connection': 'keep-alive',
    # 'Cookie': 'JSESSIONID=Y2-2062f923-6441-466d-8603-ad8e2d7b90c3.node3; TS01c7a627=01245915d7fb980b837dd4223549ea1d2a955f6ef29aa96f0338b074563831dedd3f098bd3c0be989f77c0aa8784ccaf4e211cf91af4408fb491ab2e19c590d013ba8687cb; _gcl_au=1.1.901293010.1728657623; _ga=GA1.2.1595138255.1728657624; _gid=GA1.2.1699274773.1728657624; hubspotutk=11228325cf7623f9cb12bf87e47727a8; __hssrc=1; _et_coid=90733702604c03e769b992d4869c3531; isSdEnabled=true; __hstc=227576258.11228325cf7623f9cb12bf87e47727a8.1728657624227.1728800471033.1728805844742.5; RT="z=1&dm=maxongroup.de&si=6pg1qki9rvd&ss=m24u44wt&sl=0&tt=0"; TS01a5dca8=01245915d7969581984e1f8fa8762a7361aa63ef01c5a65f16387d371ca3238a8919689678d5f17e5bf849261892fa1757881b36bd',
    # 'Pragma': 'no-cache',
    # 'Referer': 'https://www.maxongroup.de/maxon/view/content/cart',
    'Sec-Fetch-Dest': 'document',
    # 'Sec-Fetch-Mode': 'navigate',
    # 'Sec-Fetch-Site': 'same-origin',
    # 'Sec-Fetch-User': '?1',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    # 'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Linux"',
}

response = requests.get('https://www.maxongroup.de/maxon/view/content/cart',
                        cookies=cookies,
                        headers=headers
                        )


soup = BeautifulSoup(response.content, "html.parser")
print(soup.select("a.article-delivery-state"))
