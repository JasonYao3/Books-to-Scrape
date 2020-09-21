# -*-  coding:utf-8 -*-
# coding:utf-8
# @Time: 2020-08-17
# @Author: Jason
# @File: booktocrape_spider.py
# @Software: PyCharm


# TODO: Web scrape bookstoscrape for book content data.

# Step 1. get list of all book urls for all pages on the website
# Step 2 . parse the list and save it to a csv file

import requests
from lxml import etree
import csv

book_list = []
all_book = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

def get_url(page):
    # Returns valid HTML trees with all content it can manage to parse.
    url = 'http://books.toscrape.com/catalogue/page-{}.html'.format(page)
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.content)
    return html

def get_book_url(html):
    # Returns a list of book urls
    book_urls = html.xpath('//*[@id="default"]/div/div/div/div/section/div[2]/ol/li/article/div[1]/a/@href')
    for book_url in book_urls:
        book_list.append('http://books.toscrape.com/catalogue/' + book_url)
    return book_list

def parse_book_url(book_url):
    # Returns valid HTML trees for list of book urls with all content it can manage to parse.
    book_response = requests.get(book_url, headers=headers)
    print(book_url, book_response)
    book_html = etree.HTML(book_response.content)
    return book_html

def get_content(book_html):
    # Returns a list of dictionaries contain relevant information about books.
    div_list = book_html.xpath('//*[@id="default"]/div/div')

    for div in div_list:
        item = {}
        item['title'] = div.xpath('./ul/li[4]/text()')[0]
        item['category'] = div.xpath('./ul/li[3]/a/text()')[0]
        item['price in euro'] = float(div.xpath('.//article/div[1]/div[2]/p[1]/text()')[0].replace('£', ''))

        item['availability'] = div.xpath('.//article/div[1]/div[2]/p[2]//text()')[1]
        item['availability'] = item['availability'].strip().split(' ')[2].replace('(', '')

        item['rating'] = div.xpath('//p[3]/@class')[0].split(' ')[1]
        # Replace rating from words to numbers for better formatting.
        nums = {'0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four', '5': 'Five'}
        for keys, values in nums.items():
            if item['rating'] == values:
                item['rating'] = item['rating'].replace(values, keys)

        item['img'] = div.xpath('//*[@id="product_gallery"]/div/div/div/img/@src')[0].split('..')[2]
        item['img'] = 'http://books.toscrape.com/' + item['img']
        all_book.append(item)
    return all_book

def save_content(content_list):
    # Saves data into a csv file.
    fieldsname = content_list[0].keys()
    with open('./booktoscrape.csv', 'a', encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fieldsname)
        for row in content_list:
            writer.writerow(row.values())
        print('write in csv over')
        print('-' * 20)

def main():
    for page in range(1,51):
        html = get_url(page)
        print(page)
        book_list = get_book_url(html)
    #print(book_list)
    for book_url in book_list:
        book_html = parse_book_url(book_url)
        content_list = get_content(book_html)
    save_content(content_list)
    print(len(content_list))


if __name__ == '__main__':
    main()
