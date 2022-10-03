import sys
import requests
import urllib
import argparse
import os
import time
from  pprint import  pprint as pp
from bs4 import BeautifulSoup
import csv
# user_cmds = sys.argv[1:]
# query = sys.argv[1]
# Google_query = f"https://www.google.com/search?q={query}"

# you can change the CBRN
cbrn = ['chemical', 'chem', 'biology', 'bio', 'nuclear', 'nukes', 'radiological', 'bomb', 'terrorist', ]


def google_search(query, num):
    pages = []

    for i in range(0,num, 5):
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'

        }
        # 'as_qdr': 0
        resp = requests.get(f'https://google.com/search?q={query}',
                     params={'num': '', 'start': i}, headers=headers)

        print(f'url: {resp.url} and status code :{resp.status_code}')
        if resp.status_code == 200:
            pages.append(resp.content)
            time.sleep(50)
        else:
            break
    return pages


def has_no_character(css_class):
    return css_class is None


def link_cleaner(li):
    cleaned_url = ''
    # print(li[0:5])
    if li.startswith('https'):
        cleaned_url = li
    else:
        for word in li.split('&'):
            if 'url=' in word:
                cleaned_url = word
        cleaned_url = cleaned_url.split('url=')
        cleaned_url = "".join(cleaned_url)
    return cleaned_url


def google_soup(page) -> dict:
    pages_dict = dict()
    soup = BeautifulSoup(page, 'html.parser')
    search_result = soup.find_all('a')
    # print(bool(search_result))

    for item in search_result:
        def check_title(w: str) -> bool:
            if w in item.text.lower():
                return True
            else:
                return False

        if any(list(map(check_title, cbrn))) or 'h3' in item.contents:
            item_url = item.get('href')
            print(item_url)
            print(f'{item.text} : {link_cleaner(item_url)}')
            title, link = item.text, link_cleaner(item_url)
            pages_dict[title] = link
            # print(pages_dict)

        else:
            pass
    return pages_dict


def combine_page(lst: list) -> dict:
    pp("Start file")
    total_dict = list()
    print(len(lst))
    for page in lst:
        result = google_soup(page)
        total_dict.append(result)
    for i in range(1, len(total_dict)):
        total_dict[0].update(total_dict[i])
    return total_dict[0]


def output_to_csv(f: dict) -> None:
    with open(f'{name}.csv', 'w', newline='') as csvfile:
        fieldnames = ['tile', 'links']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key in f:
            writer.writerow({'tile': key, 'links': f[key]})


if __name__ == '__main__':
    try:
        url = input("Enter your search term? ")
        date = input("Enter a date ")
        url += " " + f"after:{date}"
        url = urllib.parse.quote_plus(url, safe=':*-)(/"\'')
        print(url)
        page_count = int(input("How many pages do you wish to search? (recommended is 50 for 5 SERP or 5 for 1 SERP) "))
        resp_list = google_search(url, page_count)
        output_file = combine_page(resp_list)
        save_query = input("Would you like to save your search result in to a csv file? Y/N ")
        while True:
            if save_query.lower() == 'y':
                name = input('input the name of the file: ')
                output_to_csv(output_file)
                pp('Thanks')
                exit()
            elif save_query.lower() == 'n':
                print("Okay bye bye")
                break
            else:
                save_query = input("you need to specify a command? Y/N ")

    except Exception as err:
        print(err)

    finally:
        print('Done')




