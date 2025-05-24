from prepare_data import prepared_data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
 

data = pd.read_csv('ecommerce_data.csv')
df = prepared_data(data)


# Display specific data from order id: ORD-100033
df = df.set_index('order_id')
filtered_data = df.filter(like='ORD-100033', axis=0).filter(items=['customer_name', 'product'])
print(filtered_data)

# Display total Blender products
blender_data = df[df['product'] == 'Blender']
print(f'Total number of Blenders: {blender_data.shape[0]}')

# Sort data by Customer Name, Email and Product
sorted_data = df.sort_values(by=['customer_name', 'email', 'product'])
print(sorted_data[['customer_name', 'email', 'product']].head(10).to_string(index=False))

# Sample data
print(df.sample(n=5, random_state=42, replace=False))

# Data types
print(df.dtypes)

#Data stats

data_stats = {
    'mean': df['price_per_unit'].mean(),
    'median': df['price_per_unit'].median(),
    'mode': df['price_per_unit'].mode()[0],
    'min': df['price_per_unit'].min(),
    'max': df['price_per_unit'].max(),
    'count': df['price_per_unit'].count(),
}

for key, value in data_stats.items():
    print(f"{key}: {value}")

#Average price per category

avg_price_per_category = df.groupby("category")["price_per_unit"].mean().sort_values(ascending=False)
print("Average price per category is:\n", avg_price_per_category.round(2),'USD')

#product stats

product_stats = df.groupby('product').agg({
    'price_per_unit' : ['mean', 'median'],
})

print(product_stats.round(2).sort_values(by=('price_per_unit', 'mean'), ascending=False))

#date distribution

def plot_distribution_kde(df, column, title=None, xlabel=None):
    plt.figure(figsize=(10, 5))
    sns.kdeplot(df[column], fill=True, color="skyblue")
    plt.title(title or f"Distribution of {column}")
    plt.xlabel(xlabel or column)
    plt.ylabel("Count")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig('order_date.png')

#Product distribution

def plot_distribution_histplot(df, column, title=None, xlabel=None):
    plt.figure(figsize=(20, 5))
    sns.histplot(df[column], fill=True, color="skyblue")
    plt.title(title or f"Distribution of {column}")
    plt.xlabel(xlabel or column)
    plt.ylabel("Count")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig('products.png')


plot_distribution_kde(df, "order_date", title="Order date", xlabel="Order Date") #uniform distribution

plot_distribution_histplot(df, "product", title="Product", xlabel="Product")

