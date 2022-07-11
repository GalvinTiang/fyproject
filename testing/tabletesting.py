import pymysql

# Connect to the database
conn = pymysql.connect(host='localhost',user='root',passwd='root',db='stock',port=3307)

# Create a Cursor object
cur = conn.cursor()

# Execute the query: To get the name of the tables from a specific database
# replace only the my_database with the name of your database
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'stock'")

# Read and print tables
for table in [tables[0] for tables in cur.fetchall()]:
    print(table)