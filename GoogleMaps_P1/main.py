'''
Google Maps Data Scraper/ Extractor using Python and Playwright
'''

from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse


@dataclass
class Business:
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None

@dataclass
class BusinessList:
    business_list: list[Business] = field(default_factory=list)

    def dataframe(self):
        return pd.json_normalize((asdict(business) for business in self.business_list), sep="")

    def save_to_excel(self, filename):
        self.dataframe().to_excel(f'{filename}.xlsx', index=False)

    def save_to_csv(self, filename):
        self.dataframe().to_csv(f'{filename}.csv', index=False)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(5000)

        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.wait_for_timeout(3000)

        page.keyboard.press('Enter')
        page.wait_for_timeout(5000)

        listings = page.locator('//div[@class="UaQhfb fontBodyMedium"]').all()
        print(len(listings))

        business_list = BusinessList()

        for num, listing in enumerate(listings):    # [:5]
            listing.click()
            page.wait_for_timeout(3000)

            name_xpath = '//h1[contains(@class, "DUwDvf lfPIob")]'
            address_path = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
            website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
            phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'

            business = Business()
            business.name = page.locator(name_xpath).inner_text()
            business.address = page.locator(address_path).inner_text()
            business.website = page.locator(website_xpath).inner_text()
            try:
                business.phone_number = page.locator(phone_number_xpath).inner_text()
            except:
                business.phone_number = " Not Found"

            print(f"\n########{num+1}########\nname:{business.name}\nAddress:{business.address}\nWebsite:{business.website}\nPhone:{business.phone_number}\n################")
            business_list.business_list.append(business)

        business_list.save_to_excel('google_maps_data')
        business_list.save_to_csv('google_maps_data')

        browser.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search',type=str)
    parser.add_argument('-l', '--location',type=str)
    args = parser.parse_args()

    if args.location and args.search:
        search_for = f"{args.search} in {args.location}"
    else:
        search_for = "restaurants in new cairo"

    main()
