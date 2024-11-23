from flask import Flask, request, render_template
import pandas as pd
import nltk
import re
import string
import seaborn as sns
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import os
import time
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form ['product_link']  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    

   
    title = driver.find_element(By.CLASS_NAME, "VU-ZEz").text
    rate = driver.find_element(By.CSS_SELECTOR, ".XQDdHH").text
    
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    links = driver.find_elements(By.TAG_NAME, "a")
    filtered_links = [link.get_attribute("href") for link in links if link.get_attribute("href") and link.get_attribute("href").endswith("marketplace=FLIPKART")]

    for link in filtered_links:
        print(link)
    driver.get(link)
    '''if filtered_links:
        driver.get(filtered_links[0])
        time.sleep(5)'''
    stars = driver.find_elements(By.XPATH, "//div[contains(@class, 'BArk-j')]")
    ratings=[]
    for star in stars:
        ratings.append(star.text)
    ratings = [int(rating.replace(",", "")) for rating in ratings]

    with open('flipkart_reviews.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Review"])
        while True:
            try:
                comments = driver.find_elements(By.CLASS_NAME, '_11pzQk')  
                
                if not comments:
                    comments = driver.find_elements(By.CLASS_NAME, 'z9E0IG') 
                for comment in comments:
                    writer.writerow([comment.text])
                next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
                ActionChains(driver).move_to_element(next_button).click(next_button).perform()
                time.sleep(3)
            except:
                break

    driver.quit()

    
    data = pd.read_csv("flipkart_reviews.csv")
    nltk.download('stopwords')
    stemmer = nltk.SnowballStemmer('english')
    from nltk.corpus import stopwords
    stopword = set(stopwords.words('english'))

    def clean(text):
        text = str(text).lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)
        text = [word for word in text.split(' ') if word not in stopword]
        text = " ".join(text)
        text = [stemmer.stem(word) for word in text.split(' ')]
        text = " ".join(text)
        return text

    data["Review"] = data["Review"].apply(clean)

    

    labels = ["5 Star", "4 Star", "3 Star", "2 Star", "1 Star"]


    plt.figure(figsize=(8, 8))
    plt.pie(ratings, labels=labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title("Distribution of Ratings")


    if not os.path.exists('static'):
        os.makedirs('static')


    plt.savefig('static/ratings_pie_chart.png')

    
    plt.close()

    
    nltk.download('vader_lexicon')
    sentiments = SentimentIntensityAnalyzer()
    data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["Review"]]
    data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["Review"]]
    data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["Review"]]

    x = sum(data["Positive"])
    y = sum(data["Negative"])
    z = sum(data["Neutral"])
    if (x > y) and (x > z):
        sentiment = "Positive 😊"
    elif (y > x) and (y > z):
        sentiment = "Negative 😠"
    else:
        sentiment = "Neutral 🙂"

    
    return render_template(
        'result.html',
        title=title,
        rate=rate,
        sentiment=sentiment,
        positive=x,
        negative=y,
        neutral=z,
        image_url='static/ratings_pie_chart.png'
    )

if __name__ == '__main__':
    app.run(debug=True)
