import requests
import pprint
from bs4 import BeautifulSoup
import json
import csv

# url = 'https://coinmarketcap.com/cryptocurrency-category/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
}

# req = requests.get(url, headers=headers)
# src = req.text
# print(src)
#
# with open('CoinMarketCap.html', 'w', encoding='utf-8') as file:
#     file.write(src)
#
#
# with open('CoinMarketCap.html', 'r', encoding='utf-8') as file:
#     res = file.read()
#
# soup = BeautifulSoup(res, 'lxml')
#
# all_categories_names = soup.find('tbody').find_all("p", class_='sc-71024e3e-0 ktjszO')
# all_categories_hrefs = soup.find('tbody').find_all("p", class_='sc-71024e3e-0 ktjszO')
#
# full_information_dict = {}
#
# for names, hrefs in zip(all_categories_names, all_categories_hrefs):
#     item_hrefs = 'https://coinmarketcap.com' + hrefs.previous_element.get('href')
#     full_information_dict[names.text] = item_hrefs

"Сохраняем данные в JSON файл"
# with open('full_information.json', 'w') as file:
#     json.dump(full_information_dict, file, indent=4, ensure_ascii=False)
"Считываем ифнормацию для дальнейшего сбора"
with open('full_information.json', 'r', encoding='utf-8') as file:
    allInfo = json.load(file)


counter = 0
iteration = int(len(allInfo)) - 1
print(f"Всего итераций осталось {iteration}")
for sector_names, sector_hrefs in allInfo.items():

    sector_names = sector_names.replace(' ', '_')

    req = requests.get(sector_hrefs, headers=headers)
    src = req.text

    with open(f"data/{counter}_{sector_names}.html", 'w', encoding='utf-8') as file:
        file.write(src)

    with open(f"data/{counter}_{sector_names}.html", 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    "Соберем заголовки с таблицы (монета, цена и так далее)"
    table_head = soup.find('thead').find_all("p", class_='sc-71024e3e-0 fSsxNG')
    name_tokens = table_head[0].text
    price_token = table_head[1].text
    market_cap = table_head[5].text
    volume24 = table_head[6].text
    circulatingSupply = table_head[7].text

    with open(f"data/{counter}_{sector_names}.csv", "w", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                name_tokens,
                price_token,
                market_cap,
                volume24,
                circulatingSupply
            )
        )

    "Собирам данные о монетах sc-ae0cff98-3 ipWPGi cmc-table  "
    infoAboutCoin = soup.find('tbody').find_all('tr')

    infoAboutCoin_json = []

    # print(infoAboutCoin)
    # .find_all("p", class_="sc-71024e3e-0 ehyBa-d")
    for item in infoAboutCoin:
        coin_tds = item.find_all('td')

        full_name = coin_tds[2].text
        price = coin_tds[3].text

        infoAboutCoin_json.append(
            {
                "full_name":full_name,
                "price":price
            }
        )

        with open(f"data/{counter}_{sector_names}.csv", "a", encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    full_name,
                    price,
                )
            )


    with open(f"data_json/{counter}_{sector_names}.json", "w", encoding='utf-8') as file:
        json.dump(infoAboutCoin_json, file, indent=4, ensure_ascii=False)

    counter += 1
    print(f"Итерация {counter}. {sector_names} записан...")
    iteration -= 1
    print(f"Осталось итераций {iteration}")
