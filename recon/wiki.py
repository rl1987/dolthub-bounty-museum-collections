#!/usr/bin/python3

import pandas as pd

def main():
    dfs = pd.read_html("https://en.wikipedia.org/wiki/List_of_largest_art_museums")
    df = dfs[0]
    print(df)
    df.to_csv("wiki_largest_art_museums.csv")

    dfs = pd.read_html("https://en.wikipedia.org/wiki/List_of_most-visited_art_museums")
    df = dfs[0]
    print(df)
    df.to_csv("wiki_most_visited_art_museums.csv")

    dfs = pd.read_html("https://en.wikipedia.org/wiki/List_of_most-visited_museums_in_the_United_States")
    df = dfs[0]
    print(df)
    df.to_csv("wiki_usa_most_visited_museums.csv")

    dfs = pd.read_html("https://en.wikipedia.org/wiki/List_of_most_visited_museums_in_the_United_Kingdom")
    df = dfs[0]
    print(df)
    df.to_csv("wiki_uk_most_visited_museums.csv")

    dfs = pd.read_html("https://en.wikipedia.org/wiki/List_of_most-visited_museums")
    df = dfs[0]
    print(df)
    df.to_csv("wiki_global_most_visited_museums.csv")

if __name__ == "__main__":
    main()

