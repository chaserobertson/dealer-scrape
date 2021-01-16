#!/usr/bin/python3
from requests_html import AsyncHTMLSession

NUM_PAGES = 5
NUM_REVIEWS_TO_DISPLAY = 3
MAX_RATING = 50
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

    def positivityScore(self):
        # start with rating out of max
        score = self.rating / MAX_RATING

        for subrating in self.subratings.values():
            # if dealership not recommended, halve the score
            if type(subrating) == bool and not subrating:
                score *= 0.5
            score *= subrating / MAX_RATING
        return self.rating


class ReviewCollection:
    def __init__(self):
        self.reviews = []

    def __str__(self):
        output = ''
        for review in self.reviews:
            output += str(review)
        return output

    def addReview(self, **kwargs):
        self.reviews.append(Review(**kwargs))

    def getReviews(self):
        return self.reviews

    def numReviews(self):
        return len(self.reviews)

    def identifyPositive(self):
        self.reviews.sort(key=Review.positivityScore, reverse=True)
        if len(self.reviews) > NUM_REVIEWS_TO_DISPLAY:
            return self.reviews[:NUM_REVIEWS_TO_DISPLAY]
        else:
            return self.reviews


def create_request(page_num):
    # define new request with different page num
    async def get_reviews_page():
        request_url = URL + str(page_num)
        r = await asession.get(request_url)
        return r
    return get_reviews_page


def digest_review_element(r):
    subratings = dict()

    # extract subratings from this review
    ratings = r.find('.review-ratings-all')[0].find('.tr')
    for rating in ratings:
        # get text name of this subrating
        text = rating.find('.td')[0].text

        # get numerical or boolean score of this subrating
        score = rating.search(' rating-{} ')
        if score == None:
            score = rating.find('.small-text.boldest')[0].text == 'Yes'
        else:
            score = int(score[0])

        # add this subrating to dict
        subratings.setdefault(text, score)

    # create struct from processed review element
    return {
        'rating': int(r.search(' rating-{} ')[0]),
        'content': r.find('.review-content')[0].text,
        'subratings': subratings
    }


def generateReviewCollection():
    review_collection = ReviewCollection()

    # get all review pages asynchronously
    get_review_pages = [create_request(i) for i in range(1, NUM_PAGES + 1)]
    results = asession.run(*get_review_pages)

    for result in results:
        # get all review elements in current page
        review_elements = result.html.find('.review-entry')

        for re in review_elements:
            # digest html of review element
            review = digest_review_element(re)

            # add review to collection
            review_collection.addReview(**review)

    return review_collection


def main():
    # Step 1: scrape the first 5 pages of reviews
    reviews = generateReviewCollection()

    # Step 2: identify the top three most overly positive endorsements
    top_reviews = reviews.identifyPositive()

    # Step 3: output top three reviews to the console in order of severity
    for review in top_reviews:
        print(review)

    return 0


if __name__ == '__main__':
    main()
