import pandas as pd
import numpy as np
from openpyxl.utils.dataframe import dataframe_to_rows

# Test how dataframe_to_rows handles None and NaN values
df = pd.DataFrame({
    'A': [1, 2],
    'B': [None, np.nan],
    'C': ['test', '']
})

print("Testing dataframe_to_rows with None, NaN, and empty string:")
for row in dataframe_to_rows(df, index=False, header=True):
    print(repr(row))
