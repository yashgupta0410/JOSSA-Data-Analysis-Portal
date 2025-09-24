import pandas as pd

year1='20'
for i in range(16,24):

    for j in range(1,7):
        df = pd.read_csv(f"./josaadata/20{i}round{j}.csv")
        df["year"] = year1+str(i)
        df["round"] = j
        df.to_csv(f'./josaadata/mixed/20{i}round{j}.csv', index=False)
