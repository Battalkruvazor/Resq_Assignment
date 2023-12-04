import sqlite3


print("1) Query to find the top 10 users by sales who have registered this year (2023).")
# Query to find the top 10 users by sales who have registered this year (2023).
with sqlite3.connect("./database/mock_resq.db") as conn:
    c = conn.cursor()
    c.execute("""SELECT userid, sum(sales) as tot_sales, registereddate from orders
    INNER JOIN users ON userid = users.id
    WHERE registereddate LIKE "%2023%"
    GROUP BY userid 
    ORDER BY tot_sales DESC
    LIMIT 10""")

    records = c.fetchall()
    print("(User, Total Sales, Registration Date)")
    for record in records:
        print(record)




    
    