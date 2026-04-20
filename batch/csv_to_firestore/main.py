from extract import extract
from transform import transform
from load import load
from datetime import datetime


def run():
    try:
        raw = extract("../../data/OnlineRetail.csv")
        aggregated = transform(raw)
        load(aggregated, "192.168.1.100:8082", "demo-event-app")
    except Exception as e:
        print(e)


run()
