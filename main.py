from database import check_database, count_database, add_item, pull_items
from image import download_image
from flask import Flask, render_template, request

app = Flask(__name__)


def main():
    database = check_database()

    pull_items()

    if not database:
        print(
            "Erorr creating or opening the database, check to ensure you have permissions for the folder."
        )
        return False


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        foods = pull_items()
        return render_template("index.html", foods=foods)
    else:
        # POST method
        values = request.form.keys()
        if (
            "food" in values
            and "description" in values
            and "food_type" in values
            and "image" in values
        ):

            form_submissions = request.form.items()
            food, description, food_type, image_link = (
                request.form.get("food"),
                request.form.get("description"),
                request.form.get("food_type"),
                request.form.get("image"),
            )
            count = count_database()
            if count == None:
                #! Error Message
                return render_template("index.html")

            image_location = download_image(image_link, str(count))
            if image_location == None:
                #! Error Message
                print("ERROR")
                return render_template("index.html")
            print("MADE IT")
            db_add = add_item(food, food_type, description, image_location, image_link)
            if db_add == None:
                #! Error Message
                print("ERROR")
                return render_template("index.html")

            foods = pull_items()
            return render_template("index.html", foods=foods)


if __name__ == "__main__":
    main()
    app.run()