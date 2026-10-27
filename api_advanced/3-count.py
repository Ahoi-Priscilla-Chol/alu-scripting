#!/usr/bin/python3
"""Recursively counts keywords in the titles of a subreddit's hot posts."""
import requests


def print_counts(counts, words):
    """Print keyword totals, sorted by count (desc) then name (asc)."""
    totals = {}
    for word, num in counts.items():
        totals[word] = num * words.count(word)
    for word, num in sorted(totals.items(), key=lambda x: (-x[1], x[0])):
        if num > 0:
            print("{}: {}".format(word, num))


def count_words(subreddit, word_list, after=None, counts=None):
    """Query hot posts page by page and print sorted keyword counts.

    Prints nothing if the subreddit is invalid or no keywords match.
    """
    if counts is None:
        counts = {}
    if not subreddit or not isinstance(subreddit, str) or not word_list:
        return

    words = [w.lower() for w in word_list]
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "alu-scripting:count_words:v1.0 (by /u/alu_user)"}
    params = {"limit": 100}
    if after:
        params["after"] = after

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=10)
        if response.status_code != 200:
            print_counts(counts, words)
            return
        data = response.json().get("data", {})
    except (requests.RequestException, ValueError):
        print_counts(counts, words)
        return

    for post in data.get("children", []):
        title = post.get("data", {}).get("title", "")
        for token in title.lower().split():
            if token in words:
                counts[token] = counts.get(token, 0) + 1

    after = data.get("after")
    if after:
        return count_words(subreddit, word_list, after, counts)
    print_counts(counts, words)
