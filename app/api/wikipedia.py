import wikipedia

class WikipediaApi:  
    def search_wikipedia(self, query: str):
        try:
            query = query.lower().replace("wikipedia", "").strip()
            if not query:
                return "Please specify what you want to search on Wikipedia."
            summary = wikipedia.summary(query, sentences=2)
            return f"According to Wikipedia: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"There are multiple results for your query: {e.options[:5]}"
        except wikipedia.exceptions.PageError:
            return "I couldn't find anything on Wikipedia for your query."
        except Exception:
            return "An error occurred while searching Wikipedia."
        