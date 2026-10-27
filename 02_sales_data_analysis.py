import pandas as pd
import matplotlib.pyplot as plt
import pymysql
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import matplotlib.ticker as ticker

password=quote_plus("YOUR_MYSQL_PASSWORD")

engine = create_engine(f"mysql+pymysql://root:{password}@hostname/data_analysis") # database se connect 

query="select * from sales_data"
df=pd.read_sql(query,con=engine)
print("data successfully loaded")
# df=pd.DataFrame(df2)
# df=pd.read_csv("train.csv")
print(df.columns.to_list())

print("data set size \n",df.shape)


print("columns \n",df.shape[1])
df.info()

miss_values=df.isnull().sum()
print(miss_values[miss_values>0].sort_values(ascending=False))

total_sales=df["Sales"].sum()
print("total sales",total_sales)
 #                top 10 sales
top_10=df.nlargest(10,"Sales")
print(top_10[["Row_ID","Product_Name", "Sales"]])

#               Cotegory Wise Sales
high_sale_category=df.groupby("Category")["Sales"].sum()
print("Sabse zyada sales ki category\n",high_sale_category.sort_values(ascending=False))

#                Region wise Sales
sales_wise_region=df.groupby("Region")["Sales"].sum()
print("Kis region mein sabse zyada sales\n",sales_wise_region.sort_values(ascending=False))

ax= sales_wise_region.plot(
    kind="bar",
    figsize=(14,7),
    color=["blue","black","yellow","red"],
    title="Region wise sales",
    ylabel="sales",
    xlabel="Region",
    grid=True,
    rot=0
    )
ax.bar_label(
    ax.containers[0],
    fmt="%.0f",
    padding=3,)
plt.legend()
plt.tight_layout()
plt.savefig("Region wise sales.png" , dpi=300)
plt.show()

##                Monthly sales 

df["Order_Date"] = pd.to_datetime(df["Order_Date"],format="%d/%m/%Y")
print(df["Order_Date"].dtype)
print(df["Order_Date"].head())

monthly_sales=df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum()
print("Monthly Sales\n",monthly_sales)

monthly_sales.plot(
    kind="line",
    figsize=(12,6),
    marker="o",
    title="Monthly Sales",
    xlabel="Date",
    ylabel="Sales",
    grid=True
)

plt.tight_layout()
plt.savefig("Monthly sales analysis.png" , dpi=300)
plt.show()

#                  top 10 product sales
# top_10_product=df.nlargest(10,"Sales")
# print("top 10 product\n",top_10_product[["Product ID", "Sales"]])
top_10_product=df.groupby("Product_ID")["Sales"].sum().nlargest(10)
print(top_10_product)

ax= top_10_product.plot(
    kind="barh",
    figsize=(12,6),
    xlabel="Sales",
    ylabel="Product ID",
    grid=True,
    rot=0
)
ax.bar_label(
    ax.containers[0],
    fmt="%.0f",
    padding=3,)
plt.tight_layout()
plt.savefig("top_10_product_ID.png", dpi=300)
plt.show()

#                 Category wise sales
category_wise=df.groupby("Category")["Sales"].sum()
print("category_wise sales\n",category_wise)
ax= category_wise.plot(
    kind="bar",
    figsize=(10,5),
    title="Category wise sales",
    xlabel="category",
    ylabel="sales",
    grid=True,
    rot=0
)
ax.bar_label(
    ax.containers[0],
    fmt="%.0f",
    padding=3,)
plt.tight_layout
plt.savefig("Category wise Sales.png",dpi=300)
# plt.show()


##                  SubCategory wise sales
Sub_category_wise=df.groupby("Category")["Sales"].sum()
print("Sub_category_wise sales\n",Sub_category_wise)
ax= Sub_category_wise.plot(
    kind="bar",
    figsize=(10,5),
    title="Sub_Category wise sales",
    xlabel="Sub_category",
    ylabel="sales",
    rot=0, # letters ka angle set karta hai 0, 45 , 90 degree
    grid=True
)
ax.bar_label(
    ax.containers[0],
    fmt="%.0f",
    padding=3,)
plt.tight_layout
plt.savefig("Sub_Category wise Sales.png",dpi=300)
plt.show()

#                  monthly wise sales
df["Order_Date"]=pd.to_datetime(df["Order_Date"],format="%d/%m/%Y")
monthly_sales=df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum().sort_values(ascending=False)
print(f"high sale month\n {monthly_sales.idxmax()} = {monthly_sales.max()}")
print(f"Min sale month\n {monthly_sales.idxmin()} = {monthly_sales.min()}")
print(monthly_sales)
import numpy as np
sales_goal=monthly_sales*0.99
fig, ax= plt.subplots(figsize=(14,7))

bars=monthly_sales.plot(
    kind="bar",
    ax=ax,
    title="Month wise sales",
    xlabel="Months",
    ylabel="Sales",
    color="coral",
    grid=True,
    rot=90,
)

ax.bar_label(
    bars.containers[0],
    labels=[F"{v:,.0f}"for v in monthly_sales.values],
    padding=3,
    fontsize=8,
    rotation=90
)

ax.plot(
    range(len(monthly_sales)),
    sales_goal.values,
    color="red",
    marker="o",
    linestyle="--",
    linewidth=2,
    label="sales_goal",
)

ax.legend()
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("Month Wise sales",dpi=300,bbox_inches="tight")
plt.show()

                        # top 10 Cities by sales
top_10_cities=df.groupby("City")["Sales"].sum().sort_values(ascending=False).nlargest(10)
print("Top 10 cities",top_10_cities)
ax= top_10_cities.plot(
    kind="bar",
    figsize=(14,7),
    title="top 10 cities by sales",
    xlabel="city",
    ylabel="Sales",
    grid=True,
    rot=0
)
ax.bar_label(
    ax.containers[0],
    fmt="%.0f",
    padding=3,)
plt.tight_layout()
plt.savefig("top 10 cities by sales.png", dpi=300)
plt.show()

#                      top 10 costumer
top_10_costumer=df.groupby("Customer_Name")["Sales"].sum().nlargest(10)
print("top 10 costumer",top_10_costumer)
ax= top_10_costumer.plot(
    kind="bar",
    figsize=(14,7),
    title="top 10 costumer",
    xlabel="costumer name",
    ylabel="Sales",
    grid=True,
    rot=0
)
ax.bar_label(
    ax.containers[0],
    fmt="%.0f",
    padding=3,)
plt.tight_layout()
plt.savefig("top 10 costumer.png", dpi=300)
plt.show()


# ##              segment Wise analysis 
Segment_wise_analysis=df.groupby("Segment")["Sales"].sum().sort_values(ascending=True)
print("segment wise analysis",Segment_wise_analysis)
ax=Segment_wise_analysis.plot(
    kind="bar",
    figsize=(10,5),
    title="Segment_wise_analysis",
    xlabel="Segment",
    ylabel="Sales",
    grid=True,
    rot=0
)
ax.ticklabel_format(axis="y",style="plain")
ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: f"{x:,.0f}")
)
ax.bar_label(
    ax.containers[0],
    fmt="%.0f",
    padding=3,
)
plt.tight_layout()
plt.savefig("Segment_wise_analysis.png", dpi=300)
plt.show()
    
##                  ship mode analysis
ship_mode_analysis=df.groupby("Ship_Mode")["Sales"].sum().sort_values(ascending=False)
print("ship mode analysis",ship_mode_analysis)
ax=ship_mode_analysis.plot(
    kind="bar",
    figsize=(12,6),
    title="ship_mode_analysis",
    xlabel="Ship mode",
    ylabel="Sales",
    grid=True,
    rot=0
)
ax.ticklabel_format(axis="y", style="plain")
ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: f"{x:,.0f}")
)
ax.bar_label(
    ax.containers[0],
    fmt="%.0f",
    padding=3,
)
plt.tight_layout()
plt.savefig("ship mode analysis.png",dpi=300)
plt.show()