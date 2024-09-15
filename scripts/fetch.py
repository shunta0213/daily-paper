import arxiv
from pprint import pprint

import time
from datetime import datetime, timedelta
import os
import pandas as pd

client = arxiv.Client()


def get_arxiv(q, query):
    print(query)
    search = arxiv.Search(
        query=query,
        max_results=100,
    )

    data = pd.DataFrame(columns=["title", "id", "arxiv_url", "published"])
    for r in client.results(search):
        print(r.title)
        id = r.entry_id.split("/")[-1].split("v")[0]
        data_tmp = pd.DataFrame(
            {
                "title": r.title,
                "id": id,
                "arxiv_url": r.entry_id,
                "published": r.published,
            },
            index=[0],
        )
        data = pd.concat([data, data_tmp]).reset_index(drop=True)

    t = time.strftime("%Y%m%d")
    os.makedirs(f"./{q}/{t}", exist_ok=True)
    filename = f"./{q}/{t}/arxiv.csv"
    data.to_csv(filename)


if __name__ == "__main__":
    date = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
    cat = ["cs.AI", "quant-ph"]

    for q in cat:
        query = f"cat:{q} AND submittedDate:[{date} TO {date}235959]"
        get_arxiv(q, query)
