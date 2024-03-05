import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#load data
def load_data():
    data = pd.read_csv("main_data.csv")

    data['order_delivered_customer_date'] = pd.to_datetime(
        data['order_delivered_customer_date'], errors='coerce')
    data['order_purchase_timestamp'] = pd.to_datetime(
        data['order_purchase_timestamp'], errors='coerce')
    
    valid_dates = data.dropna(subset=['order_delivered_customer_date', 'order_purchase_timestamp'])
    valid_dates['delivery_time'] = (valid_dates['order_delivered_customer_date'] - valid_dates['order_purchase_timestamp']).dt.days

    filtered_df = valid_dates[valid_dates['delivery_time'] <= 90]

    delivery_review_relation = filtered_df.groupby('delivery_time')['review_score'].mean().reset_index()
    
    return data, delivery_review_relation

data, delivery_review_relation = load_data()

st.title('Visualisasi Data E-Commerce Public Dataset by Olist')

# preview
st.subheader('Preview Dataset')
st.write(data.head())

# slider untuk interaktif pemilihan kategori
max_price_limit = st.sidebar.slider('Batas maksimum harga:', 0, int(data['price'].max()), 1000)
max_freight_limit = st.sidebar.slider('Batas maksimum biaya pengiriman:', 0, int(data['freight_value'].max()), 1000)
max_count_limit = st.sidebar.slider('Batas maksimum jumlah pembelian:', 0, 4000, 4000)

# histogram harga
st.subheader(f'Distribusi Harga Produk (Harga sampai {max_price_limit})')
fig, ax = plt.subplots()
filtered_price_data = data[data['price'] <= max_price_limit]
sns.histplot(filtered_price_data['price'], kde=True, ax=ax, bins=50)
ax.set_xlim(0, max_price_limit) 
ax.set_ylim(0, max_count_limit)  
plt.title('Distribusi Harga Produk')
plt.xlabel('Harga Produk')
plt.ylabel('Jumlah')
st.pyplot(fig)

# histogram biaya pengirima
st.subheader(f'Distribusi Biaya Pengiriman (Biaya Pengiriman sampai {max_freight_limit})')
fig, ax = plt.subplots()
filtered_freight_data = data[data['freight_value'] <= max_freight_limit]
sns.histplot(filtered_freight_data['freight_value'], kde=True, ax=ax, bins=50)
ax.set_xlim(0, max_freight_limit) 
ax.set_ylim(0, max_count_limit)  
plt.title('Distribusi Biaya Pengiriman')
plt.xlabel('Biaya Pengiriman')
plt.ylabel('Jumlah')
st.pyplot(fig)

# hubungan antara harga dan skor ulasan
st.subheader('Hubungan antara Waktu Pengiriman dan Rating Ulasan')
fig, ax = plt.subplots()
sns.scatterplot(data=delivery_review_relation, x='delivery_time', y='review_score', ax=ax)
plt.title('Hubungan antara Waktu Pengiriman dan Rating Ulasan')
plt.xlabel('Waktu Pengiriman (hari)')
plt.ylabel('Rata-Rata Rating Ulasan')
st.pyplot(fig)

# menyimpan perubahan
if st.button('Save Changes to CSV'):
    data.to_csv("main_data.csv", index=False)
    st.success('Data saved successfully!')

# download link
with open("main_data.csv", "rb") as file:
    st.download_button(
        label="Download CSV",
        data=file,
        file_name="main_data.csv",
        mime="text/csv",
    )
