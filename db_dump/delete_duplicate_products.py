import psycopg2

# Connect to the database
connection = psycopg2.connect(
    host="db",
    database="postgres",
    user="postgres",
    password="password",
    port=5432,
)

# Create a cursor
cursor = connection.cursor()

# Find duplicate products by name
cursor.execute("""
    SELECT name, COUNT(*)
    FROM store_product
    GROUP BY name
    HAVING COUNT(*) > 1
""")

# Loop through each duplicate product
for name, count in cursor.fetchall():
    # Delete all but one of the duplicates
    cursor.execute("""
        DELETE FROM store_product
        WHERE id NOT IN (
            SELECT id
            FROM store_product
            WHERE name = %s
            ORDER BY id ASC
            LIMIT 1
        )
        AND name = %s
    """, (name, name))

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
