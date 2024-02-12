from playwright.sync_api import sync_playwright
from discord import SyncWebhook
from discord import Embed
from datetime import datetime
import sys

# https://discord.com/api/webhooks/1206179289750306857/uAytMLa8EM8-XddtKOvVjwAq9caHBd2fRW7BH4P40j4kR15vRnqSGlRqzNgsojKMu3EH

def send_to_discord(embad):
    webhook = SyncWebhook.partial('1206179289750306857', 'uAytMLa8EM8-XddtKOvVjwAq9caHBd2fRW7BH4P40j4kR15vRnqSGlRqzNgsojKMu3EH')

    webhook.send(username='AmazonBot', embed=embad)


def main():

    for link_index , link in enumerate(products_links):

        page.goto(link, wait_until='domcontentloaded')
        page.wait_for_timeout(5000)

        title_xpath = '//span[@id="productTitle"]'
        price_xpath = '//span[@class="a-price-whole"]'

        title = page.locator(title_xpath).inner_text()
        price = page.locator(price_xpath).all()[0].inner_text()

        em = Embed(title=title, description='', color=242424)
        em.add_field(name='URL', value=link, inline=False)
        em.add_field(name='Price', value=price, inline=False)
        em.timestamp = datetime.now()
        em.set_footer(text='Powered by Amazon Bot')

        send_to_discord(em)


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
