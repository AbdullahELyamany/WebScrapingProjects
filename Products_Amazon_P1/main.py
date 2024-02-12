from playwright.sync_api import sync_playwright
import sys


def main():

    for link_index , link in enumerate(products_links):
        print(f"Scraping Product: {link_index}")

        page.goto(link, wait_until='domcontentloaded')
        page.wait_for_timeout(5000)

        title_xpath = '//span[@id="productTitle"]'
        price_xpath = '//span[@class="a-price-whole"]'

        title = page.locator(title_xpath).inner_text()
        price = page.locator(price_xpath).all()[0].inner_text()

        print(f"Product: {title} Price: {price}")


if __name__ == '__main__':

    with open('products_links.txt') as f:
        products_links = f.readlines()

    if len(products_links) == 0:
        print("No Links Found In Products_links.txt")
        sys.exit()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless= True)
        context = browser.new_context()
        page = context.new_page()

        main()
