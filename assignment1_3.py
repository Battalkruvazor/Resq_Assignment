import sqlite3


print("3) Query to find out what is the M1 retention for any given user cohort. A cohort consists of users who made their first order within the same month.")
# Query to find out what is the M1 retention for any given user cohort. A cohort consists of users who made their first order within the same month
month = 10
year = 2022
date = f"{year}-{month}"

    
with sqlite3.connect("./database/mock_resq.db") as conn:
    c = conn.cursor()
    c.execute(f" select DISTINCT userid from orders group by userid having strftime('%Y-%m', min(createdat)) = '{date}' \
   ")
    cohort_size = len(c.fetchall())

    c = conn.cursor()
    c.execute(f" select DISTINCT userid from orders \
   inner join (select DISTINCT userid as uid, min(createdat) as first_sale_date from orders group by userid having strftime('%Y-%m',first_sale_date) = '{date}') on userid = uid \
   WHERE JULIANDAY(createdat) - JULIANDAY(first_sale_date) between 30 and 60\
   ")

    M1_size = len(c.fetchall())

    print(f"M1 retention = {M1_size/cohort_size}")