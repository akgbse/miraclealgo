def log_trade(data):
    with open("trades.csv", "a") as f:
        f.write(",".join(str(v) for v in data.values()) + "\n")
# CSV log function placeholder
