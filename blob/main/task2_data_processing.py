# task2_data_processing.py
import json
import csv
import os

KEYWORDS_MATRIX = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def determine_category(title):
    title_lower = title.lower()
    for category, keywords in KEYWORDS_MATRIX.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return "uncategorized"

def main():
    print("[2/4] Initializing data cleansing and trend categorization...")
    input_file = "raw_stories.json"
    output_file = "clean_stories.csv"  # Updated extension
    
    if not os.path.exists(input_file):
        print(f"[!] Error: Reference '{input_file}' missing. Please run 1_fetch.py first.")
        return
        
    with open(input_file, "r", encoding="utf-8") as f:
        raw_stories = json.load(f)
        
    cleaned_stories = []
    
    for item in raw_stories:
        # Data Guardrail: Skip dead entries, deleted items, or entries that aren't stories
        if not item or item.get("type") != "story":
            continue
            
        title = item.get("title")
        if not title:
            continue
            
        # Extract fields securely, defaulting missing values to 0
        cleaned_item = {
            "id": item.get("id"),
            "title": title.strip(),
            "score": item.get("score", 0),
            "comments_count": item.get("descendants", 0),
            "category": determine_category(title)
        }
        cleaned_stories.append(cleaned_item)
        
    # Write output to CSV format
    fieldnames = ["id", "title", "score", "comments_count", "category"]
    
    # 'newline=""' is recommended by Python documentation to prevent blank rows on Windows
    with open(output_file, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the CSV column headers
        writer.writeheader()
        
        # Write all the dict rows
        writer.writerows(cleaned_stories)
        
    print(f"[✓] Stage 2 Complete. Validated and sorted {len(cleaned_stories)} items into '{output_file}'.")

if __name__ == "__main__":
    main()
  