import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import json
import time
import random

def scrape_bing_top_10(query, session, headers):
    query = query.replace(' ', '+')
    url = f"https://www.bing.com/search?q={query}"
    print(f"Fetching URL: {url}")
    response = session.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('li', class_='b_algo')[:10]
        results_data = []
        for index, result in enumerate(results):
            title_tag = result.find('h2')
            link_tag = result.find('a')
            if title_tag and link_tag and 'href' in link_tag.attrs:
                link = link_tag['href']
                results_data.append(link)
            else:
                print(f"No href found for result {index + 1} in query: {query}")
        return results_data
    else:
        print(f"Failed to retrieve search results for query: {query}. Status code: {response.status_code}")
        return []

def read_queries_from_file(file_path):
    with open(file_path, 'r') as file:
        queries = [line.strip() for line in file if line.strip()]
    return queries

def main():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Referer": "https://www.bing.com/",
    }
    queries = read_queries_from_file('/Users/sahithinamala/Documents/IR Assignments/Assignment 1/100QueriesSet1.txt')
    all_results = {}
    
    for query in queries:
        print(f"Processing query: {query}")
        query_results = scrape_bing_top_10(query, session, headers)
        all_results[query] = query_results
        sleep_time = random.randint(10, 100)
        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)
    
    json_output = json.dumps(all_results, indent=4)
    
    with open('/Users/sahithinamala/Documents/IR Assignments/Assignment 1/results.json', 'w') as json_file:
        json_file.write(json_output)
    
    print("Results saved to json file")

if __name__ == "__main__":
    main()
