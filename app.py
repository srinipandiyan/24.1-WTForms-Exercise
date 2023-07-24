"""Pet Adoption Agency Flask Application"""

from flask import Flask, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.app_context().push()

app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adopt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

## APP ROUTES
@app.route("/")
def show_all_pets():
    """Show all pets on homepage."""

    pets = Pet.query.all()
    return render_template("pet_index.html", pets=pets)


@app.route("/add", methods=["GET", "POST"])
def add_new_pet():
    """Add new pet to index."""

    form = AddPetForm()

    if form.validate_on_submit():
        ##dictionary unpacking and passes data dictionary to Pet model as keyword arguments
            # data = {k: v for k, v in form.data.items() if k != "csrf_token"}
            # new_pet = Pet(**data)

        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data,
            age=form.age.data,
            notes=form.notes.data,
            available=True
        )

        db.session.add(new_pet)
        db.session.commit()

        return redirect(url_for('show_all_pets'))

    else:
        return render_template("add_pet_form.html", form=form)


@app.route("/<int:pet_id>", methods=["GET", "POST"])
def edit_pet(pet_id):
    """Edit existing pet within index."""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():

        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        
        db.session.commit()

        return redirect(url_for('show_all_pets'))

    else:
        return render_template("edit_pet_form.html", form=form, pet=pet)


## INTERNAL API ROUTE FROM SOLUTIONS
    # CAN BE CALLED USING REQUEST OR URL_FOR
    @app.route("/api/pets/<int:pet_id>", methods=['GET'])
    def api_get_pet(pet_id):
        """Return basic info about pet in JSON."""

        pet = Pet.query.get_or_404(pet_id)
        info = {"name": pet.name, "age": pet.age}

        return jsonify(info)