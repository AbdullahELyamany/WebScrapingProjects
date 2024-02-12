from playwright.sync_api import sync_playwright
import pandas as pd

def main():

    with sync_playwright() as p:

        checkin = '2024-02-07'
        checkout = '2024-02-15'

        page_url = f"https://www.booking.com/searchresults.html?ss=Cairo&ssne=Cairo&ssne_untouched=Cairo&label=gen173bo-1DCAEoggI46AdIM1gDaEOIAQGYATG4ARfIAQzYAQPoAQH4AQOIAgGYAiGoAgO4ApGGja4GwAIB0gIkYWY4NDI0MzEtOTdiMS00MzgyLTljMDUtMWIzYjU3ZjZmYmEw2AIE4AIB&sid=a7a1c776a8b73d78a8f45c2b983c181b&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id=-290692&dest_type=city&checkin={checkin}&checkout={checkout}&group_adults=2&no_rooms=1&group_children=0"

        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(page_url, timeout=60000)

        hotels = page.locator('//div[@data-testid="property-card"]').all()
        print(f'\n\n\nThere are: {len(hotels)} hotels.')

        hotels_list = []
        for hotel in hotels:
            hotel_dict = {}
            hotel_dict['hotel'] = hotel.locator('//div[@data-testid="title"]').inner_text()
            hotel_dict['price'] = hotel.locator('//span[@data-testid="price-and-discounted-price"]').inner_text()
            hotel_dict['score'] = hotel.locator('//div[@data-testid="review-score"]/div[1]').inner_text()
            hotel_dict['avg review'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[1]').inner_text()
            hotel_dict['reviews count'] = hotel.locator('//div[@data-testid="review-score"]/div[2]/div[2]').inner_text()

            hotels_list.append(hotel_dict)

        browser.close()

        df = pd.DataFrame(hotels_list)
        df.to_excel('hotels_list.xlsx', index=False)
        df.to_csv('hotels_list.csv', index=False)


if __name__ == '__main__':
    main()
