#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from sys import argv

from msg import *


def set_pref(modes: dict[int, str]) -> dict:
    args = argv[1:]
    preferences = {}

    if not args:
        print(welcome_msg)
        print(help_msg)
        print(startup_msg)
        delimiter_ch = int(input(prompt_msg))
        preferences["mode"] = modes[delimiter_ch]
        preferences["delimiter"] = input(prompt_msgs[delimiter_ch - 1])
        if post_num := input(post_number_msg):
            preferences["satisfied"] = int(post_num)
            return preferences
        preferences["satisfied"] = 5
        return preferences
    preferences["mode"] = modes[int(args[0])]
    preferences["delimiter"] = args[1]
    preferences["satisfied"] = args[2]
    return preferences


def get_response_from(page_number: int) -> BeautifulSoup:
    response = requests.get(f"https://news.ycombinator.com/news?p={page_number}")
    return BeautifulSoup(response.text, "html.parser")


def page_slider(page_number: int) -> zip:
    almighty_soup = get_response_from(page_number)
    news_text = almighty_soup.select(".titleline")
    news_sub = almighty_soup.select(".subtext")
    return zip(news_text, news_sub, strict=True)


def limit_slider(chance: int, final: list) -> int:
    if chance <= 1:
        print(
            f"\n=> the data you specified had only {len(final)} occurrences in the last 5 pages. it could take a long time to find the specified number of items, or they may not be found at all...\nDo you want to continue querying another 5 pages? [Y/n]"
        )
        if input(">> ").casefold() == "y":
            return 5
        return 0
    return chance - 1


def page_parser(raw_data: zip, preferences: dict):
    news_info = {}
    for news, sub in raw_data:

        news_link = news.findChild("a")
        news_info["headline"] = news_link.get_text()
        news_info["url"] = news_link.attrs.get("href", None)

        if "subline" in (subline := sub.findChild("span")).attrs.get("class", None):  # type: ignore
            news_info["poster"] = subline.select_one(".hnuser").get_text()  # type: ignore
            news_info["post_time"] = subline.select_one(".age").attrs.get("title", None).split("T")  # type: ignore
            try:
                news_info["vote_value"] = int(subline.select_one(".score").get_text().split(" ")[0])  # type: ignore
            except ValueError as e:
                if preferences["mode"] == "vote_value":
                    print(f"\n=> Minor Err: {e}\nMoving on...\n")
                    continue
                news_info["vote_value"] = 0
            try:
                news_info["comment_value"] = int(subline.findChildren("a")[-1].get_text().split("\xa0")[0])  # type: ignore
            except ValueError as e:
                if preferences["mode"] == "comment_value":
                    print(f"\n=> Minor Err: {e}\nMoving on...\n")
                    continue
                news_info["comment_value"] = 0

            yield news_info


def is_match(data: dict, conditions: dict) -> bool:
    if conditions["mode"] in ("comment_value", "vote_value"):
        return int(conditions["delimiter"]) <= data[conditions["mode"]]
    return conditions["delimiter"] in data[conditions["mode"]]


page = 1
threshold = 4
final_data = list()
query_mode = {
    1: "headline",
    2: "poster",
    3: "post_time",
    4: "vote_value",
    5: "comment_value",
}

user_pref = set_pref(query_mode)
res = page_slider(page)


if __name__ == "__main__":
    while len(final_data) < user_pref["satisfied"]:
        try:
            curr_item = next(page_parser(res, user_pref))
        except StopIteration:
            page += 1
            print(
                f"\n=> All matching data on page was consumed...\n=> Moving to HackerNews page: {page} ⏳\n"
            )
            threshold = limit_slider(threshold, final_data)
            if threshold:
                res = page_slider(page)
                continue
            print("\nOK! have a good day 👋")
            break
        else:
            if is_match(curr_item, user_pref):
                final_data.append(curr_item)
                print()
                for k, v in curr_item.items():
                    print(f"item {len(final_data)} {k}:\t\t {v}")
