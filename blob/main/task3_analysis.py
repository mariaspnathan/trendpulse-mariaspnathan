# task3_analysis.py
import pandas as pd
import numpy as np
import os

def main():
    print("[3/4] Processing core metric aggregations using Pandas & NumPy...")
    input_file = "hn_clean_stories.csv"
    output_file = "hn_analytics_summary.csv"  # Updated output extension to CSV
    
    if not os.path.exists(input_file):
        print(f"[!] Error: Reference '{input_file}' missing. Please run 2_clean.py first.")
        return
        
    # 1. Load the cleaned data from CSV into a Pandas DataFrame
    df = pd.read_csv(input_file)
    
    # 2. Complete List of Target Categories to ensure zero-counts are included
    all_categories = ["technology", "worldnews", "sports", "science", "entertainment", "uncategorized"]
    
    # 3. Use Pandas GroupBy coupled with NumPy aggregation methods
    agg_df = df.groupby("category").agg(
        story_count=("id", "count"),
        total_score=("score", np.sum),
        total_comments=("comments_count", np.sum),
        avg_score=("score", np.mean),
        avg_comments=("comments_count", np.mean)
    )
    
    # 4. Reindex to guarantee all categories are present, even if they have 0 stories
    agg_df = agg_df.reindex(all_categories, fill_value=0)
    
    # 5. Clean up numbers: Round averages to 1 decimal place using NumPy
    agg_df["avg_score"] = np.round(agg_df["avg_score"].astype(float), 1)
    agg_df["avg_comments"] = np.round(agg_df["avg_comments"].astype(float), 1)
    
    # Reset index so 'category' becomes a normal column instead of a row identifier
    agg_df = agg_df.reset_index()
    
    # 6. Filter to only the core reporting summary columns
    summary_columns = ["category", "story_count", "avg_score", "avg_comments"]
    final_summary_df = agg_df[summary_columns]
    
    # 7. Write the analytical metrics payload out to a CSV file
    # index=False prevents Pandas from adding an arbitrary numbers column to your file
    final_summary_df.to_csv(output_file, index=False)
        
    print(f"[✓] Stage 3 Complete. Pandas calculated analytics engine successfully saved to '{output_file}'.")

if __name__ == "__main__":
    main()
