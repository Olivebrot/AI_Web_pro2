from flask import Flask, render_template, request
from whoosh.fields import *
from crawler import Crawler
from search import Search

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    srch_url = request.args.get('srch_url', '')
    srch_text = request.args.get('srch_text', '')

    # Initialize the crawler with the user-provided URL
    crwl = Crawler(srch_url)
    all_links = crwl.get_all_links(itteration=20)
    crwl.extract_info(all_links)

    # Create a Search object and perform the search
    srch = Search(field_weights={"title": 10.0, "headder": 10.5, "content": 1.0})
    results = srch.search_default(srch_text)
    
    # Format results for display
    if results:
        formatted_results = [
            {
                "url": result["url"],
                "title": result["title"],
                "header": result["headder"],
                "score": result["score"]
            }
            for result in results
        ]
    else:
        formatted_results = []
    return render_template('results.html', srch_url=srch_url, srch_text=srch_text, results=formatted_results)

if __name__ == '__main__':
    app.run(debug=True)
