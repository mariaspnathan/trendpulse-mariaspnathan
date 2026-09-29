# task4_visualization.py
import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    print("[4/4] Generating TrendPulse Matplotlib Dashboard Suite...")
    
    # Define reference files
    clean_stories_file = "clean_stories.csv"
    summary_file = "analytics_summary.csv"
    output_dir = "outputs"
    output_image_path = os.path.join(output_dir, "dashboard.png")
    
    # System Guardrail: Ensure required data assets are present
    if not os.path.exists(clean_stories_file) or not os.path.exists(summary_file):
        print("[!] Error: Core CSV pipeline data assets are missing.")
        print("    Please run 2_clean.py and 3_analyze.py before creating visualizations.")
        return
        
    # Ensure our target output folder exists
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Load data streams into Pandas DataFrames
    df_stories = pd.read_csv(clean_stories_file)
    df_summary = pd.read_csv(summary_file)
    
    # 2. Setup the global layout matrix (2x2 Grid Layout)
    # We will use subplots (2, 2) and delete the 4th empty quadrant to look clean
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("TrendPulse Dashboard", fontsize=22, fontweight="bold", y=0.98)
    
    # Flatten axes map into an easy-to-index list
    ax_list = axes.flatten()
    
    # -------------------------------------------------------------
    # TASK 1: Horizontal Bar Chart - Top 10 Stories by Score
    # -------------------------------------------------------------
    ax1 = ax_list[0]
    # Filter out top 10 rows sorting descending by score metrics
    top_10 = df_stories.sort_values(by="score", ascending=False).head(10)
    # Truncate overly long text strings so they display beautifully on the chart axis
    truncated_titles = top_10["title"].apply(lambda x: x[:30] + "..." if len(x) > 30 else x)
    
    # Plotting horizontally (invert y axis so number 1 rank is at the top)
    ax1.barh(truncated_titles, top_10["score"], color="teal", edgecolor="black")
    ax1.invert_yaxis()
    ax1.set_title("Top 10 Stories by Score", fontsize=12, fontweight="bold")
    ax1.set_xlabel("HackerNews Score Value")
    ax1.grid(axis="x", linestyle="--", alpha=0.5)

    # -------------------------------------------------------------
    # TASK 2: Vertical Bar Chart - Story Counts by Category
    # -------------------------------------------------------------
    ax2 = ax_list[1]
    # Define a distinct color mapping matrix for your categories
    colors = ["#3498db", "#e74c3c", "#2ecc71", "#9b59b6", "#f1c40f", "#95a5a6"]
    
    ax2.bar(df_summary["category"], df_summary["story_count"], color=colors, edgecolor="black")
    ax2.set_title("Story Distribution by Category", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Trend Categories")
    ax2.set_ylabel("Total Story Vol")
    ax2.tick_params(axis="x", rotation=15) # Tilt words so labels do not overlap
    ax2.grid(axis="y", linestyle="--", alpha=0.5)

    # -------------------------------------------------------------
    # TASK 3: Scatter Plot - Score vs Comments Engagement
    # -------------------------------------------------------------
    ax3 = ax_list[2]
    # Injecting the dynamic feature column engineering rule:
    # A story is tagged 'Popular' if it scores above the median baseline threshold
    score_median = df_stories["score"].median()
    df_stories["is_popular"] = df_stories["score"] > score_median
    
    # Segment data frames cleanly into subsets for separate point coloring
    popular_df = df_stories[df_stories["is_popular"] == True]
    regular_df = df_stories[df_stories["is_popular"] == False]
    
    # Overlay the scatter plots
    ax3.scatter(regular_df["score"], regular_df["comments_count"], 
                color="gray", alpha=0.6, label="Standard Story", edgecolor="none", s=40)
    ax3.scatter(popular_df["score"], popular_df["comments_count"], 
                color="orange", alpha=0.8, label="Popular Story", edgecolor="darkorange", s=60)
                
    ax3.set_title("Engagement Analysis: Score vs Comments", fontsize=12, fontweight="bold")
    ax3.set_xlabel("Story Score")
    ax3.set_ylabel("Number of Comments")
    ax3.legend(loc="upper left")
    ax3.grid(True, linestyle="--", alpha=0.4)

    # -------------------------------------------------------------
    # DASHBOARD CLEANUP & PRESENTATION SAVE
    # -------------------------------------------------------------
    # Completely remove/hide the 4th empty chart area to create a polished layout
    fig.delaxes(ax_list[3])
    
    # Adjust layout padding values dynamically so text labels do not clash
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # SECURITY PARADIGM: Always call savefig BEFORE executing interactive rendering windows
    plt.savefig(output_image_path, dpi=300)
    print(f"[✓] Stage 4 Complete. Dashboard graphics successfully generated at '{output_image_path}'.")
    
    # Show the canvas screen panel interface
    plt.show()

if __name__ == "__main__":
    main()
