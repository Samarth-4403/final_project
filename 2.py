import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

db = mysql.connector.connect(host = "localhost",
                             username = "root",
                             password = "alka04parija",
                             database = "ecommerce")

cur = db.cursor()

# Listing all unique cities where customers are located
query = """ select distinct customer_city from customers """

cur. execute (query)

data = cur.fetchall()

data

# Counting the number of orders placed in 2017
query = """ select count(order_id) from orders where year(order_purchase_timestamp) = 2017 """

cur. execute (query)

data = cur.fetchall()

"total orders placed in 2017 are", data[0][0]

# Finding the total sales per category
query = """ select products.product_category category, 
sum(payments.payment_value) sales
from products join order_items 
on products.product_id = order_items.product_id
join payments
on payments.order_id = order_items.order_id
group by category """

cur. execute (query)

data = cur.fetchall()

df = pd.DataFrame(data, columns = [""])
df

# Calculating the percentage of orders that were paid in installments
query = """ select (sum(case when payment)) """

cur. execute (query)

data = cur.fetchall()

"the percentage of orders that were paid in installments is", data[0][0]

# Count the number of customers from each state
query = """ select customer_state, count(customer_id)
from customers group by customer_state"""

cur. execute (query)

data = cur.fetchall()

df = pd.DataFrame(data, columns = ["state", "customer_count"])
df = df.sort_values(by= "customer_count", ascending= False)

plt.figure(figsize = (8,3))
plt.bar(df["state"], df["customer_count"])
plt.xticks(rotation = 90)
plt.xlabel("states")
plt.ylabel("customer_count")
plt.title("Count of Customers by States")
plt.show()

# Calculating the numbers of orders per month in 2018
query = """ select monthname(order_purchase_timestamp) months, count(order_id) order_count
from orders where year(order_purchase_timestamp) = 2018
group by months """

cur. execute (query)

data = cur.fetchall()

df = pd.DataFrame(data, columns = ["months", "order_count"])
o = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]

ax = sns.barplot(x = df["months"], y = df["order_count"], data = df, order = o, hue = df["months"], palette = "viridis")
plt.xticks(rotation = 45)
ax.bar_label(ax.containers[0])
plt.title("Count of Orders by Months is 2018")

plt.show()

# Find the average number of products per order, grouped by customer city
query = """ with count_per_order as 
(select orders.order_id, orders.customer_id, count(order_items.order_id) as  oc
from orders join order_items
on orders.order_id = order_items.order_id
group by orders.order_id, orders.customer_id)

select customers.customer_city, round(avg(count_per_order.oc),2) average_orders
from customers join count_per_order
on customers.customer_id = count_per_order.customer_id
group by customers.customer_city order by average_orders desc
"""

cur.execute(query)

data = cur.fetchall()
df = pd.DataFrame(data, columns = {"customer city", "average products/order"})
df.head(10)