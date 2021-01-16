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
    def __init__(self, rating, content):
        self.rating = rating
        self.content = content

    def __str__(self):
        output = '\n'
        output += 'Rating: ' + str(self.rating) + '\n'
        output += self.content + '\n'
        return output


class ReviewCollection:
    def __init__(self):
        self.reviews = []

    def __str__(self):
        output = ''
        for review in self.reviews:
            output += str(review)
        return output

    def addReview(self, rating, content):
        self.reviews.append(Review(rating, content))

    def getReviews(self):
        return self.reviews


def main():
    # get all NUM_PAGES review pages asynchronously
    results = asession.run(get_reviews_page)
    # initialize review collection
    review_collection = ReviewCollection()

    for result in results:
        # get all review elements in current page
        review_elements = result.html.find('.review-entry')

        for re in review_elements:
            # get rating of this review
            rating = re.search(' rating-{} ')[0]

            # get content of this review
            content = re.find('.review-content')[0].text

            # add review to collection
            review_collection.addReview(rating, content)

    print(review_collection)


main()
