# =============================================================================
#                   EXPLORING THE INSIGHT OF EACH VARIABLE
# =============================================================================

# import modules
exec(open('import_modules.py').read())

# read file 
df = pd.read_csv('data.csv', encoding='ANSI',
                 dtype={'CustomerID' : str, 'InvoiceNo' : str})
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Explore

    # Countries in dataframe
temp = (df
        .filter(['CustomerID', 'InvoiceNo', 'Country'])
        .groupby(['CustomerID', 'InvoiceNo', 'Country'])
        .count()
        .reset_index(drop = False))
countries = temp['Country'].value_counts()

        # Customers and Products
pd.DataFrame([{'n_products' : len(df['StockCode'].unique()),
               'n_customers' : len(df['CustomerID'].unique()),
               'n_transitions' : len(df['InvoiceNo'].unique())
               }], 
             index = ['quantity'])

            # The number products of a basket
temp = (df 
        .groupby(['CustomerID', 'InvoiceNo'], as_index = False)
        .InvoiceDate.count()
        .rename(columns = {'InvoiceDate' : 'n_products_of_basket'})
        .sort_values(['n_products_of_basket']))

            # The number cancelling orders
temp['order_canceled'] = temp['InvoiceNo'].apply(lambda x: int('C' in x))
n_canceled = temp['order_canceled'].sum()
n = temp['order_canceled'].shape[0]
print('The number of orders canceled: {}/{} ({:.2f}%)'
      .format(n_canceled, n, n_canceled/n * 100))

            # Check canceled transactions in the dataframe, mostly identical
            # except for the Quantity and InvoiceDate variables.
df_check = (df
            .query('Quantity < 0 and Description != "Discount"')
            .filter(['CustomerID', 'Quantity', 'StockCode', 'Description', 'UnitPrice']))
for index, col in df_check.iterrows():
    if df[(df['CustomerID'] == col[0]) & (df['Quantity'] == -col[1]) 
          & (df['Description'] == col[2])].shape[0] == 0:
        print(df_check.loc[index])
        print(15*'-' + '>' + 'Hypothesis not fulfilled')
        break

df_clean = df.copy(deep = True)
df_clean['QuantityCanceled'] = 0
entry_to_remove = []
doubtfull_entry = []
for index, col in df.iterrows():
    if (col['Quantity'] > 0) or (col['Description'] == 'Discount'): continue
    df_test = df[(df['CustomerID'] == col['CustomerID']) &
                 (df['StockCode'] == col['StockCode']) &
                 (df['InvoiceDate'] < col['InvoiceDate']) &
                 (df['Quantity'] > 0)].copy()
            # Cancelation WITHOUT counterpart
    if (df_test.shape[0] == 0):
        doubtfull_entry.append(index)
            # Cancelation with a counterpart
    elif (df_test.shape[0] == 1):
        index_order = df_test.index[0]
        df_clean.loc[index_order, 'QuantityCanceled'] = -col['Quantity']
        entry_to_remove.append(index)
    elif (df_test.shape[0] > 1):
        df_test.sort_index(inplace = True, axis = 0, ascending = False)
        for ind, val in df_test.iterrows():
            if val['Quantity'] < -col['Quantity']: continue
            df_clean.loc[ind, 'QuantityCanceled'] = -col['Quantity']
            entry_to_remove.append(index)
            break

print('Entry to remove: {}'.format(len(entry_to_remove)),
      '\nDoubtfull entry: {}'.format(len(doubtfull_entry)))
 
df_clean.drop(entry_to_remove, axis = 0, inplace = True)
df_clean.drop(doubtfull_entry, axis = 0, inplace = True)

remaining_entries = df_clean[(df_clean['Quantity'] < 0) & (df_clean['StockCode'] != 'D')]

    # StockCode
list_special_codes = df_clean[df_clean['StockCode']
                              .str.contains('^[A-z]+', regex = True)]['StockCode'].unique()
for code in list_special_codes:
    print('{:<20} -> {:>30}'.format(code, df_clean[df_clean['StockCode'] == code]['Description']
                            .unique()[0]))

    # Basket price

df_clean['TotalPrice'] = df_clean['UnitPrice'] * (df_clean['Quantity'] - df_clean['QuantityCanceled'])
temp = (df_clean
        .groupby(['CustomerID', 'InvoiceNo'], as_index = False)
        .TotalPrice.sum())
basket_price = temp.rename(columns = {'TotalPrice' : 'BasketPrice'})

df_clean['InvD'] = df_clean['InvoiceDate'].astype('int64')
temp = (df_clean
        .groupby(['CustomerID', 'InvoiceNo'], as_index = False)
        .InvD.mean())
df_clean.drop('InvD', axis = 1, inplace = True)
basket_price.loc[:, 'InvoiceDate'] = pd.to_datetime(temp['InvD'])
basket_price = basket_price[basket_price['BasketPrice'] > 0]
        # plot
price_range = [0, 50, 200, 500, 1000, 2000, 5000, 40000]
count_price = []
for i, price in enumerate(price_range):
    if i == 0: continue
    val = basket_price[(basket_price['BasketPrice'] < price) &
                       (basket_price['BasketPrice'] > price_range[i - 1])]['BasketPrice'].count()
    count_price.append(val)

f, ax = plt.subplots(figsize=(11, 6))
colors = ['yellowgreen', 'gold', 'wheat', 'c', 'violet', 'royalblue','firebrick']
sizes = count_price
labels = [ '{}<.<{}'.format(price_range[i-1], s) for i,s in enumerate(price_range) if i != 0]
explode = [0.0 if sizes[i] < 200 else 0.0 for i in range(len(sizes))]
ax.pie(sizes, explode = explode, colors = colors,
       autopct = lambda x:'{:1.0f}%'.format(x) if x > 1 else '', 
       labels = labels)
















