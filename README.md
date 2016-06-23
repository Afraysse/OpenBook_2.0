# OpenBook
OpenBook is a social networking site centered around creative writing. By creating a profile, users can create drafts and save to a highly dynamic editing page, which allows them to continue saving and editing until they are ready to publish. Once finished working on a draft, the user may publish to a newsfeed that displays the completed work to their follower list. Likewise, the user may also view other user work, including those they are following, in the newsfeed as well. The overall purpose of OpenBook is to provide creative networking, allowing hobbiest writers to show of their work to a select number of viewers. 

###Table of Contents
* [Technology Stack](#technology stack)
* [How to Use OpenBook] (#How to Use OpenBook)
* [Features + Screenshots] (#features + screenshots)
* [Local Installation & Running Application] (#local installation)
* [Looking Ahead] (#looking ahead)
* [Author] (#author)

<a name="technology stack"/>
###Technology Stack

* Python
* Flask
* SQLAlchemy
* PostgreSql
* Javascript/jQuery
* AJAX/JSON
* Jinja2
* CSS + Bootstrap
* HTML/CSS

(Dependencies are listed in requirements.txt)

<a name="How to Use OpenBook"/>
### How to Use OpenBook
* Create three PostgreSQL databases: 'User', 'Drafts', and 'Published'
* Transform information stored in each db into a dictionary 
* 'User_id', autoincremented through the User db once user is added, is saved to session at login
* Use SQLAlchemy to query postgres databases 
* GET/POST requests grab dictionaries stored in db
* JSON sends dictionaries as JavaScript objects 
* AJAX calls allow for drafts to be retrieved and edited readily 
* Jinja2 displays content, including title and draft body, stored in db.

<a name="features + screenshots"/>
###Features + Screenshots

####Homepage

User can log in if they have previously created an account. If not, the can register. Once registration is completed, the user's information is saved to the postgreSQL database 'User', where an autoincrimenting 'user_id' is created. This id is then used as a ForeignKey in both the 'Draft' and 'Published' databases. Once the user logs in, the user_id is saved to the session.

####Dashboard

The dashboard is used to display both the user's posts, as well as those posts belonging to the user's following list. The published drafts are first queried from the "Published" database as a GET request in the server file. The dictionary object stored in the database is then sent over. Using Jinja on the HTML page, the contents of the object, including 'title' and 'draft' can then be displayed.

####Profile

The profile is used as a homebase for the user. It shows not only their profile picture, but their current statistics, including number of followers, following and published posts. The profile also provides a route to creating a new draft.

####Saved Draft

The saved draft page allows the user to access previously saved drafts. Once the new draft has been created in the new draft html page, a redirect is called from the server file and the information stored in the new draft textarea is then stored to the 'Draft' database, where it is also assigned a single 'draft_id.' From this point on, once redirected to the saved draft page, all further saves are committed using AJAX calls, which prevents the page from having to reload each time. Furthermore, using JQuery, the previously saved drafts are able to be clicked on directly in order to display within the text box for editing. This is completed by using JSON, which jsonifies the dictionary acquired and transforming into an object for use in JavaScript.

<a name="local installation"/>
###Local Installation & Running Application 
* Set up and activate a python virtualenv, and install all dependencies:

`pip install -r requirements.txt`

* Create the tables in your database:

`python -i model.py`

* While in interactive mode, `create tables: db.create_all()`
* Now, quit interactive mode. Start up the flask server:

`python server.py`
* Go to localhost:5000 to see the web app


<a name="looking ahead"/>
###Looking Ahead

While I have followers and following listed in my profile page, I would like to give these functions life by building the integration needed to have multiple users communicate.

<a name="author"/>
###Author

Anne Fraysse is a software engineer living in the San Francico Bay Area.

