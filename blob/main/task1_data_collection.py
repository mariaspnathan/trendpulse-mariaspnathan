# task1_data_collection.py
import urllib.request
import json
import concurrent.futures

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL_TEMPLATE = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

def fetch_single_story(story_id):
    """Worker function to pull down an individual story object."""
    url = ITEM_URL_TEMPLATE.format(story_id)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None # Return None if network fails for this item

def main():
    print("[1/4] Connecting to HackerNews Top Stories API...")
    
    # Fetch top 500 IDs
    try:
        req = urllib.request.Request(TOP_STORIES_URL, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as response:
            story_ids = json.loads(response.read().decode())[:500]
    except Exception as e:
        print(f"[!] Critical Error fetching top stories index: {e}")
        return

    print(f"[*] Found {len(story_ids)} story IDs. Initializing concurrent workers...")
    
    # ThreadPoolExecutor to pull down metadata concurrently
    raw_stories = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(fetch_single_story, story_ids)
        for idx, item in enumerate(results):
            if item:
                raw_stories.append(item)
            if (idx + 1) % 100 == 0:
                print(f"    -> Progress: Downloaded {idx + 1}/500 metadata records.")

    # Save output to staging area
    output_file = "raw_stories.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(raw_stories, f, indent=4)
        
    print(f"[✓] Stage 1 Complete. Ingested {len(raw_stories)} raw profiles into '{output_file}'.")

if __name__ == "__main__":
    main()
