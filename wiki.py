#!/usr/bin/python3

import pandas as pd

def main():
    dfs = pd.read_html("https://en.wikipedia.org/wiki/List_of_largest_art_museums")
    df = dfs[0]
    print(df)
    df.to_csv("wiki.csv")

if __name__ == "__main__":
    main()

