from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
from random import randint

import concurrent.futures

MAX_THREADS = 15

def scrape_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    df = pd.DataFrame()
    productImageLinkList = []  # for detailed
    productNameList = []
    productPriceList = []
    productQuantityList = []

    driver.get(url)
    b = randint(12, 39)
    sleep(b)
    print("Next Page after", b)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    cards = soup.find_all('div', attrs={'class': 'style__product-box___liepi'})
    print(len(cards))
    products = []
    for card in cards:
        aa = card.find_next("a",attrs={"class": "style__product-link___UB_67"})
        c = aa.find_next('div', attrs={
            "class": 'style__product-image___1F9l3'})
        print(c)
        # d = c.find_next('img', attrs={
        #     "class": 'style__image___Ny-Sa style__loaded___22epL'})
        # print(d)
        # img = d['src']
        # print(d)
        # dd = card.find_next('div', attrs={
        #     "class": 'style__product-description___2XaG0'})
        # e = dd.find_next('div', attrs={
        #     "class": 'style__pro-title___2QwJy'}).get_text()
        # name = str(e)
        # f = dd.find_next('div', attrs={
        #     "class": 'style__pack-size___2JQG7'}).get_text()
        # quantity = str(f)
        # gg = card.find_next('div', attrs={
        #     "class": 'style__product-pricing___38PRR'})
        # g = gg.find_next('span', attrs={
        #     "class": 'style__discount-price___25Bya'}).get_text()
        # price = str(g)

        # productImageLinkList.append(img)
        # productNameList.append(name)
        # productPriceList.append(price)
        # productQuantityList.append(quantity)

    # df['name'] = productNameList
    # df['price'] = productPriceList
    # # df['priceNoSign'] = medicinePriceNoSignList
    # # df['prescriptionRequired'] = medicinePrescriptionRequiredList
    # df['detail_quantity'] = productQuantityList
    # # df['covers'] = medicineQuantityCoverList
    # df['quantity'] = productQuantityList
    # # df['units'] = medicineQuantityLastUnitList
    # # df['manufacturer'] = medicineManufacturerList
    # df['prodLink'] = productImageLinkList
    # # df['salts'] = medicineSaltsList
    # # df['prodUrl'] = medicineDetailUrlList

    # return df




if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--ignore-gpu-blocklist")
    chrome_options.add_argument("--disable-software-rasterizer")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

    names = []  # List to store name of the product
    urls = []  # List to store price of the product


    url = ("https://www.1mg.com/categories/personal-care/sexual-wellness-22")

    mainAlphabetUrls = []

    # # first we make 26 links for the alphabet
    # for a in alphabets:
    #     mainAlphabetUrls.append("https://www.1mg.com/drugs-all-medicines?label=" + a)
    #     print(mainAlphabetUrls[len(mainAlphabetUrls) - 1])

    # We then fetch 26 last page numbers for those links
    lastPageNumber = 0
    driver.get(url)
    sleep(randint(2, 10))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    my_table = soup.find('ul', attrs={'class': 'list-pagination'})
    i = 0
    for tag in my_table:
        if i == 6:
            lastPageNumber = tag.get_text()
            print(tag.get_text())
        i = i + 1


    # updatedUrlsWithPage = []

    for i in range(1,2): #replace 2 by lastPageNumber
        urls.append(f'{url}?filter=true&pageNumber={i}')

    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_THREADS) as executor:
        results = executor.map(scrape_data, urls)
        # results_df = pd.concat(results)
        # results_df.to_csv('sexualWellness.csv',encoding='utf-8')


    # df.to_csv(f'${alphabets[index]}.csv', index=True, encoding='utf-8')


