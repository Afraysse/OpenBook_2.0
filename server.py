"""Openbook - A Writing Database"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, flash, redirect, request, jsonify, url_for, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Draft, Published


app = Flask(__name__)

app.secret_key = "CBA"

app.jinja_env.undefined = StrictUndefined


@app.route('/', methods=['GET'])
def index():
    """ Homepage with login/register. """

    current_session = session.get('user_id', None)
    return render_template("homepage.html")


@app.route('/login', methods=['POST'])
def login():
    """ Processes login. """

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash ("User not found. Please register.")
        return redirect("/register")

    if user.password != password:
        flash("Wrong password. Please try again.")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Welcome {}".format(user.first_name))
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
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    # username = request.form ["username"] --> to be added later
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")

    new_user = User(first_name=first_name, last_name=last_name, email=email,
        password=password, age=age)

    db.session.add(new_user)
    db.session.commit()

    flash("User {} {} added.".format(first_name, last_name))
    return redirect('/')

############################# FEED + PROFILE ###################################

@app.route('/profile/<int:user_id>')
def user_detail(user_id):
    """ Show info about user. """

    user = User.query.get(session["user_id"])
    return render_template("profile.html", user=user)

################################ NEW DRAFTS ####################################

@app.route('/new_draft', methods=['GET'])
def set_new_draft():

    """ Renders the template for the new_draft.html page. """

    user = User.query.get(session["user_id"])
    return render_template('new_draft.html', user=user)

@app.route('/new_draft.json', methods=['POST'])
def new_draft():

    """ Grabs what is posted in new_draft and commits to DB. """

    title = request.form.get("title-field")  
    draft = request.form.get("draft-field") 
    user_id = session["user_id"]
    user = User.query.filter(User.user_id == user_id).one()

    new_draft = Draft(title=title, draft=draft, user_id=user_id)

    db.session.add(new_draft)
    db.session.commit()

    return redirect("/draft_page")

################################ OLD DRAFTS ####################################

@app.route('/draft_page')
def get_drafts_app():
    """ Renders the drafts app """

    user = User.query.get(session["user_id"])
    return render_template("draft_page.html", user=user)


@app.route('/api/drafts', methods=['GET'])
def get_drafts():

    """ 
    Queries and binds to variable 'drafts' before jsonifying for use in 
    drafts.js to pull and display old drafts.

    """
    drafts = Draft.query.filter_by(user_id=session["user_id"]).order_by(Draft.draft_id.desc()).all()

    draft_dicts = [draft.to_dict() for draft in drafts]

    
    return jsonify({'drafts': draft_dicts})

################################ SAVE DRAFT ####################################


@app.route('/save_draft/<int:id>', methods=['POST'])
def save_draft(id):
    """ Saves new draft to template 'draft' so draft_id is saved only once. """

    # import pdb; pdb.set_trace()

    # if not draft or title:
    #     #return 400
    #     pass

    new_title = request.form.get("title") #contains value id title_field
    new_draft = request.form.get("draft") #contains value id draft_field
    user_id = session["user_id"]

    # import pdb; pdb.set_trace()

    draft = Draft.query.filter(Draft.draft_id == id).one()
    
    if not draft:
        # Return 404 not found to user
        pass
   
    
    draft.draft = new_draft
    draft.title = new_title

    db.session.add(draft)
    db.session.commit()

    flash("Draft Successfully Saved!")
    return jsonify({"success": 1})

############################### PUBLISH DRAFT ##################################


@app.route('/publish', methods=['POST'])
def feed_publish():

    title = request.form.get("title")  
    draft = request.form.get("draft")
    draft_id = request.form.get("id")
    user_id = session["user_id"]

    print title
    print draft

    publish_draft = Published.query.filter_by(title=title, user_id=user_id).first()

    if publish_draft:

        publish_draft.title = title
        publish_draft.draft = draft

    else:

        user = User.query.get(user_id)
        published_draft = Published(title=title, draft=draft, user_id=user_id, draft_id=draft_id)

        print published_draft

        db.session.add(published_draft)
        db.session.commit()


    print "finished"

    flash("You have published to your Dashboard")
    return redirect("/feed")



@app.route('/feed', methods=['GET']) 
def user_dashboard():
    """ Interactive feed. """

    user = User.query.get(session["user_id"])
    published_drafts = Published.query.filter_by(user_id=user.user_id).order_by(Published.publish_id.desc()).all()
    
    return render_template("feed.html", user=user, published_drafts=published_drafts)


##############################################################################
# Connects to DB

if __name__ == "__main__":
    
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()






