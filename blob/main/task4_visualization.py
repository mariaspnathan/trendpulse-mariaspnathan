# 4_visualize.py
import json
import os

def generate_visual_report():
    print("[4/4] Generating scannable terminal presentation report...")
    input_file = "analytics_summary.json"
    
    if not os.path.exists(input_file):
        print(f"[!] Error: '{input_file}' not found. Please run 3_analyze.py first.")
        return
        
    with open(input_file, "r") as f:
        summary_data = json.load(f)
        
    print("\n" + "="*60)
    print("                TRENDPULSE LIVE METRICS REPORT          ")
    print("="*60)
    print(f"{'TRENDING TOPIC':<20} | {'TOTAL VOL':<10} | {'SENTIMENT':<10} | {'VOLUME CHART'}")
    print("-"*60)
    
    for item in summary_data:
        topic = item["topic"]
        vol = item["aggregate_volume"]
        sent = item["average_sentiment"]
        
        # Categorize sentiment context visually using visual emoji anchors
        if sent > 0.5:
            sent_str = f"{sent} 🟢"
        elif sent < 0.0:
            sent_str = f"{sent} 🔴"
        else:
            sent_str = f"{sent} 🟡"
            
        # Draw a relative scale text-bar using block characters
        bar_size = min(int(vol / 2000), 20)
        bar_chart = "■" * bar_size
        
        print(f"{topic:<20} | {vol:<10,} | {sent_str:<10} | {bar_chart}")
        
    print("="*60 + "\n")

if __name__ == "__main__":
    generate_visual_report()
