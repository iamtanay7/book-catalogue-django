import psycopg2
conn = psycopg2.connect(
    host="ec2-3-227-195-74.compute-1.amazonaws.com",
    database="dfrpns4kts0d8i",
    user="prebmyellstkww",
    password="43f06e36b54de6197fa7096dfbdfbe14065ce1474ee371355167d64c177a7ad2",
    port="5432"
    )
cursor = conn.cursor()
print("PostgreSQL server information")
print(conn.get_dsn_parameters(), "\n")
# Executing a SQL query
cursor.execute("SELECT version();")
# Fetch result
record = cursor.fetchone()
print("You are connected to - ", record, "\n")
sql = "COPY (SELECT * FROM webapp_book) TO STDOUT WITH CSV DELIMITER ','"
with open("Books.csv", "w") as file:
    cursor.copy_expert(sql, file)
