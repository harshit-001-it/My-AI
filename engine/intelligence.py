import requests
from bs4 import BeautifulSoup

class IntelligenceHub:
    def __init__(self):
        self.news_sources = {
            "global": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
            "tech": "https://feeds.feedburner.com/TechCrunch/"
        }
        self.last_weather = "STORM_SENSING_INACTIVE"

    def fetch_news(self, category="global"):
        """Fetches the latest headlines for the Master's review."""
        try:
            url = self.news_sources.get(category, self.news_sources["global"])
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, features="xml")
            
            items = soup.find_all('item')[:5] # Top 5 headlines
            headlines = [item.title.text for item in items]
            
            print(f"Intelligence: Synchronising news headlines for category {category}.")
            return headlines
        except Exception:
            return ["NEWS_NODE_OFFLINE: Re-attempting sync..."]

    def fetch_weather(self, city="GlobalHub"):
        """Localized weather sensing for the Master's current grid."""
        # This is a simulation for now, can be linked to OpenWeatherMap
        print(f"Intelligence: Sensing local atmosphere at {city}.")
        return {
            "temp": "24°C",
            "condition": "CLEAR_SKIES",
            "humidity": "45%",
            "wind": "12km/h"
        }

intelligence = IntelligenceHub()

def get_briefing():
    news = intelligence.fetch_news()
    weather = intelligence.fetch_weather()
    return {"news": news, "weather": weather}

if __name__ == "__main__":
    print("Intelligence Hub Test:")
    briefing = get_briefing()
    print(f"Top News: {briefing['news'][0]}")
    print(f"Weather: {briefing['weather']['temp']}")
