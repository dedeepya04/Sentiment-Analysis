# Sentiment-Analysis
This is a project on Flipkart reviews Sentiment Analysis.Here is a brief explanation of how the code works and all the technologies that I have used to develop this project.

We give the link of the product page from flipkart website as the input and the overall analysis of all reviews is displayed along with the piechart of ratings distribution.
The two main concepts used in  this project are Webscrapping and sentiment analysis.

1) Webscrapping: It is the process of extracting information/content from a website. Inspect the product page to know the class names of Title, ratings and reviews. These classes are to be included in the code to 
                 scrape the data that we need.
   NOTE: Class names may change sometimes as E-commerce websites update frequently. Ensure to specify the correct class names in order to get exact output. To check class names, go to a product page then right 
         click and select 'Inspect' option.
  All the reviews are scraped and stored in a .csv file. This file is dynamically created when you run the code.

2) Sentiment Analysis: It is the process of analysing digital text to determine if tone of message is positive, negative or neutral.
     Data cleaning is done to reviews stored in .csv file. I used vader_lexicon which is a prebuilt sentiment analysis tool. It gives 3 scores: positive score, negative score and neutral score for each review.
     Scores of all reviews are added to get overall Positive , negative and neutral scores. The highest of these 3 scores would be the overall sentiment of the product.

A piechart showing the percentages of users rated 5 star, 4star, 3 star, 2 star, 1 star is also dispalyed.

3) The final step is to connect this code to a webpage and I used Flask which is a popular web framework for python. I designed the web pages using HTML and CSS.

Libraries used are: 1) Flask
                       2)Pandas
                       3)seaborn
                       4)nltk
                       5)selenium
                       6)matplotlib
                       7)csv
                       8)os
   
Techstacks used are :1)Python
                        2)Flask
                        3) HTML
                        4)CSS
   
   
