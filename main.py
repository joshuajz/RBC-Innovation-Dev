from database import (
    check_database,
    count_database,
    add_item,
    pull_items,
    return_foods,
    find_item,
    remove_item,
)
from image import download_image
from flask import Flask, render_template, request

# Create a flask app
app = Flask(__name__)


def main():
    """Main function to run at startup, checks for a database."""

    # Checks for a databaase
    database = check_database()

    # Error message
    if not database:
        print(
            "Erorr creating or opening the database, check to ensure you have permissions for the folder."
        )
        return False


@app.route("/recipe")
def recipe():
    """Handles the /recipe part of the website.
    Will display a recipe given the name of the recipe."""

    # Grabs the name of the recipe
    recipe_name = request.args.get("recipe")

    # Finds the recipe in the database
    values = find_item(food=recipe_name)

    # Renders the recipe page with the found values
    return render_template("recipe.html", values=values)


@app.route("/")
def home():
    """Handles the / (or home) part of the website."""

    # List of all of the foods that can be autocompleted
    autocomplete_foods = return_foods()

    # Render the main site providing the 'active page' (to ensure "Home" is bolded)
    # Provide the list of foods, and the length of the list for auto completion purposes
    return render_template(
        "index.html",
        active_page="index",
        autocomplete_foods=autocomplete_foods,
        autocomplete_len=len(autocomplete_foods),
    )


@app.route("/database", methods=["GET", "POST"])
def database_page():
    """Handles the /database (or database view) of the website."""

    # If there is a "GET" request (ie. just loading the page)
    # Load the page with the list of foods pulled from the database
    if request.method == "GET":
        return render_template(
            "database.html", foods=pull_items(), active_page="database"
        )
    else:
        # POST method -> "ADD" Form has been submitted

        # Pulls the 'keys' or items in the form
        values = list(request.form.keys())

        # Checks to ensure all of the values required are present
        if (
            "food" in values
            and "description" in values
            and "food_type" in values
            and "image" in values
            and "recipe" in values
            and "recipe_link" in values
        ):
            # Assigns variables to all of the form's items
            food, description, food_type, image_link, recipe, recipe_link = (
                request.form.get("food"),
                request.form.get("description"),
                request.form.get("food_type"),
                request.form.get("image"),
                request.form.get("recipe"),
                request.form.get("recipe_link"),
            )

            # Current count of the database
            count = count_database()

            #
            if count == None:
                #! Error!  count_database has returned invalid input

                # Re-render the page again
                return render_template(
                    "database.html", foods=pull_items(), active_page="database"
                )

            # Downloads the image, stores it, and provides the location
            image_location = download_image(image_link, str(count))

            # Adds all of the information to the database
            db_add = add_item(
                food=food,
                food_type=food_type,
                recipe=recipe,
                recipe_source=recipe_link,
                description=description,
                image_location=image_location,
                image_link=image_link,
            )

            # If the addition fails, reload the page
            if db_add == None:
                #! Error! db_add provided invalid input
                return render_template(
                    "database.html", foods=pull_items(), active_page="database"
                )

            # * The form has been succesfully added to the database, reload the page
            return render_template(
                "database.html", foods=pull_items(), active_page="database"
            )
        elif "food_select" in values:
            # Post Method -> "REMOVE" form has been submitted
            print(request.form.get("food_select"))

            # Removes from the database
            remove_item(str(request.form.get("food_select")))

            # Renders the page
            return render_template(
                "database.html", foods=pull_items(), active_page="database"
            )

        else:
            # Catch-all, re-renders the page
            render_template("database.html", foods=pull_items(), active_page="database")


if __name__ == "__main__":
    # Runs main() to check for a database and then app.run() to run the Flask application
    main()
    app.run()