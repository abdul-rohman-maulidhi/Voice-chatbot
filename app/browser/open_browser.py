import webbrowser

class OpenBrowser:
    def handle_open_browser(self, text: str):
        """
        Handles requests to open popular websites in the browser.
        """
        if "youtube" in text.lower():
            return self.open_website("https://www.youtube.com", "YouTube")
        elif "youtube music" in text.lower():
            return self.open_website("https://music.youtube.com", "YouTube Music")
        elif "maps" in text.lower():
            return self.open_website("https://www.google.com/maps", "Google Maps")
        elif "classroom" in text.lower():
            return self.open_website("https://classroom.google.com", "Google Classroom")
        elif "google document" in text.lower() or "google doc" in text.lower():
            return self.open_website("https://docs.google.com", "Google Docs")
        elif "google sheet" in text.lower() or "spreadsheet" in text.lower():
            return self.open_website("https://sheets.google.com", "Google Sheets")
        elif "presentation" in text.lower() or "google slide" in text.lower():
            return self.open_website("https://docs.google.com/presentation", "Google Slides")
        elif "calendar" in text.lower():
            return self.open_website("https://calendar.google.com", "Google Calendar")
        elif "drive" in text.lower():
            return self.open_website("https://drive.google.com", "Google Drive")
        elif "mail" in text.lower() or "email" in text.lower() or "gmail" in text.lower():
            return self.open_website("https://mail.google.com", "Google Mail")
        elif "google keep" in text.lower():
            return self.open_website("https://keep.google.com", "Google Keep")
        elif "search" in text.lower():
            return self.open_website("https://www.google.com/search", "Google Search")
        elif "google translate" in text.lower() or "translate" in text.lower():
            return self.open_website("https://translate.google.com", "Google Translate")
        elif "google news" in text.lower():
            return self.open_website("https://news.google.com", "Google News")
        elif "weather" in text.lower():
            return self.open_website("https://www.weather.gov", "Weather.gov")
        elif "finance" in text.lower():
            return self.open_website("https://finance.google.com", "Google Finance")
        elif "shopping" in text.lower():
            return self.open_website("https://www.google.com/shopping", "Google Shopping")
        elif "travel" in text.lower():
            return self.open_website("https://www.google.com/travel", "Google Travel")
        elif "google meet" in text.lower() or "meet" in text.lower():
            return self.open_website("https://www.google.com/meet", "Google Meet")
        elif "google form" in text.lower():
            return self.open_website("https://www.google.com/form", "Google Form")
        elif "spotify" in text.lower():
            return self.open_website("https://www.spotify.com", "Spotify")
        elif "twitter" in text.lower():
            return self.open_website("https://www.twitter.com", "Twitter")
        elif "instagram" in text.lower():
            return self.open_website("https://www.instagram.com", "Instagram")
        elif "linkedin" in text.lower():
            return self.open_website("https://www.linkedin.com", "LinkedIn")
        elif "facebook" in text.lower():
            return self.open_website("https://www.facebook.com", "Facebook")
        elif "github" in text.lower():
            return self.open_website("https://www.github.com", "GitHub")
        elif "netflix" in text.lower():
            return self.open_website("https://www.netflix.com", "Netflix")
        elif "amazon" in text.lower():
            return self.open_website("https://www.amazon.com", "Amazon")
        elif "whatsapp web" in text.lower():
            return self.open_website("https://web.whatsapp.com", "WhatsApp Web")
        elif "tiktok" in text.lower():
            return self.open_website("https://www.tiktok.com", "TikTok")
        elif "telegram web" in text.lower():
            return self.open_website("https://web.telegram.org", "Telegram Web")
        elif "chatgpt" in text.lower() or "gpt" in text.lower():
            return self.open_website("https://chat.openai.com", "OpenAI ChatGPT")
        elif "gemini" in text.lower():
            return self.open_website("https://gemini.com", "Gemini")
        elif "claude" in text.lower():
            return self.open_website("https://www.claude.ai", "Claude")
        elif "perplexity" in text.lower():
            return self.open_website("https://www.perplexity.ai", "Perplexity")
        elif "black box" in text.lower():
            return self.open_website("https://blackbox.ai", "Black Box")
        else:
            return "I couldn't find the specified site."
        
    def open_website(self, url, site_name):
        """
        Open a website in the default web browser.
        """
        try:
            webbrowser.open(url)
            return f"Opening {site_name} in your browser..."
        except Exception as e:
            return f"Sorry, I couldn't open {site_name}. Error: {e}"