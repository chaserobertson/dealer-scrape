
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
        return self.reviews
