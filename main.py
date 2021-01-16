#!/usr/bin/python3
from requests_html import AsyncHTMLSession

NUM_PAGES = 5
URL = 'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page'
asession = AsyncHTMLSession()


class Review:
    def __init__(self, rating, content, subratings):
        self.rating = rating
        self.content = content
        self.subratings = subratings

    def __str__(self):
        output = '\n'
        output += 'Rating: ' + str(self.rating) + '\n'
        output += self.content + '\n'
        for rating in self.subratings.keys():
            output += str(rating) + ': ' + str(self.subratings[rating]) + '\n'
        return output


class ReviewCollection:
    def __init__(self):
        self.reviews = []

    def __str__(self):
        output = ''
        for review in self.reviews:
            output += str(review)
        return output

    def addReview(self, rating, content, subratings):
        self.reviews.append(Review(rating, content, subratings))

    def getReviews(self):
        return self.reviews

    def numReviews(self):
        return len(self.reviews)


def create_request(page_num):
    async def get_reviews_page():
        request_url = URL + str(page_num)
        r = await asession.get(request_url)
        return r
    return get_reviews_page


def digest_review_element(r):
    ratings_dict = dict()
    ratings = r.find('.review-ratings-all')[0].find('.tr')
    for rating in ratings:
        text = rating.find('.td')[0].text
        score = rating.search(' rating-{} ')
        if score == None:
            score = rating.find('.small-text.boldest')[0].text == 'Yes'
        else:
            score = score[0]
        ratings_dict.setdefault(text, score)
    review = {
        'rating': r.search(' rating-{} ')[0],
        'content': r.find('.review-content')[0].text,
        'subratings': ratings_dict
    }
    return review


def main():
    # get all NUM_PAGES review pages asynchronously
    get_review_pages = [create_request(i) for i in range(1, NUM_PAGES + 1)]

    results = asession.run(*get_review_pages)
    # initialize review collection
    review_collection = ReviewCollection()

    for result in results:
        # get all review elements in current page
        review_elements = result.html.find('.review-entry')

        for re in review_elements:
            # digest html of review element
            review = digest_review_element(re)

            # add review to collection
            review_collection.addReview(**review)

    print(review_collection)


if __name__ == '__main__':
    main()
