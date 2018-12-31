import re
from typing import List

VK_MAXIMUM_POSTS = 100


def remove_anything_except_punctuation(word: str) -> str:
    """Removes anything except punctuation"""
    regex = re.compile('(?![\w.\-\?:,\'\"\(\)])')
    return regex.sub('', word)


def retreive_n_posts(api, group_id: int, count: int) -> List[str]:
    """Returns count of posts from group with group_id using api"""
    posts = []
    for offset in range(1, count, VK_MAXIMUM_POSTS):
        response = api.wall.get(owner_id=-group_id,
                                count=VK_MAXIMUM_POSTS,
                                offset=offset)
        posts += [item["text"] for item in response["items"]]
    return posts
