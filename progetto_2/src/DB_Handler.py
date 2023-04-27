import psycopg2
import csv
import pandas as pd

class DB_Handler():
    def __init__(self, database, user, password, host, database_name):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.database_name = database_name
        try:
            # Connect to the PostgreSQL server
            self.conn = psycopg2.connect(database=database, user=user, password=password, host=host)
            # Open a cursor to perform database operations
            self.cur = self.conn.cursor()
            # Rollback any open transaction
            self.cur.execute("ROLLBACK")
            # Drop the database if it already exists
            self.cur.execute(f"DROP DATABASE IF EXISTS {database_name};")
            # Execute a CREATE DATABASE command
            self.cur.execute(f"CREATE DATABASE {database_name};")
            # Commit the transaction
            self.conn.commit()
            print("Database created successfully")
        except psycopg2.Error as e:
            print("Error creating database:", e)
        finally:
            if self.conn is not None:
                self.cur.close()
                self.conn.close()

    def create_table(self, query, table_name):
        try:
            # Connect to the PostgreSQL server and create a new database
            self.conn = psycopg2.connect(database=self.database_name, user=self.user, password=self.password, host=self.host)
            # Open a cursor to perform database operations
            self.cur = self.conn.cursor()
            # Drop the database if it already exists
            self.cur.execute(f"DROP TABLE IF EXISTS {table_name};")
            # Execute the query to create the table
            self.cur.execute(query)
            # Commit the transaction
            self.conn.commit()
            print("Table created successfully")
        except psycopg2.Error as e:
            print("Error creating table:", e)
        finally:
            if self.conn is not None:
                self.cur.close()
                self.conn.close()

    def insert_values_categories(self, path, query):
        try:
            # Connect to the PostgreSQL server
            self.conn = psycopg2.connect(database=self.database_name, user=self.user, password=self.password, host=self.host)
            # Open a cursor to perform database operations
            self.cur = self.conn.cursor()
            # Read in the CSV file and insert data into the categories table
            with open(path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader)  # skip the header row
                for row in reader:
                    category = row[2]
                    self.cur.execute(query, (category, category))
            # Commit the transaction
            self.conn.commit()
            print("Data inserted successfully")
        except psycopg2.Error as e:
            print("Error inserting data:", e)
        finally:
            if self.conn is not None:
                self.cur.close()
                self.conn.close()
    
    def app(self, path, query):
        try:
            # Connect to the PostgreSQL server
            self.conn = psycopg2.connect(database=self.database_name, user=self.user, password=self.password, host=self.host)
            # Open a cursor to perform database operations
            self.cur = self.conn.cursor()
            with open(path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader)  # skip the header row
                num_rows = 0
                for row in reader:
                    app_name = row[1]
                    self.cur.execute(query, (app_name, app_name))
                    num_rows += 1
                # Commit the transaction
                self.conn.commit()
                print("Data inserted successfully")
        except psycopg2.Error as e:
            print("Error inserting data:", e)
        finally:
            if self.conn is not None:
                self.cur.close()
                self.conn.close()


    def insert_values_apps(self, path, query):
        try:
            # Connect to the PostgreSQL server
            self.conn = psycopg2.connect(database=self.database_name, user=self.user, password=self.password, host=self.host)
            # Open a cursor to perform database operations
            self.cur = self.conn.cursor()
            # Read in the CSV file and insert data into the apps table
            with open(path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader)  # skip the header row
                for row in reader:
                    Index, app_id, category_id, rating, reviews, size, installs, app_type, price, content_rating, genres, last_updated, age_restriction = row
                    app_id_query = """SELECT "App ID" FROM Apps WHERE "name" = %s"""
                    category_id_query = """SELECT "Category ID" FROM categories WHERE Name = %s"""
                    self.cur.execute(category_id_query, (category_id,))
                    category_id = self.cur.fetchone()[0]
                    self.cur.execute(app_id_query, (app_id,))
                    app_id = self.cur.fetchone()[0]
                    app_values = (Index, app_id, category_id, rating, reviews, size, installs, app_type, price, content_rating, genres, last_updated, age_restriction)
                    self.cur.execute(query, app_values)
            # Commit the transaction
            self.conn.commit()
            print("Data inserted successfully")
        except psycopg2.Error as e:
            print("Error inserting data:", e)
        finally:
            if self.conn is not None:
                self.cur.close()
                self.conn.close()

    def insert_values_reviews(self, path, query):
        try:
            # Connect to the PostgreSQL server
            self.conn = psycopg2.connect(database=self.database_name, user=self.user, password=self.password, host=self.host)
            # Open a cursor to perform database operations
            self.cur = self.conn.cursor()
            # Read in the CSV file and insert data into the apps table
            with open(path, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                next(reader)  # skip the header row
                for row in reader:
                    app_id, translated_review = row
                    app_id_query = """SELECT "App ID" FROM Apps WHERE "name" = %s"""
                    self.cur.execute(app_id_query, (app_id,))
                    app_id = self.cur.fetchone()[0]
                    app_values = (app_id, translated_review)
                    self.cur.execute(query, app_values)
            print("Values inserted into table reviews successfully.")
        except psycopg2.Error as e:
            print("Error creating table:", e)
        finally:
            if self.conn is not None:
                self.cur.close()
                self.conn.close()

    def read_table(self, table_name):
        try:
            # Connect to the PostgreSQL server
            conn = psycopg2.connect(database=self.database_name, user=self.user, password=self.password, host=self.host)
            # Open a cursor to perform database operations
            cur = conn.cursor()
            # Execute a SELECT query on the table
            cur.execute(f"SELECT * FROM {table_name} LIMIT 10;")
            data = cur.fetchall()
        except psycopg2.Error as e:
            print("Error executing SELECT query:", e)

        # Create dataframe
        cols = []
        for elt in cur.description:
            cols.append(elt[0])

        return pd.DataFrame(data=data, columns=cols)
    
    def test_query(self, table_name, limit=False):
        try:
            # Connect to the PostgreSQL server
            conn = psycopg2.connect(database=self.database_name, user=self.user, password=self.password, host=self.host)
            # Open a cursor to perform database operations
            cur = conn.cursor()
            # Execute a SELECT query on the table
            if limit==True:
                cur.execute(f"SELECT * FROM {table_name};")
            else:
                cur.execute(f"SELECT * FROM {table_name};")
            rows = cur.fetchall()
            # Print the rows returned by the query
            for row in rows:
                print(row)
        except psycopg2.Error as e:
            print("Error executing SELECT query:", e)
        finally:
            if conn is not None:
                cur.close()
                conn.close()
    def test_query2(self, table_name, limit=False):
        try:
            # Connect to the PostgreSQL server
            conn = psycopg2.connect(database=self.database_name, user=self.user, password=self.password, host=self.host)
            # Open a cursor to perform database operations
            cur = conn.cursor()
            # Execute a SELECT query on the table
            if limit==True:
                cur.execute("""
    SELECT "App ID" FROM apps WHERE name = '10 Best Foods for You';
""")
            else:
                cur.execute(f"SELECT * FROM {table_name};")
            rows = cur.fetchall()
            # Print the rows returned by the query
            for row in rows:
                print(row)
        except psycopg2.Error as e:
            print("Error executing SELECT query:", e)
        finally:
            if conn is not None:
                cur.close()
                conn.close()
db = DB_Handler('postgres', 'postgres', 'c', 'localhost', 'prova_db')

# CATEGORY TABLE
table_query = """
    CREATE TABLE categories (
        "Category ID" SERIAL PRIMARY KEY,
        Name VARCHAR(256) NOT NULL
    )
"""
db.create_table(table_query, 'categories')
insert_query = """
    INSERT INTO categories (Name)
    SELECT %s
    WHERE NOT EXISTS (
        SELECT 1 FROM categories WHERE Name = %s
    )
"""
db.insert_values_categories('./database/output/processed_googleplaystore.csv', insert_query)
db.test_query('categories')


# APP TABLE
# Define the table creation query
table_query = """
    CREATE TABLE apps (
        "App ID" SERIAL PRIMARY KEY,
        name VARCHAR(256) NOT NULL
    )
"""
# Create the table
db.create_table(table_query, 'apps')
# Define the query for inserting data into the table
insert_query = """
    INSERT INTO apps (name)
    SELECT %s
    WHERE NOT EXISTS (
        SELECT 1 FROM apps WHERE name = %s
    )
"""
# Insert data from CSV file into the table
db.app('./database/output/processed_googleplaystore.csv', insert_query)
db.test_query2('apps', True)

# APPS TABLE
table_query = """
    CREATE TABLE Main (
    "Index" INT,
    "App ID" INT REFERENCES apps("App ID"),
    "Category ID" INT REFERENCES categories("Category ID"),
    Rating VARCHAR(10),
    Reviews VARCHAR(50),
    Size VARCHAR(50),
    Installs VARCHAR(50),
    Type VARCHAR(10),
    Price VARCHAR(50),
    "Content Rating" VARCHAR(50),
    Genres VARCHAR(50),
    "Last Updated" VARCHAR(50),
    "Age Restriction" VARCHAR(50)
    )
"""
db.create_table(table_query, 'Main')
query = """INSERT INTO Main (
                "Index", "App ID", "Category ID", Rating, Reviews, Size, Installs, Type, Price, 
                "Content Rating", Genres, "Last Updated", "Age Restriction") 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
path = './database/output/processed_googleplaystore.csv'
db.insert_values_apps(path, query)
db.test_query('Main', True)

#REVIEWS TABLE
# Define the table creation query
table_query = """
            CREATE TABLE IF NOT EXISTS reviews (
                ReviewID SERIAL PRIMARY KEY,
                AppID INT REFERENCES apps("App ID"),
                Translated_review TEXT
            )
        """
db.create_table(table_query, 'reviews')
# Define the query for inserting data into the table
insert_query = """
    INSERT INTO reviews ("App ID", review)
    SELECT a."App ID", r.Translated_Review
    FROM apps a
    INNER JOIN reviews_csv r ON a.App = r.App
    WHERE NOT EXISTS (
        SELECT 1 FROM reviews WHERE "App ID" = a."App ID" AND review = r.Translated_Review
    )
"""
path = r'C:\Users\Crypto.gunner\Desktop\CODING\DevelHope\Progetto_APP\develhope_2023_team2\progetto_2\database\output\processed_reviews.csv'
db.insert_values_reviews(path, insert_query)
