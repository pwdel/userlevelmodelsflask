# Flask with Different Types of Users Project

## Objective

The objective of this project is to implement a Flask website with multiple user types that include different types of permissions.

## Software Concept

* Four Classes of Users, Including Admin, Author, Editor and Reader.
* Document Sharing with a Type of Messaging Protocol Among Users.

Basically, we want to build an app that allows "Workers" including Authors and Editors to write articles at the request of Viewers. 

The flow is as follows: 

1. A viewer submits a request for a topic, which goes to the author.
2. The author writes the first draft of the article and submits it to the Editor.
3. Editor then modifies the article into a second draft and saves.
4. Editor finalizes the article second draft and submits that second draft article to the Viewer.
4. Viewer is able to see a diff of the first vs. the second article.

## Software Architecture

1. Build the User Model
2. Build Dashboards and Access for Each User
3. Build Document and Articles Model. Documents may include different classes of Documents besides Articles in the future.
4. Build Relationships Between Documents and Users.
5. Build "Messaging" Protocol which .includes saves and submits and requests back and fourth.

## Getting Started

We have previous work already done having built a [Flask App on Docker for Heroku with Postgres and Login Capability](https://github.com/pwdel/postgresloginapiherokudockerflask).

However, this app only included one user type and one main type of Blueprint for that user for login.

We know that flask Blueprints can be used to build different page types, and that within those page types, logic can be built which stipulates whether a user can view them or not. It would seem reasonable to believe that Blueprints could also be used to determine whether certain types of users could log in to certain types of pages.

## Visual Layout

* In designing the app itself, I can use Balsamiq, which I have been able to download and use on Lubuntu.
* For architecting the database design, I decided to try out [System Architect v5.0.0 Alpha](https://www.codebydesign.com/index.php/downloads/system-architect-v5-0-0-alpha-3/).
* Another option that I could try out if this does not work well is [Kexi](http://www.kexi-project.org/wiki/wikiview/index.php@KexiFeatures.html#Features)

There are other tool recommendations given on the [Postgres wiki](https://wiki.postgresql.org/wiki/Design_Tools#Open_Source_.28Free.29).

Starting off, I attempetd to install System Architect 5 (SArch5).

However, this did not work, so I pivoted to attempting to use [Umbrello](https://snapcraft.io/umbrello).

There is also a web version of a [database designer](https://app.dbdesigner.net/dashboard) which I was able to log into with a Google account.

### Modeling Current User Database

To start off with, we can simply copy the table and database that we already have in place within our [postgresflask app](https://github.com/pwdel/postgresloginapiherokudockerflask/blob/main/services/web/project/models.py). 

Here we created at db.Model using [UserMixin](https://flask-login.readthedocs.io/en/latest/#flask_login.UserMixin) from the flask-login module.

UserMixin(object) provides default implementations for methods that flask-login expects users to have.

Our code looked as follows:

```
class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'flasklogin-users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    email = db.Column(
        db.String(40),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)
    website = db.Column(
        db.String(60),
        index=False,
        unique=False,
        nullable=True
	)
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
```

Duplicating this database within DBDesigner.net, we get the following:

![Initial Database](/img/initialdatabase.png)


## Structuring Code

Flask app code is often written as a tree structure. We can use this to organize how the code will be laid out.



## Setting Up New Dockerfile

Our previous project had a dockerfile built which launched an application called, "hello_flask."  We should probably pick a different name in the case that we want to run this app simultaneously on the same machine - same goes for the database name, which has been db.

## User Model for Different Users

## Dashboards for Different Users

## References

[](https://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/)
[Flask Markdown Editor Plugin](https://pypi.org/project/Flask-MDEditor/)
[Example Creation of Table Data - Cars](https://stackabuse.com/using-sqlalchemy-with-flask-and-postgresql/)
[Proper way to handle two different types of user session in one app in flask](https://stackoverflow.com/questions/33575918/proper-way-to-handle-two-different-types-of-user-session-in-one-app-in-flask)
[Stack Overflow: Implementing Flask Login with Multiple User Classes](https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes)
[Using Flask Blueprint to Architect Your Applications](https://realpython.com/flask-blueprint/)