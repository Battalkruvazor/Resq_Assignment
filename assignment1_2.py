import sqlite3

print("2) Query to identify the users favourite provider segments (default offer types).")
# Query to identify the users� favourite provider segments (default offer types). Providers are the companies who sell surplus items on the marketplace.
with sqlite3.connect("./database/mock_resq.db") as conn:
    c = conn.cursor()
    c.execute("""SELECT id, defaultoffertype, max(tot_sales) as max_sales from (
    SELECT providers.id, defaultoffertype, sum(sales) as tot_sales FROM providers
    INNER JOIN orders ON providers.id = orders.providerid
    GROUP BY providers.id, defaultoffertype
    )
    GROUP BY defaultoffertype 
    HAVING tot_sales = max_sales
    ORDER BY tot_sales DESC""")

    records = c.fetchall()
    print("(User, OfferType, Total Sales)")
    for record in records:
        print(record)