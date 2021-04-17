import sqlite3
import os


def add_item(
    food,
    food_type,
    recipe,
    description=None,
    image_location=None,
    image_link=None,
    recipe_source=None,
):
    """Adds an item to the database."""

    # Checks to ensure a food, food_type, and recipe have been included
    if not food or not food_type or not recipe:
        return False

    # Pulls a database connection
    database = database_connection()

    # Attemtps to write to the database
    try:
        # Inserts into the database
        database["db"].execute(
            "INSERT INTO food (food, description, type, image_location, image_link, recipe, recipe_source) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                food,
                description,
                food_type,
                image_location,
                image_link,
                recipe,
                recipe_source,
            ),
        )

        # Commits the changes to the database
        database["con"].commit()
    except:
        # Writing to the database errored out, therefore return False
        return False

    # Everything worked, return True
    return True


def pull_items():
    """Returns all of the items in the database."""

    # Database connection
    database = database_connection()

    # All of the items
    items = database["db"].execute("SELECT * FROM food").fetchall()

    foods = []

    # Creates a list with only the values we want
    for food in items:
        foods.append(
            {
                "id": food[0],
                "food": food[1],
                "description": food[2],
                "food_type": food[3],
                "image_loc": food[4],
            }
        )

    return foods


def return_foods():
    """Returns an alphabetized list of all of the foods in the database."""

    # Database connection
    database = database_connection()

    # List of all of the foods
    foods = [
        food[0] for food in database["db"].execute("SELECT food FROM food").fetchall()
    ]

    # Sort them alphabeticlly
    foods.sort()

    return foods


def find_item(food_id=None, food=None):
    """Find's an item with an id or food name."""

    # Database connection
    database = database_connection()

    # Pulls based off a food id
    if food_id:
        data = (
            database["db"]
            .execute("SELECT * FROM food WHERE id = (?)", (food_id,))
            .fetchone()
        )
    # Pulls based off the name of the food
    elif food:
        data = (
            database["db"]
            .execute("SELECT * FROM food WHERE food = (?)", (food,))
            .fetchone()
        )

    if not data:
        return False

    # Returns the information
    try:
        return {
            "id": data[0],
            "food": data[1],
            "description": data[2],
            "type": data[3],
            "image_location": data[4],
            "image_link": data[5],
            "recipe": data[6],
            "recipe_source": data[7],
        }
    except:
        return False


def check_database():
    """Checks for a database connection on startup.  Will return the database connection and cursor.
    Will also check to ensure there is a database folder in the static/images directory."""

    # Creates a database folder if there isn't one
    if not os.path.exists(f"{os.getcwd()}/static/images/database"):
        os.mkdir(f"{os.getcwd()}/static/images/database")

    if os.path.exists(f"{os.getcwd()}/database.db"):
        # Database exists, return a connection
        return database_connection()
    else:
        # Database doesn't exist, create a database
        create_database()

        # Return the database connection
        return database_connection()


def database_connection():
    """Returns a database connection or False if it cannot find one."""

    # Attempt to connect to the database
    try:
        db_con = sqlite3.connect("database.db")
    except:
        # If it doesn't exist, return False
        return False

    # Returns the database connection and cursor
    db = db_con.cursor()
    return {"db": db, "con": db_con}


def create_database():
    """Creates a database with the default table."""

    # Create a database connection
    db_con = sqlite3.connect("database.db")
    # Create a cursor to interface with the database
    db = db_con.cursor()

    # Create the table if it doesn't exist
    db.execute(
        """CREATE TABLE IF NOT EXISTS food (
        	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "food"	TEXT NOT NULL,
            "description"	TEXT,
            "type"	TEXT NOT NULL,
            "image_location" TEXT,
            "image_link" TEXT,
            "recipe" TEXT,
            "recipe_source" TEXT
        );"""
    )

    # Commit the new table to the database
    db_con.commit()


def count_database():
    """Counts the amount of values in the database."""

    database = database_connection()

    count = database["db"].execute("SELECT COUNT(id) FROM food").fetchone()[0]

    if not count:
        # No values in the database yet
        count = 0

    return count