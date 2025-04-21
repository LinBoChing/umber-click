import requests
from bs4 import BeautifulSoup
import json

# 來源網址
omission_url = 'https://www.lot539.com/lottery/fantasy5/lost/asc/mis'
freq_url = 'https://www.calotteryx.com/Fantasy-5/latest-50-draws/order-by-ranks/frequency-chart.htm'

# 抓取遺漏資料
resp1 = requests.get(omission_url)
soup1 = BeautifulSoup(resp1.text, 'html.parser')
omit_table = soup1.find('table')
omit_data = {}
if omit_table:
    for row in omit_table.select('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) >= 3:
            num = cells[0].text.strip().zfill(2)
            miss = int(cells[2].text.strip())
            omit_data[num] = miss

# 抓取50期次數資料
resp2 = requests.get(freq_url)
soup2 = BeautifulSoup(resp2.text, 'html.parser')
freq_table = soup2.find('table')
freq_data = {}
if freq_table:
    for row in freq_table.select('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) >= 3:
            num = cells[1].text.strip().zfill(2)
            times = int(cells[2].text.strip())
            freq_data[num] = times

# 平均值
avg = 250 / 39

# 找出交集
matched = []
for num in freq_data:
    if freq_data[num] < avg and omit_data.get(num, 0) > 7:
        matched.append({
            'number': num,
            'miss': omit_data[num]
        })

# 寫出 JSON
with open('ttll_crossmatch.json', 'w', encoding='utf-8') as f:
    json.dump({
        'title': '【天天樂遺漏比對】',
        'matched': matched
    }, f, ensure_ascii=False, indent=2)
