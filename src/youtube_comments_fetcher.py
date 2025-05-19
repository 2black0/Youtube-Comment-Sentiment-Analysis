#!/usr/bin/env python3
"""
youtube_comments_fetcher.py
-------------------------------------------------
Download YouTube comments using just the video ID (11 characters).

• DEFAULT MODE: "scraper"  →  No API needed (youtube-comment-downloader)
• "api" MODE: YouTube Data API v3  →  Requires Google API_KEY

Result is automatically saved to:  data/comments_<videoID>_<timestamp>.csv
"""

import csv
import argparse
from datetime import datetime
import pandas as pd
from tqdm import tqdm

# ---------- MODE 1 : Scraper (tanpa API) ----------
def download_comments_scraper(video_id: str,
                              max_comments: int | None = None,
                              sort: str = "popular") -> list[dict]:
    """
    Ambil komentar memakai youtube-comment-downloader.
    sort = "popular" (default) atau "recent"
    """
    from youtube_comment_downloader import (
        YoutubeCommentDownloader,
        SORT_BY_POPULAR,
        SORT_BY_RECENT,
    )

    sort_flag = SORT_BY_POPULAR if sort == "popular" else SORT_BY_RECENT
    dl = YoutubeCommentDownloader()
    gen = dl.get_comments(video_id, sort_by=sort_flag)

    rows = []
    for i, c in enumerate(tqdm(gen, desc="Mengunduh")):
        rows.append(
            {
                "author": c["author"],
                "published": c["time"],
                "text": c["text"],
            }
        )
        if max_comments and i + 1 >= max_comments:
            break
    return rows


# ---------- MODE 2 : YouTube Data API v3 ----------
def download_comments_api(video_id: str,
                          api_key: str,
                          max_comments: int = 1000,
                          order: str = "relevance") -> list[dict]:
    """Ambil komentar via YouTube Data API v3."""
    from googleapiclient.discovery import build

    yt = build("youtube", "v3", developerKey=api_key)
    rows, next_token = [], None
    with tqdm(total=max_comments, desc="Mengunduh") as bar:
        while len(rows) < max_comments:
            req = yt.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                order=order,
                pageToken=next_token,
            )
            res = req.execute()
            for item in res["items"]:
                snip = item["snippet"]["topLevelComment"]["snippet"]
                rows.append(
                    {
                        "author": snip["authorDisplayName"],
                        "published": snip["publishedAt"],
                        "text": snip["textDisplay"],
                    }
                )
                bar.update(1)
                if len(rows) >= max_comments:
                    break
            next_token = res.get("nextPageToken")
            if not next_token:
                break
    return rows


# ---------- UTIL : Save CSV ----------
def save_csv(rows: list[dict], vid: str) -> str:
    import os
    
    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Create DataFrame with original text
    df = pd.DataFrame(rows)
    
    # Add preprocessing to clean the text for analysis
    df['clean_text'] = df['text'].apply(preprocess_text)
    
    # Add metadata columns
    df['video_id'] = vid
    df['extracted_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Add empty sentiment columns for later analysis
    df['sentiment_score'] = ""
    df['sentiment_label'] = ""
    df['sentiment_analysis_at'] = ""
    
    # Reorder columns for better readability
    columns_order = [
        'video_id', 'author', 'published', 'text', 'clean_text',
        'sentiment_label', 'sentiment_score', 'sentiment_analysis_at',
        'extracted_at'
    ]
    df = df[columns_order]
    
    # Save with consistent format
    fname = os.path.join(data_dir, f"youtube_comments_{vid}.csv")
    df.to_csv(fname, index=False, quoting=csv.QUOTE_ALL, encoding='utf-8')
    return fname


def preprocess_text(text: str) -> str:
    """
    Simple preprocessing for text analysis.
    - Remove URLs
    - Remove special characters
    - Remove extra spaces
    """
    import re
    
    # Convert to string (in case it's not)
    text = str(text)
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove special characters except basic punctuation
    text = re.sub(r'[^\w\s.,!?]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


# ---------- CLI ----------
if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Unduh komentar YouTube dengan satu ID video"
    )
    ap.add_argument("video_id", help="ID video YouTube (mis. SzXMacu80o8)")
    ap.add_argument(
        "--mode",
        choices=["scraper", "api"],
        default="scraper",
        help="scraper = tanpa API (default), api = YouTube Data API v3",
    )
    ap.add_argument("--api_key", help="API key Google (wajib jika --mode api)")
    ap.add_argument(
        "--max",
        type=int,
        default=1000,
        help="Maksimum komentar yang diambil (default 1000)",
    )
    args = ap.parse_args()

    if args.mode == "api":
        if not args.api_key:
            ap.error("Mode api butuh --api_key")
        comments = download_comments_api(args.video_id, args.api_key, args.max)
    else:
        comments = download_comments_scraper(args.video_id, args.max)

    out = save_csv(comments, args.video_id)
    print(f"Done! Comments saved to →  {out}")
