# YouTube Sentiment Analysis for Indonesian Comments

![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/youtube-sentiment)
![License](https://img.shields.io/github/license/yourusername/youtube-sentiment)

A comprehensive tool for analyzing sentiment in Indonesian YouTube comments. This project provides an end-to-end workflow from comment extraction to sentiment analysis and visualization, specifically optimized for Indonesian language content.

## 📋 Overview

This tool allows you to:
1. Extract comments from any YouTube video using just the video ID
2. Analyze the sentiment of these comments using state-of-the-art NLP models for Indonesian
3. Visualize the results with customizable charts and word clouds

## ✨ Features

- **YouTube Comment Extraction**:
  - **Scraper Mode**: No API key required, uses the youtube-comment-downloader library
  - **API Mode**: Uses the official YouTube Data API v3 (requires Google API key)
  - Flexible sorting options: by popularity or recency
  
- **Advanced Sentiment Analysis**:
  - Pre-trained Indonesian RoBERTa model for accurate sentiment detection
  - Three-category classification: Positive, Neutral, Negative
  - Sentiment scores with confidence levels

- **Rich Visualization Suite**:
  - Sentiment distribution charts
  - Time-based sentiment trends
  - Interactive word clouds
  - Customizable visualization options

- **Data Processing**:
  - Automatic text cleaning and preprocessing
  - Integrated date parsing and formatting
  - Consistent CSV format for easy analysis

## 🗂️ Project Structure

```
youtube-sentiment/
├── data/                     # CSV files with comments and analysis
│   └── youtube_comments_<VIDEO_ID>.csv
├── notebooks/                # Jupyter notebooks
│   └── YouTube_Sentiment_Analysis_Workflow.ipynb
├── src/                      # Source code
│   └── youtube_comments_fetcher.py
├── environment.yml           # Conda environment specification
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

## 🚀 Installation

### Prerequisites
- Python 3.11+
- Conda package manager (recommended) or pip

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/youtube-sentiment.git
   cd youtube-sentiment
   ```

2. **Set up the environment using Conda** (recommended):
   ```bash
   conda env create -f environment.yml
   conda activate youtube-sentiment
   ```

   **Alternative**: If not using Conda, install dependencies with pip:
   ```bash
   pip install -r requirements.txt  # Note: Create this from environment.yml if needed
   ```

3. **Download NLTK resources**:
   ```bash
   python -c "import nltk; nltk.download('stopwords')"
   ```

## 📊 Usage Guide

### Step 1: Download YouTube Comments

```bash
python src/youtube_comments_fetcher.py VIDEO_ID [options]
```

**Options**:
- `--mode`: Choose between `scraper` (default, no API needed) or `api` (requires Google API key)
- `--api_key`: Your Google API key (required if using API mode)
- `--max`: Maximum number of comments to download (default: 1000)

**Examples**:
```bash
# Using scraper mode (no API key needed)
python src/youtube_comments_fetcher.py SzXMacu80o8 --max 500

# Using API mode (requires Google API key)
python src/youtube_comments_fetcher.py SzXMacu80o8 --mode api --api_key YOUR_API_KEY --max 1000
```

The command will create a CSV file in the `data` directory: `youtube_comments_<VIDEO_ID>.csv`

### Step 2: Run Sentiment Analysis

Launch Jupyter Lab or Notebook:

```bash
jupyter lab
# or
jupyter notebook
```

Open and run the notebook: `notebooks/YouTube_Sentiment_Analysis_Workflow.ipynb`

The notebook will:
1. Load your comments data
2. Run sentiment analysis using pre-trained models
3. Generate visualizations
4. Save results back to your CSV file

### Understanding the Results

The sentiment model classifies comments into three categories:

| Label | Meaning | Description |
|-------|---------|-------------|
| `LABEL_0` | Positive | The comment expresses positive sentiment |
| `LABEL_1` | Neutral | The comment is neutral or factual |
| `LABEL_2` | Negative | The comment expresses negative sentiment |

Each analysis includes:
- Sentiment label
- Confidence score (0-1)
- Timestamp of analysis

## 📑 Output Format

The CSV output contains the following columns:

| Column | Description |
|--------|-------------|
| `video_id` | YouTube video ID |
| `author` | Comment author username |
| `published` | Comment publication timestamp |
| `text` | Raw comment text |
| `clean_text` | Preprocessed comment text |
| `sentiment_label` | Sentiment classification result |
| `sentiment_score` | Confidence score of the classification |
| `sentiment_analysis_at` | Timestamp of analysis |
| `extracted_at` | Timestamp of comment extraction |

## 🔧 Technical Details

### Models

The sentiment analysis uses [`w11wo/indonesian-roberta-base-sentiment-classifier`](https://huggingface.co/w11wo/indonesian-roberta-base-sentiment-classifier), a RoBERTa model fine-tuned for Indonesian sentiment analysis.

### Dependencies

Core dependencies include:
- `youtube-comment-downloader`: For scraping comments without API
- `google-api-python-client`: For API-based comment extraction
- `transformers` & `torch`: For running sentiment analysis models
- `pandas`: For data manipulation
- `matplotlib` & `seaborn`: For visualization
- `nltk` & `PySastrawi`: For Indonesian text processing
- `wordcloud`: For generating word clouds

See `environment.yml` for the complete list.

## 👥 Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -am 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

If you have any questions or suggestions, please open an issue in this repository.

---

Made with ❤️ for Indonesian NLP research