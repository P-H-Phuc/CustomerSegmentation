# =============================================================================
# Customer Segmentation 
# =============================================================================

# import modules
import import_modules
import_modules.import_modules()

# read file 
df = pd.read_csv('data.csv', encoding='ANSI',
                 dtype={'CustomerID' : str, 'InvoiceNo' : str})
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Exploring the content of variables

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

























































