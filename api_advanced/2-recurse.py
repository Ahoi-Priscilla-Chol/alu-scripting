#!/usr/bin/python3
"""Recursively queries the Reddit API and returns titles of all hot posts."""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """Return a list of titles of all hot posts for a given subreddit.

    Returns None if the subreddit is invalid or no results are found.
    """
    if hot_list is None:
        hot_list = []
    if not subreddit or not isinstance(subreddit, str):
        return None

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "alu-scripting:recurse:v1.0 (by /u/alu_student)"}
    params = {"limit": 100}
    if after:
        params["after"] = after

    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=10)
        if response.status_code != 200:
            return hot_list if hot_list else None
        data = response.json().get("data", {})
    except (requests.RequestException, ValueError):
        return hot_list if hot_list else None

    for post in data.get("children", []):
        hot_list.append(post.get("data", {}).get("title"))

    after = data.get("after")
    if after:
        return recurse(subreddit, hot_list, after)
    return hot_list if hot_list else None
