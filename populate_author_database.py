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
cursor.execute("SET datestyle = dmy;")
f = open(r'Authors.csv', 'r')
cursor.copy_from(f, "webapp_author", sep=',')
f.close()
sql3 = '''select * from webapp_author;'''
cursor.execute(sql3)
for i in cursor.fetchall():
    print(i)
  
conn.commit()
conn.close()