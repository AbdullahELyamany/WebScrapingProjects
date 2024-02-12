
from numpy import double
from playwright.sync_api import sync_playwright
import psycopg2
from psycopg2.extras import execute_values


def main():
    with sync_playwright() as p:

        # Scrape Data
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('https://coinmarketcap.com/')

        # Scrolling Down
        for i in range(4):
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(1500)

        trs_xpath = '//table[@class="sc-feda9013-3 ePzlNg cmc-table  "]/tbody/tr'
        trs_list = page.query_selector_all(trs_xpath)

        master_list = []
        for tr in trs_list:

            coin_dict = {}

            tds = tr.query_selector_all('//td')

            coin_dict['id'] = tds[1].inner_text()
            coin_dict['Name'] = tds[2].query_selector('//p[@color="text"]').inner_text()
            coin_dict['Symbol'] = tds[2].query_selector('//p[@color="text3"]').inner_text()
            coin_dict['Price'] = float(tds[3].inner_text().replace('$', '').replace(',', '').replace('...', '0000'))
            coin_dict['Market_cap_usd'] = int(tds[7].inner_text().replace('$', '').replace(',', ''))
            coin_dict['Volume_24h_usd'] = int(tds[8].query_selector('//p[@color="text"]').inner_text().replace('$', '').replace(',', ''))


            master_list.append(coin_dict)

        browser.close()


        # Taples (id, Name, Symbol, ...)
        list_of_tuples = [tuple(dic.values()) for dic in master_list]
        # print(list_of_tuples)
        # Connect to DB
        pgconn = psycopg2.connect(
            host = 'localhost',
            database = 'Cryptocurrency',
            user = 'postgres',
            password = 'postg1344'
        )

        # Create cursor
        pgcursor = pgconn.cursor()

        execute_values(
            pgcursor,
            "INSERT INTO crypto (id, name, symbol, price_usd, market_cap_usd, volume_24h_usd) VALUES %s",
            list_of_tuples
        )

        # Commit
        pgconn.commit()

        # Close connection
        pgconn.close()

        print("Data Saved Successfully")


if __name__ == '__main__':
    main()

