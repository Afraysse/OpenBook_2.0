"""Openbook - A Writing Database"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, flash, redirect, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Book, Published


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """ Homepage with login/register. """
    # import pdb; pdb.set_trace()

    return render_template("homepage.html")


@app.route('/login', methods=['GET'])
def login_form():
    """Login form."""

    return render_template("login.html")

    #form variables for route: email and password

@app.route('/login', methods=['POST'])
def login():
    """ Processes login. """

    # Get form variables 
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash ("User not found. Please register.")
        return redirect("/register")

    if user.password != password:
        flash("Wrong password. Please try again.")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Welcome!")
    return redirect('/feed')


@app.route('/logout')
def logout():
    """ Log out. """

    del session["user_id"]
    flash("You have now logged out.")
    return redirect("/")


@app.route('/register', methods=['GET'])
def registration_form():
    """ registration form. """

    return render_template("registration.html")

@app.route('/register', methods=['POST'])
def registration():
    """ register new user. """

    """ Get form variables """
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    # username = request.form ["username"] --> to be added later
    email = request.form["email"]
    password = request.form["password"]
    age = request.form["age"]

    new_user = User(first_name=first_name, last_name=last_name, email=email,
        password=password, age=age)

    db.session.add(new_user)
    db.session.commit()

    flash("User {} {} added.".format(first_name, last_name))
    return redirect('/login')


@app.route('/feed') #feed
def user_dashboard():
    """ Interactive feed. """

    return render_template("feed.html")


@app.route('/profile/<int:user_id>')
def user_detail(user_id):
    """ Show info about user. """

    # Button will take you to book list 

    user = User.query.get(user_id)
    return render_template("profile.html", user=user)

@app.route('/get_drafts', methods=['GET'])
def get_old_drafts():

    """ 
    Pulls all drafts stored in database and presents them in the 
    HTML file new_draft, ordered_by draft_id. 

    """

    drafts = Draft.query.order_by('draft_id').all()

    draft_list = []

    if draft in drafts:
        for draft in drafts:
            draft_dict = {
                "draft_id": draft_id,
                "user_id": user_id,
                "title": title,
                "draft": draft
        }

    draft_list = draft_list.append(draft_dict)

    return jsonify(draft_list)


@app.route('/drafts/<int:book_id>', methods=['GET'])
def get_one_draft():

    """ 
    Will query and pull for a draft to present on the right screen from the 
    writing database and then change URL to reflect book_id. 

    """

    book = Book.query.get(book_id)

    single_book = []

    one_book = {
        "title": title,
        "draft": draft,
        }

    single_book = single_book.append(one_book)

    return jsonify(single_book)


@app.route('/drafts', methods=['POST'])
def save_new_draft():

    """ 
    Saves a new draft to the database, assiging it one book_id.

    """

    title = request.form["title"]
    draft = request.form["draft"]
    user_id = session["user_id"]

    save_new_draft = Book(title=title, draft=draft, user_id=user_id)

    db.session.add(save_new_draft)
    db.session.commit()

    new_draft = Book.query.filter_by(title=title, draft=draft, user_id=user_id).first()
    session["book_id"] = new_draft.book_id


@app.route('/draft/<int:draft_id>', methods=['PUT'])
def save_old_draft(draft_id):

    """ Saves an old draft to overwrite the current book_id. """

    book = Book.query.filter_by('book_id').one()



@app.route('/drafts/<int:draft_id>', methods=['DEL'])
def delete_draft(draft_id):

    """ Deletes current draft, whether saved or new. """

    #need to add in data 


@app.route('/new_draft', methods=['GET'])
def render_new_draft_template():
    """ Renders new_draft template """

    return render_template("new_draft.html")

@app.route('/save_draft', methods=['POST'])
def redirects_saved_draft():
    """ Saves new draft to template 'book' so book_id is saved only once. """

    title = request.form["title"]
    draft = request.form["draft"]
    user_id = session["user_id"]

    saving_draft = Book(title=title, draft=draft, user_id=user_id)

    db.session.add(saving_draft)
    db.session.commit()

    draft = Draft.query.filter_by(title=title, draft=draft, user_id=user_id).first()
    session['draft_id'] = draft.draft_id

    return redirect("/draft/<int:draft_id>", title=title,
                                            draft=draft,
                                            draft_id=draft_id)

@app.route('/publish_draft', methods=['POST'])
def publish_new_draft():

    title = request.form["title"]
    draft = request.form["draft"]
    user_id = request.form["user_id"]
    book_id = request.form["book_id"]

    publish_draft = Published(title=title, draft=draft, user_id=user_id, book_id=book_id)

    saved = Book.query.filter_by(book_id=book_id).first()

    if not saved:
        flash("Please save before publishing.")

    db.session.add(publish_draft)
    db.session.commit()

    publishing = Published.query.filter_by(title=title, draft=draft, user_id=user_id, book_id=book_id)
    session['publish_id'] = publishing.publish_id

    return redirect("/dashboard")


##############################################################################
# Connects to DB

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
