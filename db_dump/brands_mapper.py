import json
import psycopg2


def update_products_with_brand(file_path):
    # Open the JSONL file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    connection = psycopg2.connect(
        host="db",
        database="postgres",
        user="postgres",
        password="password",
        port=5432
    )

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Iterate over each line in the JSONL file
    for line in lines:
        # Parse the JSON data
        json_data = json.loads(line)
        brand_name = json_data['brand_name']

        # update the products with matching brand name if brand name in db is null
        cursor.execute("""
            UPDATE store_product
            SET brand = %s
            WHERE brand IS NULL AND (name ILIKE '%%' || %s || '%%' OR description ILIKE '%%' || %s || '%%')
        """, (brand_name, brand_name, brand_name))

    # Commit the changes to the database
    connection.commit()

    # Close the cursor and the database connection
    cursor.close()
    connection.close()


# Provide the path to your JSONL file
jsonl_file_path = 'allo_products_brands.jsonl'

# Call the function to update the products
if __name__ == '__main__':
    update_products_with_brand(jsonl_file_path)
