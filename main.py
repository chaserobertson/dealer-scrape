#!/usr/bin/python3
from requests_html import AsyncHTMLSession

NUM_PAGES = 5
NUM_REVIEWS_TO_DISPLAY = 3
MAX_RATING = 50
URL = 'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page'
asession = AsyncHTMLSession()


class Review:
    def __init__(self, rating, content, subratings, employee_ratings):
        self.rating = rating
        self.content = content
        self.subratings = subratings
        self.employee_ratings = employee_ratings
        self.positivityScore = 0

    def __str__(self):
        output = '\n'
        output += 'Rating: ' + str(self.rating) + '\n'
        output += self.content + '\n'
        for rating in self.subratings.keys():
            output += str(rating) + ': ' + str(self.subratings[rating]) + '\n'
        for rating in self.employee_ratings:
            output += 'Employee Rating: ' + str(rating) + '\n'
        return output

    def getPositivityScore(self):
        return self.positivityScore

    def calcPositivityScore(self, body_max, num_emp_max):
        # start with review rating multiplied by 5
        subscores = [self.rating * 5]

        # sum subratings and divide by 2 if dealership not recommended
        subrating_subscore = sum(self.subratings.values())
        if self.subratings['Recommend Dealer'] == True:
            subrating_subscore -= 1
        else:
            subrating_subscore /= 2
        subscores.append(subrating_subscore)

        # number of employee ratings relative to max, scaled to 25, multiplied by avg rating out of 5
        num_emp = len(self.employee_ratings)
        if num_emp == 0:
            emp_subscore = 0
        else:
            avg_rating = sum(self.employee_ratings) / num_emp
            emp_subscore = (25 * num_emp / num_emp_max) * (avg_rating / 5)
        subscores.append(emp_subscore)

        # number of words in the review body, relative to maximum, scaled to 25
        body_score = (len(self.content.split(' ')) / body_max) * 25
        subscores.append(body_score)

        self.positivityScore = sum(subscores)


class ReviewCollection:
    def __init__(self):
        self.reviews = []
        self.body_max = 0.1
        self.num_emp_max = 0.1

    def __str__(self):
        output = ''
        for review in self.reviews:
            output += str(review)
        return output

    def addReview(self, **kwargs):
        # update max review body size and number of employee reviews
        body_size = len(kwargs['content'].split(' '))
        if body_size > self.body_max:
            self.body_max = body_size
        num_emp = len(kwargs['employee_ratings'])
        if num_emp > self.num_emp_max:
            self.num_emp_max = num_emp

        # add the review
        self.reviews.append(Review(**kwargs))

    def getReviews(self):
        return self.reviews

    def numReviews(self):
        return len(self.reviews)

    def identifyPositive(self):
        # calculate score of each review
        for review in self.reviews:
            review.calcPositivityScore(self.body_max, self.num_emp_max)
        # sort by positivity score, descending
        self.reviews.sort(key=Review.getPositivityScore, reverse=True)
        return self.reviews[:NUM_REVIEWS_TO_DISPLAY]


def create_request(page_num):
    # define new request with different page num
    async def get_reviews_page():
        request_url = URL + str(page_num)
        r = await asession.get(request_url)
        return r
    return get_reviews_page


def digest_review_element(r):
    # extract subratings
    subratings = dict()
    ratings = r.find('.review-ratings-all')[0].find('.tr')
    for rating in ratings:
        # get text name of this subrating
        text = rating.find('.td')[0].text

        # get numerical or boolean score of this subrating
        score = rating.search(' rating-{} ')
        if score == None:
            score = rating.find('.small-text.boldest')[0].text == 'Yes'
        else:
            score = int(score[0]) / 10

        # add this subrating to dict
        subratings.setdefault(text, score)

    # extract employee ratings
    employees = []
    emp_ratings = r.find('.review-employee')
    for er in emp_ratings:
        rating_found = er.search(' rating-{} ')
        if rating_found != None:
            employees.append(int(rating_found[0]) / 10)

    # create kwargs struct from processed review element
    return {
        'rating': int(r.search(' rating-{} ')[0]) / 10,
        'content': r.find('.review-content')[0].text,
        'subratings': subratings,
        'employee_ratings': employees
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
