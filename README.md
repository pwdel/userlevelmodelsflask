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

### Finalized Database Design

![Final Database Design](/readme_img/finaldatabase.png)

## Logic

### Models.py

Within models.py there are a couple of embedded functions:

```
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
```

These are basically functions that help set passwords. We need to create additional functions that help set the user type.

We also note that Flask-User v1.9 has a built-in [Role-based authorization](https://flask-user.readthedocs.io/en/latest/authorization.html) capability.  There is also a [basic app](https://flask-user.readthedocs.io/en/latest/basic_app.html) example which shows how this functionality can be implemented.

When we look at the user db.Model for this class, we see that:

* User role was structured in a seperate association table.
* This association table allows what appears to be an arbitrary role name, which can then map back to permissions.


```
    # Define the User data-model.
    # NB: Make sure to add flask_user UserMixin !!!
    class User(db.Model, UserMixin):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

        # User authentication information. The collation='NOCASE' is required
        # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
        email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
        email_confirmed_at = db.Column(db.DateTime())
        password = db.Column(db.String(255), nullable=False, server_default='')

        # User information
        first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
        last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

        # Define the relationship to Role via UserRoles
        roles = db.relationship('Role', secondary='user_roles')

    # Define the Role data-model
    class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define the UserRoles association table
    class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    # Setup Flask-User and specify the User data-model
    user_manager = UserManager(app, db, User)

    # Create all database tables
    db.create_all()

    # Create 'member@example.com' user with no roles
    if not User.query.filter(User.email == 'member@example.com').first():
        user = User(
            email='member@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=user_manager.hash_password('Password1'),
        )
        db.session.add(user)
        db.session.commit()

    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    if not User.query.filter(User.email == 'admin@example.com').first():
        user = User(
            email='admin@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=user_manager.hash_password('Password1'),
        )
        user.roles.append(Role(name='Admin'))
        user.roles.append(Role(name='Agent'))
        db.session.add(user)
        db.session.commit()
```

* In the above example, we define, "roles" as a relationship to Role via UserRoles, which requires an additional association table.
* Within UserRoles, we get user_id and role_id.
* role_id maps back to roles.id, in the 'roles' table, which has a "name."

* We can give users "no roles" by not assigning any role.
* We can also give users roles with user.roles.append(Role(name='Admin')) or user.roles.append(Role(name='Agent')).

This type of logic is consistent with the idea that roles are not fundamentally a part of user information, they are something that gets, "assigned," from a list of options. The idea would be that if you create an increasingly dynamic number of roles arbitrarily over time, you can just keep adding them to the list.

While this is an interesting feature, if we can avoid this level of complexity at this stage, we should.

So, rather than using the function:

```
user.roles.append(Role(name='Admin'))
user.roles.append(Role(name='Agent'))
```
We could, at the point of sign-up on the appropriate page under auth.py, use the function (assuming user_type='sponsor':

```
        if existing_user is None:
        	# create a new user
            user = User(
                name=form.name.data,
                email=form.email.data,
                organization=form.organization.data
                user_type='Sponsor'
            )
```

Then, within routes, we modify the suggested function from flask-user, but still use the flask-user module with:

```
    # The Sponsor page requires an 'Sponsor' role.
    @app.route('/sponsor')
    @roles_required('Sponsor')    # Use of @roles_required decorator
    def sponsor_page():
```
Essentially using the @roles_required function to achieve what we are looking to do.

* That being said, looking at the [Flask-User](https://github.com/lingthio/Flask-User) Github, we see they list Flask-Login as an alternative, which we are already using.  However it does not seem that Flask-User has built-in permissions.
* This [StackOverflow answer on role based authorization in flask-login](https://stackoverflow.com/questions/61939800/role-based-authorization-in-flask-login) discussion suggests using Flask Principal.
* This [Stackoverflow answer on flask login supporting roles](https://stackoverflow.com/questions/52285012/does-flask-login-not-support-roles) recommends spinning up one's own function.

Give the oldness of the Github repos above and the evident non-supportability, it is probably better to just spin up our own function. functools is a cython library, meaning it is likely extremely well supported.

```
from functools import wraps

def sponsor_required(f):
@wraps(f)
def wrap(*args, **kwargs):
    if current_user.role == "Sponsor":
        return f(*args, **kwargs)
    else:
        flash("You need to be a Sponsor to view this page.")
        return redirect(url_for('index'))

return wrap
```

functools is included within python's main library, so there is no need to install it.

#### Diagnosing Errors after models.py Modifications

After we get everything modified, we attempted to docker-compose in detached build mode, however this created a situation where there was no localhost port for the actual flask server.

So, running the following allows us to see the actual server processes:

```
sodu docker-compose up
```
This is without '-d build'

1. Here we see the error:

```
flask  |   File "/usr/src/app/project/models.py", line 74
flask  |     @wraps(f)
flask  |     ^
flask  | IndentationError: expected an indented block
```
This was simply fixed by modifying the indentation block.

2. We get a Syntax error on:

```
flask  |   File "/usr/src/app/project/models.py", line 135
flask  |     class Retentions('retentions')
```

This was fixed by inserting the ':' symbol.

3. SyntaxError

```
flask  |   File "/usr/src/app/project/models.py", line 148
flask  |     unique=False,
flask  |     ^
flask  | SyntaxError: invalid syntax
```
Here we have a case of lack of commas after the db.ForeignKey, so we placed that in place:

```
    sponsor_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        unique=False,
        nullable=False
    )
```

4. flask  | NameError: name 'relationship' is not defined

We didn't import 'from sqlalchemy import relationship'.  When we try this, we cannot import 'relationship' from 'sqlalchemy

So, we had to import from [sqlalchemy.orm](https://docs.sqlalchemy.org/en/14/orm/), which is the SQLAlchemy Object Relational Mapper.

```
from sqlalchemy.orm import relationship
```

This cleared the error.

5. backref not defined.

```
flask  |     backref=backref("retentions", cascade="all, delete-orphan")
flask  | NameError: name 'backref' is not defined
```

This comes from:

```
    """backreferences to user and document tables"""
    user = relationship(
        'User', 
        backref=backref('retentions', cascade="all, delete-orphan")
        )

    document = relationship(
        'Document', 
        backref=backref('retentions', cascade="all, delete-orphan")
        )
```

Much more precisely, what is [backref](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref)?

There are some examples within the [sqlalchemy documentation](https://docs.sqlalchemy.org/en/13/orm/backref.html#relationships-backref).

Notably, the example given from this documentation shows the below imports:

```
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
```

What is [Cascades](https://docs.sqlalchemy.org/en/13/orm/cascades.html#unitofwork-cascades)?

Basically, there are a bunch of different options dealing with how items get deleted or updated, based upon SQL rules. Per [this SQL Guide](https://www.sqlshack.com/delete-cascade-and-update-cascade-in-sql-server-foreign-key/):

```
DELETE CASCADE: When we create a foreign key using this option, it deletes the referencing rows in the child table when the referenced row is deleted in the parent table which has a primary key.

UPDATE CASCADE: When we create a foreign key using UPDATE CASCADE the referencing rows are updated in the child table when the referenced row is updated in the parent table which has a primary key.

```
The default cascading behavior for backrefs is: 

> cascades will occur bidirectionally by default. This basically means, if one starts with an User object that’s been persisted in the Session. The above behavior is known as the “save update cascade."

What appears to be happening, is that with:

```
x = relationship('Y', backref=backref('retentions', cascade="all, delete-orphan"))
```
backref is referencing backref, so the variable doesn't know what's being assigned. E.g. backref is being treated both as a function and a variable, for some reason here.  So, we could instead go to the default cascading behavior and simply allow backref='retentions'


```
    """backreferences to user and document tables"""
    user = relationship(
        'User', 
        backref='retentions'
        )

    document = relationship(
        'Document', 
        backref='retentions'
        )
```

When we did this, that cleared the error.


6. Note - __tablename__ = 'flasklogin-users' should be changed to:

__tablename__ = 'users'

After this was changed, there was no apparent errors.

7. class Retentions('retentions'): string error.

```
flask  |   File "/usr/src/app/project/models.py", line 142, in <module>
flask  |     class Retentions('retentions'):
flask  | TypeError: str() argument 2 must be str, not tuple

```
This is an oversight and we evidently needed the class to have (db.Model) to work properly.  When we fixed this, the error was gone.

8. NoReferencedTableError - products

```
flask  | sqlalchemy.exc.NoReferencedTableError: Foreign key associated with column 'retentions.document_id' could not find table 'products' with which to generate a foreign key to target column 'id'
```
This is a simple oversight - evidently we used "products.id" from seperate code rather than "documents.id"

```
    document_id = db.Column(
        db.Integer, 
        db.ForeignKey('products.id'),
        unique=False,
        nullable=False
    )
```
The above cleared the error.

#### Inspecting Database

After all of the above errors were cleared, we were able to get to localhost.

So, we ran in detached mode with:

```
sudo docker-compose up -d --build
```

We now have a perpetually running app on localhost.  However, we need to be able to log into bash and inxpect the database, so we use:

```
sudo docker run --rm -it userlevels_flask bash
```
From within the root docker container, we get:

```
root@af424625f527:/usr/src/app# 

```

From the command line, we can log into the database with (using our new database name):

```
sudo docker-compose exec db psql --username=userlevels_flask --dbname=userlevels_flask_dev
```
Checking for a list of databases:

```
userlevels_flask_dev=# \l                                                                                                                                  
                                                  List of databases                                                                                        
         Name         |      Owner       | Encoding |  Collate   |   Ctype    |           Access privileges                                                
----------------------+------------------+----------+------------+------------+---------------------------------------                                     
 postgres             | userlevels_flask | UTF8     | en_US.utf8 | en_US.utf8 |                                                                            
 template0            | userlevels_flask | UTF8     | en_US.utf8 | en_US.utf8 | =c/userlevels_flask                  +                                     
                      |                  |          |            |            | userlevels_flask=CTc/userlevels_flask                                      
 template1            | userlevels_flask | UTF8     | en_US.utf8 | en_US.utf8 | =c/userlevels_flask                  +                                     
                      |                  |          |            |            | userlevels_flask=CTc/userlevels_flask                                      
 userlevels_flask_dev | userlevels_flask | UTF8     | en_US.utf8 | en_US.utf8 |                                         

```


Checking for a list of relations:

```
userlevels_flask_dev=# \dt                                                                                                                                 
                  List of relations                                                                                                                        
 Schema |       Name       | Type  |      Owner                                                                                                            
--------+------------------+-------+------------------                                                                                                     
 public | documents        | table | userlevels_flask                                                                                                      
 public | flasklogin-users | table | userlevels_flask                                                                                                      
 public | retentions       | table | userlevels_flask                                                                                                      
 public | users            | table | userlevels_flask 
```
We can look at the database by connecting to it, and then selecting * from users.

```
userlevels_flask_dev=# \c userlevels_flask_dev                                                                                                             
You are now connected to database "userlevels_flask_dev" as user "userlevels_flask".                                                                       
userlevels_flask_dev=# select * from users;                                                                                                                
 id | name | user_type | email | password | organization | created_on | last_login                                                                         
----+------+-----------+-------+----------+--------------+------------+------------                                                                        
(0 rows)            
```
Which interestingly, shows the updated column including 'organization'.  However when we do:

```
userlevels_flask_dev-# select * from documents
```
We get nothing.

Why do we get nothing for documents, not even the table? Perhaps because we haven't constructed the table itself (much less seeded data into it).  

However, within postgres, [we can use a command to describe the database](https://stackoverflow.com/questions/3362225/describe-table-structure).

```
userlevels_flask_dev-# \d documents                                                                                                                        
                                          Table "public.documents"                                                                                         
    Column     |            Type             | Collation | Nullable |                Default                                                               
---------------+-----------------------------+-----------+----------+---------------------------------------                                               
 id            | integer                     |           | not null | nextval('documents_id_seq'::regclass)                                                
 document_name | character varying(100)      |           | not null |                                                                                      
 body          | character varying(1000)     |           | not null |                                                                                      
 created_on    | timestamp without time zone |           |          |                                                                                      

userlevels_flask_dev-# \d retentions                                                                                                                       
                                         Table "public.retentions"                                                                                         
   Column    |            Type             | Collation | Nullable |                Default                                                                 
-------------+-----------------------------+-----------+----------+----------------------------------------                                                
 id          | integer                     |           | not null | nextval('retentions_id_seq'::regclass)                                                 
 sponsor_id  | integer                     |           | not null |                                                                                        
 editor_id   | integer                     |           |          |                                                                                        
 document_id | integer                     |           | not null |                                                                                        
 created_on  | timestamp without time zone |           |          |                                                                                        

```
So given the above, it appears that the tables have been set up properly.

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

### forms.py

Since we now have two forms of users which can enter in through two different forms, we need to modify the forms.py.

Basically, we need two forms - one for the sponsor page, one for the editor page.

#### Sponsor Form on forms.py

So basically the main thing we need to do here is ensure that everything on our form corresponds to the user_type Sponsor in our database.

Form-Generated Data:

* name - enter in form
* email - enter in form
* password - enter in form
* organization - enter in form

Auto-Generated Data:

* user_type - automatically generated based upon page
* id - automatically generated
* created_on - automatically generated
* last_login - automatically generated

What I did to change the form was basically copy and paste the original form and create:

```
class SignupFormSponsor(FlaskForm):
```
Which has the four (4) human-inputed datapoints, same as the original sign-up form. It's possible that we don't really need two different forms.

## Creating Users via Forms

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

#### Modifiying Auth.py and Routes

* First thing I did, just to clean things up a bit, was to move the /login route to the top of the file, since that's really the, "first page" so to speak.
* We have to modify the login function to check for user type, and then route the user to the appropriate page.
* def signup() should be split into two functions, one for sponsor and one for editor.

##### signup() split into sponsorsignup() and editorsignup()

It seems that the most logical place to start is at the point where the user gets created, to be able to understand more about how the data is being inserted into the database.

We set up a custom class within the forms.py file, class SignupFormSponsor(FlaskForm):

We start with:

```
@auth_bp.route('/signupsponsor', methods=['GET', 'POST'])
def signupsponsor():
```

So, we are using the auth_bp, rather than sponsor_bp.

```
# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
```

We could hypothetically set up a completely different blueprint for auth_sponsor_bp and auth_editor_bp.

However, to keep things simple, we can just see if we can use the same auth blueprint for both, to have less code to change, and add usertype within the function itself.

* On our URL for /signupsponsor
* We are calling function signupsponsor()
* We are using the form = SponsorSignupForm()

The key point of creating a new user appears to be here:

```
            # create a new user
            user = User(
                name=form.name.data,
                email=form.email.data,
                website=form.website.data
            )
```

Which we can change to:

```
            # create a new user
            user = User(
                name=form.name.data,
                email=form.email.data,
                organization=form.organization.data,
                user_type='sponsor'
            )
```

Note again back on our form in forms.py that we had changed, "website" (lower case for the variable) to "organization" (lower case for a variable) and 'Organization' as the String prompt.

```
    organization = StringField(
        'Organization',
        validators=[Optional()]
    )
    submit = SubmitField('Register')
```
We also have to be sure to import the new type of signup form:

```
from .forms import LoginForm, SignupForm. SignupFormSponsor
```
Also, we have to modify our Jinja2 template so that we are no longer asking for a website, but rather an organization, change:

```
      <fieldset class="website">
        {{ form.website.label }}
        {{ form.website(placeholder='http://example.com') }}
      </fieldset>
```
to:

```
      <fieldset class="organization">
        {{ form.organization.label }}
        {{ form.organization(placeholder='Organization, LLC') }}
      </fieldset>
```

After this point, the application writes a new user with the information given, as shown below:

```
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user - from flask_login
```

I realized upon reading further into the "def signupsponsor():" function, that the auth_bp blueprint does not limit directing only to the url's on its own blueprint, we can hand off the user to another blueprint using the following (which was originally handing the user over to main_bp.dashboard):

```
return redirect(url_for('sponsor_bp.dashboard'))
```

The final step is to of course attempt to sign in as a sponsor, and then inspect the database to see if it worked.

In our case, I attempted to sign up and got the following:

```
sqlalchemy.exc.InvalidRequestError: When initializing mapper mapped class User->users, expression 'Document' failed to locate a name ('Document'). If this is a class name, consider adding this relationship() to the <class 'project.models.User'> class after both dependent classes have been defined.
```
I also noted that the user was being redirected to /signup rather than /dashboard_sponsor.

Basically, it looks like the error is referring to this portion of the models.py file, specifically the User class where we backreference to the Document class.

```
    """Backreference to Document class on retentions associate table."""
    documents = relationship(
        'Document', 
        secondary='retentions', 
        back_populates='users'
        )
```

Different troubleshooting guides online mention using a, "Base" model as an input in order for SQLAlchemy to work with relational databases.

* [StackOverflow SQAlchemy Import Tables with Relationships](https://stackoverflow.com/questions/11046039/sqlalchemy-import-tables-with-relationships)
* [SQLAlchemy Basic Application Template with Declarative Base](https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/database/sqlalchemy.html#importing-all-sqlalchemy-models)
* [Pointer to Declarative Base Tutorial](https://stackoverflow.com/questions/9088957/sqlalchemy-cannot-find-a-class-name)

<hr>

Summary of Signup form Conversion for New Data Capture

0. If you haven't already, update your database to hold the new data.
1. Setup a Custom Class in forms.py if needed, to capture newly needed data or change old form.
2. Configure blueprint and folder layout if needed to point to new webpage layouts and/or static css, js, etc.
3. If necessary, modify or create a New python Function or Class to handle thew new part of the application you are working with.
4. Modify the Custom Class call on the New Function for the part of the application you are working on to include the data you are looking for, for either automatic or manually recorded data. Make sure you pay attention to your data model to make sure the database has been updated.
5. Update Jinja2 Templates. Register new blueprints on __init__.py

<hr>

![](/readme_img/ConvertFlaskFormsSummary.png)

##### login() within auth.py

* Check user_type
* If user_type is shown to be sponsor, return one type of template, if editor, return another type of template.

```
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))"Log in with your User account."
    )
```

Should send user to:

* dashboard_sponsor.jinja2

or

* dashboard_editor.jinja2

We will have different jinja2 templates for all various views being shown to different users.

We can setup blueprints for different users which point to different template folders and static folers.  After adding the appropriate blueprints and dashboards, I modified the bypass code as follows:

```
    # Bypass if user is logged in
    if current_user.is_authenticated:
    	if current_user.
	        return redirect(url_for('main_bp.dashboard'))"Log in with your User account."
    	if current_user.
	        return redirect(url_for('main_bp.dashboard'))"Log in with your User account."    		        
    )
```

### Running Through SQLAlchemy Tutorial

What we are following are the below resources:

* [StackOverflow SQAlchemy Import Tables with Relationships](https://stackoverflow.com/questions/11046039/sqlalchemy-import-tables-with-relationships)
* [SQLAlchemy Basic Application Template with Declarative Base](https://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/database/sqlalchemy.html#importing-all-sqlalchemy-models)
* [Pointer to Declarative Base Tutorial](https://stackoverflow.com/questions/9088957/sqlalchemy-cannot-find-a-class-name)
* [Declaring a Base Model in Flask-SQLAlchemy](https://stackoverflow.com/questions/22976445/how-do-i-declare-a-base-model-class-in-flask-sqlalchemy)
* [Miguel Grinberg Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database)
* [SQLAlchemy Declaring and Mapping](](https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_declaring_mapping.htm)
* [SQAlchemy Docs on Declarative Mapping](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#declare-a-mapping)


#### Object Relational Mapping (ORM)

SQLAlchemy has something called the, "[Object Relational Mapper API](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#declare-a-mapping)" which associates 

1. User-defined Python classes with database tables
2. Instances of those classes with rows in corresponding tables

ORM is in contrast to, "SQLAlchemy Expression Language" represents the primitive constructs of a relational database directly without opinion. ORM presents a high level abstracted pattern of usage. Applications can be built with the ORM exclusively. ORM may make use of Expression Language on an as-needed basis.

[A comparison of the different paradigms can be found here](https://enterprisecraftsmanship.com/posts/domain-centric-vs-data-centric-approaches/).

Expression is Schema Centric:

* Database is the center of everything
* Application code is secondary to the data
* Database structure modeled out first
* Achieves code reuse by putting code close to the data, introduces common functionality in the database itself. More than one applciation querying the same data. You don't have to write API's.

Expression language in SQLAlchemy basically allows Python to directly call SQL statements, and create more complex queries. It represents the more primitive constructs of the relational database.

ORM is Domain Centric:

* Creates API's in the application code using REST or SOAP.
* Database not shared between applications
* Microservices, external services

Basically, ORM/Declarative is the more modern version of doing things, while Expression is closer to the hardware/database so to speak. 

#### The Base Class

db.Model, or as it gets defined, "Base Class,"  and appears to not have been created as a declarative base in our original code, we don't have anything calling out what db.Model is, in terms of it being declarative within models.py.

Per [this tutorial](https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_declaring_mapping.htm),

> A base class stores a catlog of classes and mapped tables in the Declarative system. This is called as the declarative base class. There will be usually just one instance of this base in a commonly imported module. The declarative_base() function is used to create base class. This function is defined in sqlalchemy.ext.declarative module.

```
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```

> Once base classis declared, any number of mapped classes can be defined in terms of it. Following code defines a Customer’s class. It contains the table to be mapped to, and names and datatypes of columns in it.


Tutorials out there at least instruct using the following:

```
self.Model = self.make_declarative_base()
```

However, additional tutorials actually suggest using the function:

```
Base = declarative_base()
```
...and then substituting this for db.Model. The reason for this is presumably because, per [this StackOverflow Q&A ](https://stackoverflow.com/questions/22698478/what-is-the-difference-between-the-declarative-base-and-db-model), there are various options within the declarative_base() function which allow for things like; accessing query objects as Model.query rather than session.query(Model), computing table names, handling binds, etc.

It also appears that we may need to feed in, "Base" first as:

```
class User(Base, UserMixin):
```

After making these changes, we run the code in docker.

### User Query Error

We now get a different error:

```
File "/usr/src/app/project/auth.py", line 59, in signup

existing_user = User.query.filter_by(email=form.email.data).first()
```

Whereas previously we had a, "backreference" error, now we see an error in the signup form, which points to this code:

```
    form = SignupForm()
    # validate if the user filled out the form correctly
    # validate_on_submit is a built-in method
    if form.validate_on_submit():
        # make sure it's not an existing user
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            # create a new user
            user = User(
                name=form.name.data,
                email=form.email.data,
                website=form.website.data
            )
``` 
I can see that our signup form is not valid, because it's asking for, "Website"

I also note that the user type is not being set in auth.py. Whereas in forms.py we setup a new class 

```
class SignupFormSponsor(FlaskForm):
```
Now under auth.py, we don't seem to have a way to set the user_type.

We could set up a seperate auth.py function and blueprint, but this seems like a lot of work, so it would be better to perhaps create a, "hidden" form and feed the data in from the page it's coming from.

Then we could have this in our auth.py signup class:

```
            user = User(
                name=form.name.data,
                email=form.email.data,
                organization=form.organization.data
                user_type=form.organization.data
            )
```
However, upon closer inspection, what seems to be happening is that we are being redirected to, /signup rather than:

```
@auth_bp.route('/signupsponsor', methods=['GET', 'POST'])
def signupsponsor():
```
There seems to be a couple things happening in our logic:

```
@auth_bp.route('/signupsponsor', methods=['GET', 'POST'])
def signupsponsor():
    """
    Sponsor sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupFormSponsor()
    # validate if the user filled out the form correctly
    # validate_on_submit is a built-in method
    if form.validate_on_submit():
        # make sure it's not an existing user
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            # create a new user

    # if form not validated, send back to signup form
    return render_template(
        'signup.jinja2',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )
```

We need to replace our redirect, which was sending to a page that didn't exist, "sponsor_bp.dashboard" needs to be "sponsor_bp.dashboard_sponsor":

```
return redirect(url_for('sponsor_bp.dashboard_sponsor'))
```

Besides this, we still have a query error.  [This StackOverflow Article](https://stackoverflow.com/questions/31578555/attributeerror-type-object-user-has-no-attribute-query) goes into the fact that UserMixin from flask-login does not have a query attribute.

Further comments talk about how we need an option set within the declarative base, basically;

```
Base.query = session.query_property()
```
So that the flask-security module will be able to access user tables using the query.

Hence in models.py we add:

```
Base = declarative_base(
    Base.query = db_session.query_property()
    )
```

* [What is UserMixin in flask-login?](https://stackoverflow.com/questions/63231163/what-is-usermixin-in-flask)

> Flask-login requires a User model with the following properties:
>    has an is_authenticated() method that returns True if the user has provided valid credentials
>    has an is_active() method that returns True if the user’s account is active
>    has an is_anonymous() method that returns True if the current user is an anonymous user
>    has a get_id() method which, given a User instance, returns the unique ID for that object
> UserMixin class provides the implementation of this properties. Its the reason you can call for example is_authenticated to check if login credentials provide is correct or not instead of having to write a method to do that yourself.

[We can create our own User class which mimics UserMixin](https://stackoverflow.com/questions/31578555/attributeerror-type-object-user-has-no-attribute-query)

We could also try adding our own function:

```
# user loader to implement query
@login_manager.user_loader
def get_user(ident):
  return User.query.get(int(ident))
```
If we look at the error we are being given, we see that the error is being thrown in the "signup" function, so we take this out:

```
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    # validate if the user filled out the form correctly
    # validate_on_submit is a built-in method
    if form.validate_on_submit():
        # make sure it's not an existing user
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            # create a new user
            user = User(
                name=form.name.data,
                email=form.email.data,
                organization=form.organization.data
            )
            # use our set_password method
            user.set_password(form.password.data)
            # commit our new user record and log the user in
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user - from flask_login
            # if everything goes well, they will be redirected to the main application
            return redirect(url_for('main_bp.dashboard'))
        flash('A user already exists with that email address.')
    return render_template(
        'signup.jinja2',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )
```
Once we take that out, we get re-directed to the /signup page, which now no longer exists.

After playing around with this for a while, I realize that it's necessary to go back and look at the __init__.py file to see what else we might be missing.

* Of course, any time we add new bluepritns, we need to, "register" them.  This gets added to __init__.py

```
    # initialize login manager plugin
    login_manager.init_app(app)
    with app.app_context():
        from . import routes
        from . import auth
        from .assets import compile_static_assets
        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(routes.sponsor_bp)
        app.register_blueprint(routes.sponsor_bp)

```
After doing this, rather than getting a 404 error, we get a, "sponsor_bp" is not defined from the auth.py file.  This just means we need to add that blueprint within auth.py or import it.

We try importing with:

```
from .routes import sponsor_bp, editor_bp
```
After this, and upon pinging, "http://localhost:5000/signupsponsor" - we are now shown the expected signupsponsor form.

Of course after we fill out the form, we are still redirected back to "/signup".  Why are we being redirected here?  Where in the entire codebase does this even exist anymore?

Basically, the expected behavior is that we should be redirected to:

```
return redirect(url_for('sponsor_bp.dashboard_sponsor'))
```
However, what is happening is that we are getting re-directed back to /signup. So basically, we're not being validated upon submission within the signup form. Rather, flask-wtf validate-on-submit is not being executed.

Per this Stackexchange; [Flask-WTF validate_on_submit is never executed](https://stackoverflow.com/questions/10722968/flask-wtf-validate-on-submit-is-never-executed):

> You're not inserting the CSRF field in the HTML form.

[CRSF Token](https://flask-wtf.readthedocs.io/en/latest/quickstart.html#creating-forms)

If we look on our .jinja2 files,

signup.jinja2

```
    <form method="POST" action="/signup">
      {{ form.csrf_token }}
```
signup_sponsor.jinja2

```
    <form method="POST" action="/signupsponsor">
      {{ form.csrf_token }}
```
So we are doing this, exactly as the documents suggest.

After doing some work re-arranging blueprints and working with the auth.py, routes,py as well as jinja files, it appears that after sponsor signup, we are now re-directed to, "/signupsponsor" but we still get the attributeerror in that User has no attribute Query.

So, it appears that we do indeed need to make a custom validator.

### Creating a Custom Login Validator

#### Current Login Validator

Note - this gets bypassed if current user is already validated. We always get sent here as a check-in.

This is getting bypassed with an error because there is no, "user = User.query.filter_by(email=form.email.data).first()"

```
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_bp.dashboard'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))
    return render_template(
        'login.jinja2',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
    )

```

Basically:

```
user = User.query.filter_by(email=form.email.data).first()
```

Is from SqlAlchemy, whereas our User class uses "UserMixin" from flask-login [source](https://flask-login.readthedocs.io/en/latest/_modules/flask_login/mixins.html#UserMixin). 

#### Custom Login Validator

Rough Sketch

```

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.Unicode(128))
    name = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(1024))
    authenticated = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post')
    #-----login requirements-----
    def is_active(self):
    #all users are active
        return True 

    def get_id(self):
        # returns the user e-mail. not sure who calls this
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        # False as we do not support annonymity
        return False

    #constructor
    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password
        self.authenticated = True
```

We start out by adding to our current user class:

```
    #-----login requirements-----
    def is_active(self):
    #all users are active
        return True 

    def get_id(self):
        # returns the user e-mail. not sure who calls this
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        # False as we do not support annonymity
        return False
```

Keep in mind, we are having the User class inherit from "Base" now - "class User(Base):" - the declarative base, from SQAlchemy.

So, the User Class from SQLAlchemy does not have the query property.

As attempted above, we can add:

```
Base.query = db_session.query_property()
```

However now we don't have db_session and we get an error:

```
flask  | NameError: name 'db_session' is not defined

```

There seems to be more documentation about this specific, "query_property()" here:

* [SQLAlchemy 13 ORM Scoping Scoped Session Query Property](https://docs.sqlalchemy.org/en/13/orm/contextual.html?highlight=query_property#sqlalchemy.orm.scoping.scoped_session.query_property)
* [SQLAlchemy 14 Query API](https://docs.sqlalchemy.org/en/14/orm/query.html)

We are likely using SQLAlchemy version 13.

#### Reframing the Objective

Basically, the objective at this point is being able to use SQL to connect to, and work with a database through our application.  Nothing seems to be working right now, because I don't fully understand the requirements for connecting to a database.

So basically, our objective should be to just purely get SQLAlchemy working with Flask at this point.  Without this critical step, we can't really build the application.  We can read more about the documentation, setting up databases, watch tutorials on the topic, whatever works to get a fuller understanding and finally get things working.

We are using, [Flask-SQLAlchemy==2.4.1](https://flask-sqlalchemy.palletsprojects.com/en/2.x/).  We can follow the following plan to understand more about SQLAlchemy:

1. [Read the Flask SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/).  Really read through and try to understand it.
2. [Read the SQL Alchemy Current Release Documentation](https://docs.sqlalchemy.org/en/13/).  We can assume we are on the current release until we know different.
3. [ReRead the SQLAlchemy Tutorial from Hackers and Slackers](https://hackersandslackers.com/flask-sqlalchemy-database-models)
4. [Use Flask and SQLalchemy, not Flask-SQLAlchemy!](https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4)
5. [Flask SQL Alchemy Tutorial](https://www.youtube.com/watch?v=cYWiDiIUxQc)
6. [Relationship() function documentation](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship)
7. [Building a Relationship Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#building-a-relationship)
8. [Object Relational Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#object-relational-tutorial-1-x-api)

##### Initial Fix Attempts:

Through the process of reading 1, SQLAlchemy Documentation:

1. We see that our database setup, SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://") should be:


SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://")

2. in the SQLAlchemy Documentation, the following is mentioned:

> For the common case of having one Flask application all you have to do is to create your Flask application, load the configuration of choice and then create the SQLAlchemy object by passing it the application.

We appear to do this as follows within __init__.py:

```
# activate SQLAlchemy
db = SQLAlchemy()

app = Flask(__name__)

db.init_app(app)
```

While the main SQAlchemy example shows feeding as follows:

There is documentation for [init_app](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/?highlight=init_app#flask_sqlalchemy.SQLAlchemy.init_app) showing that we can use a callback to initialize the application.

> Once created, that object then contains all the functions and helpers from both sqlalchemy and sqlalchemy.orm. Furthermore it provides a class called Model that is a declarative base which can be used to declare models:

The documentation mentions:

```
class User(db.Model):
```

Which is different than what we had done most recently, which was to try to set up a declarative base Base.  Taking out "Base" from our model and replacing it back with db.Model clears the User.query error.

The tutorial goes on to say we can create our database with:

```
db.create_all()

```

Which we do in manage.py.

Once we have the database created we can query it with:

```
User.query.all()
```

The tutorial goes on to talk about accepting keyword arguments for all columns and relationships.

> Note how we never defined a __init__ method on the User class? That’s because SQLAlchemy adds an implicit constructor to all model classes which accepts keyword arguments for all its columns and relationships. If you decide to override the constructor for any reason, make sure to keep accepting kwargs and call the super constructor with those kwargs to preserve this behavior



Once we updated our model, we get a new error:

```
sqlalchemy.exc.InvalidRequestError

sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'mapped class User->users'. Original exception was: When initializing mapper mapped class User->users, expression 'Document' failed to locate a name ('Document'). If this is a class name, consider adding this relationship() to the <class 'project.models.User'> class after both dependent classes have been defined.

```

Next in the tutorial, we see a section on relationships, including blog posts and categories.  This is what might be classified as a, "Simple Relationship" and might not cover many-to-many relationships, so we should keep reading.

* [Contexts](https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/) is used in the case that we need to use multiple applications, or create an application dynamically within a function, which we do.  Basically it talks about using db.init_app, and then in the case that we are working in a shell, or using a with statement to "set up" the context with session.

```
def my_function():
    with app.app_context():
        user = db.User(...)
        db.session.add(user)
        db.session.commit()
```
[app_context](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.app_context) is actually a flask function. This makes the current app point at this application.

[Configuration](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/) is something we already have achieved within the config.py file.  Some possibly interesting notes include:

* SQLALCHEMY_BINDS is for connecting to multiple databases.
* SQLALCHEMY_ENGINE_OPTIONS has a dictionary of options and keyword args to send to create_engine()

The tutorial goes into MetaData, which can be useful for migrations, and timeouts, which can be imposed by servers. 

[Types of Relationship Models](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/) are covered in the "Declaring Models" part of the tutorial.  The following examples are given:

* Simple Example
* [One to Many](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#one-to-many-relationships)
* [Many to Many](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships) which also defines the helper table.

From the tutorial:

> What does db.relationship() do? That function returns a new property that can do multiple things. In this case we told it to point to the Address class and load multiple of those. How does it know that this will return more than one address? Because SQLAlchemy guesses a useful default from your declaration. If you would want to have a one-to-one relationship you can pass uselist=False to relationship().

* backref is a simple awy to declare a new property on the, "other" Class being backreferenced to.  So if you have two classes, A and B, and want to have "widgets" as a property of A, you can add, "backref='widgets'" on B.
* lazy defines when SQLAlchemy will load the data from the database. lazy="True" is the default, means that SQLAlchemy will load the data as necessary in one go.  There are different options for loading:

* 'joined' / False
* 'subquery'
* 'dynamic'

You can define lazy status for backrefs right in the backref()

There is then an example given for many-to-many relationships.

```
tags = db.Table(
    'tags',

    db.Column(
        'tag_id', db.Integer, 
        db.ForeignKey('tag.id'), 
        primary_key=True
        ),

    db.Column(
        'page_id', 
        db.Integer, 
        db.ForeignKey('page.id'), 
        primary_key=True
        )
)

class Page(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
        )

    tags = db.relationship(
        'Tag', 
        secondary=tags, 
        lazy='subquery',

        backref=db.backref(
            'pages', 
            lazy=True
            )

        )

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
```

Notably, this example above does not include a class for "tags" as a database, but it does include a class for, "Tag."

Looking at our [Database Sketch](https://github.com/pwdel/userlevelmodelsflask/blob/main/readme_img/finaldatabase.png) we should question what do we really need within each class to make this work.

Above we have Page and Tag, whereas our database has User and Document.

Look at the documentation for the [Relationship function](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship).

Typical relationship using declarative mapping in SQLAlchemy:

```
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship(
        "Child", 
        order_by="Child.id"
        )
```

Beyond this, there are different sections on usage of flask-sqlalchemy as shown below:

* [Select, Insert, Delete, Query](https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/)
* [Multiple Databases with Binds](https://flask-sqlalchemy.palletsprojects.com/en/2.x/binds/)
* [Track Modifications to Database](https://flask-sqlalchemy.palletsprojects.com/en/2.x/signals/)

* [Customizing](https://flask-sqlalchemy.palletsprojects.com/en/2.x/customizing/)
A couple interesting notes about customization:

Model Mixins - these are for if behavior is only needed on some models rather than all models. mixin classes customize only those models. For example, if some models track when they are created or updated.

The, "UserMixin" however provides default implementations that Flask-Login expects user objects to have.  This includes:

```

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
```
    
However we might be able to add these (and anything else needed), manually.

* [API Documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/)

Next on the reading list:

2. [Read the SQL Alchemy Current Release Documentation](https://docs.sqlalchemy.org/en/13/).  We can assume we are on the current release until we know different.
6. [Relationship() function documentation](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship)
7. [Building a Relationship Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#building-a-relationship)
8. [Object Relational Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#object-relational-tutorial-1-x-api)

##### SQLAlchemy Current Release Documentation

2. [Read the SQL Alchemy Current Release Documentation](https://docs.sqlalchemy.org/en/13/).  We can assume we 

* Notes on SQLAlchemy philosophy - basically, treating a database like a bunch of algebra rather than a bunch of tables, and having an Object Relational Mapper (ORM), an optional component that provides a data mapper pattern, where classes can be mapped to the database in open ended, multiple ways. The object model and database schema can be decoupled from the beginning.

**Getting Started** basically talks about how SQLAlchemy is a collection different components which can optionally be used including an ORM, and a Core, which includes schema/types, SQL Expression language, Engine, Connection Pooling and Dialects (for different database types), as well as a Database API.

**The SQLAlchemy ORM** goes directly into the ORM Tutorial, linked to below.

**SQLAlchemy Core** goes directly into the Expression Language Tutorial, linked below.

[Dialect Documentation for Postgres](https://docs.sqlalchemy.org/en/13/dialects/postgresql.html)


##### Object Relational Tutorial

[Object Relational Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#object-relational-tutorial-1-x-api)

>The SQLAlchemy Object Relational Mapper presents a method of associating user-defined Python classes with database tables, and instances of those classes (objects) with rows in their corresponding tables.

* First we set up an engine, which is already covered in the flask-sqlalchemy module.
* Mapping delcaration is also covered in flask-sqlalchemy
* "Creating a schema" goes through and hels explain the reason why our schemas are written the way they are in model.py. However, the actual creation of the schema itself with User.__table__ is covered in flask-sqlalchemy.
* The standard way of creating a class which describes a table is shown.
* "Creating an Instance" shows how you can use the python console to insert data by ClassName(info='info')
* "Creating a Session" is covered by flask-sqlalchemy
* "Session" means, an object is sitting in the environment, it sits in the session but has not been committed to SQL. You can use session.add(data_point) to put that datapoint into a session without writing it to SQL. Once you want to commit that data you can use, session.commit().
* "Rollback" is like, "undo" for a session, you can roll back a piece of data before committing it.
* **Querying** Query objects are created using query() on Session. So basically you can do: session.query(User.id) to load User instances.
* Query can also use ORM-instrumented descriptors as arguments, such as session.query(User.name, User.id)
* Query can also be used with filter by doing: query.filter(User.name == 'ed') to filter anyone named ed, for example.
* Query can also be used to return a whole list of something, such as with Query.all()
* text() can be used to filter for literals, such as filter(text("id<244")) to get all id's lower than a particular number. Parameters can be bundled.
* Counting can be done with Query.count() to determine the number of rows a particular SQL statment would return.
* [Building a Relationship](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#building-a-relationship) seems to be a more critical section that we should dedicate its own section to below.

##### Building a Relationship Tutorial

[Building a Relationship Tutorial](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#building-a-relationship)

* Within the tutorial, out a second table called, "Address".  This implies a basic one to many relationship.

```
class Address(Base):
     __tablename__ = 'addresses'
     id = Column(Integer, primary_key=True)
     email_address = Column(String, nullable=False)
     user_id = Column(Integer, ForeignKey('users.id'))

     user = relationship(
        "User", 
        back_populates="addresses"
        )

     def __repr__(self):
         return "<Address(email_address='%s')>" % self.email_address


User.addresses = relationship(
    "Address", 
    order_by=Address.id, 
    back_populates="user"
    )

```
* The ForeignKey construct is a directive applied to Column that indicates that the values shold be constrained to be values in the named remote column.  So basically, user_id in Address must be taken from users.id from the User table.
* relationship() tells the Object Relationship Map that the "user" column in the Address table should be linked to the User class, backpopulating to the tablename "addresses"

Foreignkey relationships between the two tables determine the nature of the linkage. The fact that Address has a ForeignKey tells us that it will be the, "many" to the, "one" of users.

* The relationship.back_populates is assigned to back-populate in both directions.
* relationship() is making a decision about what's happening based upon how we place the relationship() function and the back_populate options.
* [backref](https://docs.sqlalchemy.org/en/13/orm/backref.html#relationships-backref) is for linking competing relationships such as Address.user and User.addresses.  This is a [bidirectional relationship](https://docs.sqlalchemy.org/en/13/glossary.html#term-bidirectional-relationship), which means two robjects can be mutually associated with each other. This can be applied to any relationship.


##### Linking Relationships with Backref

What does Backref do?

* [Linking Relationships with Backref](https://docs.sqlalchemy.org/en/13/orm/backref.html#relationships-backref) goes into more detail on usage of Backref.

We are presented with the following example:

```
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    addresses = relationship("Address", backref="user")

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
```

relationship.backref is a common shortcut for placing a second relationship() into the address mapping. The equivalent to the above "addresses" would be:

```
# User Class
addresses = relationship("Address", back_populates="user")

# Address Class
user = relationship("User", back_populates="addresses")

```
So basically, rather than putting a relationship() function under both the User and Address class pointing to each other, we put one relationship() function under User and backref it to "addresses".  The second example is, "explicitly" telling each relationship about the other one.

backref() is not merely a shortcut for relationship() it means that certain behavior will change, meaning that configurational arguments apply in both directions rather than in one direction.

Many-to-many relationships have a [relationship.secondary argument](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondary), which specifies an intermediary table, which is usually an instance of [Table].(https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table)

There is basically the ability to run backref arguments inside of each other, as a string, in order to apply options in one direction.  They can also be cascaded.

##### Relationship Function Documentation

6. [Relationship() function documentation](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship)

```
class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    children = relationship("Child", order_by="Child.id")
```
* argument - is the target of the relationship.  It basically feeds into a function called, "[Mapper](https://docs.sqlalchemy.org/en/14/orm/mapping_api.html#sqlalchemy.orm.Mapper)" which links a user defined class with table metadata.
* secondary is used in many-to-many relationships and specifies the intermediary table.
* active_history=False indicates that the many-to-one reference should be loaded if not already loaded.
* backref - discussed above, indicates the relationship in the other direction.
* back_populates takes a string name, but the complementary property is not created automatically, and must be configured explicitly on the mapper.
* overlaps - eliminates warnings of conflicts
* bake_queries - caches the construction of SQL in lazyloads.
* cascade - comma seperated cascade rules.
* foreign_keys - a list of columns to be used as foriegn key columns.  Most cases this is not required as it is done automatically.

(and lots of other options)


##### Table Documentation

[Table Documentation](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table()


##### Building a Many to Many Relationship

* [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#relationship-patterns) goes into much more detail as to the different categories of relationships.

First off, the association table seems to not be a class, but rather just a Table object.

However [Building a Many to Many Relationship](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#orm-tutorial-many-to-many) is a tutorial on just that topic.

```
association_table = Table('association', Base.metadata,
    Column('left_id', Integer, ForeignKey('left.id')),
    Column('right_id', Integer, ForeignKey('right.id'))
)

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Child",
                    secondary=association_table)

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)
```


If you want to create a many to many relationship with a class, this is known as an Association Object:

```
class Association(Base):
    __tablename__ = 'association'
    left_id = Column(Integer, ForeignKey('left.id'), primary_key=True)
    right_id = Column(Integer, ForeignKey('right.id'), primary_key=True)
    extra_data = Column(String(50))
    child = relationship("Child")

class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Association")

class Child(Base):
    __tablename__ = 'right'
    id = Column(Integer, primary_key=True)
```
> Working with the association pattern in its direct form requires that child objects are associated with an association instance before being appended to the parent; similarly, access from parent to child goes through the association object.

What does this mean?  Basically all objects go through the association instance first.  So within the logical flow of the app code, first the Parent is associated with the association table, then the Child is associated with the association table, then they are linked together. [Association Proxy](https://docs.sqlalchemy.org/en/13/orm/extensions/associationproxy.html) exists to help with this logical flow.

Also it is important to note (per a warning in the tutorial) that relationships don't change until Session.commit() has been completed.

To make an attempt at fixing our database relationship, we can do the following:

1. Add "primary_key = True" to our Retentions class for sponsor_id and document_id.

```
    sponsor_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        primary_key=True,
        unique=False,
        nullable=False
    )

    document_id = db.Column(
        db.Integer, 
        db.ForeignKey('documents.id'),
        primary_key=True,
        unique=False,
        nullable=False
    )
```

2. Take out, "created_on" because it's not really needed and may require some special logic.
3. Ensure the back_populates function points to user and document tables are included in the retentions table, as they do not appear to be needed, and appear to be needed in the User and Documents classes instead.

Use singular, "user" and "document" in the Association (Retention) object to signify that columns are within this object. Use plural "users" and "documents" to specify the columns in the User and Document classes.

```
    """backreferences to user and document tables"""
    user = db.relationship(
        'User', 
        back_populates='documents'
        )

    document = db.relationship(
        'Document', 
        back_populates='users'
        )
```
4. Ensure that the relationship() on both User and Document objects points to the Retentions object, and back_populates to the correct column in that association (Retentions) table.

As mentioned above, use singular, "user" and "document" in the Association (Retention) object to signify that columns are within this object. Use plural "users" and "documents" to specify the columns in the User and Document classes.

```
# for User class

documents = relationship('Retentions',back_populates='user')

# for Document class

users = relationship('Retentions',back_populates='document')

```
Once this is properly built, we can try to re-launch to see what happens.

##### Running with Clean Relationship Setup

When we run this, we get the error:

```
on line76 of auth.py

from login_user(user)

AttributeError: 'User' object has no attribute 'is_active'
```

This is in part because we had deleted the extra attributes for user after eliminating the UserMixin model. This has to do with flask_login. We can add the required attributes once again.

To be cleaner about this, [we can look right at the codebase on Github](https://github.com/maxcountryman/flask-login/blob/fd7984cd645c1e7c34c6af53b0571f7380b17cc3/flask_login/utils.py#L145). 

On auth.py we can change the relevant section to be explicit in our options:

```
            db.session.add(user)
            db.session.commit()  # Create new user
            # log in as newly created user from flask_login
            login_user(user, remember=False, duration=None, force=True, fresh=True)
            # if everything goes well, they will be redirected to the main application

```
* remember - we don't want to remember the user after their session expires.
* duration - cookie never expires
* force - if this is set to true, it will log them in regardless of is_active. This we need to set to True
* fresh - per the [flask_login](https://flask-login.readthedocs.io/en/latest/#fresh-logins) documentation, basically high security activities require a fresh login.

After this error was cleared, we see another flask_login error, which is that:

```
AttributeError: 'User' object has no attribute 'get_id'
```
Basically, there are four main methods which flask_login requires:

* is_authenticated()
* is_active()
* is_anonymous() 
* get_id()

UserMixin provides the default implementations.  We can copy from UserMixin, it is not required to inheret from [UserMixin](https://flask-login.readthedocs.io/en/latest/_modules/flask_login/mixins.html#UserMixin).

We should be able to copy and paste the following from UserMixin into our User class.

```
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return text_type(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

```
Why do we use @property?  Basically this is a shortcut for a property() function which allows attributes or instances from classes to be able to be get, set or deleted (read, write, delete).  It basically makes the instances manipulatable. For users, we need to be able to manipulate the instances of users in terms of whether they are active (yes/no), authenticated (yes/no), or annonymous (yes/no). The user_id is of course static.

This [StackOverflow](https://stackoverflow.com/questions/17330160/how-does-the-property-decorator-work-in-python) discussion covers it well, as well as the [Python Documentation](https://docs.python.org/3/reference/datamodel.html#object.__get__).

After implementing the above, next, we get an error that: text_type is not defined.  Where does text_type come from?  Looking in the [flask_login Github for compat.py](https://github.com/maxcountryman/flask-login/blob/main/flask_login/_compat.py) we see that there is a module for flask_login.-compat (replace - with underscore). So we simply add to auth.py:

```
from flask_login.-compat import text_type
```
After this was correctly implemented, we see a werkzeug.routing.BuildError, which means we are now at the blueprint layer.  The error is fairly self-explanitory, we just seemed to have the wrong blueprint name.

After working around with Blueprints and templates, I was able to easily modify the code and update things on the fly since the application is on a Docker container.

### Double Checking Database

First we completely rebuild the image as a detached, static image with:

```
sudo docker-compose up -d --build
```
Then we connect directly to the database with:

```
sudo docker-compose exec db psql --username=userlevels_flask --dbname=userlevels_flask_dev
```

We can list our relations and view them with:

```
userlevels_flask_dev=# \dt                                                                 
                  List of relations                                                        
 Schema |       Name       | Type  |      Owner                                            
--------+------------------+-------+------------------                                     
 public | documents        | table | userlevels_flask                                      
 public | flasklogin-users | table | userlevels_flask                                      
 public | retentions       | table | userlevels_flask                                      
 public | users            | table | userlevels_flask                                      
```

We inspect each relation table with the following commands:

```
 \d documents
 \d users
 \d retentions
```
Upon inspection, we see that a relation setup is now properly listed for each table, with an example shown below:

```
userlevels_flask_dev-# \d retentions                                                       
               Table "public.retentions"                                                   
   Column    |  Type   | Collation | Nullable | Default                                    
-------------+---------+-----------+----------+---------                                   
 id          | integer |           | not null |                                            
 sponsor_id  | integer |           | not null |                                            
 document_id | integer |           | not null |                                            
Indexes:                                                                                   
    "retentions_pkey" PRIMARY KEY, btree (id, sponsor_id, document_id)                     
Foreign-key constraints:                                                                   
    "retentions_document_id_fkey" FOREIGN KEY (document_id) REFERENCES documents(id)       
    "retentions_sponsor_id_fkey" FOREIGN KEY (sponsor_id) REFERENCES users(id)             
```

Double checking that a user type, "sponsor" was created within the database when we log in as a sponsor:

```
 id | name | user_type |     email     |  password      | organization | created_on | last_login              
----+------+-----------+---------------+----------------+--------------+------------+------------             
  1 | 11   | sponsor   | test@test.com | sha256$6ieI9WHh | a            |            |                         
```
So basically the sponsor login is working.

## Pages and Blueprints for Different User Types

Now that we have a login working with a properly working relational database, we can create different user types and different login pages for the user types.  We should in theory be able to duplicate the sponsor login page with an editor blueprint.

Above, we created a layout which helps us understand what kinds of users have what kinds of dashboards. We can start out with the, "Signup" functionality which now has one type of user, and create a setup which will allow links to two different types of users.

### Adding Additional Blueprints

I added a couple new blueprints for sponsors and editors in the routes.py file, where other blueprints were kept.

```

# Sponsor Blueprint
sponsor_bp = Blueprint(
    'sponsor_bp', __name__,
    template_folder='templates_sponsors',
    static_folder='static'
)

# Editor Blueprint
editor_bp = Blueprint(
    'editor_bp', __name__,
    template_folder='templates_editors',
    static_folder='static'
)

```

Corresponding to these blueprints, I added folders and .jinja2 files within each folder into the project structure.

I also deleted "home_bp" and all corresponding routes to avoid confusion, since this is not being used.

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

#### auth_bp for usertype sponsor

Initially, we only can create one user type, sponsor.  We need to re-write our authentication function to route users over to redirect the sponsor user type over to "sponsor_bp.dashboard_sponsor".

According to the flask-login documentation, [current_user](https://flask-login.readthedocs.io/en/latest/#flask_login.current_user) is a proxy for the user, so in theory we should be able to just query from the user class.

```
    # Bypass if user is logged in
    if current_user.is_authenticated:
        # get user type
        if current_user.user_type=='sponsor':
            return redirect(url_for('sponsor_bp.dashboard_sponsor'))
        elif current_user.user_type=='editor':
            return redirect(url_for('editor_bp.dashboard_editor'))

```

current_user 

```
ERROR:  invalid input syntax for type integer: "user_type" at character 301

STATEMENT:  SELECT users.id AS users_id, users.name AS users_name, users.user_type AS users_user_type, users.email AS users_email, users.password AS users_password, users.organization AS users_organization, users.created_on AS users_created_on, users.last_login AS users_last_login


db     |        FROM users 
db     |        WHERE users.id = 'user_type'
```

So evidently the statement current_user.user_type sees current_user as being equivalent to user.user.id or rather, [the current_user is only calling the id, per this StackOverflow post](https://stackoverflow.com/questions/30778221/flask-login-current-user-returns-only-id).

We have a function called, "login_manager.user_loader":

```
@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None
```
So this returns the user_id. We could try to query based upon the user_id.

To build an appropriate SQL function, we could try it out by logging into our database and playing around with the user table.

To gain a better understanding of how to query a user_type given a user.id, we can check out the [SQLAlchemy Core Tutorial](https://docs.sqlalchemy.org/en/13/core/tutorial.html).  

```
    if current_user.is_authenticated:
        # get user type
        if current_user.user_type=='sponsor':
            return redirect(url_for('sponsor_bp.dashboard_sponsor'))
        elif current_user.user_type=='editor':
            return redirect(url_for('editor_bp.dashboard_editor'))
```

To re-write the above, we're trying to figure out how we can get access to the SQALchemy API, and then performcommands on the Flask application. Within the app itself, and according to the [SQLAlchemy API documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/?highlight=get), we are already connected to the database through what we had set under __init__.py

```
db = SQLAlchemy()
```
On the other hand, we can also use flask-login to do different kinds of queries. "current_user" is from flask-login.

We can define a function within the class that queries for the actual user type, and call that. However, if we are only going to use this once, why would we want to create a function for it?  Well, we might not just do this once - we might repeat it.

Let's just make sure we can create a successful function in this instance first, on the fly, and then we can go back and add it as a function within the User class.

To help build this, we can enter into the python bash within our Docker container:

```
sudo docker run --rm -it userlevels_flask bash

root@60b795f0f834:/usr/src/app# python

```

Do we need a session?  Yes, we need a session. [Per the SQLAlchemy documentation](https://docs.sqlalchemy.org/en/13/orm/session_basics.html), The session establishes conversations and represents a, "holding zone" for objects which we have loaded.  We can use:

```
db.session.query()
```

Because at the top of auth.py we import, "from .models import db, User"

* [This stackoverflow discussion about flask-login with multiple roles](https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes) has the author writing a decorator to check user role type.
* [This function on github](https://github.com/schwartz721/role_required) creates a decorator that can be customized to restrict access to flask views to users who have been given a specific role.

There seem to be a lot of articles on how to solve the general problem of multiple user roles, from different perspectives - however rather than guessing and checking, I should probably focus on what my core issue is, which is - understanding how to use the database, SQLAlchemy, and knowing how to communicate back and fourth with SQL commands or SQLAlchemy commands to read, write, add and delete data from the database in general.

## Reviewing SQLAlchemy ORM and SQLAlchemy Core

### SQLAlchemy Working with Related Objects

[SQLAlchemy Working with Related Objects](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#working-with-related-objects)

#### Adding Data via ORM

For a one to many relationship, to add a piece of data, for example a user, we would do that as follows:

```
jack = User(name='jack', fullname='Jack Bean', nickname='gjffdd')
```
The tutorial itself uses the python command line as a way to demonstrate how to add data and run SQLAlchemy commands. It would be nice if we could log in to the Flask Python command line.  We do have a CLI called, ["Click" which is a part of Flask](https://flask.palletsprojects.com/en/1.1.x/cli/).

What is an SQL Join query?  Basically it's a query that combines two tables, such as a, "User" and a "Document."  This would be the type of query we need when we want to list certain documents attached to certain users, for example.  However right now, we just need a simple query, that lists one type of user.

[W3Schools has an SQL Syntax Tutorial](https://www.w3schools.com/sql/sql_syntax.asp) that we could go through to better understand what we are really trying to do.

##### SQL Statements Tutorial

I went through this tutorial and [put it under a different Github repo here](https://github.com/pwdel/sqltutorial).

##### Back to SQLAlchemy

So in psuedocode, we want an SQLAlchemy command which effectively does:

```
SELECT * FROM users WHERE user_id = current_user;
```
We could pull out the user_type with something along the lines of:

```
SELECT DISTINCT user_type FROM users
WHERE user_id=current_user;
```
Which should display the user_type for the current user.  From this point, we should be able to route the current user to the proper location.

How do we do this in SQLAlchemy and our current code?

Basically, it seems that it needs to be a Query.  Per the documentation [here on Query](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) and the [tutorial on Querying](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#working-with-related-objects):

1. Query can do iterative listing of a set of objects.

```
for instance in session.query(User).order_by(User.id):
     print(instance.name, instance.fullname)
```

2. Query accepts ORM-instrumented descriptors as arguments.

```
for name, fullname in session.query(User.name, User.fullname):
...     print(name, fullname)
```

3. Query can pull out entire rows as tuples with .all() appended to the end.

```
>> for row in session.query(User, User.name).all():
...    print(row.User, row.name)
```

So for what we are trying to achieve above, we likely would use something like:

```
session.query(User.id)
```
However since we had already set up a session, and imported via: "from .models import db, User" we could likely set up and find the user number by a Query, as shown in the [Query API](https://docs.sqlalchemy.org/en/13/orm/query.html).  Query is the source of all SELECT statements generated by the ORM.  :

```
Roughly...

SELECT DISTINCT user_type FROM users
WHERE user_id=current_user;

translates to

user_type = User.query(User.user_type)

or possibly

user_type = User.query(User.user_type).distinct()


```

Overall, our "Bypass if user is logged in" section of auth.py ends up looking like:

```
    # Bypass if user is logged in
    if current_user.is_authenticated:
        # get user number
        user_type = User.query(User.user_type)
        print(user_type)

        # based upon user type, route to location
        if user_type=='sponsor':
            return redirect(url_for('sponsor_bp.dashboard_sponsor'))
        elif user_type=='editor':
            return redirect(url_for('editor_bp.dashboard_editor'))

```
If we take this out, we get a 302 redirect error after logging in, so it may have been solved, e.g. we are being sensed as being a sponsor, and being redirected to sponsordashboard, so it appears to be working. We will have to fix the 302 redirect error and come back to this problem.


##### Understanding Flask-Login

Looking at the [source code for flask-login](https://flask-login.readthedocs.io/en/latest/_modules/flask_login/utils.html#login_fresh) the "current_user" is nothing more than a proxy:

```
#: A proxy for the current user. If no user is logged in, this will be an
#: anonymous user

current_user = LocalProxy(lambda: _get_user())
```

The get_user() function is:

```
def _get_user():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        current_app.login_manager._load_user()

    return getattr(_request_ctx_stack.top, 'user', None)
```

Source code for [login_manager.-load-user() can be found here](https://flask-login.readthedocs.io/en/latest/_modules/flask_login/login_manager.html#LoginManager).

Which, if we look at that we see that:

```
    def _load_user(self):
        '''Loads user from session or remember_me cookie as applicable'''

        if self._user_callback is None and self._request_callback is None:
            raise Exception(
                "Missing user_loader or request_loader. Refer to "
                "http://flask-login.readthedocs.io/#how-it-works "
                "for more info.")
```

So basically it uses remember_me, a cookie based function, rather than checking the database. There is [documentation for remember_me here](https://flask-login.readthedocs.io/en/latest/#remember-me).

Fromn the flask-login documentation, we see that:

> “Remember Me” functionality can be tricky to implement. However, Flask-Login makes it nearly transparent - just pass remember=True to the login_user call. A cookie will be saved on the user’s computer, and then Flask-Login will automatically restore the user ID from that cookie if it is not in the session. The amount of time before the cookie expires can be set with the REMEMBER_COOKIE_DURATION configuration or it can be passed to login_user. The cookie is tamper-proof, so if the user tampers with it (i.e. inserts someone else’s user ID in place of their own), the cookie will merely be rejected, as if it was not there.

So would hypothetically pass "remember=False" to login_user rather than worry about filtering the right type of user to the right section. Basically we could require users to log in even after they close their browser.

## Returning to Routing, Pages, Views


---\/---


```
    # Bypass if user is logged in
    if current_user.is_authenticated:
        # get user number
        
        # get user type
        usertype_check = User.query.filter_by(=).first()

        # based upon user type, route to location
        if current_user.user_type=='sponsor':
            return redirect(url_for('sponsor_bp.dashboard_sponsor'))
        elif current_user.user_type=='editor':
            return redirect(url_for('editor_bp.dashboard_editor'))

```

### Routing Issues on "/"

Of course, once we do this, we have a routing problem, we had previously been routing through to main_bp, via this dashboard, but we no longer have a, "main" dashboard.

```
@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard.jinja2',
        title='User Dashboard.',
        template='dashboard-template',
        current_user=current_user,
        body="You are now logged in!"
    )
```
We should be able to delete the above, however what's more important is to understand what's sending us here. For that we look further into the auth.py file, after the "# Bypass if user is logged in."

```
    # Validate login attempt
    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_bp.dashboard'))
```

Basically the point at which we validate the login is the next section of auth.py after checking whether a user can Bypass the login process.

The user is being redirected to the main_bp.dashboard. Instead we need to check user type and redirect them to the appropriate dashboard as follows:

```
   form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if user.user_type=='sponsor':
                return redirect(url_for('sponsor_bp.dashboard_sponsor'))
            elif user.user_type=='editor':
                return redirect(url_for('editor_bp.dashboard_editor'))
```
The next_page argument may not even matter, because we are not redirecting to a "next_page or..."

Note - there are some specifics in how SQLAlchemy is able to query columns in the database.

##### Main Route "/" Change to Sponsor

Previously we had:

```
@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard.jinja2',
        title='User Dashboard.',
        template='dashboard-template',
        current_user=current_user,
        body="You are now logged in!"
    )
```
When we remove this, we get:

```
flask  | AssertionError: View function mapping is overwriting an existing endpoint function: main_bp.logout

```

We seem to have multiple methods using the same name.

If we remove:

```
@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
```

The error clears. However what happens when we try to log out?  We have to log in to be able to see.


We also had been getting a dashboard error.  

```
werkzeug.routing.BuildError: Could not build url for endpoint 'sponsor_bp.dashboard_sponsor'. Did you mean 'sponsor_bp.dashboard' instead?
```

Whereas previously we had the following definition for the dashboard route:

```
@sponsor_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    return render_template(
        'dashboard_sponsor.jinja2',
        title='Sponsor Dashboard.',
        template='dashboard-template',
        current_user=current_user,
        body="You are now logged in!"
    )
```
We change this to:

```
@sponsor_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return redirect(url_for('sponsor_bp.dashboard_sponsor'))

```
Which still created an error.

What was really happening was that both the function and the template had to be renamed, and share the same name. Therefore on routes.py we had to change our @sponsor.bp route for "/" to:

```
@sponsor_bp.route('/sponsordashboard', methods=['GET'])
@login_required
def dashboard_sponsor():
    """Logged-in User Dashboard."""
    return redirect(url_for('sponsor_bp.dashboard_sponsor'))
```

Basically it seems that we have multiple redirects to "/" and we can't do that.  We have to actually have unique pages.


##### 302 Redirect Error on /sponsordashboard

Once we have the above fixed, we get a repeating 302 error on /sponsordashboard.

Basically, we set up our route for /sponsordashboard, but it looked like this:

```

@sponsor_bp.route('/sponsordashboard', methods=['GET'])
@login_required
def dashboard_sponsor():
    """Logged-in User Dashboard."""
    return redirect(url_for('sponsor_bp.dashboard_sponsor'))

```

So what was happening, was a circular redirect, we were being redirected back to this webpage again and again with that redirect() function.  Instead we needed to add a render_template:

##### werkzeug.routing.BuildError: Could not build url for endpoint 'main_bp.logout'

Basically, we had deleted main_bp.logout to clear another error.  Now we need it back.

However, once we add it back in again, we get the error:

> AssertionError: View function mapping is overwriting an existing endpoint function: main_bp.logout

Which is what we had previously.  Reading more carefully into this error, the, "vew function" appears to refer to the jinja2 file, which has:

```
<a href="{{ url_for('main_bp.logout') }}">Log Out.</a>
```
If we look in our main template folder, under "/project/templates", we can see that there seems to no longer be a logout.jinja2 anymore, so we probably just need to put this back in.

Evidently there is something called a, ["View Decorator" within flask](https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/).

> Because each view in Flask is a function, decorators can be used to inject additional functionality to one or more functions. The route() decorator is the one you probably used already. But there are use cases for implementing your own decorator. For instance, imagine you have a view that should only be used by people that are logged in. If a user goes to the site and is not logged in, they should be redirected to the login page. This is a good example of a use case where a decorator is an excellent solution.

The flask-login [logout_user function](https://flask-login.readthedocs.io/en/latest/_modules/flask_login/utils.html#logout_user) seems to have some conflict.

Logout route:

```
@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
```

The docs mention that @login_required is a decorated view.

The place where this error seems to leave anything we have written is here:

```
flask  |   File "/usr/src/app/project/__init__.py", line 44, in create_app
flask  |     app.register_blueprint(routes.main_bp)

```

Basically, as the blueprint is being registered, there is an error.  Doing some more Googling on the topic, we come up with [this Stackoverflow article](https://stackoverflow.com/questions/34865873/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi):

Which says:

> This error is because you are cyclic import app (you imported app in routes.py and imported routes.py in app) This pattern doesn't work and is not correct. In flask you can write the whole application in single file or you can use flask blueprints to make in modular

So basically, we need to register the sponsor_bp and editor_bp rather than import them as from .routes in the auth.py file.

Take this out of auth.py:

```
# import sponsor and editor blueprints, which includes custom sign-in and sign-up blueprints
from .routes import sponsor_bp, editor_bp
```
Then within __init__.py put under the app_context() function:

```
        # Register Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(routes.sponsor_bp)
        app.register_blueprint(routes.editor_bp)

```

Once we do this, it appears to clear our conflicting logout route, which appears to have been due to a cyclic import.  However now we have:

"flask  | NameError: name 'sponsor_bp' is not defined"

##### NameError: name 'sponsor_bp' is not defined

Basically we're getting this error now because we are not importing the blueprints.

So we can instead try to add the blueprints ad-hoc on auth.py, since we are using them anyway.

```
# Sponsor Blueprint
sponsor_bp = Blueprint(
    'sponsor_bp', __name__,
    template_folder='templates_sponsors',
    static_folder='static'
)

# Editor Blueprint
editor_bp = Blueprint(
    'editor_bp', __name__,
    template_folder='templates_editors',
    static_folder='static'
)
```

Once we do this, we are back to:

```
ssertionError: View function mapping is overwriting an existing endpoint function: main_bp.logout
```
Looking at the imports on auth.py, we see that we have the logout function imported at the top:

```
from flask_login import login_required, logout_user, current_user, login_user
```
However, there is no logout happening here in this function.  So we can try to remove it.  However, this just results in the same error.

Perhaps we need two different logout URLs for sponsor and for editor, or logout needs to be part of auth.py.

##### Finalizing Logout as Sponsor

So in the end, the final way of allowing a sponsor to logout was basically to create a completely different route for sponsor logout:

```
@sponsor_bp.route("/logoutsponsor")
@login_required
def logoutsponsor():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))

@sponsor_bp.route('/sponsordashboard', methods=['GET'])
@login_required
def dashboard_sponsor():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard_sponsor.jinja2',
        title='Sponsor Dashboard',
        template='layout',
        body="Welcome to the Sponsor Dashboard."
    )

```

##### Main Route /login

```
    # Bypass if user is logged in
    if current_user.is_authenticated:
        # Check if user is sponsor
        if current_user.
        return redirect(url_for('main_bp.dashboard'))
```
So where is current_user coming from?  This was an issue at one point, and it was basically due to the vagaries of what current_user really meant, and how it came from flask-login instead of SQLAlchemy-flask.  This was diagnosed and solved above.

##### LoginForm() and SignupForm()

I was able to use the same LoginForm for both users. The login form just gets imported

### Changing routes.py

The main hangup here was that the /logout route seemed to already be used by some internal Flask process or by perhaps flask-login, so we couldn't seem to use it with all of our different blueprints.  I had to create my own new route specifically for logouts by user type at /sponsorlogout and /editorlogout so that the name didn't conflict.

## Creating, Editing and Deleting Documents

Creating documents appears to call for a completely new set of logic.

If we look at this [Flask Blog Example Github Source Code](https://github.com/gouthambs/Flask-Blogging), we see that they have things architected as follows:

#### Flask-Blogging Rough Outline

* Blogging Engine Module (handles the blog storage, configuration, permissions, extension, configuration, user loaders, and calls other functions.)
* Has a Post Processor (handles markdown extensions)
* Uses SQLAStorage
* Stores data in Google Cloud

Basically, it isn't well-organized and there is not a lot of documentation regarding how it should be organized.

However, the convention they seem to use is put a lot of processes into, "Blogging Engine."  We could likewise, create an, "Engine" however we might just call it a, "DocumentEngine," within engine.py.  That being said, "engine.py" is used for a lot of programs and could mean a lot of things, so perhaps we may want to just start a, "documents.py" file.

### Starting with Sponsor Dashboard - Creating Documents

The place I would like to start is simply the Sponsor Dashboard - to create links to additional pages where were can create new documents.

The main page of the sponsor dashboard looks like [this](/readme_img/SponsorDashboard.png) - so we basically just need two links to:

* Document Creation Page
* Document Listing Page

Steps to Quickly Create Document Creation Page without functionality:

1. Create Jinja2 Template for newdocument.jinja2
2. Create /sponsor/newdocument route which renders the Jinja2 template.
3. Make sure links to new pages using, {{ url_for('sponsor_bp.newdocument_sponsor') }} link to the templates and functions, not the routes. the url_for function points toward assets and functions, not toward URL's, that's why it's "url for."

#### New Document Form

While there are much better ways of creating documents with all sorts of markdown editors, we're just going to start out with a simple form.

The form needs to correspond to the Document class, which means we need a "document_name" and a "body." We also need a save button.

Overall, the steps to create a new form displaying, without functionality included:

1. Create thew NewDocumentForm
2. Import "from .forms import NewDocumentForm" on routes.py.
3. Author and adapt the form on our .jinja2 template.
4. Include form=form under render_template within the routes function.

#### New Document Form Logic

Once we have the new document form ready to go, we need to create extended functionality to be able to insert the data from the form into the database, and then reroute the user back to the sponsor dashboard.

Furthermore, we want to be able to assign this document to the User (Sponsor) who created the document, through the relational associaton table (retentions), automatically.

We can use [this python-flask tutorial on creating forms with flask/SQLAlchemy](https://python-adv-web-apps.readthedocs.io/en/latest/flask_db3.html) to help us out.

Filling out the form data includes a couple steps, using SQLAlchemy.  First, we have to put the form data into a variable which follows our Document class from models.py:

```
            # create new document
            newdocument = Document(
                document_name=form.document_name.data,
                document_body=form.document_body.data
            )
```
We then need to commit the record to the database
```
            # add and commit new document
            db.session.add(newdocument)
            db.session.commit()
```
Finally, we can flash a success message and ask to create another document.  Basically, we're just rendering the same document again.

```
# message included in the route python function
            message = "New Document saved. Create another document if you would like."
            return render_template('newdocument_sponsor.jinja2',
        form=form
        )
```

Pulling it all together:

```
    # create new document
    form = NewDocumentForm()
    newdocument = Document(
        document_name=form.document_name.data,
        document_body=form.document_body.data
    )
    # add and commit new document
    db.session.add(newdocument)
    db.session.commit()

    # message included in the route python function
    message = "New Document saved. Create another document if you would like."

    return render_template('newdocument_sponsor.jinja2',
    form=form
    )
```

When we put the above under our new route, we get an error that, "Document" is not defined - which is because we didn't import this from the database. So we have to do the import:

"from .models import db, Document"

However, once we import Document, we get an error from sqlalchemy:

```
column "document_body" of relation "documents" does not exist
```
The reason for this was because I was running the database without having updated it, after updating the column name, "body" to, "document_body."  After restarting the database, this error cleared - however, the not-null constraint of the document_name threw another error.  Basically, the document name can't start off as blank and yet we have a not null constraint.

We can eliminate null document names later through validation, so it's easier to just change the constraint for now.

The above seemed to work, and the form itself saved and worked, however we are now routed to a page that doesn't exist. 

This was because under newdocument_sponsor.jinja2 we had put:

```
      <form method="POST" action="/newdocumentsave">
```
Which redirects us to a non-existant page, /newdocumentsave

Typically with forms being filled out, there is at least some kind of validation, which uses the function, "if form.validate_on_submit():" 

However, even if we redirect to a proper page, we get a, "Method not allowed" error.  This is because we are only allowing, "GET" as a method within our routes, and we need to add, "POST" as well.

```
@sponsor_bp.route('/sponsor/newdocument', methods=['GET','POST'])

AND

@sponsor_bp.route('/sponsor/dashboard', methods=['GET','POST'])
```
After this, we were able to add new documents.

Now, how do we inspect the documents from the command line while running the docker instance with flask on it in the terminal already?

There is a very simple command, we just have to know the database name.  The database name can be found via:

```
sudo docker ps -a
```
From there given that the name is "db", and we get the database name and username from docker-compose.yml do:

```
sudo docker exec -it db psql -d userlevels_flask_dev -U userlevels_flask
```
Generalized this is:

```
sudo docker exec -it DOCKERNAME psql -d DATABASENAME -U USERNAME
```
Once we are in the shell, we can do (don't forget the semicolons):

```
userlevels_flask_dev=# SELECT * FROM users;

userlevels_flask_dev=# SELECT * FROM documents;

```
However, when we do this, we see our user, test@test.com but we don't see any documents.  So this means that documents are not being created, there are not even id's being assigned.

When we take out our, "validate_on_submit" logic, which is not needed at this time because we don't have any form validation, it creates document id's however they are blank document_names and document_body.  This may be because we are not importing using, "session" from Flask.

```
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
```
This did nothing.  Somehow we are "grabbing" blank data.  We are successfully writing that blank data, but the data that we are grabbing is blank, which suggests that there is a problem with the form or interface between the form and the command.

If we instead:

```
    newdocument = Document(
        document_name= request.form.get('document_name'),
        document_body= request.form.get('document_body')
        )

```

Changing to the above still results in blank data.

The problem evidently is in the flask form, which was written as:

```
class NewDocumentForm(FlaskForm):
    """Create New Document Form."""
    document_name = StringField(
        'Document Name',
        validators=[
            DataRequired(),
            Email(message='Enter the Name of the Document.')
        ]
    )
    document_body = StringField(
        'Document Body',
        validators=[
            DataRequired(),
            Email(message='Enter Document Content Here.')
        ]
    )
    save = SubmitField('Save')
```
The, "Email" validator seems to be hanging things up.  These are not emails, so the form should read:


```
class NewDocumentForm(FlaskForm):
    """Create New Document Form."""
    document_name = StringField(
        'Document Name',
        validators=[
            DataRequired()
        ]
    )
    document_body = StringField(
        'Document Body',
        validators=[
            DataRequired()
        ]
    )
    save = SubmitField('Save')
```
With those validators out of the way, the form should work, however the .get() functionality may not have been the proper way to get the data from the form.

When we change it back to this method, and take away all validators, we still have blank data going into our database.

```
from newdocument_sponsor()

    newdocument = Document(
        document_name=form.document_name.data,
        document_body=form.document_body.data
    )

class NewDocumentForm(FlaskForm):
    """Create New Document Form."""
    document_name = StringField(
        'Document Name'
    )
    document_body = StringField(
        'Document Body',
    )
    save = SubmitField('Save')

```
This may be another case where I need to [read the wft documentation extensively](https://wtforms.readthedocs.io/en/2.3.x/forms/#using-forms) in order to solve this simple problem.

There isn't much documentation, but here is a [tutorial on WTF-flask](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms/page/9).

After starting this tutorial, I found the solution, which was decivingly simple.  Basically, the "action" at the top of the form on the form template should just be blank. Previously we had it leading to, /sponsor/dashboard, however it seems that somehow this action was screwing up the way data was going into the form, the action being taken was to, "POST" to the URL rather than just POST in general.  The final form this was written is as follows, at the top of the form on the .jinja2 template:

```
      <form method="POST" action="">
```
Then, updating how the data is captured from the form in our routes.py, we get:

```
def newdocument_sponsor():
    
    # new document form
    form = NewDocumentForm()
    
    if form.validate_on_submit():
        # take new document
        # create new document
        newdocument = Document(
            document_name=form.document_name.data,
            document_body=form.document_body.data
            )
        # add and commit new document
        db.session.add(newdocument)
        db.session.commit()
         # message included in the route python function
        message = "New Document saved. Create another document if you would like."
        # if everything goes well, they will be redirected to newdocument
        return render_template('dashboard_sponsor.jinja2', form=form)

    return render_template('newdocument_sponsor.jinja2',form=form)
```

"validate_on_submit" may have been a critical part of how this pulled together.

#### Explicitly Defining Document Retentions

Once documents can successfully be created, the question arises - who owns these documents?  It's one thing to be able to write a document and throw it into a pile, it's another thing to be able to sort them by author (and editor).

My initial thought would be that this needs to be a piece of logic, or db.session.add to the retentions table within routes.py, based upon the current user (sponsor).

The first logical step is to import the 'Retention' and 'User' classes to routes.py.  We previously had named "Retention," "Retentions" but need to change the word to singluar rather than plural for consistency with, "User" and "Document" classes.

```
from .models import db, Document, Retention
```

Then, within the validate_on_submit conditional function of the, "new document" route, in psuedocode...

```
if form.validate_on_submit():
        # take new document
        # create new document
        newdocument = Document(
            document_name=form.document_name.data,
            document_body=form.document_body.data
            )

        # get current user (sponsor) id

        # populate sponsr id into retentions sponsor_id

        # populate document id into retentions document_id


        # add and commit new document
        db.session.add(newdocument)
        db.session.commit()
         # message included in the route python function
        message = "New Document saved. Create another document if you would like."
        # if everything goes well, they will be redirected to newdocument
        return render_template('dashboard_sponsor.jinja2', form=form)

```

##### Getting the Current User ID and Document ID

Previously within auth.py I had establishe two ways of accessing user information:

1. User query with direct access to data.

```
user_type = User.query(User.user_type)
```

2. User Query with filter_by decorator function

```
user = User.query.filter_by(email=form.email.data).first() 
```
The funny thing is, I don't know for sure if (1) is actually operating or not, as I haven't written any test-based coding to ensure it does anything.

However, (2) for sure is working, because we are able to get a signup/login.

(2) was purely reliant on form data to write a user into the database, not to access any existing database information. So we can build based off of (1) and hopefully it works.

Establishing the user_id:

```
user_id = User.query(User.id)
```
Then populating this id into retentions sponsor_id:

```
newretention = Retention(
    sponsor_id=user_id
    )
```
Finally, adding and committing to session/database:

```
db.session.add(newretention)
db.session.commit()
```

Of course the above logic only takes care of the user_id for the Sponsor, but not the document_id, so it's fairly useless.  To finish things out with the document_id as well:

```
newdocument_id = Document.query(Document.id)
user_id = User.query(User.id)

newretention = Retention(
    sponsor_id=user_id,
    document_id=newdocument_id
    )

db.session.add(newretention)
db.session.commit()

```

All of the above seems logical, except for one thing - in order for us to access the Document id, the Document first must have been written into the database and have had an id assigned to it.  So, we have to first add/commit the Document to database, and then access that most recent Document id with the .first() function.

```
newdocument_id = Document.query(Document.id).first()
```
Moreover, the User class can't just come out of nowhere.  Within auth.py we had set the user based upon the information put into forms by the user. We did not persist the user from the function into the operating environment. Once the user was logged in, that's it - we lost who they are.  The function current_user from wtf-flask seems to just be a cookie, and does not seem to mirror the actual User class model, although I might be wrong on that.

Starting out on a simpler level, just attempting to enter in, "document_id" to the retention table, we get the following error:

```
sqlalchemy.exc.ProgrammingError

sqlalchemy.exc.ProgrammingError: (psycopg2.ProgrammingError) can't adapt type 'Document'
[SQL: INSERT INTO retentions (document_id) VALUES (%(document_id)s)]
[parameters: {'document_id': <Document 1>}]
(Background on this error at: http://sqlalche.me/e/13/f405)

```
So basically, we're inserting data incorrectly.  If we attempt to set document_id to = 1, we get:

```
sqlalchemy.exc.IntegrityError

sqlalchemy.exc.IntegrityError: (psycopg2.errors.NotNullViolation) null value in column "id" of relation "retentions" violates not-null constraint
DETAIL:  Failing row contains (null, null, 1).

[SQL: INSERT INTO retentions (document_id) VALUES (%(document_id)s)]
[parameters: {'document_id': 1}]
(Background on this error at: http://sqlalche.me/e/13/gkpj)

```

So to start off with, we can't even write anything to the retentions table because we have no null values allowed.  Changing that under models.py so that all values are nullable, we still get the error.

So basically, there is no id being written at all in the retentions table.  [This Stackoverflow discussion on sqlalchemy not null constraint failing on primary key](https://stackoverflow.com/questions/34581905/flask-sqlalchemy-not-null-constraint-failed-on-primary-key) showed that we have to set autoincrement equal to true.

```
class Retention(db.Model):
    """Model for who retains which document"""
    """Associate database."""
    __tablename__ = 'retentions'

    id = db.Column(
        db.Integer, 
        primary_key=True,
        autoincrement=True
    )
```
Now that this table is autoincrementing corretly, the next trick is to associate the sponsor_id columns with the current user_id and document_id that was just created, rather than a fixed number.

###### Working with Filtering

So to first attack the documentID, we can go back to entering in our code which involves filtering and using order_by:

```
descending = Document.query.order_by(Document.id.desc())
newdocument_id = descending.first()
```
This results in a sqlalchemy error.  If we look closely at the error:

```
[parameters: {'sponsor_id': 1, 'document_id': <Document 1>}]
```
While the sponsor_id appears valid while entering in a value of 1, document_id seems to be giving, <Document 1> which is not valid. This could be because of the .desc() function, which seems to be more of a description than the actual value.

So what if we want to experiment around with SQLAlchemy commands right within a python shell?  That might be a lot faster way of figuring out exactly what does and does not work, rather than guessing and checking code.

It turns out there is a way to get into the flask shell.

```
Log into the container name "flask"

$ sudo docker exec -it flask /bin/bash

Then enter into flask shell with command "flask shell"

root@1a46f80b993c:/usr/src/app# flask shell
Python 3.9.1 (default, Jan 12 2021, 16:56:42) 
[GCC 8.3.0] on linux
App: project [development]
Instance: /usr/src/app/instance
>>> 
```
Now we can see if we can use [SQLAlchemy-flask commands directly](https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/) within this shell first before we write code.

So first, if we try to add a Document object, we do the following:

```
>>> newdocument = Document(document_name=2,document_body=2)                                                                             
Traceback (most recent call last):
  File "<console>", line 1, in <module>
NameError: name 'Document' is not defined

```
When we try to import the models, we get:

```
>>> from .models import db, Document, User, Retention
Traceback (most recent call last):                                                                                                      
  File "<console>", line 1, in <module>                                                                                                 
KeyError: "'__name__' not in globals" 
```
So rather than importing everything one by one, we can use [RequestContext](https://flask.palletsprojects.com/en/1.1.x/api/#flask.ctx.RequestContext) to evaluate all functions registered on the application for teardown execution. The documentation specifies using test_request_context rather than request_context directly.

```
>>> ctx = app.test_request_context()

We can then work with the ctx if we do:

>>> ctx.push()

We then run:

>>> app.preprocess_request()

until we call "pop"

>>> ctx.pop()

```
However even with the above, things may still not work.  This is because, per this [Stackoverflow discussion on Flask Shell Commands Not working](https://stackoverflow.com/questions/49626250/flask-shell-commands-not-working), you cannot have a module and a package with the same name.  So basically, we can't have:

```
/app and app.py at the same time.
```

We can solve this problem by renaming our app folder within the Dockerfile and docker-compose.yml from:

```
Dockerfile

# set the working directory in the container
WORKDIR /usr/src/app

...

# copy the content of the local src directory to the working directory
COPY ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]


docker-compose.yml

    volumes:
      - ./services/web/:/usr/src/app/

```
 to something like:


```
Dockerfile

# set the working directory in the container
WORKDIR /usr/src/theapp

...

# copy the content of the local src directory to the working directory
COPY ./requirements.txt /usr/src/theapp/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/theapp/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/theapp/entrypoint.sh"]


docker-compose.yml

    volumes:
      - ./services/web/:/usr/src/theapp/

```

Of course once we do that, we have to wait through a long build process on Docker, after running the command, "sudo docker-compose up --build".

After doing this, we still get an error when attempting to set a variable for the Document() class. NameError 'Document' is not defined shows up again.

According to the [Miguel Grinberg Tutorial on Databases within Flask](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database) we actually have to create a shell_context_processor function within our app in order to run it with the context we are looking for.

```
from app import app, db
from project.models import User, Document, Retention

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
```

Where do we put this?  We already have a manage.py with a cli, so we could put it in that file, we just have to make sure we get the import folders correct.  We could also add a function to automatically make the shell context within manage.py by changing our entrypoint.sh to say:

```
if [ "$FLASK_ENV" = "development" ]
then
    echo "Creating the database tables..."
    python manage.py create_db
    echo "Tables created"
    echo "Making the shell context"
    python manage.py make_shell_context
fi
```
Once we save this and then enter into the Container Bash, and then flask shell, if we try to run "db" we get nothing.

```
>>> db

NameError: name 'db' is not defined

```

Attempting to run manage.py make_shell_context also resultsin an error, "invalid syntax."

There are a lot of problems getting this function implemented.  Basically, there is a circular import problem, in that:

* Adding it into manage.py seems to do nothing. In fact, this file seems like it may not run at all anymore, and that our database is actually being initialized under __init__.py.
* If we put this under "models.py," then, "app" is not defined until the app is initialized under __init__.py.
* If we add this under __init__.py, after app initialization, we get another circular problem once we log into the flask shell, in that, "User" is not defined until after the models.py file is imported.

So, to get this all working, we have to go to __init__.py below the app initialization, and enter in:

```
from .models import db, Document, User, Retention
# python shell context processor
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Document': Document, 'Retention': Retention}

```

Note that the models including Document, User, Retention are all being imported.  Once we log into the container instances and then the flask shell, you get:

```
Instance: /usr/src/theapp/instance                                                                                                      
>>> User                                                                                                                                
<class 'project.models.User'>                                                                                                           
>>> Document                                                                                                                            
<class 'project.models.Document'>                                                                                                       
>>> Retention                                                                                                                           
<class 'project.models.Retention'> 
```

So with that, we should double check that everything still works on localhost - which it does.

We now have the direct ability to work with objects in the database and test out commands which will result in a successful query. Replicating what we did above:

```
>>> newdocument = Document(document_name=2,document_body=2)                                                                             
>>> newdocument                                                                                                                         
<Document (transient 139795608497504)>                                                                                                  
>>> descending = Document.query.order_by(Document.id.desc())                                                                            
>>> descending                                                                                                                          
<flask_sqlalchemy.BaseQuery object at 0x7f24b391abb0>                                                                                   
>>> newdocument_id = descending.first()                                                                                                 
>>> print(newdocument_id)                                                                                                               
<Document 1>
```
So the trick is now to find a way to actually print out that document_id.  Interestingly, now that we are in the python shell, we can print out what the various commands are doing, and it shows the exact SQL command being performed.

```
>>> print(Document.query)

SELECT documents.id AS documents_id, documents.document_name AS documents_document_name, documents.document_body AS documents_document_body, documents.created_on AS documents_created_on

which is the same as:

>>> print(db.session.query(Document))                                                                                                   
SELECT documents.id AS documents_id, documents.document_name AS documents_document_name, documents.document_body AS documents_document_body, documents.created_on AS documents_created_on 

```
The SQLAlchemy documentation may not have all of the answers for what we are trying to do. Neither may there may a cookie cutter answer which sovles our problem on StackExchange if we are looking directly for SQL type commands by searching through SQLAlchemy. However, if we search for help with SQL commands, for which there is a ton of documentation, we can probably translate this into SQLAlchemy API language using the [SQLAlchemy API](https://docs.sqlalchemy.org/en/13/core/selectable.html).

Furthermore, we can log into our actual Postgres db container and try out the command in SQL to ensure that's what we really want, before going back and trying it in the python terminal, and then writing the command to code.  Basically we have multiple levels of testing to percolate up what we are trying to do.

So if we just want the most recent document, or highest document number created just moments ago, we can use, in SQL:

```
SELECT MAX(id) FROM documents;
```

How do we actually show this result in SQLAlchemy?  Here are some various commands and their results:

```
>>> Document.query.all()                                                           
[<Document 1>, <Document 2>, <Document 3>]

>>> Document.query.count()
3

>>> Document.query.get(1)
<Document 1>

>>> Document.query.get(Document.query.count())                                     
<Document 3>


>>> Document.query.filter(Document.document_name=='A') 

<flask_sqlalchemy.BaseQuery object at 0x7fa2b2799340>


>>> a = Document.query.get(1)
<Document 1>

>>> a.id
1

>>> a.document_name
'a'

>>> a.document_body
'a'

>>> x = Document.query.order_by(Document.id)
<class 'flask_sqlalchemy.BaseQuery'> 

>>> x[2]
<Document 3>

>>> document_count = Document.query.count() - 1
2

>>> last_document = x[document_count]
<Document 3>

>>> last_document = x[document_count]

>>> last_document.id
3

>>> type(last_document.id)                                                                                                              
<class 'int'>


```

So basically we can get the last document by:

1. Ordering by Document.id
2. Get a count of the Documents
3. Find the last document by indexing by the document_count
4. Index for the last document id

We use this method because documents could hypothetically be deleted in the future, meaning that we can't just get a route count of documents and index for that raw ID, because the IDs may not be equal to the count in the future.

Documentation:

[Document.query.all()](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.all)
[Document.query.count()](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.count)
[Document.query.filter()](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter)
[Document.query.filter_by()](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter_by)
[Document.query.first()](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.first)
[Document.query.get()](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.get)

The final string of code to make everything work with the retentions table was:

```
# after this document has just been added to the database, add retention
# query all documents in order, put into a python object
all_documents_ordered = Document.query.order_by(Document.id)
# query count of all documents, subtract 1 because python index starts at 0
document_index = Document.query.count() - 1
# last document object is document index, or count-1
last_document = all_documents_ordered[document_index]
# new document id for retentions database is indexed last documentid integer
newdocument_id = last_document.id

```
Now, to get user id's, we need a different method.  User Id's are not something that can be pulled out of a, "most recent stack."  The userid is specific to the user in question who happens to be utilizing the app not only at this time, but in future instances.

Looking at [this Stackexchange question on finding the current user in SQLAlchemy](https://stackoverflow.com/questions/47038961/sqlalchemy-current-db-user), there is evidently a database specific, literal way to find the current user.

So first off, if we look at our database object, db:

```
>>> db                                                                                                                                  
<SQLAlchemy engine=postgresql://userlevels_flask:***@db:5432/userlevels_flask_dev>
```
We can see that we can access this.

```
>>> db.session.query(literal_column("current_user"))
```

However, to start off with, "literal_column" is not defined. We need to import this. The [literal_column comes from the sqlalchemy core](https://docs.sqlalchemy.org/en/14/core/sqlelement.html#sqlalchemy.sql.expression.literal_column).

```
from sqlalchemy import literal_column 

current_user_object = db.session.query(literal_column("current_user"))

<flask_sqlalchemy.BaseQuery object at 0x7f4f98549c40>

```
The problem is, this seems to be pulling out the database user, rather than the logged in user within our app.

```
>>> current_user_object[0]                                                                                                             
('userlevels_flask',)
```
If we use the flask-login module, we can't test it out on our python terminal, because the user is, "none" since we're not logged into the app.

Evidently, we can actually get the user-id by indexing current_user.

```
        # get the current userid
        user_id = current_user.id
```
In order to test this out, we have to create a seperate sponsor user, log back in as that user, and create a new document. If we look at the retentions table, we should see a new document tied to a new user.

After logging back in and logging out again, from user1 to user2, and creating two new documents each, the retentions table looks like this:

```
userlevels_flask_dev=# SELECT * FROM retentions;                                                                                        
 id | sponsor_id | document_id                                                                                                          
----+------------+-------------                                                                                                         
  1 |          1 |           1                                                                                                          
  2 |          2 |           2                                                                                                          
  3 |          2 |           3                                                                                                          
  4 |          1 |           4 
```
So basically, it works!


### Listing Existing Documents

#### Setup

We do the same 4 steps we did for the New Document pages for the listing pages to quickly spin up what we need.

1. Create new form if needed
2. Import new form to routes.py or appropriate function.
3. Author and adapt the form or view on our .jinja2 template, with a new view.
4. Include form=form under render_template within the routes function, or any other necessary new view.

Of course, that's not all since we are now displaying rather than intaking information, there will also be back end data querying and possibly the creation of some kind of table or grid view.

#### Views / Jinja2 Templates

This is fairly easy and I was able to basically copy and paste previous work.

#### Querying Documents by User with Retention Table

One of the key parts of being able to work with documents on a user by user basis will of course be to query, using the Retention table, which documents belong to which user.

* We know how to get a specific user now, using current_user.id
* We know that we can look at the retention table, and filter by user_id.

It should be a matter of filtering by user_id on the retention table, and displaying all documents for a given id in a for loop, and putting the results in an array.

We can start off by using the flask shell.

```
current_user_document_ids = Retention.query.filter_by(sponsor_id=1)

>>> current_user_document_ids[0].document_id                                                                                            
1                                                                                                                                       
>>> current_user_document_ids[1].document_id                                                                                           
2  

```
So basically we need a count of all of the document_id's available for that user, and then we iterate through the object from that count and "print out" all of the document id's into another array.

Using that array, we can go back and query the actual document names, id's, or whatever other information we would like to display. Since the SQL index starts at 1, and Python for loops count iteratively with a range starting at 0, we don't need to change the count number by subtracting 1.

```
current_user_document_ids = Retention.query.filter_by(sponsor_id=1)

document_count = Retention.query.count()

document_id_list=[]

for counter in range(0,document_count):
    # create document_id_array by appending all user-document-id's
    document_id_list.append(current_user_document_ids[counter].document_id)

```
So from the above, "document_id_array" is now an array with the document id's tied to the user in question, which we extracted from the Retention table, in order.  We can now access and print these names with:

```
>>> Document.query.filter_by(id=1)[0].document_name                                                                                     
'Document Name 1'                                                                                                                       
>>> Document.query.filter_by(id=1)[0].document_body                                                                                     
'Document Body 1' 

```
Before we build an array or list out of this, it would be helpful to understand what we really need to display this list on a .jinja2 template.


#### Displaying Documents in Grid

[The documentation for jinja2 is here](https://jinja.palletsprojects.com/en/2.11.x/).

Basically, the first step is to render the template from our routes:

```
@sponsor_bp.route('/sponsor/documentlist', methods=['GET','POST'])
@login_required
def documentlist_sponsor():
    """Logged-in User Dashboard."""

    documents = [1,2,3]

    return render_template(
        'documentlist_sponsor.jinja2',
        documentlist=documentlist
    )

```

We have now fed the variable, "documentlist" to the jinja template, as a list.

```
  <div>
  {% for document in documents %}
    <option>{{ document }}</option>
  {% endfor %}
  </div>  
```

This prints out a super simple list of our documents.

Quick review of arrays vs. lists in python:

Lists: 1. Contain different data types. 2. Don't need to explicitly envoke a module. 3. Can't handle arithmetic. 4. Can be listed. 5. Better for shorter sequences.

Arrays: 1. Same datatype. 2. Need to envoke array.array() . 3. Can handle arithmetic. 4. All elements may be the same size.

Beyond normal python arrays, incidentally, numpy arrays are faster and use less memory.

### Putting Documents by User in a List

#### Side Note on Flask Shell

One brief problem I ran into while attempting to log back into the flask shell is that there are two distinct commands for logging into a docker container that I have come across:

```
sudo docker run --rm -it app_name bash

sudo docker exec -it flask /bin/bash
```
The first one runs a new container, which we don't want to do, because it overwrites and can't connect to the database. The second one just connects to an existing container. Exec = execute, go in and execute on the command. "Run" = run the whole system.

#### Adding Document Filtering Listing to Route

Below is the final working code which displays all of the documents to our route function.

```
def documentlist_sponsor():
    """Logged-in Sponsor List of Documents."""
    # get the current user id
    user_id = current_user.id
    # get document id's filtered by the current user
    current_user_document_ids = Retention.query.filter_by(sponsor_id=user_id)
    # get a count of the filtered documents for that particular user
    document_count = current_user_document_ids.count()
    # blank list to put in for loop
    document_id_list=[]
    # loop through documents
    for counter in range(0,document_count):
        # create document_id_array by appending all user-document-id's
        document_id_list.append(current_user_document_ids[counter].document_id)

    # show list of document id's
    documents = document_id_list

    return render_template(
        'documentlist_sponsor.jinja2',
        documents=documents
    )

```

Something we may want to think about, is whether this function could be used on more than just sponsors, and whether we can re-use the code. If this is the case, then we might want to call the function, "documentlist_user()" or something more general.

Since we are rendering the template and passing the variable, "documents" this can then get picked up by the .jinja2 file, and the list of document id's gets neatly printed out.

But what if we wanted to display the document names instead of the ID's?  IT should be a matter of changing the appended indexer, so that rather than using .id, we use .document_name.

In other words:

```
    document_name_list=[]
    # loop through documents
    for counter in range(0,document_count):
        # create document_id_array by appending all user-document-id's
        document_name_list.append(current_user_document_ids[counter].document_name)

    # show list of document id's
    documents = document_name_list

```
Of course, when I attempt to implement the above, we get an error because the "Retentions" class does not have an attribute .document_name.  Basically we have to filter based upon the indicies in Retentions. The, "join" method is the way to do filtering using two tables, rather than multiple for loops.  According to this [StackOverflow discussion on doing a MySQL Query vs. a For Loop]():

> The join method is generally considered better, if only because it reduces the overhead of sending queries back and forth to the database.

Database memory is scarce, as databases are typically smaller processing units, with an extremely thin linux client, such as alpine linux, running one specific program, to manage a database. This contrasts to the architecture of a server, which has more memory as well as a larger processor.  In addition, the join method consolidates the data logic in one place, making the code more transparent.

##### Playing around with Creating a Join SQL Query

So we can create a joined table by running the following SQL command:

```
# SELECT * FROM documents JOIN retentions ON documents.id = retentions.sponsor_id; 
```
Which pulls up a table that looks like the following:

```
 id |  document_name  |        document_body         | created_on | id | sponsor_id | document_id                                       
----+-----------------+------------------------------+------------+----+------------+-------------                                      
  1 | Document Name 1 | This is the first document.  |            |  1 |          1 |           1                                       
  1 | Document Name 1 | This is the first document.  |            |  2 |          1 |           2                                       
  2 | Document Name 2 | This is the second document. |            |  3 |          2 |           3                                       
  2 | Document Name 2 | This is the second document. |            |  4 |          2 |           4                                       
  1 | Document Name 1 | This is the first document.  |            |  5 |          1 |           5                                       
```
So as we can see here, it's a sort of mega-table lining up everything by the document_id.

How do we create this same type of query within SQLAlchemy?  The documentation for [query.join is here](https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.join).

To join Document and Retention tables, you can use the pythonic command:

```
db.session.query(Document).join(Retention)
```
This results in a new object.



### Editing, Saving, Deleting Documents




### Creating a Dropdown for Adding Editors to Documents



### Adding Flash Messages


### 


## Logical Flows Diagramming - Summarization

To create the logic behind what user can see which dashboard, I used [Lucid online flowcharts](https://lucid.app/documents#/dashboard).

![](/readme_img/logical.png)

We have all of the above built now, so it's time to introduce documents.

## Future Work

* We may want to create different tables for different types of users rather than keep the users all in the same table. This is a philosophical design problem. Basically this design problem is based upon whether sponsors and editors may ever change their type, e.g. whether editors may ever be promoted to sponsors. If this is a customer/vendor relationship, then there may never or very infrequently a need to switch user type back and fourth. However if this is a blog writing application, with a group or team of relatively equal types of people who can perform different roles over time, it may be better to keep them in the same table.
* Having an additional user class, basically an administrator, which would be able to change, "trial accounts" who can only see the software into, "sponsor accounts" who can have access to the software, will be fairly critical.  Basically if this is a paid service, or even if it's a non-paid service, there needs to be some kind of administrative user management.
* Further, creating pools, teams or groups of eligibility for use together might be something else fairly universal. Essentially, particularly with larger applications, you may have one or a small team of editors who may be assigned to a sponsor (which could also be considered an author).  There may also be different sponsor accounts. The ability to create different types of relationship tables dynamically will be extremely helpful in this scenario.
* Resources may also be an important thing to create - basically giving a sponsor or privleged account access to a resource, which might be a part of a microservice, even possibly in a different container, may become important in the future.
* Error prevention and UX considerations are extremely minimal in this application. There are lots of easy to fix, low hanging fruit here.
* Dedicated role table - rather than having hard-coded roles, just improve the database to have a table including roles, so that we can write one function which dynamically checks for roles rather than have to continously write different functons for different roles - that's if we anticipate many different roles coming into play in the future.
* [Self Referential Many to Many Relationship](https://docs.sqlalchemy.org/en/13/orm/join_conditions.html#self-referential-many-to-many)
* [Configuring Many to Many Relationships](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/relationships.html#declarative-many-to-many
)
* [SQL Expression Language Tutorial](https://docs.sqlalchemy.org/en/13/core/tutorial.html)

> presents a system of representing the primitive constructs of the relational database directly without opinion, the ORM presents a high level and abstracted pattern of usage, which itself is an example of applied usage of the Expression Language.

* [SQL Statements and Expressions](https://docs.sqlalchemy.org/en/13/core/expression_api.html)
* Dynamically creating pages on routes. So for example, once we are in the sponsor dashboard, rather than calling it, /sponsordashboard we call it /sponsor/dashboard. Going further, once we create new items, such as document1, we have that hosted at /sponsor/documents/document1, for example, with some kind of dynamic naming system such as /sponsor/documents/<doc1>.  However if the optimal system would be using a static page with a loader, do that instead.
* Adding flash messages to form.
* Fix manage.py so we can operate the app and various commands from the CLI.

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