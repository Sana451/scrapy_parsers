import pandas
import requests
from bs4 import BeautifulSoup

DOMAIN = "https://www.balluff.com"

# resp = requests.get("https://www.balluff.com/de-de/produkte")
# soup = BeautifulSoup(resp.content, "html.parser")
# cats = [a["href"] for a in soup.select("")]

cats = [
    "https://www.balluff.com/de-de/products/areas/A0001",
    "https://www.balluff.com/de-de/products/areas/A0003",
    "https://www.balluff.com/de-de/products/areas/A0005",
    "https://www.balluff.com/de-de/products/areas/A0007",
    "https://www.balluff.com/de-de/products/areas/A0009",
    "https://www.balluff.com/de-de/products/areas/A0017",
    "https://www.balluff.com/de-de/products/areas/A0018",
    "https://www.balluff.com/de-de/products/areas/A0019",
]

sub_cat_links = [
    'https://www.balluff.com/de-de/products/areas/A0011',
    'https://www.balluff.com/de-de/products/areas/A0013',
    'https://www.balluff.com/de-de/products/areas/A0015'
]

# for cat in cats:
#     resp = requests.get(cat)
#     soup = BeautifulSoup(resp.content, "html.parser")
#     links = [DOMAIN + a["href"] for a in soup.select("ul.mt-6 a")]
#     print(len(links))
#     sub_cat_links.extend(links)
#
# print(sub_cat_links)
# print(len(sub_cat_links))

sub_cat_links = [
    'https://www.balluff.com/de-de/products/areas/A0011',
    'https://www.balluff.com/de-de/products/areas/A0013',
    'https://www.balluff.com/de-de/products/areas/A0015',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0101',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0102',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0105',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0113',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0104',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0107',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0116',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0109',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0110',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0114',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0117',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0119',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0120',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0121',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0305',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0304',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0301',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0302',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0307',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0306',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0504',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0501',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0502',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0503',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0508',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0507',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0505',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0506',
    'https://www.balluff.com/de-de/products/areas/A0007/groups/G0701',
    'https://www.balluff.com/de-de/products/areas/A0007/groups/G0703',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0906',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0901',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0902',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0903',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0905',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1706',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1704',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1705',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1707',
    'https://www.balluff.com/de-de/products/areas/A0018/groups/G1802',
    'https://www.balluff.com/de-de/products/areas/A0018/groups/G1801',
    'https://www.balluff.com/de-de/products/areas/A0019/groups/G1902',
    'https://www.balluff.com/de-de/products/areas/A0019/groups/G1901'
]

# all_group_links = []
#
# for sub_c_link in sub_cat_links:
#     resp = requests.get(sub_c_link)
#     soup = BeautifulSoup(resp.content, "html.parser")
#     group_links = [DOMAIN + a["href"] for a in soup.select("a:has(> button)")]
#     print(len(group_links))
#     all_group_links.extend(group_links)
#
# print(all_group_links)
# print(len(all_group_links))

all_group_links = [
    'https://www.balluff.com/de-de/products/areas/A0011/products/G1102',
    'https://www.balluff.com/de-de/products/areas/A0011/products/G1103',
    'https://www.balluff.com/de-de/products/areas/A0011/products/G1101',
    'https://www.balluff.com/de-de/products/areas/A0011/products/G1111',
    'https://www.balluff.com/de-de/products/areas/A0011/products/G1110',
    'https://www.balluff.com/de-de/products/areas/A0011/products/G1105',
    'https://www.balluff.com/de-de/products/areas/A0011/products/G1109',
    'https://www.balluff.com/de-de/products/areas/A0011/products/G1104',
    'https://www.balluff.com/de-de/products/areas/A0011/products/G1108',
    'https://www.balluff.com/de-de/products/areas/A0011/products/G1107',
    'https://www.balluff.com/de-de/products/areas/A0011/products/G1106',
    'https://www.balluff.com/de-de/products/areas/A0013/products/G1301',
    'https://www.balluff.com/de-de/products/areas/A0013/products/G1305',
    'https://www.balluff.com/de-de/products/areas/A0013/products/G1306',
    'https://www.balluff.com/de-de/products/areas/A0015/products/G1503',
    'https://www.balluff.com/de-de/products/areas/A0015/products/G1504',
    'https://www.balluff.com/de-de/products/areas/A0015/products/G1501',
    'https://www.balluff.com/de-de/products/areas/A0015/products/G1505',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0101/products/F01102',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0101/products/F01113',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0101/products/F01115',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0101/products/F01110',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0101/products/F01118',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0102/products/F01202',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0102/products/F01204',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0102/products/F01201',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0102/products/F01210',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0102/products/F01207',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01319',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01318',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01327',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01325',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01317',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01321',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01326',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01324',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01322',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01314',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01316',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01323',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0103/products/F01328',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0105/products/F01502',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0105/products/F01521',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0105/products/F01507',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0105/products/F01520',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0105/products/F01508',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0113/products/F01301',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0113/products/F01302',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0113/products/F01311',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0113/products/F01305',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0113/products/F01306',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0113/products/F01307',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0113/products/F01308',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0113/products/F01332',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0113/products/F01309',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0113/products/F01303',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0113/products/F01304',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0104/products/F01405',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0104/products/F01401',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0104/products/F01408',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0107/products/F01707',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0107/products/F01709',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0107/products/F01708',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0107/products/F01710',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0107/products/F01701',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0116/products/F01809',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0116/products/F01812',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0116/products/F01811',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0116/products/F01807',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0116/products/F01813',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0116/products/F01810',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0116/products/F01814',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0109/products/F01901',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0110/products/F01007',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0110/products/F01006',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0110/products/F00108',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0114/products/F01407',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0117/products/F11701',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0119/products/F011901',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0120/products/F012001',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0121/products/F012102',
    'https://www.balluff.com/de-de/products/areas/A0001/groups/G0121/products/F012101',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0305/products/F03501',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0305/products/F03506',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0305/products/F03502',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0305/products/F030506',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0304/products/F03401',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0304/products/F03406',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0304/products/F03402',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0304/products/F03405',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0301/products/F03101',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0301/products/F03106',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0301/products/F03107',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0301/products/F03102',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0302/products/F03201',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0302/products/F03206',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0302/products/F03202',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0302/products/F03205',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0302/products/F03207',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0307/products/F03701',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0306/products/F03601',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0306/products/F03603',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0306/products/F03604',
    'https://www.balluff.com/de-de/products/areas/A0003/groups/G0306/products/F03605',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0504/products/F05401',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0504/products/F05406',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0504/products/F05404',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0504/products/F05405',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0504/products/F05403',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0504/products/F05402',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0504/products/F05407',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0501/products/F05108',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0502/products/F05205',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0503/products/F05301',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0503/products/F05302',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0508/products/F05801',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0508/products/F05802',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0508/products/F05803',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0507/products/F05701',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0505/products/F05501',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0505/products/F05502',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0505/products/F05505',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0506/products/F05603',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0506/products/F05604',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0506/products/F05602',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0506/products/F05601',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0506/products/F05605',
    'https://www.balluff.com/de-de/products/areas/A0005/groups/G0506/products/F05607',
    'https://www.balluff.com/de-de/products/areas/A0007/groups/G0701/products/F07102',
    'https://www.balluff.com/de-de/products/areas/A0007/groups/G0701/products/F07101',
    'https://www.balluff.com/de-de/products/areas/A0007/groups/G0701/products/F07103',
    'https://www.balluff.com/de-de/products/areas/A0007/groups/G0703/products/F07503',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0906/products/F09602',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0906/products/F09603',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0901/products/F09111',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0901/products/F09105',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0901/products/F09102',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0901/products/F09104',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0901/products/F09103',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0901/products/F09106',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0901/products/F09107',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0901/products/F09109',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0902/products/F09201',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0903/products/F09301',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0903/products/F09303',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0903/products/F09302',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0905/products/F09503',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0905/products/F09502',
    'https://www.balluff.com/de-de/products/areas/A0009/groups/G0905/products/F09501',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1706/products/F17610',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1706/products/F17611',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1706/products/F17603',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1706/products/F17604',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1706/products/F17613',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1704/products/F17403',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1704/products/F17402',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1704/products/F17401',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1704/products/F17404',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1705/products/F17504',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1705/products/F17503',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1705/products/F17501',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1705/products/F17502',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1705/products/F17505',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1707/products/F17702',
    'https://www.balluff.com/de-de/products/areas/A0017/groups/G1707/products/F17704',
    'https://www.balluff.com/de-de/products/areas/A0018/groups/G1802/products/F190203',
    'https://www.balluff.com/de-de/products/areas/A0018/groups/G1802/products/F190202',
    'https://www.balluff.com/de-de/products/areas/A0018/groups/G1802/products/F190204',
    'https://www.balluff.com/de-de/products/areas/A0018/groups/G1801/products/F180101',
    'https://www.balluff.com/de-de/products/areas/A0019/groups/G1902/products/F170603',
    'https://www.balluff.com/de-de/products/areas/A0019/groups/G1901/products/F170602',
    'https://www.balluff.com/de-de/products/areas/A0019/groups/G1901/products/F170601',
]

all_prod_links = []

for gr_link in all_group_links:
    resp = requests.get(gr_link)
    prod_count_soup = BeautifulSoup(resp.content, "html.parser")
    prod_count = prod_count_soup.select("h3.text-2xl.font-normal")[0].text.replace("Ausführungen", "").strip()

    params = {"page": "1", "perPage": prod_count}
    resp = requests.get(gr_link, params=params)
    soup = BeautifulSoup(resp.content, "html.parser")
    pr_links = [DOMAIN + a["href"] for a in soup.select("#product-table a.block")]
    print(len(pr_links))
    all_prod_links.extend(pr_links)

print(len(all_prod_links))

pandas.DataFrame(all_prod_links).to_csv(
    "/home/sana451/PycharmProjects/scrapy_parsers/balluff_com/balluff_com/results/balluff.com.links.csv",
    index=False)
