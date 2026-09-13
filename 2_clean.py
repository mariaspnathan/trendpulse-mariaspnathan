{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOA7J2o1ch3MGGZO0CDuEo+",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/mariaspnathan/trendpulse-mariaspnathan/blob/main/2_clean.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "PGKuq_XJXb_V",
        "outputId": "4c3a6a4a-ceaa-4b22-a243-df8f448d7d74"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "[1/4] Connecting to TrendPulse ingestion stream...\n",
            "[✓] Successfully ingested 9 raw records into 'raw_trends.json'.\n"
          ]
        }
      ],
      "source": [
        "# 1_fetch.py\n",
        "import json\n",
        "\n",
        "def fetch_trending_data():\n",
        "    print(\"[1/4] Connecting to TrendPulse ingestion stream...\")\n",
        "\n",
        "    # Simulating raw API responses containing varying data quality issues\n",
        "    simulated_raw_data = [\n",
        "        {\"timestamp\": 1792150000, \"topic\": \"AI Agents\", \"volume\": 12500, \"sentiment_score\": 0.85, \"region\": \"us\"},\n",
        "        {\"timestamp\": 1792150005, \"topic\": \"Quantum Computing\", \"volume\": 8400, \"sentiment_score\": 0.62, \"region\": \"uk\"},\n",
        "        {\"timestamp\": 1792150010, \"topic\": \"Green Energy\", \"volume\": 15100, \"sentiment_score\": 0.91, \"region\": \"eu\"},\n",
        "        {\"timestamp\": 1792150015, \"topic\": \"AI Agents\", \"volume\": 13200, \"sentiment_score\": 0.78, \"region\": \"uk\"},\n",
        "        {\"timestamp\": 1792150020, \"topic\": \"Web3 Gaming\", \"volume\": 4100, \"sentiment_score\": -0.15, \"region\": \"us\"},\n",
        "        {\"timestamp\": 1792150025, \"topic\": \"Cybersecurity\", \"volume\": 9800, \"sentiment_score\": 0.45, \"region\": \"global\"},\n",
        "        {\"timestamp\": 1792150030, \"topic\": \"Remote Work\", \"volume\": -500, \"sentiment_score\": 0.22, \"region\": \"us\"}, # Buggy volume\n",
        "        {\"timestamp\": 1792150035, \"topic\": None, \"volume\": 3200, \"sentiment_score\": 0.05, \"region\": \"eu\"},       # Missing topic name\n",
        "        {\"timestamp\": 1792150040, \"topic\": \"AI Agents\", \"volume\": 14000, \"sentiment_score\": 0.88, \"region\": \"global\"}\n",
        "    ]\n",
        "\n",
        "    output_file = \"raw_trends.json\"\n",
        "    with open(output_file, \"w\") as f:\n",
        "        json.dump(simulated_raw_data, f, indent=4)\n",
        "    print(f\"[✓] Successfully ingested {len(simulated_raw_data)} raw records into '{output_file}'.\")\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    fetch_trending_data()\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# 2_clean.py\n",
        "import json\n",
        "import os\n",
        "\n",
        "def clean_data():\n",
        "    print(\"[2/4] Initializing data cleaning pipeline...\")\n",
        "    input_file = \"raw_trends.json\"\n",
        "    output_file = \"clean_trends.json\"\n",
        "\n",
        "    if not os.path.exists(input_file):\n",
        "        print(f\"[!] Error: '{input_file}' not found. Please run 1_fetch.py first.\")\n",
        "        return\n",
        "\n",
        "    with open(input_file, \"r\") as f:\n",
        "        raw_data = json.load(f)\n",
        "\n",
        "    cleaned_data = []\n",
        "    for record in raw_data:\n",
        "        # 1. Validation Guardrail: Ensure fields aren't blank\n",
        "        if not record.get(\"topic\"):\n",
        "            print(\"[-] Dropping record: Missing 'topic' name identifier.\")\n",
        "            continue\n",
        "\n",
        "        # 2. Validation Guardrail: Volume metrics cannot logically be zero or negative\n",
        "        if record.get(\"volume\", 0) <= 0:\n",
        "            print(f\"[-] Dropping record for '{record['topic']}': Invalid negative volume data.\")\n",
        "            continue\n",
        "\n",
        "        # 3. Standardization: Normalize data structures\n",
        "        record[\"topic\"] = record[\"topic\"].strip().title()\n",
        "        record[\"region\"] = record[\"region\"].upper()\n",
        "        cleaned_data.append(record)\n",
        "\n",
        "    with open(output_file, \"w\") as f:\n",
        "        json.dump(cleaned_data, f, indent=4)\n",
        "    print(f\"[✓] Data cleansing complete. {len(cleaned_data)} valid records saved to '{output_file}'.\")\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    clean_data()\n"
      ],
      "metadata": {
        "id": "70KtAE5zMpSY"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}