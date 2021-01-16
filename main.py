#!/usr/bin/python3
from requests_html import AsyncHTMLSession

NUM_PAGES = 5
asession = AsyncHTMLSession()


async def get_reviews_page():
    page_num = 1
    request_url = 'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page'
    request_url += str(page_num)
    r = await asession.get(request_url)
    return r


class Review:
    def __init__(self, rating, text):
        self.rating = rating
        self.text = text

    def __str__(self):
        output = 'Rating: ' + str(self.rating) + '\n'
        output += self.text + '\n'
        return output


def main():
    # get all NUM_PAGES review pages asynchronously
    results = asession.run(get_reviews_page)

    for result in results:
        # get all review elements in current page
        review_elements = result.html.find('.review-entry')
        for re in review_elements:
            # get rating of this review
            rating = re.search(' rating-{} ')[0]


main()
