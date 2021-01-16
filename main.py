#!/usr/bin/python3
from requests_html import AsyncHTMLSession

NUM_PAGES = 5
asession = AsyncHTMLSession()


async def get_reviews_page():
    page_num = 1
    request_url = 'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page'
    request_url += page_num
    request_url += '/?filter=ONLY_POSITIVE'
    r = await asession.get(request_url)
    return r


def main():
    results = asession.run(get_reviews_page)
    for result in results:
        print(result.html.url)


main()
