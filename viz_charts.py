import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from customtkinter import *

#import data
file = "./Data/coffee_sales.csv"
sales_df = pd.read_csv(file)

#calculating state performance broken down by product type
northeast = ['NY', 'CT', 'NH', 'MA']
product_location_performance = sales_df.groupby(['State_abbr', 'Product_type'])[['Sales']].sum().reset_index()
NE_product_sales = product_location_performance[product_location_performance['State_abbr'].isin(northeast)]

#adding color pallette
mellow_palette = ['#003f5c', '#7a5195', '#ef5675', '#ffa600']



#creating grouped bar chart of Sales by State and Product Type
pivot_df = NE_product_sales.pivot(index='State_abbr', columns='Product_type', values='Sales')
product_types = pivot_df.columns
fig, ax = plt.subplots(figsize=(8, 6))

# Define the width of each bar and the positions
bar_width = 0.2
x = range(len(pivot_df))

for i, product_type in enumerate(product_types):
    ax.bar(
        [pos + i * bar_width for pos in x],
        pivot_df[product_type],
        bar_width,
        label=product_type,
        color=mellow_palette[i]
    )

# Customize the chart
ax.set_xlabel('States')
ax.set_ylabel('Sales')
ax.set_title('Grouped Bar Chart of Sales by State and Product Type')
ax.set_xticks([pos + bar_width for pos in x])
ax.set_xticklabels(pivot_df.index)
ax.legend()

# Show the chart
plt.grid(axis='y', linestyle='--', alpha=0.7)
ax.set_facecolor('#F5F5F5')
plt.tight_layout()
#plt.show()




#creating Quarterly sales trend chart
# Convert 'Date' column to datetime format
sales_df['Date'] = pd.to_datetime(sales_df['Date'])
sales_df = sales_df[sales_df['State_abbr'].isin(northeast)]
# Group data by quarter and calculate total sales for each quarter
sales_df['Quarter'] = sales_df['Date'].dt.to_period('Q')
quarterly_sales = sales_df.groupby('Quarter')['Sales'].sum().reset_index()
quarterly_sales['Quarter'] = quarterly_sales['Quarter'].dt.strftime('Q%q %Y')
#updating 'quarter' column datatypes to string so it can be used with plt
sales_df['Quarter'] = sales_df['Quarter'].astype(str)
quarterly_sales['Quarter'] = quarterly_sales['Quarter'].astype(str)

# Create a line chart to visualize sales trends over provided timeline
fig2, ax2 = plt.subplots()
ax2.plot(quarterly_sales['Quarter'], quarterly_sales['Sales'], marker='o', color=mellow_palette[3])
ax2.set_title('Monthly Sales Trends')
ax2.set_xlabel('Month')
ax2.set_ylabel('Total Sales')
ax2.fill_between(quarterly_sales['Quarter'], quarterly_sales['Sales'], color=mellow_palette[2])
ax2.set_xticklabels(quarterly_sales['Quarter'],rotation=45)  # Rotate x-axis labels for better readability
ax2.set_facecolor('#F5F5F5')
ax2.grid(True)
#plt.show()

#creating Pie chart for customer demand for specific products
#specific product sales
product_sales = sales_df.groupby('Product')['Sales'].sum()

fig3, ax3 = plt.subplots()
product_sales.plot(kind='pie', autopct='%1.1f%%', colors=mellow_palette)
ax3.set_title('Customer Demand by Product Category')
ax3.set_ylabel('')
ax3.set_facecolor('#F5F5F5')
#plt.show()


#create tkinter window and add charts
#creates customtkinter window, allowing for improved UX/UI
root = CTk()
root.title("Sales Dashboard")
root.state("zoomed")


#adds sidebar to dash
side_frame = tk.Frame(root, bg="#003f5c")
side_frame.pack(side="left", fill="y")

label = tk.Label(side_frame, text="Dashboard", bg="#003f5c", fg="#FFF", font=25)
label.pack(pady=50, padx=20)

#adds upper row (frame) to dash, then adding canvas 1 & 2 to add charts
upper_frame = tk.Frame(root)
upper_frame.pack(fill="both", expand=True)


canvas1 = FigureCanvasTkAgg(fig, upper_frame)
canvas1.draw()
canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

canvas2 = FigureCanvasTkAgg(fig2, upper_frame)
canvas2.draw()
canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

#creates lower row (frame) and charts. Placing code for lower chart below the lower_frame creation puts it in the bottom frame
lower_frame = tk.Frame(root)
lower_frame.pack(fill="both")

canvas3 = FigureCanvasTkAgg(fig3, lower_frame)
canvas3.draw()
canvas3.get_tk_widget().pack(side="left", fill="both", expand=True)

root.mainloop()