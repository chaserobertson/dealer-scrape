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
- If the dealer is recommended, leave this section's score as-is. If the dealer is not recommended, divide this section's summed score by 2.
### 25 pts: Employee Ratings
The number of employee reviews, relative to the other reviews processed, scaled by the average positivity of the employee reviews.
- No employee reviews results in a score of 0 for this section.
- If a review has the maximum number of employee ratings of all processed reviews, and they are all 5 star ratings, the score for this section is 25 * 5/5 = 25.
- If a review has half the maximum number of employee ratings of all processed reviews, and they are all 4 star ratings, the score for this section is 12.5 * 4/5 = 10.
### 25 pts: Review Body
Number of words in the review, relative to the maximum number of words from the other reviews processed.
- If a review has the maximum number of words of all processed reviews, the score for this section is 25 * 5/5 = 25.
- If a review has very few words, the score for this section will be quite low, depending on the number of words in other reviews.