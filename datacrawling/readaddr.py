import requests
from bs4 import BeautifulSoup
import re 
city = ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구','성동구',
        '성북구','송파구','양천구','영등포구', '용산구','은평구','종로구','중구','중랑구']
#강서, 중구 빼고 다 됨 

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.220 Whale/1.3.51.7 Safari/537.36',
    'Referer': 'https://m.land.naver.com/'
}
f = open("gu.txt", 'r+')
for i in city:
    url = "https://m.land.naver.com/search/result/" + i
    response = requests.get(url, headers=header)
    
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        filter = re.findall('filter: {(.+?)},' ,str(soup.select('script')[3]), flags=re.DOTALL)
        #soup.find_all('img>script')
        data = {}
        try:
            filter2 = filter[0].split()
            
            for i in range(len(filter2)):
                if i % 2 == 0:
                    data[filter2[i].strip(":")] = filter2[i+1].strip(',').strip("'")
        except IndexError:
            pass
        f.write(str(data))
        f.write("\n")
f.close()