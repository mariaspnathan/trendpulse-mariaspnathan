# 3_analyze.py
import json
import os

def analyze_trends():
    print("[3/4] Performing aggregation and analytics calculations...")
    input_file = "clean_trends.json"
    output_file = "analytics_summary.json"
    
    if not os.path.exists(input_file):
        print(f"[!] Error: '{input_file}' not found. Please run 2_clean.py first.")
        return
        
    with open(input_file, "r") as f:
        data = json.load(f)
        
    topic_metrics = {}
    
    # Calculate group-by reductions for total volume and sentiment means
    for record in data:
        topic = record["topic"]
        vol = record["volume"]
        sent = record["sentiment_score"]
        
        if topic not in topic_metrics:
            topic_metrics[topic] = {"total_volume": 0, "sentiment_sum": 0.0, "count": 0}
            
        topic_metrics[topic]["total_volume"] += vol
        topic_metrics[topic]["sentiment_sum"] += sent
        topic_metrics[topic]["count"] += 1

    summary = []
    for topic, stats in topic_metrics.items():
        avg_sentiment = round(stats["sentiment_sum"] / stats["count"], 2)
        summary.append({
            "topic": topic,
            "aggregate_volume": stats["total_volume"],
            "average_sentiment": avg_sentiment,
            "mentions_count": stats["count"]
        })
        
    # Sort results by the most high-impact volume descending
    summary = sorted(summary, key=lambda x: x["aggregate_volume"], reverse=True)
    
    with open(output_file, "w") as f:
        json.dump(summary, f, indent=4)
    print(f"[✓] Insights calculated. Summary analysis written to '{output_file}'.")

if __name__ == "__main__":
    analyze_trends()
