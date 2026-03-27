import requests
from flask import Flask, render_template, request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Initialize
nltk.download('vader_lexicon')
app = Flask(__name__)
sia = SentimentIntensityAnalyzer()

API_KEY = 'YOUR_NEWSAPI_KEY' # Get one at newsapi.org

def get_forex_news(market):
    url = f'https://newsapi.org{market}&apiKey={API_KEY}'
        response = requests.get(url).json()
            return response.get('articles', [])

            def analyze_signals(articles):
                total_score = 0
                    if not articles: return "Neutral", 50
                        
                            for article in articles:
                                    # Analyze title and description for sentiment
                                            text = f"{article['title']} {article['description']}"
                                                    score = sia.polarity_scores(text)['compound']
                                                            total_score += score
                                                                    
                                                                        avg_score = (total_score / len(articles))
                                                                            # Normalize score to 0-100 Greed Scale
                                                                                greed_scale = (avg_score + 1) * 50 
                                                                                    
                                                                                        if greed_scale > 70: return "Strong Buy (Extreme Greed)", greed_scale
                                                                                            elif greed_scale > 55: return "Buy (Greed)", greed_scale
                                                                                                elif greed_scale < 30: return "Strong Sell (Extreme Fear)", greed_scale
                                                                                                    elif greed_scale < 45: return "Sell (Fear)", greed_scale
                                                                                                        else: return "Hold (Neutral)", greed_scale

                                                                                                        @app.route('/', methods=['GET', 'POST'])
                                                                                                        def index():
                                                                                                            signal, scale, news = None, 50, []
                                                                                                                if request.method == 'POST':
                                                                                                                        market = request.form.get('market')
                                                                                                                                news = get_forex_news(market)[:10] # Top 10 news
                                                                                                                                        signal, scale = analyze_signals(news)
                                                                                                                                            return render_template('index.html', signal=signal, scale=scale, news=news)

                                                                                                                                            if __name__ == '__main__':
                                                                                                                                                app.run(debug=True)
                                                                                                                                    