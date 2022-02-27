import psycopg2
conn = psycopg2.connect(
    host="ec2-3-227-195-74.compute-1.amazonaws.com",
    database="dfrpns4kts0d8i",
    user="prebmyellstkww",
    password="43f06e36b54de6197fa7096dfbdfbe14065ce1474ee371355167d64c177a7ad2",
    port="5432"
    )
cursor = conn.cursor()
cursor.execute("delete from webapp_book where id=14")
  
conn.commit()
conn.close()