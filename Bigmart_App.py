import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# ==============================
# DB CONNECTION
# ==============================
engine = create_engine("mysql+mysqlconnector://ml_user:1234@localhost/big_mart")

df = pd.read_sql("bigmart_with_predictions", con=engine)

# ==============================
# TITLE
# ==============================
st.title("🛒 BigMart Sales Prediction Dashboard")


# ==============================
# SIDEBAR (ADVANCED CONTROLS)
# ==============================
st.sidebar.title("📊 Dashboard Controls")

# 🔹 Outlet Filter (Main slicer)
outlet = st.sidebar.selectbox(
    "🏪 Select Outlet Type",
    options=df['Outlet_Type'].unique()
)

# 🔹 Item Type Filter
item_type = st.sidebar.multiselect(
    "📦 Select Item Type",
    options=df['Item_Type'].unique(),
    default=df['Item_Type'].unique()
)

# 🔹 Fat Content Filter
fat = st.sidebar.multiselect(
    "🥗 Fat Content",
    options=df['Item_Fat_Content'].unique(),
    default=df['Item_Fat_Content'].unique()
)

# 🔹 MRP Range Filter
price_range = st.sidebar.slider(
    "💰 Select Item MRP Range",
    float(df['Item_MRP'].min()),
    float(df['Item_MRP'].max()),
    (float(df['Item_MRP'].min()), float(df['Item_MRP'].max()))
)

# 🔹 Outlet Size Filter
outlet_size = st.sidebar.multiselect(
    "🏢 Outlet Size",
    options=df['Outlet_Size'].unique(),
    default=df['Outlet_Size'].unique()
)

# 🔹 Sort Option
sort_option = st.sidebar.radio(
    "📌 Sort Sales By",
    ["High to Low", "Low to High"]
)

# ==============================
# APPLY FILTERS
# ==============================
filtered_df = df[
    (df['Outlet_Type'] == outlet) &
    (df['Item_Type'].isin(item_type)) &
    (df['Item_Fat_Content'].isin(fat)) &
    (df['Item_MRP'].between(price_range[0], price_range[1])) &
    (df['Outlet_Size'].isin(outlet_size))
]

# Sorting
if sort_option == "High to Low":
    filtered_df = filtered_df.sort_values(by="Item_Outlet_Sales", ascending=False)
else:
    filtered_df = filtered_df.sort_values(by="Item_Outlet_Sales", ascending=True)


# ==============================
# KPIs
# ==============================
st.metric("💰 Total Sales", int(filtered_df['Item_Outlet_Sales'].sum()))
st.metric("📦 Average Sales", int(filtered_df['Item_Outlet_Sales'].mean()))
st.metric("📊 Total Items", filtered_df.shape[0])


# ==============================
# BAR CHART
# ==============================
st.subheader("Top Products by Sales")

top_products = filtered_df.groupby('Item_Type')['Item_Outlet_Sales'].sum().sort_values(ascending=False)

st.bar_chart(top_products)

# ==============================
# FAT CONTENT ANALYSIS
# ==============================
st.subheader("🥗 Sales by Fat Content")

fat_data = filtered_df.groupby('Item_Fat_Content')['Item_Outlet_Sales'].sum()
st.bar_chart(fat_data)

# ==============================
# OUTLET SIZE ANALYSIS
# ==============================
st.subheader("🏪 Sales by Outlet Size")

size_data = filtered_df.groupby('Outlet_Size')['Item_Outlet_Sales'].sum()
st.bar_chart(size_data)

# ==============================
# RAW DATA
# ==============================
st.subheader("📋 Data Preview")
st.dataframe(filtered_df)


# ==============================
# PIE CHART
# ==============================
st.subheader("Sales Distribution")

st.write(filtered_df.groupby('Item_Fat_Content')['Item_Outlet_Sales'].sum())

# ==============================
