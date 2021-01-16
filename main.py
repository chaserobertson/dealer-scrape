#!/usr/bin/python3
from requests_html import AsyncHTMLSession

NUM_PAGES = 5
asession = AsyncHTMLSession()


class Review:
    def __init__(self, superrating, content, ratings):
        self.superrating = superrating
        self.content = content
        self.ratings = ratings

    def __str__(self):
        output = '\n'
        output += 'Superrating: ' + str(self.superrating) + '\n'
        output += self.content + '\n'
        for rating in self.ratings.keys():
            output += str(rating) + ': ' + str(self.ratings[rating]) + '\n'
        return output


class ReviewCollection:
    def __init__(self):
        self.reviews = []

    def __str__(self):
        output = ''
        for review in self.reviews:
            output += str(review)
        return output

    def addReview(self, superrating, content, ratings):
        self.reviews.append(Review(superrating, content, ratings))

    def getReviews(self):
        return self.reviews


async def get_reviews_page():
    page_num = 1
    request_url = 'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page'
    request_url += str(page_num)
    r = await asession.get(request_url)
    return r


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
        'superrating': r.search(' rating-{} ')[0],
        'content': r.find('.review-content')[0].text,
        'ratings': ratings_dict
    }
    return review


def main():
    # get all NUM_PAGES review pages asynchronously
    results = asession.run(get_reviews_page)
    # initialize review collection
    review_collection = ReviewCollection()

    for result in results:
        # get all review elements in current page
        review_elements = result.html.find('.review-entry')

        for re in review_elements:
            # digest html of review element
            review = digest_review_element(re)

            # add review to collection
            review_collection.addReview(
                review['superrating'], review['content'], review['ratings'])

    print(review_collection)


main()
