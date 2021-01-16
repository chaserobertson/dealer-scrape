# dealer-scrape
scrapes reviews and identifies those most "overly positive", as defined below

1. scrapes the first five pages of reviews of McKaig Chevrolet Buick on DealerRater.com
2. identifies the top three most “overly positive” endorsements (criteria below)
3. outputs these three reviews to the console, in order of severity

## What makes a review overly positive?
A review is given an "overly positive" score based on the sum of the following points system. 
The minimum score is 0, and the maximum is 100.

### 25 pts: The overall rating of the review, out of 5 stars, multiplied by 5 to scale between 0% and 25% properly
A rating of 0 stars results in a score of 0 for this section
A rating of 1 star results in a score of 5 for this section
### 25: Sum of each subrating score from the review, each out of 5 stars e.g. Customer Service 5, Pricing 4, etc.
### 25: Number of words in the review, relative to the maximum number of words from the other reviews processed
### 25: Number of employee reviews relative to the other reviews processed, scaled by the positivity of the review