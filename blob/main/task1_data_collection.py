# 1_fetch.py
import json

def fetch_trending_data():
    print("[1/4] Connecting to TrendPulse ingestion stream...")

    # Simulating raw API responses containing varying data quality issues
    simulated_raw_data = [
        {"timestamp": 1792150000, "topic": "AI Agents", "volume": 12500, "sentiment_score": 0.85, "region": "us"},
        {"timestamp": 1792150005, "topic": "Quantum Computing", "volume": 8400, "sentiment_score": 0.62, "region": "uk"},
        {"timestamp": 1792150010, "topic": "Green Energy", "volume": 15100, "sentiment_score": 0.91, "region": "eu"},
        {"timestamp": 1792150015, "topic": "AI Agents", "volume": 13200, "sentiment_score": 0.78, "region": "uk"},
        {"timestamp": 1792150020, "topic": "Web3 Gaming", "volume": 4100, "sentiment_score": -0.15, "region": "us"},
        {"timestamp": 1792150025, "topic": "Cybersecurity", "volume": 9800, "sentiment_score": 0.45, "region": "global"},
        {"timestamp": 1792150030, "topic": "Remote Work", "volume": -500, "sentiment_score": 0.22, "region": "us"}, # Buggy volume
        {"timestamp": 1792150035, "topic": None, "volume": 3200, "sentiment_score": 0.05, "region": "eu"},       # Missing topic name
        {"timestamp": 1792150040, "topic": "AI Agents", "volume": 14000, "sentiment_score": 0.88, "region": "global"}
    ]

    output_file = "raw_trends.json"
    with open(output_file, "w") as f:
        json.dump(simulated_raw_data, f, indent=4)
    print(f"[✓] Successfully ingested {len(simulated_raw_data)} raw records into '{output_file}'.")

if __name__ == "__main__":
    fetch_trending_data()
