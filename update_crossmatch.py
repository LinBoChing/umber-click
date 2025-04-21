import requests
from bs4 import BeautifulSoup
import json

# 網址
omission_url = 'https://www.lot539.com/lottery/fantasy5/lost/asc/mis'
freq_url = 'https://www.calotteryx.com/Fantasy-5/latest-50-draws/order-by-ranks/frequency-chart.htm'

omit_data = {}
freq_data = {}
error_msg = ""

try:
    resp1 = requests.get(omission_url, timeout=10)
    soup1 = BeautifulSoup(resp1.text, 'html.parser')
    omit_table = soup1.find('table')
    if omit_table:
        for row in omit_table.select('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) >= 3:
                num = cells[0].text.strip().zfill(2)
                try:
                    miss = int(cells[2].text.strip())
                    omit_data[num] = miss
                except ValueError:
                    continue
    else:
        error_msg += "遺漏表格未找到；"
except Exception as e:
    error_msg += f"遺漏資料錯誤：{e}；"

try:
    resp2 = requests.get(freq_url, timeout=10)
    soup2 = BeautifulSoup(resp2.text, 'html.parser')
    freq_table = soup2.find('table')
    if freq_table:
        for row in freq_table.select('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) >= 3:
                num = cells[1].text.strip().zfill(2)
                try:
                    times = int(cells[2].text.strip())
                    freq_data[num] = times
                except ValueError:
                    continue
    else:
        error_msg += "次數表格未找到；"
except Exception as e:
    error_msg += f"次數資料錯誤：{e}；"

matched = []
avg = 250 / 39
if not error_msg:
    for num in freq_data:
        if freq_data[num] < avg and omit_data.get(num, 0) > 7:
            matched.append({
                'number': num,
                'miss': omit_data[num]
            })

# 輸出 JSON 檔
with open('ttll_crossmatch.json', 'w', encoding='utf-8') as f:
    json.dump({
        'title': '【天天樂遺漏比對】',
        'matched': matched,
        'error': error_msg if error_msg else None
    }, f, ensure_ascii=False, indent=2)
