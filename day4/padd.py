import pandas as pd

import numpy as np
s= pd.Series()

print("pandas series: ", s)
data = np.array(['a', 'b', 'c', 'd'])

s= pd.Series(data)
print("pandas series:", s)


import pandas as pd

df = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'customer_name': ['Alice', 'Bob', 'Charlie'],
    'product_id': [101, 102, 103],
    'product_name': ['Widget', 'Gadget', 'Thingamajig'],
    'product_price': [19.99, 29.99, 39.99],

    'purchase_date': [pd.Timestamp('2024-01-01'), pd.Timestamp('2024-01-02'), pd.Timestamp('2024-01-03')]
})


print(df)


# check the data types in pandas using pandas.dataframe.select_dtypes() method