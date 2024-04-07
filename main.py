import pandas as pd


def find_best_days():
    results = []
    for i in range(1, 11):
        df = pd.read_csv(f"data_csv\\variant{i}.csv", sep="\t")

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        grouped = df.groupby(df["timestamp"].dt.to_period("M"))

        for name, group in grouped:
            if len(group) > 0 and name != list(grouped.groups.keys())[0] and name != list(grouped.groups.keys())[-1]:
                purchases = group[group["action"] == "confirmation"]
                if not purchases.empty:
                    best_day = purchases.groupby(purchases["timestamp"].dt.date)["value"].sum().idxmax()
                    best_value = purchases.groupby(purchases["timestamp"].dt.date)["value"].sum().max()
                    results.append([best_day, int(best_value)])

    results.sort(key=lambda x: x[0])

    with open("output.csv", "w", encoding="utf-8") as csv_file:
        csv_file.write("timestamp\tvalue\n")
        for result in results:
            csv_file.write('{}\t{}\n'.format(result[0], result[1]))


find_best_days()
