# dealer-scrape
Scrapes reviews and identifies those most "overly positive", as defined below:

1. Scrapes the first five pages of reviews of McKaig Chevrolet Buick on DealerRater.com.
2. Identifies the top three most “overly positive” endorsements (criteria below).
3. Outputs these three reviews to the console, in descending order of positivity score.

## What makes a review overly positive?
A review is given a positivity score based on the sum of the following points system.<br>
The minimum score is 0, and the maximum is 100.

### 25 pts: Overall Rating
The overall rating of the review, out of 5 stars, multiplied by 5.
- A rating of 0 stars results in a score of 0 for this section.
- A rating of 1 star results in a score of 5 for this section.
- ...
- A rating of 5 stars results in a score of 25 for this section.
### 25 pts: Subratings and Recommendation
The sum of each subrating from the review, each out of 5 stars, divided by 2 if the dealer is not recommended.
- A Customer Service rating of 5 stars adds 5 to the score for this section.
- A Quality of Work rating of 4 stars adds 4 to the score for this section.
- ...
- If the dealer is not recommended, divide the above summed scores by 2.
### 25 pts: Employee Ratings
Number of employee reviews relative to the other reviews processed, scaled by the positivity of the review
### 25 pts: Review Body
Number of words in the review, relative to the maximum number of words from the other reviews processed
