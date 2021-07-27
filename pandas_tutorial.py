import numpy as np

import pandas as pd

# create a series

s = pd.Series([1,3,4,5, np.nan,6,8])

print(s)

dates = pd.date_range("20210101", periods=6)

df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list("ABCD"))

df.sort_index(axis=1, ascending=False)

print(df[df["A"] > 0])

