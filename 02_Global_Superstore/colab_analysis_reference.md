# Colab Notebook Full Code & Analysis Reference

## Cell 0 (markdown)
# **IMPORT LIBRARY**

## Cell 1 (code)
``python
import kagglehub

# Download latest version
path = kagglehub.dataset_download("anandaramg/global-superstore")

print("Path to dataset files:", path)
``

## Cell 2 (code)
``python
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mtick
import os
``

## Cell 3 (code)
``python
filepath = os.path.join(path, 'Global Superstore.txt')
df = pd.read_csv(filepath, sep='\t')
``

## Cell 4 (code)
``python
df.info()

# cek missing value
df.isnull().sum()

# cek duplikat
df.duplicated().sum()
``

## Cell 5 (code)
``python
# Cek leading/trailing space
obj_cols = df.select_dtypes(include="object").columns
space_check = {}

for col in obj_cols:
    count = (df[col] != df[col].str.strip()).sum()
    if count > 0:
        space_check[col] = count

space_check
``

## Cell 6 (markdown)
# **DATA CLEANING**

## Cell 7 (code)
``python
def clean_data(filepath):
    # tampilin data
    filepath = os.path.join(path, 'Global Superstore.txt')
    df = pd.read_csv(filepath, sep='\t')
    df

    # Convert tipe kolom date dr object jadi datetime
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])

    # hapus kolom ga kepake
    cols_to_drop = ['è®°å½•æ•°', 'Row ID']
    df = df.drop(columns=cols_to_drop, errors='ignore')

    # hapus spasi di tipe kolom object
    obj_cols = df.select_dtypes(include='object').columns
    df[obj_cols] = df[obj_cols].apply(lambda x: x.str.strip())

    # hapus baris yang duplikat
    df = df.drop_duplicates()

    return df

superstore = clean_data(filepath)

# cek ulang
display(superstore.head(5))
superstore.info()
superstore.isnull().sum()

categorical_cols = [
    "Category",
    "Sub-Category",
    "Segment",
    "Region",
    "Market",
    "Ship Mode",
    "Order Priority",
    "Country",
    "State",
    "City"
]

for col in categorical_cols:
    print(f"\n===== {col} =====")
    print(sorted(superstore[col].unique()))
``

## Cell 8 (code)
``python
#feature engineering

#1. nambahin shipping days
superstore["Shipping_Days"] = (
    superstore["Ship Date"] - superstore["Order Date"]
).dt.days

#2. nambahin profit margin
superstore["Profit_Margin"] = np.where(
    superstore["Sales"] != 0,
    superstore["Profit"] / superstore["Sales"],
    0
)

#3. nambahin lost_flag
superstore["Loss_Flag"] = np.where(
    superstore["Profit"] < 0,
    "Loss",
    "Profit"
)
#4. nambahin discount group
bins = [-0.01,0,0.1,0.2,0.3,0.4,1]

labels = [
    "0%",
    "0-10%",
    "10-20%",
    "20-30%",
    "30-40%",
    "40%+"
]

superstore["Discount_Group"] = pd.cut(
    superstore["Discount"],
    bins=bins,
    labels=labels
)
#5. nambahin sales category
superstore["Sales_Category"] = pd.qcut(
    superstore["Sales"],
    q=3,
    labels=["Low","Medium","High"]
)
#6. nambahin Order month
superstore["Order_Month"] = superstore["Order Date"].dt.month_name()

#7. nambahin Order quater
superstore["Order_Quarter"] = (
    "Q" +
    superstore["Order Date"].dt.quarter.astype(str)
)
#7. nambahin Order year
superstore["Order_Year"] = superstore["Order Date"].dt.year

#7. nambahin Order Weekday
superstore["Order_Weekday"] = (
    superstore["Order Date"]
    .dt.day_name()
)
``

## Cell 9 (code)
``python
display(superstore.head(5))
``

## Cell 10 (markdown)
# **Analisis 1- Profit**

## Cell 11 (code)
``python
yearly_performance = superstore.groupby('Order_Year')[['Sales', 'Profit']].sum().reset_index()

print('Tren Sales dan Profit Tahunan:')
display(yearly_performance)

# Create a line chart for Sales and Profit
fig, ax1 = plt.subplots(figsize=(12, 7))

# Plot Sales
sns.lineplot(x='Order_Year', y='Sales', data=yearly_performance, marker='o', color='blue', ax=ax1, label='Total Sales')
ax1.set_xlabel('Tahun Pemesanan')
ax1.set_ylabel('Total Sales', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_title('Tren Sales dan Profit Tahunan')
ax1.grid(True, linestyle='--', alpha=0.7)

# Create a second y-axis for Profit
ax2 = ax1.twinx()
sns.lineplot(x='Order_Year', y='Profit', data=yearly_performance, marker='o', color='red', ax=ax2, label='Total Profit')
ax2.set_ylabel('Total Profit', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Combine legends
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.tight_layout()
plt.show()
``

## Cell 12 (markdown)
**Insight :** Total sales menunjukkan tren pertumbuhan yang konsisten dari tahun 2011 hingga 2014. Sejalan dengan itu, total profit juga terus meningkat. Hal ini menunjukkan bahwa peningkatan omzet masih diikuti oleh peningkatan laba perusahaan.

## Cell 13 (code)
``python
regional_yearly_profit = superstore.groupby(['Order_Year', 'Region'])['Profit'].sum().reset_index()

print('Tren Profit Tahunan per Region:')
display(regional_yearly_profit.style.format({'Profit': '${:,.2f}'}))

plt.figure(figsize=(14, 8))
sns.lineplot(x='Order_Year', y='Profit', hue='Region', data=regional_yearly_profit, marker='o')
plt.title('Tren Profit Tahunan per Region')
plt.xlabel('Tahun Pemesanan')
plt.ylabel('Total Profit')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(regional_yearly_profit['Order_Year'].unique())
plt.legend(title='Region')

# Format y-axis as currency
def currency_formatter(x, pos):
    return '${:,.0f}'.format(x)

formatter = FuncFormatter(currency_formatter)
plt.gca().yaxis.set_major_formatter(formatter)

plt.tight_layout()
plt.show()
``

## Cell 14 (markdown)
#**Analisis** **2**-**Profit** **Leakage** **Analysis**

## Cell 15 (code)
``python
#Untuk mengetahui skala atau seberapa besar masalah kerugian yang sedang dihadapi perusahaan secara keseluruhan.
loss_df = df[df["Profit"] < 0]

print("Jumlah transaksi rugi :", len(loss_df))
print("Total kerugian :", loss_df["Profit"].sum())
``

## Cell 16 (code)
``python
#Melihat total Kerugian tiap tahun nya
yearly_loss = superstore[superstore['Profit'] < 0].groupby('Order_Year')['Profit'].sum().reset_index()

print('Total Kerugian Tahunan:')
display(yearly_loss.style.format({'Profit': '${:,.2f}'}))

plt.figure(figsize=(10, 6))
sns.barplot(x='Order_Year', y='Profit', data=yearly_loss, palette='Reds')
plt.title('Total Kerugian Tahunan')
plt.xlabel('Tahun Pemesanan')
plt.ylabel('Total Kerugian')

def currency_formatter(x, pos):
    return '${:,.0f}'.format(x)

formatter = FuncFormatter(currency_formatter)
plt.gca().yaxis.set_major_formatter(formatter)

plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
``

## Cell 17 (code)
``python
regional_yearly_loss = superstore[superstore['Profit'] < 0].groupby(['Order_Year', 'Region'])['Profit'].sum().reset_index()

print('Total Kerugian Tahunan per Region:')
display(regional_yearly_loss.style.format({'Profit': '${:,.2f}'}))

plt.figure(figsize=(15, 8))
sns.lineplot(x='Order_Year', y='Profit', hue='Region', data=regional_yearly_loss, marker='o')
plt.title('Tren Total Kerugian Tahunan per Region')
plt.xlabel('Tahun Pemesanan')
plt.ylabel('Total Kerugian')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(regional_yearly_loss['Order_Year'].unique())
plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')

def currency_formatter(x, pos):
    return '${:,.0f}'.format(x)

formatter = FuncFormatter(currency_formatter)
plt.gca().yaxis.set_major_formatter(formatter)

plt.tight_layout()
plt.show()
``

## Cell 18 (markdown)
Disini terlihat kalo region central menjadi penyumbang profit tertinggi dan kerugian terbesar

## Cell 19 (markdown)
### Analisis Profit dan Kerugian di Regional 'Central'


## Cell 20 (code)
``python
# Filter profit dan loss untuk regional 'Central'
central_profit = regional_yearly_profit[regional_yearly_profit['Region'] == 'Central']
central_loss = regional_yearly_loss[regional_yearly_loss['Region'] == 'Central']

print("Profit Tahunan Regional 'Central':")
display(central_profit.style.format({'Profit': '${:,.2f}'}))

print("Kerugian Tahunan Regional 'Central':")
display(central_loss.style.format({'Profit': '${:,.2f}'}))

# Gabungkan profit dan loss untuk visualisasi yang lebih baik
central_summary = pd.merge(central_profit, central_loss, on=['Order_Year', 'Region'], suffixes=('_Profit', '_Loss'))
central_summary['Total Net Profit'] = central_summary['Profit_Profit'] + central_summary['Profit_Loss']

print("Ringkasan Profit dan Kerugian Tahunan Regional 'Central':")
display(central_summary.style.format({
    'Profit_Profit': '${:,.2f}',
    'Profit_Loss': '${:,.2f}',
    'Total Net Profit': '${:,.2f}'
}))

fig, ax = plt.subplots(figsize=(12, 7))

bar_width = 0.35
r1 = np.arange(len(central_summary['Order_Year']))
r2 = [x + bar_width for x in r1]

# Plot Profit dan Loss
plt.bar(r1, central_summary['Profit_Profit'], color='skyblue', width=bar_width, edgecolor='grey', label='Total Profit')
plt.bar(r2, central_summary['Profit_Loss'], color='salmon', width=bar_width, edgecolor='grey', label='Total Loss (Negatif)')

plt.xlabel('Tahun Pemesanan', fontweight='bold')
plt.ylabel('Amount', fontweight='bold')
plt.title('Profit vs. Loss Tahunan di Regional Central', fontweight='bold')
plt.xticks([r + bar_width / 2 for r in range(len(central_summary['Order_Year']))], central_summary['Order_Year'])
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

formatter = FuncFormatter(currency_formatter)
plt.gca().yaxis.set_major_formatter(formatter)

plt.tight_layout()
plt.show()
``

## Cell 21 (markdown)
Dari ringkasan di atas, terlihat bahwa **Regional Central** secara konsisten menghasilkan profit yang tinggi, namun juga menanggung kerugian yang signifikan setiap tahunnya. Hal ini menunjukkan bahwa ada transaksi-transaksi yang sangat menguntungkan di wilayah ini, tetapi juga ada sejumlah besar transaksi yang merugikan.  Fenomena ini sering terjadi pada wilayah dengan volume penjualan dan aktivitas bisnis yang tinggi.

Untuk memahami lebih lanjut, mari kita selidiki lebih dalam penyebab kerugian di Regional Central. Kita akan melihat kategori produk dan grup diskon yang paling banyak menyumbang kerugian.

## Cell 22 (code)
``python
central_region_data = superstore[superstore['Region'] == 'Central']

country_profit_central = central_region_data.groupby('Country')['Profit'].sum().reset_index()

print("Negara dengan Profit Tertinggi di Regional Central:")
display(country_profit_central.sort_values(by='Profit', ascending=False).head(10).style.format({'Profit': '${:,.2f}'}))

print("\nNegara dengan Kerugian Terbanyak di Regional Central:")
display(country_profit_central.sort_values(by='Profit', ascending=True).head(10).style.format({'Profit': '${:,.2f}'}))
``

## Cell 23 (code)
``python

``

## Cell 24 (code)
``python
# Filter transaksi merugi di Regional Central
central_loss_transactions = superstore[(superstore['Region'] == 'Central') & (superstore['Profit'] < 0)]

# Analisis kerugian berdasarkan Kategori Produk
loss_by_category_central = central_loss_transactions.groupby('Category')['Profit'].sum().sort_values()

print("Kerugian Berdasarkan Kategori Produk di Regional Central:")
display(loss_by_category_central.to_frame().style.format({'Profit': '${:,.2f}'}))

# Visualisasi kerugian berdasarkan Kategori Produk
fig = plt.figure(figsize=(10, 6))
sns.barplot(x=loss_by_category_central.index, y=loss_by_category_central.values, palette='viridis')
plt.title('Kerugian per Kategori Produk di Regional Central')
plt.xlabel('Kategori Produk')
plt.ylabel('Total Kerugian')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
formatter = FuncFormatter(currency_formatter)
plt.gca().yaxis.set_major_formatter(formatter)
plt.tight_layout()
plt.show()

``

## Cell 25 (code)
``python
# Analisis kerugian berdasarkan Grup Diskon di Regional Central
loss_by_discount_central = central_loss_transactions.groupby('Discount_Group')['Profit'].sum().sort_values()

print("Kerugian Berdasarkan Grup Diskon di Regional Central:")
display(loss_by_discount_central.to_frame().style.format({'Profit': '${:,.2f}'}))

# Visualisasi kerugian berdasarkan Grup Diskon
fig = plt.figure(figsize=(10, 6))
sns.barplot(x=loss_by_discount_central.index, y=loss_by_discount_central.values, palette='magma')
plt.title('Kerugian per Grup Diskon di Regional Central')
plt.xlabel('Grup Diskon')
plt.ylabel('Total Kerugian')
plt.grid(axis='y', linestyle='--', alpha=0.7)
formatter = FuncFormatter(currency_formatter)
plt.gca().yaxis.set_major_formatter(formatter)
plt.tight_layout()
plt.show()
``

## Cell 26 (code)
``python
# Identifikasi 10 negara dengan kerugian terbanyak
country_loss = superstore[superstore['Profit'] < 0].groupby('Country')['Profit'].sum().nsmallest(10).reset_index()

print("10 Negara dengan Kerugian Terbanyak:")
display(country_loss.style.format({'Profit': '${:,.2f}'}))

# Visualisasi 10 negara dengan kerugian terbanyak
fig = plt.figure(figsize=(12, 7))
sns.barplot(x='Country', y='Profit', data=country_loss, palette='rocket')
plt.title('10 Negara dengan Kerugian Terbanyak', fontweight='bold')
plt.xlabel('Negara', fontweight='bold')
plt.ylabel('Total Kerugian', fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)

formatter = FuncFormatter(currency_formatter)
plt.gca().yaxis.set_major_formatter(formatter)

plt.tight_layout()
plt.show()
``

## Cell 27 (code)
``python
#Definisikan "Loss Transaction"
loss_df = df[df["Profit"] < 0]

print(f"Jumlah transaksi rugi : {len(loss_df)}")
print(f"Total transaksi       : {len(df)}")

print(
    f"Persentase rugi : {(len(loss_df)/len(df))*100:.2f}%"
)

print(
    f"Total kerugian : {loss_df['Profit'].sum():,.2f}"
)
``

## Cell 28 (code)
``python
#Kategori mana yang menyumbang kerugian terbesar?
loss_category = (
    loss_df
    .groupby("Category")
    .agg(
        Total_Loss=("Profit", "sum"),
        Transactions=("Order ID", "count"),
        Avg_Loss=("Profit", "mean")
    )
    .sort_values("Total_Loss")
)

display(loss_category.style.format({'Total_Loss': '${:,.2f}', 'Avg_Loss': '${:,.2f}'}))

# Visualisasi kerugian berdasarkan Kategori Produk
fig = plt.figure(figsize=(10, 6))
sns.barplot(x=loss_category.index, y='Total_Loss', data=loss_category, palette='viridis')
plt.title('Total Kerugian per Kategori Produk')
plt.xlabel('Kategori Produk')
plt.ylabel('Total Kerugian')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
formatter = FuncFormatter(currency_formatter)
plt.gca().yaxis.set_major_formatter(formatter)
plt.tight_layout()
plt.show()
``

## Cell 29 (code)
``python
#Breakdown ke Sub Category
loss_subcategory = (
    loss_df
    .groupby(["Category", "Sub-Category"])
    .agg(
        Total_Loss=("Profit","sum"),
        Transactions=("Order ID","count")
    )
    .sort_values("Total_Loss")
)

display(loss_subcategory.style.format({'Total_Loss': '${:,.2f}'}))

# Visualisasi kerugian berdasarkan Sub Kategori
fig = plt.figure(figsize=(12, 7))
sns.barplot(x=loss_subcategory.index.get_level_values(1), y='Total_Loss', hue=loss_subcategory.index.get_level_values(0), data=loss_subcategory, palette='coolwarm', dodge=False)
plt.title('Total Kerugian per Sub-Kategori Produk')
plt.xlabel('Sub-Kategori Produk')
plt.ylabel('Total Kerugian')
plt.xticks(rotation=90, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
formatter = FuncFormatter(currency_formatter)
plt.gca().yaxis.set_major_formatter(formatter)
plt.legend(title='Kategori', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
``

## Cell 30 (code)
``python
#Breakdown ke Product
loss_product = (
    loss_df
    .groupby("Product Name")
    .agg(
        Total_Loss=("Profit","sum"),
        Transactions=("Order ID","count")
    )
    .sort_values("Total_Loss")
)

loss_product.head(20)
``

## Cell 31 (code)
``python
#Breakdown ke Customer
#mencari customer mana yang sering dapat diskon
loss_customer = (
    loss_df
    .groupby("Customer Name")
    .agg(
        Total_Loss=("Profit","sum"),
        Transactions=("Order ID","count")
    )
    .sort_values("Total_Loss")
)

loss_customer.head(10)
``

## Cell 32 (markdown)
oke disini US menjadi negara yang banyak membuat rugi perusahaan

## Cell 33 (code)
``python

``

## Cell 34 (markdown)
# **Analisis 3- Diskon**

## Cell 35 (code)
``python
#menacari tahu bentuk data diskonnya.
print(df["Discount"].describe())

print(df["Discount"].unique())
``

## Cell 36 (code)
``python
#Distribusi Discount
#mencari tahu apakah mayoritas transaksi memang menggunakan diskon.
discount_dist = (
    df["Discount"]
      .value_counts()
      .sort_index()
      .reset_index()
)

discount_dist.columns = ["Discount", "Transaction"]

# Convert 'Discount' to percentage string BEFORE plotting
discount_dist['Discount_Percentage'] = discount_dist['Discount'].apply(lambda x: f'{x:.0%}')

display(discount_dist)

# Visualisasi Distribusi Discount
fig = plt.figure(figsize=(14, 7))
sns.barplot(x='Discount_Percentage', y='Transaction', data=discount_dist, palette='crest')
plt.title('Distribusi Diskon Berdasarkan Jumlah Transaksi', fontweight='bold')
plt.xlabel('Nilai Diskon', fontweight='bold')
plt.ylabel('Jumlah Transaksi', fontweight='bold')

# The FuncFormatter is no longer needed as labels are pre-formatted
# plt.gca().xaxis.set_major_formatter(formatter)

plt.xticks(rotation=60, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
``

## Cell 37 (code)
``python
#Discount vs Average Profit
discount_profit = (
    df.groupby("Discount")
      .agg(
          Avg_Profit=("Profit","mean"),
          Total_Profit=("Profit","sum"),
          Avg_Sales=("Sales","mean"),
          Transactions=("Order ID","count")
      )
      .reset_index()
)

display(discount_profit)
``

## Cell 38 (code)
``python
discount_profit = (
    df.groupby("Discount")
      .agg(
          Avg_Profit=("Profit","mean"),
          Total_Profit=("Profit","sum"),
          Avg_Sales=("Sales","mean"),
          Transactions=("Order ID","count")
      )
      .reset_index()
)

plt.figure(figsize=(8,5))

plt.plot(
    discount_profit["Discount"],
    discount_profit["Avg_Profit"],
    marker="o"
)

plt.title("Average Profit by Discount")
plt.xlabel("Discount")
plt.ylabel("Average Profit")

plt.grid(True)

plt.show()
``

## Cell 39 (markdown)
# Kesimpulan nya mulai dari diskon 30% ke atas perusahaan mulai mengalami kerugian

## Cell 40 (code)
``python
#Korelasi Discount dan Profit
correlation = df["Discount"].corr(df["Profit"])

print(correlation)
``

## Cell 41 (markdown)
Kekuatan -0.3: Angka ini berada di kisaran 0.3, yang berarti hubungannya tidak mutlak kuat, namun cukup nyata untuk diperhatikan. Diskon bukan satu-satunya penentu kerugian (ada faktor lain seperti ongkos kirim, kategori produk, atau harga dasar), tetapi diskon memiliki tren pola yang jelas menurunkan keuntungan.

## Cell 42 (code)
``python
#scatter plot
#apakah titik rugi terkumpul pada diskon tinggi?
#apakah masih ada transaksi untung pada diskon tinggi?

plt.figure(figsize=(8,6))

plt.scatter(
    df["Discount"],
    df["Profit"],
    alpha=0.3
)

plt.axhline(
    y=0,
    color="red",
    linestyle="--"
)

plt.title("Discount vs Profit")

plt.xlabel("Discount")

plt.ylabel("Profit")

plt.show()
``

## Cell 43 (code)
``python
#Discount Group
#Agar lebih mudah dibaca, buat bucket.


bins = [-0.01,0,0.1,0.2,0.3,0.4,1]

labels = [
    "0%",
    "0-10%",
    "10-20%",
    "20-30%",
    "30-40%",
    "40%+"
]

df["Discount_Group"] = pd.cut(
    df["Discount"],
    bins=bins,
    labels=labels
)
``

## Cell 44 (code)
``python
discount_summary = (
    df.groupby("Discount_Group")
      .agg(
          Avg_Profit=("Profit","mean"),
          Total_Profit=("Profit","sum"),
          Sales=("Sales","sum"),
          Transactions=("Order ID","count")
      )
)



discount_summary["Avg_Profit"].plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Average Profit by Discount Group")
plt.show()
``

## Cell 45 (code)
``python
#Cross Analysis
#mencari tahu Kategori apa yang paling terdampak oleh diskon tinggi?

discount_category = (
    df.groupby(["Category","Discount_Group"])
      .agg(
          Avg_Profit=("Profit","mean"),
          Transactions=("Order ID","count")
      )
      .reset_index()
)

# Visualisasi rata-rata profit per kategori dan kelompok diskon
plt.figure(figsize=(12, 7))
sns.barplot(x='Discount_Group', y='Avg_Profit', hue='Category', data=discount_category, palette='viridis')
plt.title('Rata-rata Profit per Kelompok Diskon dan Kategori Produk')
plt.xlabel('Kelompok Diskon')
plt.ylabel('Rata-rata Profit')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title='Kategori')
plt.tight_layout()
plt.show()
``

## Cell 46 (code)
``python
high_discount_loss = df[
    (df["Discount"] >= 0.3) &
    (df["Profit"] < 0)
]

top_products = (
    high_discount_loss.groupby("Product Name")
    .agg(
        Total_Loss=("Profit","sum"),
        Transactions=("Order ID","count")
    )
    .sort_values("Total_Loss")
)

top_products.head(20)
``

## Cell 47 (code)
``python
product_name = "Cubify CubeX 3D Printer Double Head Print"
product_info = df[df["Product Name"] == product_name][["Sales", "Discount"]]

print(f"Informasi untuk produk: {product_name}")
display(product_info.style.format({'Sales': '${:,.2f}', 'Discount': '{:.2%}'}))
``

## Cell 48 (markdown)
# **Analisis 4 â€” Shipping Cost Impact Analysis**

## Cell 49 (code)
``python
#Pertama saya ingin tahu distribusi biaya kirim.
print(df["Shipping Cost"].describe())

import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))

plt.hist(
    df["Shipping Cost"],
    bins=30
)

plt.title("Distribution of Shipping Cost")

plt.xlabel("Shipping Cost")

plt.ylabel("Frequency")

plt.show()
``

## Cell 50 (code)
``python
#Shipping Cost vs Profit

plt.figure(figsize=(8,6))

plt.scatter(
    df["Shipping Cost"],
    df["Profit"],
    alpha=0.3
)

plt.axhline(
    y=0,
    color="red",
    linestyle="--"
)

plt.title("Shipping Cost vs Profit")

plt.xlabel("Shipping Cost")

plt.ylabel("Profit")

plt.show()
``

## Cell 51 (code)
``python
#Korelasi
correlation = df["Shipping Cost"].corr(df["Profit"])

print(correlation)
``

## Cell 52 (code)
``python
#Shipping Cost Ratio
#berapa persen Sales habis untuk shipping.

df["Shipping_Cost_Ratio"] = (
    df["Shipping Cost"] /
    df["Sales"]
)
``

## Cell 53 (code)
``python
#Cari Transaksi Tidak Efisien

inefficient_shipping = df[
    df["Shipping_Cost_Ratio"] > 0.30
]

inefficient_shipping.head()

print("Jumlah transaksi:", len(inefficient_shipping))

print("Profit rata-rata:")

print(
    inefficient_shipping["Profit"].mean()
)
``

## Cell 54 (code)
``python
#Shipping Cost per Ship Mode

shipmode = (
    df.groupby("Ship Mode")
      .agg(
          Avg_Shipping=("Shipping Cost","mean"),
          Avg_Profit=("Profit","mean"),
          Total_Sales=("Sales","sum"),
          Transactions=("Order ID","count")
      )
)

shipmode

shipmode["Avg_Shipping"].plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Average Shipping Cost by Ship Mode")

plt.show()
``

## Cell 55 (code)
``python
#Shipping Cost per Category

shipping_category = (
    df.groupby("Category")
      .agg(
          Avg_Shipping=("Shipping Cost","mean"),
          Avg_Profit=("Profit","mean")
      )
)

shipping_category
``

## Cell 56 (code)
``python
#Shipping Cost per Country

shipping_country = (
    df.groupby("Country")
      .agg(
          Avg_Shipping=("Shipping Cost","mean"),
          Avg_Profit=("Profit","mean")
      )
      .sort_values("Avg_Shipping", ascending=False)
)

shipping_country.head(20)
``

## Cell 57 (code)
``python
import matplotlib.pyplot as plt

#Shipping Days vs Shipping Cost

plt.figure(figsize=(8,6))

plt.scatter(
    superstore["Shipping_Days"],
    superstore["Shipping Cost"],
    alpha=0.3
)

plt.title("Shipping Days vs Shipping Cost")

plt.xlabel("Shipping Days")

plt.ylabel("Shipping Cost")

plt.show()
``

## Cell 58 (code)
``python
#Shipping Cost pada Transaksi Rugi

df["Loss_Flag"] = np.where(
    df["Profit"] < 0,
    "Loss",
    "Profit"
)

loss_shipping = (
    superstore.groupby("Loss_Flag")
      .agg(
          Avg_Shipping=("Shipping Cost","mean"),
          Avg_Profit=("Profit","mean")
      )
)

loss_shipping
``

## Cell 59 (markdown)
# **4.1 Seasonal Trend Analysis**

## Cell 60 (code)
``python


df['Order Date'] = pd.to_datetime(df['Order Date'])

df['Month'] = df['Order Date'].dt.month_name()
df['Month Number'] = df['Order Date'].dt.month

monthly_sales = (
    df.groupby(['Month Number','Month'])
      .agg(
          Total_Sales=('Sales','sum'),
          Total_Profit=('Profit','sum'),
          Total_Orders=('Order ID','nunique')
      )
      .reset_index()
      .sort_values('Month Number')
)

display(monthly_sales)

plt.figure(figsize=(14,5))
plt.plot(monthly_sales['Month'], monthly_sales['Total_Sales'], marker='o')
plt.xticks(rotation=45)
plt.title("Monthly Sales Trend")
plt.ylabel("Sales")
plt.grid(True)
plt.show()
``

## Cell 61 (markdown)
# **4.2 segmen analis**

## Cell 62 (code)
``python
segment_analysis = (
    df.groupby('Segment')
      .agg(
          Sales=('Sales','sum'),
          Profit=('Profit','sum'),
          Orders=('Order ID','nunique'),
          Customers=('Customer ID','nunique'),
          Quantity=('Quantity','sum')
      )
      .sort_values('Sales',ascending=False)
)

display(segment_analysis)

plt.figure(figsize=(8,5))

sns.barplot(
    data=segment_analysis.reset_index(),
    x='Segment',
    y='Sales'
)

plt.title("Sales by Segment")
plt.show()
``

## Cell 63 (markdown)
# **4.3 order priority**

## Cell 64 (code)
``python
priority = (
    df.groupby("Order Priority")
      .agg(
          Sales=('Sales','sum'),
          Profit=('Profit','sum'),
          Shipping_Cost=('Shipping Cost','mean'),
          Orders=('Order ID','nunique')
      )
      .sort_values('Sales',ascending=False)
)

display(priority)

plt.figure(figsize=(8,5))

sns.barplot(
    data=priority.reset_index(),
    x="Order Priority",
    y="Sales"
)

plt.title("Sales by Order Priority")
plt.show()
``

## Cell 65 (markdown)
# **4.4 ship mode**

## Cell 66 (code)
``python
plt.figure(figsize=(8,5))

sns.barplot(
    data=priority.reset_index(),
    x='Order Priority',
    y='Shipping_Cost'
)

plt.title("Average Shipping Cost")
plt.show()



ship_mode = (
    df.groupby("Ship Mode")
      .agg(
          Sales=('Sales','sum'),
          Profit=('Profit','sum'),
          Shipping_Cost=('Shipping Cost','mean'),
          Orders=('Order ID','nunique')
      )
      .sort_values('Sales',ascending=False)
)

display(ship_mode)

plt.figure(figsize=(10,5))

sns.barplot(
    data=ship_mode.reset_index(),
    x='Ship Mode',
    y='Sales'
)

plt.title("Sales by Ship Mode")
plt.show()

plt.figure(figsize=(10,5))

sns.barplot(
    data=ship_mode.reset_index(),
    x='Ship Mode',
    y='Profit'
)

plt.title("Profit by Ship Mode")
plt.show()

plt.figure(figsize=(10,5))

sns.barplot(
    data=ship_mode.reset_index(),
    x='Ship Mode',
    y='Shipping_Cost'
)

plt.title("Average Shipping Cost")
plt.show()


``

## Cell 67 (markdown)
# **Analisis 5 â€” Geographic Intelligence**

## Cell 68 (code)
``python
#Country Performance
#melihat performa tiap negara.

country_summary = (
    df.groupby("Country")
      .agg(
          Total_Sales=("Sales","sum"),
          Total_Profit=("Profit","sum"),
          Avg_Discount=("Discount","mean"),
          Avg_Shipping=("Shipping Cost","mean"),
          Orders=("Order ID","nunique")
      )
      .reset_index() # Add .reset_index() here to make 'Country' a column
      .sort_values("Total_Profit", ascending=False)
)

country_summary

#Insight yang dicari

#Jangan hanya melihat siapa yang paling untung.

#Cari juga:

#Negara dengan Sales tinggi tapi Profit rendah
#Negara dengan Sales rendah tapi Profit tinggi

#Karena itu menunjukkan efisiensi.
``

## Cell 69 (code)
``python
#Tambahkan Profit Margin

country_summary["Profit_Margin"] = (
    country_summary["Total_Profit"] /
    country_summary["Total_Sales"]
)

country_summary.sort_values(
    "Profit_Margin",
    ascending=False
)
``

## Cell 70 (code)
``python
#Bottom 10 Profit Country

bottom_profit = (
    country_summary
    .sort_values("Total_Profit")
    .head(10)
)

bottom_profit

bottom_profit["Total_Profit"].plot(
    kind="barh",
    figsize=(10,5)
)

plt.title("Top 10 Loss Countries")

plt.show()
``

## Cell 71 (code)
``python
# country_summary
country_summary = (
    superstore.groupby("Country")
    .agg(
        Total_Sales=("Sales","sum"),
        Total_Profit=("Profit","sum"),
        Total_Customers=("Customer ID","nunique")
    )
    .reset_index()
)

country_summary["Profit_Margin"] = (
    country_summary["Total_Profit"] /
    country_summary["Total_Sales"]
)

fig = px.scatter(
    country_summary,
    x="Total_Sales",
    y="Total_Profit",
    size="Total_Customers",
    color="Profit_Margin",
    hover_name="Country",
    title="Country Performance Matrix"
)

fig.show()
``

## Cell 72 (code)
``python
#Discount by Country

country_discount = (
    df.groupby("Country")
      .agg(
          Avg_Discount=("Discount","mean"),
          Profit=("Profit","sum")
      )
      .sort_values(
          "Avg_Discount",
          ascending=False
      )
)

country_discount.head(20)
``

## Cell 73 (markdown)
# **Analisis 6 â€” Customer Profitability Analysis**

## Cell 74 (code)
``python

#Customer Summary
#Pertama kita agregasi seluruh transaksi menjadi level customer.


customer = (
    df.groupby(["Customer ID", "Customer Name"])
      .agg(
          Total_Sales=("Sales","sum"),
          Total_Profit=("Profit","sum"),
          Total_Order=("Order ID","nunique"),
          Total_Quantity=("Quantity","sum"),
          Avg_Discount=("Discount","mean"),
          Avg_Shipping=("Shipping Cost","mean")
      )
      .reset_index()
)

customer.head()
#Top Customer

top_customer = customer.sort_values(
    "Total_Profit",
    ascending=False
)

top_customer.head(10)

``

## Cell 75 (code)
``python
#Worst Customer

worst_customer = customer.sort_values(
    "Total_Profit"
)

worst_customer.head(20)
``

## Cell 76 (code)
``python
#Customer Shipping Cost
customer_shipping = (
    customer
    .sort_values(
        "Avg_Shipping",
        ascending=False
    )
)

customer_shipping.head(20)
``

## Cell 77 (code)
``python
customer["Profit_Margin"] = (
    customer["Total_Profit"] /
    customer["Total_Sales"]
)

margin_rank = customer.sort_values(
    "Profit_Margin",
    ascending=False
)

margin_rank.head(20)
``

## Cell 78 (markdown)
# **Analisis 7 â€” Product Portfolio Analysis**


*   Produk apa yang menjadi "bintang" perusahaan?
*   Produk apa yang harus dipromosikan?
*   Produk apa yang harus dievaluasi atau bahkan dihentikan?







## Cell 79 (code)
``python
#Product Summary

product = (
    df.groupby(["Product ID", "Product Name"])
      .agg(
          Category=("Category","first"),
          Sub_Category=("Sub-Category","first"),
          Total_Sales=("Sales","sum"),
          Total_Profit=("Profit","sum"),
          Total_Quantity=("Quantity","sum"),
          Avg_Discount=("Discount","mean"),
          Avg_Shipping=("Shipping Cost","mean"),
          Total_Order=("Order ID","nunique")
      )
      .reset_index()
)

product.head()
``

## Cell 80 (code)
``python
#Top Product by Sales

top_sales = (
    product
    .sort_values("Total_Sales", ascending=False)
    .head(20)
)

top_sales

plt.figure(figsize=(12,6))

plt.barh(
    top_sales["Product Name"],
    top_sales["Total_Sales"]
)

plt.title("Top 20 Product by Sales")

plt.xlabel("Sales")

plt.gca().invert_yaxis()

plt.show()
``

## Cell 81 (code)
``python
#Top Product by Profit

top_profit = (
    product
    .sort_values("Total_Profit", ascending=False)
    .head(20)
)

top_profit

plt.figure(figsize=(12,6))

plt.barh(
    top_profit["Product Name"],
    top_profit["Total_Profit"]
)

plt.title("Top 20 Product by Profit")

plt.gca().invert_yaxis()

plt.show()
``

## Cell 82 (code)
``python
#Worst Product

worst_product = (
    product
    .sort_values("Total_Profit")
    .head(20)
)

worst_product

plt.figure(figsize=(12,6))

plt.barh(
    worst_product["Product Name"],
    worst_product["Total_Profit"]
)

plt.title("Top 20 Loss Product")

plt.gca().invert_yaxis()

plt.show()
``

## Cell 83 (code)
``python
#Temukan Problem Product

sales_threshold = product["Total_Sales"].quantile(0.75)

problem_product = product[
    (product["Total_Sales"] >= sales_threshold) &
    (product["Total_Profit"] < 0)
]

problem_product
``

## Cell 84 (code)
``python
#Discount Effect

problem_product.sort_values(
    "Avg_Discount",
    ascending=False
)
``

## Cell 85 (code)
``python
#Sub Category Analysis

subcategory = (
    product
    .groupby("Sub_Category")
    .agg(
        Sales=("Total_Sales","sum"),
        Profit=("Total_Profit","sum"),
        Quantity=("Total_Quantity","sum")
    )
    .sort_values("Profit", ascending=False)
)

subcategory

subcategory["Profit"].plot(
    kind="bar",
    figsize=(12,5)
)

plt.title("Profit by Sub Category")

plt.show()
``

## Cell 86 (code)
``python
customer["Profit_Margin"] = (
    customer["Total_Profit"] /
    customer["Total_Sales"]
)

product["Profit_Margin"] = (
    product["Total_Profit"] /
    product["Total_Sales"]
)

margin_rank = (
    product
    .sort_values("Profit_Margin", ascending=False)
)

margin_rank.head(20)
``

## Cell 87 (markdown)
# **Analisis - 8 Pareto Analysis (80/20 Rule)**

## Cell 88 (code)
``python
#Profit per Product

pareto = (
    df.groupby(["Product ID","Product Name"])
      .agg(
          Total_Profit=("Profit","sum"),
          Total_Sales=("Sales","sum"),
          Total_Order=("Order ID","nunique")
      )
      .reset_index()
)
``

## Cell 89 (code)
``python
#Urutkan berdasarkan Profit

pareto = pareto.sort_values(
    "Total_Profit",
    ascending=False
)
``

## Cell 90 (code)
``python
#Hitung Cumulative Profit

pareto["Cumulative_Profit"] = (
    pareto["Total_Profit"].cumsum()
)
``

## Cell 91 (code)
``python
#Hitung Persentase
total_profit = pareto["Total_Profit"].sum()

pareto["Cumulative_Percentage"] = (
    pareto["Cumulative_Profit"] /
    total_profit
) * 100
``

## Cell 92 (code)
``python
#Ranking
pareto["Rank"] = range(1, len(pareto)+1)
``

## Cell 93 (code)
``python
#Cari Titik 80%
pareto_80 = pareto[
    pareto["Cumulative_Percentage"] <= 80
]

pareto_80
``

## Cell 94 (code)
``python
print("Jumlah produk :",len(pareto))

print("Produk penyumbang 80% profit :",len(pareto_80))
``

## Cell 95 (code)
``python
#Kontribusi Profit per Category
category_profit = (
    df.groupby("Category")
      .agg(
          Profit=("Profit","sum")
      )
      .sort_values("Profit",ascending=False)
)

category_profit
``

## Cell 96 (code)
``python
#Pareto Loss
loss_product = (
    df[df["Profit"]<0]
    .groupby("Product Name")
    .agg(
        Total_Loss=("Profit","sum")
    )
    .sort_values("Total_Loss")
)
``

## Cell 97 (code)
``python
# Hitung cumulative loss
loss_product["Cum_Loss"] = (
    loss_product["Total_Loss"].cumsum()
)

loss_product["Cum_%"] = (
    loss_product["Cum_Loss"]/
    loss_product["Total_Loss"].sum()
)*100
``

## Cell 98 (code)
``python
# Karena Total_Loss bernilai negatif, lebih aman menggunakan nilai absolut agar persentase mudah diinterpretasikan:
loss_product = loss_product.sort_values("Total_Loss")

loss_product["Abs_Loss"] = loss_product["Total_Loss"].abs()

loss_product["Cum_Loss"] = loss_product["Abs_Loss"].cumsum()

loss_product["Cum_%"] = (
    loss_product["Cum_Loss"] /
    loss_product["Abs_Loss"].sum()
) * 100
``

## Cell 99 (markdown)
## Market Comparison

## Cell 100 (code)
``python
market_perf = superstore.groupby("Market", as_index=False).agg(
    total_sales=("Sales", "sum"),
    total_profit=("Profit", "sum"),
    total_orders=("Order ID", "nunique"),
    total_customers=("Customer ID", "nunique"),
)
market_perf["profit_margin_pct"] = (
    market_perf["total_profit"] / market_perf["total_sales"] * 100
).round(2)
market_perf = market_perf.sort_values("profit_margin_pct", ascending=False)
display(market_perf)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.barplot(data=market_perf, x="Market", y="total_sales", ax=axes[0], color="#4C72B0")
axes[0].set_title("Total Sales per Market")
axes[0].tick_params(axis="x", rotation=30)

sns.barplot(data=market_perf, x="Market", y="profit_margin_pct", ax=axes[1], color="#55A868")
axes[1].set_title("Profit Margin (%) per Market")
axes[1].tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.show()

if "Market2" in superstore.columns:
    market2_perf = superstore.groupby("Market2", as_index=False).agg(
        total_sales=("Sales", "sum"), total_profit=("Profit", "sum"),
    )
    market2_perf["profit_margin_pct"] = (
        market2_perf["total_profit"] / market2_perf["total_sales"] * 100
    ).round(2)
    display(market2_perf.sort_values("profit_margin_pct", ascending=False))
``

## Cell 101 (markdown)
## Profit Margin Analysis (Overall)

## Cell 102 (code)
``python
overall_margin = superstore["Profit"].sum() / superstore["Sales"].sum() * 100
print(f"Overall Profit Margin seluruh dataset: {overall_margin:.2f}%")

margin_by_year = superstore.groupby("Order_Year", as_index=False).agg(
    total_sales=("Sales", "sum"),
    total_profit=("Profit", "sum"),
)
margin_by_year["profit_margin_pct"] = (
    margin_by_year["total_profit"] / margin_by_year["total_sales"] * 100
)
margin_by_year = margin_by_year.round(2)
display(margin_by_year)

plt.figure(figsize=(10, 6))
sns.lineplot(data=margin_by_year, x="Order_Year", y="profit_margin_pct", marker="o",
             color="#C44E52")
plt.axhline(overall_margin, color="gray", linestyle="--",
            label=f"Rata-rata keseluruhan ({overall_margin:.1f}%)")
plt.title("Tren Profit Margin (%) per Tahun", fontweight="bold")
plt.ylabel("Profit Margin (%)")
plt.xlabel("Tahun")
plt.legend()
plt.tight_layout()
plt.show()

margin_by_category = superstore.groupby("Category", as_index=False).agg(
    total_sales=("Sales", "sum"),
    total_profit=("Profit", "sum"),
)
margin_by_category["profit_margin_pct"] = (
    margin_by_category["total_profit"] / margin_by_category["total_sales"] * 100
)
margin_by_category = margin_by_category.round(2)
display(margin_by_category.sort_values("profit_margin_pct"))
``

## Cell 103 (code)
``python
import matplotlib.pyplot as plt
import seaborn as sns

# Create a new column for absolute loss in yearly_loss
yearly_loss_abs = yearly_loss.copy()
yearly_loss_abs['Total_Loss'] = yearly_loss_abs['Profit'].abs()

# Merge yearly_performance and yearly_loss_abs
yearly_combined = pd.merge(
    yearly_performance,
    yearly_loss_abs[['Order_Year', 'Total_Loss']],
    on='Order_Year',
    how='left'
)

# Rename columns for clarity in plotting
yearly_combined = yearly_combined.rename(columns={
    'Sales': 'Total Sales',
    'Profit': 'Total Profit'
})

# Plotting
fig, ax1 = plt.subplots(figsize=(12, 7))

# Plot Total Sales on the first y-axis
sns.lineplot(x='Order_Year', y='Total Sales', data=yearly_combined, marker='o', color='blue', ax=ax1, label='Total Sales')
ax1.set_xlabel('Tahun Pemesanan')
ax1.set_ylabel('Total Sales', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_title('Tren Sales, Profit, dan Loss Tahunan')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.set_xticks(yearly_combined['Order_Year'].unique()) # Ensure all years are shown as ticks

# Create a second y-axis for Total Profit and Total Loss
ax2 = ax1.twinx()

sns.lineplot(x='Order_Year', y='Total Profit', data=yearly_combined, marker='o', color='green', ax=ax2, label='Total Profit')
sns.lineplot(x='Order_Year', y='Total_Loss', data=yearly_combined, marker='o', color='red', ax=ax2, label='Total Loss')

ax2.set_ylabel('Total Profit / Total Loss', color='black') # Combined label for ax2
ax2.tick_params(axis='y', labelcolor='black')

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.show()
``

## Cell 104 (markdown)
# **DASHBOARD**

## Cell 105 (markdown)
## Executive Summary

## Cell 106 (code)
``python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ======================================================
# KPI & DATA PREPARATION
# ======================================================

sales = superstore["Sales"].sum()
profit = superstore["Profit"].sum()
margin = profit / sales
orders = superstore["Order ID"].nunique()
customers = superstore["Customer ID"].nunique()

loss_df = superstore[superstore["Profit"] < 0]
total_loss_all = loss_df["Profit"].sum()

yearly_performance = superstore.groupby("Order_Year", as_index=False).agg(
    Sales=("Sales", "sum"), Profit=("Profit", "sum")
)
yearly_performance["Margin"] = (
    yearly_performance["Profit"] / yearly_performance["Sales"]
)

yearly_loss = loss_df.groupby("Order_Year", as_index=False).agg(
    Profit=("Profit", "sum")
)
yearly_loss_abs = yearly_loss.copy()
yearly_loss_abs["Total_Loss"] = yearly_loss_abs["Profit"].abs()

yearly_combined = pd.merge(
    yearly_performance,
    yearly_loss_abs[["Order_Year", "Total_Loss"]],
    on="Order_Year",
    how="left",
)
yearly_combined["Total_Loss"] = yearly_combined["Total_Loss"].fillna(0)
yearly_combined = yearly_combined.rename(
    columns={"Sales": "Total Sales", "Profit": "Total Profit"}
)

region = (
    superstore.groupby("Region", as_index=False)
    .agg(Profit=("Profit", "sum"))
    .sort_values("Profit", ascending=True)
)
best_region = region.sort_values("Profit", ascending=False).iloc[0]["Region"]

product_margin = superstore.groupby("Product Name", as_index=False).agg(
    Sales=("Sales", "sum"), Profit=("Profit", "sum")
)
product_margin["Margin"] = (
    product_margin["Profit"] / product_margin["Sales"]
)

top_margin = product_margin.sort_values("Margin", ascending=False).head(10)
top_margin["Product Name Short"] = top_margin["Product Name"].str[:18]

# ======================================================
# FIGURE & LAYOUT (SUBGRIDSPEC)
# ======================================================

fig = plt.figure(figsize=(18, 16), constrained_layout=True)

# Grid Utama (4 Baris)
gs = fig.add_gridspec(4, 1, height_ratios=[0.5, 2, 2, 1.3])

# Subgrid khusus untuk masing-masing baris
gs_kpi = gs[0].subgridspec(1, 5, wspace=0.15)  # 5 KPI Cards Rata
gs_row1 = gs[1].subgridspec(1, 2, wspace=0.25)  # Sales Trend & Region
gs_row2 = gs[2].subgridspec(
    1, 2, wspace=0.25
)  # Profit vs Margin & Top 10 Centered
gs_row3 = gs[3].subgridspec(1, 1)  # Executive Insights

# ======================================================
# KPI CARDS (DIBENARKAN & DIPERBESAR)
# ======================================================

kpi = [
    ("TOTAL SALES", f"${sales:,.0f}"),
    ("TOTAL PROFIT", f"${profit:,.0f}"),
    ("PROFIT MARGIN", f"{margin:.2%}"),
    ("ORDERS", f"{orders:,}"),
    ("CUSTOMERS", f"{customers:,}"),
]

for col_idx, (title, value) in enumerate(kpi):
    ax_kpi = fig.add_subplot(gs_kpi[0, col_idx])

    # Background Card Box
    ax_kpi.add_patch(
        plt.Rectangle(
            (0, 0),
            1,
            1,
            facecolor="#F3F1FA",
            edgecolor="#D1CBE5",
            linewidth=1.5,
            transform=ax_kpi.transAxes,
            clip_on=False,
        )
    )

    # Angka / Value
    ax_kpi.text(
        0.5,
        0.58,
        value,
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="#1A1440",
    )

    # Label / Title
    ax_kpi.text(
        0.5,
        0.25,
        title,
        ha="center",
        va="center",
        fontsize=9,
        fontweight="bold",
        color="#6B6785",
    )

    ax_kpi.set_xlim(0, 1)
    ax_kpi.set_ylim(0, 1)
    ax_kpi.axis("off")

# ======================================================
# ROW 1, LEFT â€” Sales, Profit & Loss Trend
# ======================================================

ax1 = fig.add_subplot(gs_row1[0, 0])

sns.lineplot(
    x="Order_Year",
    y="Total Sales",
    data=yearly_combined,
    marker="o",
    color="#FFB703",
    ax=ax1,
    label="Total Sales",
)

ax1.set_xlabel("Tahun Pemesanan")
ax1.set_ylabel("Total Sales", color="#FFB703")
ax1.tick_params(axis="y", labelcolor="#FFB703")
ax1.set_title(
    "Tren Sales, Profit, dan Loss Tahunan",
    fontsize=12,
    fontweight="bold",
    loc="left",
)
ax1.grid(True, linestyle="--", alpha=0.3)
ax1.set_xticks(yearly_combined["Order_Year"].unique())

ax1_twin = ax1.twinx()

sns.lineplot(
    x="Order_Year",
    y="Total Profit",
    data=yearly_combined,
    marker="o",
    color="#06D6A0",
    ax=ax1_twin,
    label="Total Profit",
)

sns.lineplot(
    x="Order_Year",
    y="Total_Loss",
    data=yearly_combined,
    marker="o",
    color="#EF476F",
    ax=ax1_twin,
    label="Total Loss",
)

ax1_twin.set_ylabel("Total Profit / Total Loss", color="#333333")
ax1_twin.tick_params(axis="y", labelcolor="#333333")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()

ax1_twin.legend(
    lines1 + lines2,
    labels1 + labels2,
    loc="upper left",
    frameon=False,
    fontsize=9,
)
if ax1.get_legend():
    ax1.get_legend().remove()

# ======================================================
# ROW 1, RIGHT â€” Profit by Region
# ======================================================

ax_region = fig.add_subplot(gs_row1[0, 1])

ax_region.barh(region["Region"], region["Profit"], color="#118AB2")
ax_region.set_title(
    "Profit by Region", fontsize=12, fontweight="bold", loc="left"
)
ax_region.tick_params(axis="y", labelsize=9)
ax_region.grid(axis="x", linestyle="--", alpha=0.3)

# ======================================================
# ROW 2, RIGHT â€” Top 10 Products (DITENGAHKAN / DITERAPKAN RAPI)
# ======================================================

ax_top = fig.add_subplot(gs_row2[0, 1])

ax_top.barh(
    top_margin["Product Name Short"], top_margin["Margin"], color="#06D6A0"
)

ax_top.set_title(
    "Top 10 Products by Margin", fontsize=12, fontweight="bold", loc="left"
)
ax_top.invert_yaxis()
ax_top.tick_params(axis="y", labelsize=9)
ax_top.xaxis.set_major_formatter(lambda x, _: f"{x:.0%}")
ax_top.grid(axis="x", linestyle="--", alpha=0.3)

# ======================================================
# EXECUTIVE INSIGHT
# ======================================================

ax3 = fig.add_subplot(gs_row3[0, 0])
ax3.axis("off")

# ======================================================
# DASHBOARD
# ======================================================

# ======================================================
# PREPARE DATA
# ======================================================

# country_summary
country_summary = (
    superstore.groupby("Country")
    .agg(
        Total_Sales=("Sales","sum"),
        Total_Profit=("Profit","sum"),
        Total_Customers=("Customer ID","nunique")
    )
    .reset_index()
)

country_summary["Profit_Margin"] = (
    country_summary["Total_Profit"] /
    country_summary["Total_Sales"]
)

``

## Cell 107 (code)
``python
# ======================================================
# DASHBOARD
# ======================================================

# ======================================================
# PREPARE DATA
# ======================================================

# country_summary
country_summary = (
    superstore.groupby("Country")
    .agg(
        Total_Sales=("Sales","sum"),
        Total_Profit=("Profit","sum"),
        Total_Customers=("Customer ID","nunique")
    )
    .reset_index()
)

country_summary["Profit_Margin"] = (
    country_summary["Total_Profit"] /
    country_summary["Total_Sales"]
)

# ------------------------------------------------------
# Worst Sub Category
# ------------------------------------------------------

subcategory = (
    superstore.groupby("Sub-Category")
    .agg(
        Profit=("Profit","sum")
    )
    .sort_values("Profit")
    .head(10)
)

# ------------------------------------------------------
# Discount vs Margin
# ------------------------------------------------------

discount_margin = (
    superstore.groupby("Discount")
    .agg(
        Margin=("Profit_Margin","mean")
    )
    .reset_index()
)

# ------------------------------------------------------
# Investment Priority
# ------------------------------------------------------

top_country = (
    country_summary.sort_values(
        "Total_Profit",
        ascending=False
    )
    .iloc[0]["Country"]
)

worst_product = (
    subcategory.index[0]
)

# ======================================================
# FIGURE
# ======================================================

fig = plt.figure(figsize=(18,10))

gs = GridSpec(
    3,
    4,
    figure=fig,
    height_ratios=[2.2,2.8,1.4],
    hspace=0.45,
    wspace=0.35
)

# ======================================================
# CHART 1
# Worst Products
# ======================================================

ax1 = fig.add_subplot(gs[0,0:2])

ax1.barh(
    subcategory.index,
    subcategory["Profit"],
    color="#E84A5F"
)

ax1.set_title(
    "Top 10 Lowest Profit Sub-Categories",
    fontsize=12,
    weight="bold",
    loc="left"
)

ax1.grid(axis="x",alpha=.3)

ax1.axvline(
    0,
    color="black",
    linewidth=1
)

# ======================================================
# CHART 2
# Discount vs Margin
# ======================================================

ax2 = fig.add_subplot(gs[0,2:4])

ax2.scatter(
    discount_margin["Discount"]*100,
    discount_margin["Margin"]*100,
    s=70,
    color="#118AB2"
)

ax2.plot(
    discount_margin["Discount"]*100,
    discount_margin["Margin"]*100,
    color="#118AB2",
    alpha=.5
)

ax2.set_title(
    "Discount vs Profit Margin",
    fontsize=12,
    weight="bold",
    loc="left"
)

ax2.set_xlabel("Discount (%)")
ax2.set_ylabel("Profit Margin (%)")

ax2.grid(alpha=.3)

# ======================================================
# CHART 3
# Country Bubble
# ======================================================

ax3 = fig.add_subplot(gs[1,:])

bubble = ax3.scatter(

    country_summary["Total_Sales"],

    country_summary["Total_Profit"],

    s=country_summary["Total_Customers"]*3,

    c=country_summary["Profit_Margin"],

    cmap="viridis",

    alpha=.7

)

plt.colorbar(
    bubble,
    ax=ax3,
    label="Profit Margin"
)

ax3.set_title(

    "Country Performance Matrix",

    fontsize=13,

    weight="bold",

    loc="left"

)

ax3.set_xlabel("Total Sales")

ax3.set_ylabel("Total Profit")

ax3.grid(alpha=.3)

# Label Top 10 Profit Country

top10 = country_summary.nlargest(10,"Total_Profit")

for _,row in top10.iterrows():

    ax3.text(

        row["Total_Sales"],

        row["Total_Profit"],

        row["Country"],

        fontsize=8

    )
``


