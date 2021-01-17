#!/usr/bin/python3
from requests_html import AsyncHTMLSession
from review import ReviewCollection

NUM_PAGES = 5
NUM_REVIEWS_TO_DISPLAY = 3
URL = 'https://www.dealerrater.com/dealer/McKaig-Chevrolet-Buick-A-Dealer-For-The-People-dealer-reviews-23685/page'
asession = AsyncHTMLSession()


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
    for review in top_reviews[:NUM_REVIEWS_TO_DISPLAY]:
        print(review)

    return 0


if __name__ == '__main__':
    main()
