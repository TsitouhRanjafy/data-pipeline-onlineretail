from extract import extract
from transform import transform
from load import load
from datetime import datetime


def run():
    try:
        raw = extract("../../data/OnlineRetail.csv")
        aggregated = transform(raw)
        load(aggregated, f"../../warehouse/daily_online_retail_{datetime.now().date()}.csv")
    except Exception as e:
        print(e)


run()
