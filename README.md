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

## Getting Started - Reviewing Past Code

We have previous work already done having built a [Flask App on Docker for Heroku with Postgres and Login Capability](https://github.com/pwdel/postgresloginapiherokudockerflask).

However, this app only included one user type and one main type of Blueprint for that user for login.

We know that flask Blueprints can be used to build different page types, and that within those page types, logic can be built which stipulates whether a user can view them or not. It would seem reasonable to believe that Blueprints could also be used to determine whether certain types of users could log in to certain types of pages.

## Implementing the Code Changes

In order to make changes and understand how the changes in our code affect our overall design, we have to start off by using our [recently built app](https://github.com/pwdel/postgresloginapiherokudockerflask), taking the code and getting it set up in a Docker container on our local machine.

* We start off by copying all of the original code as well as Docker files into our current repo.
* We then get a development Docker container running by doing:

1. Remove the current container, since what we are working with now is similar.

```
sudo docker rm <name>
```

2. Make sure this app has a different name other than, "hello_flask."  We will arbitrarily choose: "userlevels_flask" This gets set in the following places:

docker-compose.yml - 

2.1 Name of the image.
2.2 Database URL
2.3 User database URL


dockercompose.prod.yml - 

(Same)

3. Run the build

```
sudo docker-compose up -d --build
```

When we run this, we see everything cleanly running on localhost:5000, so we can procede with modifying our existing code.


## Structuring Code

Flask app code is often written as a tree structure. We can use this to organize how the code will be laid out.

### Starting Tree Structure

In our most [recently built app](https://github.com/pwdel/postgresloginapiherokudockerflask), which included the capability to login with postgres, docker and flask, our tree structure looked like the following:

```
├── .env.dev

├── .env.prod

├── .env.prod.db

├── .gitignore

├── docker-compose.prod.yml

├── docker-compose.yml

└── services

	├── nginx

	│   	├── Dockerfile

	│   	└── nginx.conf

	└── web

	    	├── Dockerfile

    		├── Dockerfile.prod

    		├── entrypoint.prod.sh

    		├── entrypoint.sh

    		├── manage.py

     		├── requirements.txt

    		├── project

    			├── __init__.py

    			├── assets.py

    			├── auth.py

    			├── forms.py
    			
    			├── models.py

    			├── routes.py

    			├── config.py

    			└── static

	    			├── /css

	    			├── /dist

	    			├── /img

	    			├── /src

		    			└── js

	    			└── style.css	    			

    			└── /templates

	    			├── /auth

    					└── login.html

	    			├── /html	    		
	    				
	    			├── analytics.jinja2

	    			├── blueprintinfo.jinja2

	    			├── dashboard.jinja2

	    			├── layout.jinja2

	    			├── login.jinja2	    			
	    			├── navigation.jinja2

    				└── signup.jinja2

```

The above code represents the existing structure, however after mapping things out, we went in and deleted some various un-needed files and folders, namely old templates which were not being used, such as login.html. We're only using jinja2 templates now.

We can modify the above structure according to the needs of the new app.

* Each directory can represent a, "microservice."
* Within each microservice, group related functionality can be created using blueprints. There is both a front end and a backend.

### Analysing Current Blueprints

Looking at our Blueprints currently in service:

A [Blueprint object](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Blueprint) is defined as follows:

```
class.flask.Blueprint(name, import_name, static_folder=None, static_url_path=None, template_folder=None, url_prefix=None, subdomain=None, url_defaults=None, root_path=None, cli_group=<object object>)
```

* name – The name of the blueprint. Will be prepended to each endpoint name.
* import_name – The name of the blueprint package, usually __name__. This helps locate the root_path for the blueprint.
* static_folder – A folder with static files that should be served by the blueprint’s static route. The path is relative to the blueprint’s root path. Blueprint static files are disabled by default.
* static_url_path – The url to serve static files from. Defaults to static_folder. If the blueprint does not have a url_prefix, the app’s static route will take precedence, and the blueprint’s static files won’t be accessible.
* template_folder – A folder with templates that should be added to the app’s template search path. The path is relative to the blueprint’s root path. Blueprint templates are disabled by default. Blueprint templates have a lower precedence than those in the app’s templates folder.
* url_prefix – A path to prepend to all of the blueprint’s URLs, to make them distinct from the rest of the app’s routes.
* subdomain – A subdomain that blueprint routes will match on by default.
* url_defaults – A dict of default values that blueprint routes will receive by default.
* root_path – By default, the blueprint will automatically this based on import_name. In certain situations this automatic detection can fail, so the path can be specified manually instead.

#### auth_bp within auth.py

##### Blueprint code:

```
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
```
##### Breakdown:

* 'auth_bp' is the name
* __name__ is the import package name which helps identify the root folder.
* 'templates' is the template folder shown above in our project structure.
* 'static' is our static folder shown above.
* There is no tatic_url_path, template_folder, url_prefix, subdomain, url_defaults, root_path, cli_group

##### Usage:

1. Called in __init__.py under create_app(). the auth.auth_bp gets register_blueprint applied.
2. Route for /signup created with methods, 'GET' and 'POST' - user with name, email, password and website is created and added to database if user not crated yet.
3. Route for /login created with methods 'GET' and 'POST'. GET serves the login page, while POST requests validation and redirects the user to the dashboard.


#### main_bp within routes.py

##### Blueprint Code

```
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
```

##### Breakdown

Same as auth_bp above.

##### Usage

1. routes.main_bp registered with register_blueprint in __init__.py
2. @main_bp called at / with method 'GET', condition @login_required.
3. dashboard() function renders template 'dashboard.jinja2'
4. Various variables get fed in to this template.
5. There is also a /logout which redirects the user back to auth_bp.login

#### home_bp within routes.py

I actually skipped using this one, in the interests of speeding things up. This would have been used to show a bunch of products on the page. We can eliminate all of this fluff as we are starting over.

### Discussion on What Blueprints Do and Don't

#### What Blueprints Do:

1. They get "registered" at app initialization.
2. They get, "configured" within a python function which includes the Blueprints module.
3. This configuration points to the templates folder, static folder, and other options. Basically it points to the structure of where things are located.
4. They can also include url prefixes, domains and custom static folders.
5. They get called by [route](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.route) to a particular URL string, for example, '/', they route the user to a path to templates described by the blueprint.

#### What Blueprints Don't:

1. Create login forms, which is covered by an entirely different module, flask_wtf. They don't validate emails either.
2. Create user models, which is covered with flask_login and UserMixin. They don't generate and check password hashes either, which is covered by wrkzeug.security.
3. Compile or hold assets such as css, js. This is done via flask_assets module Bundle.

### Rendering Templates

[render_template](https://flask.palletsprojects.com/en/1.1.x/api/#flask.render_template) is a fundamental part of Flask which allows jinja templates to be rendered and built into sites.  It's fairly simple, render_template is broken down as follows:

flask.render_template(template_name_or_list,context) 

* template_name_or_list – the name of the template to be rendered, or an iterable with template names the first one existing will be rendered
* context – the variables that should be available in the context of the template.

So you basically call out the template name and then all of the variables which feed into that template.

### Routes

The routes are described by [route](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.route) which is described as follows:

route(rule, options)

* rule – the URL rule as string
* endpoint – the endpoint for the registered URL rule. Flask itself assumes the name of the view function as endpoint
* options – the options to be forwarded to the underlying Rule object. A change to Werkzeug is handling of method options. methods is a list of methods this rule should be limited to (GET, POST etc.). By default a rule just listens for GET (and implicitly HEAD). Starting with Flask 0.6, OPTIONS is implicitly added and handled by the standard request handling.

Important to note here is that the rules abide by [URL Route Registrations](https://flask.palletsprojects.com/en/1.1.x/api/#url-route-registrations).

There is an underlying Werkzeug routing system.

* Variable parts in the route can be specified with angular brackets such as /user/<username>/.

* Also note Flask takes away trailing / by default.
* You can create different rules for routes and URLs that get displayed.
* By default, a rule listens for 'GET' but we can supply POST and other restful API options to specify those. By default, all HTTP calls are allowed.

This is described under [werkzeug documentation](https://werkzeug.palletsprojects.com/en/1.0.x/routing/#werkzeug.routing.Rule).

#### Werkzeug

class werkzeug.routing.Rule(string, defaults=None, subdomain=None, methods=None, build_only=False, endpoint=None, strict_slashes=None, merge_slashes=None, redirect_to=None, alias=False, host=None, websocket=False)

[Documentation for Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/routing/#werkzeug.routing.Rule)

### HTTP Methods

As a refresher on HTTP Methods:


* GET - is used to request data from a specified resource. Should not be used for sensitive data, stays in the cache.
* POST - is used to send data to the server. Never cached, does not remain in the browser history.
* PUT - Same as POST, however calling the PUT request multiple times will always produce the same result. Calling POST multiple times will create the same resource multiple times. If you name the URL explicitly, use PUT. If we let the server decide, use POST. Use PUT when possible. Basically you overwrite an existing resource with PUT, so if you don't need to create new things, use PUT.
* DELETE - Obviously, delete the resource.
* HEAD - Same as GET but with just the HEAD, no body.

[More of a reference guide](https://www.w3schools.com/tags/ref_httpmethods.asp)

So specifying, 'GET' and 'POST' above was because we didn't want to specify 'PUT' which would have over-written a resource.


### Templates

The templating we use within Flask is Jinja, [the documentation for which can be found here](https://jinja.palletsprojects.com/en/2.11.x/api/#basics).

There is also parent-child templating within Jinja. 


## Going Forward

1. We need to add new user models to models.py.
2. We need to create new blueprints, templates and routes to send the various users to the right places after their signin.


## User Experience Perspective

It would be nice if the login experience were as seamless as possible, so that basically any user type can just land on the page and select the user type that they are, and based upon that log in or register.

Below is an example of a two-user account model including doctor and patient.

![Multi User Type Login Example](/readme_img/multiuserexample.png)

In our example, we will need:

* Sponsor
* Editor

Two additional login profiles at a seperate URL could be maintained, listing:

* Author
* Admin

These are more for administration of the site and it would not be necessary to display these to the other two user types, who are the main user types.


## Setting Up New Dockerfile

Our previous project had a dockerfile built which launched an application called, "hello_flask."  We should probably pick a different name in the case that we want to run this app simultaneously on the same machine - same goes for the database name, which has been db.

## User Model for Different Users


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

![Initial Database](/readme_img/initialdatabase.png)

### Creating Multiple User Types

We need the following user types, in order of importance:

* Sponsor
* Editor
* Admin
* Author

#### Sponsors, Authors and Editors

The sponsor account has a dashboard which gives them the ability to insert or generate an article that they would like to have edited, as well as some information about editors.

Basically, sponsors have:

* id
* name
* email
* organization
* password
* user_type
* created_on

We don't really need a website link, so we can take that out.

Editors basically have the same properties as above.  So the table, "Users" can basically be used for these different basic user types.

#### Admins

We could create a completely seperate administration table for future use, just to eliminate any possibility of basic users being accidentally classified as Admins.

#### Authors

As mentioned above, authors could be the same as Sponsors and Editors in terms of the table, but could have a seperate classification. If they are, "hidden" from the main screen, that is something we can put into the software rather than the database.

#### Creating Documents

Assuming we are working with some kind of shared set of documents between Sponsors and Editors, we can start off by creating extremely simple documents, the body of which goes right in the database, with a limited number of characters that can display.

We could allow sponsors to pick the editor that should be assigned to a document using a dropdown list of some type.

After working around and creating a schema, we get the following:

![](/readme_img/newdatabase.png)

With this we can create code for a new model within models.py.

Interestingly, in our database creator app, we can actually generate and export SQL, as shown below:

```
CREATE TABLE "users" (
	"id" integer NOT NULL,
	"name" VARCHAR(255) NOT NULL,
	"email" VARCHAR(40) NOT NULL UNIQUE,
	"password" VARCHAR(200) NOT NULL,
	"organization" VARCHAR(60),
	"created_on" DATETIME(60),
	"last_login" DATETIME(60),
	CONSTRAINT "users_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "documents" (
	"id" integer NOT NULL,
	"document_name" VARCHAR(255) NOT NULL,
	"created_on" DATETIME(60),
	"sponsor_id" integer NOT NULL,
	"editor_id" integer,
	"body" VARCHAR(1000),
	CONSTRAINT "documents_pk" PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);




ALTER TABLE "documents" ADD CONSTRAINT "documents_fk0" FOREIGN KEY ("sponsor_id") REFERENCES "users"("id");
ALTER TABLE "documents" ADD CONSTRAINT "documents_fk1" FOREIGN KEY ("editor_id") REFERENCES "users"("id");

```

The above is a useful printout over the relational database as it shows precisely what properties each column of each table has.


### Translating Into Our Data Model

#### Users Model, or flasklogin-users

The way the model is declared is through [flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/) - declaring models.

Some differences:

* The varchar type
* [Relationships](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship)
* [ForeignKey](https://docs.sqlalchemy.org/en/14/core/constraints.html#sqlalchemy.schema.ForeignKey)

[List of variable types are here](https://docs.sqlalchemy.org/en/14/core/type_basics.html).


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
        unique=False,
        nullable=False
    )
    user_type = db.Column(
        db.String(40),
        unique=False,
        nullable=False
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
    organization = db.Column(
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



#### Document Model

One Document is tied to, "many" users, meaning it gets tied to both a sponsor and an editor.  Hence, the relationship key, sponsor_id and editor_id.

However, one sponsor and one editor may have, "many" documents as well, so this design
 will follow the SQLAlchemy [Many-to-Many relationship paradigm](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships).



```
class Documents(db.Model):
    """Docu account model."""

    __tablename__ = 'documents'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    document_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    body = db.Column(
        db.String(1000),
        unique=False,
        nullable=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
```

### Helper Table (Or Association Table)

When creating many-to-many relationships, we have to create an association table to connect the two tables to each other.

We have multiple Users which can be attached to multiple Documents and vice versa.

What is the relationship between Users and Documents?  Thinking about a word that describes this relationship would be helpful in naming the table.

For example, with Products and People, the relationship is an Order.  The relationship between a User and a Document is probably more of a, "Hold" than an, "Ownership."  Ownership implies control, something that only Sponsor Users would have, but not Editors. Other synonyms:

* Ownership
* Holding
* Occupancy
* Grip
* Possess
* Retain
* Carry
* Control
* Maintain

Of the above, Users in general Retain Documents or Carry Documents without controlling them. So, we could call the association table, "Retentions," or "Holdings."  Holdings sounds more common, so we will go with that.


For the association table, we have to make sure to import to allow relationships:

```

from sqlalchemy.orm import relationship, backref
```

The 'retentions' table includes:

* id (Primary Key)
* sponsor_id
* editor_id (allow nulls)
* date_created

Every document must have a sponsor, but it doesn't have to have an editor. The editor may be switched.


```
class Retentions('retentions')
	__tablename__ = 'retentions'

    id = db.Column(
    	db.Integer, 
    	primary_key=True
    )

    sponsor_id = db.Column(
    	db.Integer, 
    	db.ForeignKey('users.id')
        unique=False,
        nullable=False
    )

	editor_id = db.Column(
		db.Integer, 
		db.ForeignKey('users.id')
        unique=False,
        nullable=True
	)

    document_id = db.Column(
    	db.Integer, 
    	db.ForeignKey('products.id')
    	unique=False,
        nullable=False
    )

    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    user = relationship(User, backref=backref("retentions", cascade="all, delete-orphan"))

    document = relationship(Document, backref=backref("retentions", cascade="all, delete-orphan"))

```

#### Relatinoship Descriptions in SQLAlchemy

Within SQLAlchemy, there is a way to describe the relationships between different tables which is defined within the user model classes.

Within our Retentions class, we add the following to define the backreferences between the tables:

```
    user = relationship(User, backref=backref("retentions", cascade="all, delete-orphan"))

    document = relationship(Document, backref=backref("retentions", cascade="all, delete-orphan"))
```

Note the capitalization of 'User' and 'Document' referring to the class which defines the table. note "retentions" in the back-reference referring to the 'retentions' table.

The SQLAlchemy [relationship](https://docs.sqlalchemy.org/en/13/orm/relationships.html) documentation referrs to a [Many to Many](https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many) relationship. 

[relationship()](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship) provides the relationship between two mapped classes. There are all sorts of default options within the relationship() function.

We then have to create relationship pointers in each of the other classes for User and Document, pointing go this Retentions table.

##### Relationship for Users and Documents

Within the "Document" class we put:

```
users = relationship('User', secondary='retentions', back_populates='documents')
```

* "secondary" points to the associaton table, 'retentions' which then points to the User class.  This gets defined as the 'users' variable within our Documents class.
* We use, "[back_populates](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates)" to ensure proper functionality, the same as [backref](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref) which Indicates the string name of a property to be placed on the related mapper’s class that will handle this relationship in the other direction. The other property will be created automatically when the mappers are configured. Can also be passed as a backref() object to control the configuration of the new relationship.
* We may not need this as it states that, "the other property will be automatically configured."

and...within the "User" class we put:

```
documents = relationship("Document", secondary="retentions", 
back_populates='users')
```

* "secondary" points to the associaton table, which then points to the User.

* Note the capitalized, "Document" referring to the class which defines the table. "retentions" is lower case, pointing to the table of that name.

##### Summary of Relationships

Relatinoships Table

* The class for the association table, 'Retentions' has two variables, pointing to documents and users. 
* It also has column sponsor_id which maps to a users.id which can't be blank.
* It has column product_id which maps to a users.id which can be blank initially.
* It has a document_id which points to the document, which can't be blank.

Documents 

* We point out users with a variable, pointing to the retentions database and back populate to 'documents'

Users

* We point out documents with a variable, pointing to th retentions database and back populate to 'users'.

### Finalized Design

![Final Database Design](/readme_img/finaldatabase.png)

## Logic

### Creating Users

Originally, our User class was called in the Auth.py function, as simple authentication, as summarized below.

Going forward, we will need to create two different login pages, one for each type of user. For the purposes of this app, which is a demonstration, we may need to simply create the users at-will with no approval.

#### Auth.py

* in [auth.py](https://github.com/pwdel/postgresloginapiherokudockerflask/blob/main/services/web/project/auth.py) it was imported "from .models import User"
* within a form, using validation_on_submit
* User name, email, website, password was inserted in the form.
* After the user was created, a template was rendered.
* There was also authentication logic, querying for user existence and checking password.

* Users were not called in assets.py, which is more about static assets.
* Users were not called in forms.py, but this file was used to create forms that would be used in auth.py.
* Users were not called in routes.py, other than [current_user](https://flask-login.readthedocs.io/en/latest/#flask_login.current_user) which is a built-in function for flask-login.
* Users were not called in routes.py, which is more about blueprints.

#### Creating, Editing and Deleting Documents

Creating documents appears to call for a completely new set of logic.

If we look at this [Flask Blog Example Github Source Code](https://github.com/gouthambs/Flask-Blogging), we see that they have things architected as follows:

##### Flask-Blogging Rough Outline

* Blogging Engine Module (handles the blog storage, configuration, permissions, extension, configuration, user loaders, and calls other functions.)
* Has a Post Processor (handles markdown extensions)
* Uses SQLAStorage
* Stores data in Google Cloud

Basically, it isn't well-organized and there is not a lot of documentation regarding how it should be organized.

However, the convention they seem to use is put a lot of processes into, "Blogging Engine."  We could likewise, create an, "Engine" however we might just call it a, "DocumentEngine," within engine.py.

## Creating the Forms

In order to know what forms are needed, I needed a basic layout of the software, so [I created one in Balsamiq](/balsamiq/layout.bmpr).

From that, I created the following generalized layout:

![](/readme_img/LoginPage.png)

![](/readme_img/SponsorSignup.png)

![](/readme_img/SponsorDashboard.png)

![](/readme_img/SponsorDocuments.png)

![](/readme_img/SponsorEditAssign.png)

![](/readme_img/SponsorNewDocument.png)

![](/readme_img/EditorSignupPage.png)

![](/readme_img/EditorDocuments.png)

![](/readme_img/EditorEditAssign.png)

## Logical Flows

To create the logic behind what user can see which dashboard, I used [Lucid online flowcharts](https://lucid.app/documents#/dashboard).

![](/readme_img/logical.png)

## Pages and Blueprints for Different User Types

Above, we created a layout which helps us understand what kinds of users have what kinds of dashboards. We can start out with the, "Signup" functionality which now has one type of user, and create a setup which will allow links to two different types of users.

### Changing the Login Page - login.jinja2

* The first thing that needs to be done on the login page, is simply to create buttons which link off to different types of signup pages.

```
      <div class="login-signup">
        <p></p>
        <span>Don't have an account?</span>
        <p></p>
        <a href="{{ url_for('auth_bp.signup') }}">Sign up.</a>
      </div>
```
Note that this code sends the user over to blueprint: auth_bp.signup.

We're going to have to duplicate this into sponsorauth_bp.signup and editorauth_bp.signup to have two different signup blueprints for the different user types.

Once we have that, we will change the above code to:

```
      <div class="login-signup">
        <p></p>
        <span>Don't have an account?</span>
        <p></p>
        <a href="{{ url_for('editorauth_bp.signup') }}">Sign up as an Editor.</a>
        <p></p>
        <a href="{{ url_for('sponsorauth_bp.signup') }}">Sign up as a Sponsor.</a>        
        <p></p>        
      </div>
```


### Changing the auth_bp.signup to sponsorauth.bp.signup and editorauth_bp.signup under auth.py






## Future Work

* We may want to create different tables for different types of users rather than keep the users all in the same table. This is a philosophical design problem. Basically this design problem is based upon whether sponsors and editors may ever change their type, e.g. whether editors may ever be promoted to sponsors. If this is a customer/vendor relationship, then there may never or very infrequently a need to switch user type back and fourth. However if this is a blog writing application, with a group or team of relatively equal types of people who can perform different roles over time, it may be better to keep them in the same table.
* Having an additional user class, basically an administrator, which would be able to change, "trial accounts" who can only see the software into, "sponsor accounts" who can have access to the software, will be fairly critical.  Basically if this is a paid service, or even if it's a non-paid service, there needs to be some kind of administrative user management.
* Further, creating pools, teams or groups of eligibility for use together might be something else fairly universal. Essentially, particularly with larger applications, you may have one or a small team of editors who may be assigned to a sponsor (which could also be considered an author).  There may also be different sponsor accounts. The ability to create different types of relationship tables dynamically will be extremely helpful in this scenario.
* Resources may also be an important thing to create - basically giving a sponsor or privleged account access to a resource, which might be a part of a microservice, even possibly in a different container, may become important in the future.
* Error prevention and UX considerations are extremely minimal in this application. There are lots of easy to fix, low hanging fruit here.

## References

[Flask Blog Example Github Source Code](https://github.com/gouthambs/Flask-Blogging)

[Building a Many to Many Relationship - SQLAlchemy](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#building-a-many-to-many-relationship)

[Database Design - User Types](https://stackoverflow.com/questions/8479252/database-design-3-types-of-users-separate-or-one-table)

[BaseModel in Flask](https://dev.to/chidioguejiofor/making-sqlalchemy-models-simpler-by-creating-a-basemodel-3m9c)

[Many to Many Relationships in SQAlchemy](https://www.michaelcho.me/article/many-to-many-relationships-in-sqlalchemy-models-flask)

[How to Make a Flask Blog in One Hour or Less](https://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/)

[Flask Markdown Editor Plugin](https://pypi.org/project/Flask-MDEditor/)

[Example Creation of Table Data - Cars](https://stackabuse.com/using-sqlalchemy-with-flask-and-postgresql/)

[Proper way to handle two different types of user session in one app in flask](https://stackoverflow.com/questions/33575918/proper-way-to-handle-two-different-types-of-user-session-in-one-app-in-flask)

[Stack Overflow: Implementing Flask Login with Multiple User Classes](https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes)

[Using Flask Blueprint to Architect Your Applications](https://realpython.com/flask-blueprint/)