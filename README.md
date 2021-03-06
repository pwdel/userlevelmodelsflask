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

A potential problem arises, in that, the table above has two columns named, "id"

How do we create this same type of query within SQLAlchemy?  The documentation for [query.join is here](https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.Query.join).

To join Document and Retention tables, you can use the pythonic command:

```
document_retentions = db.session.query(Document).join(Retention)
```
This results in a new object, but we can't seem to query "sponsor_id" and "document_id" - this is likely because it lacks the ON clause.

```
document_retentions = db.session.query(Document).join(Retention, Document.id==Retention.sponsor_id)
```
The above seems to have the same behavior, showing <Document 1> upon accessing with document_retentions[0], and having that object accessible by id, name and body but nothing mixed with Retentions. If we are a bit more scrupulous about how we create our join clause, specifying that we are setting the Retention.document_id equal to the Document.id, we do:

```
q = db.session.query(Document.id).join(Retention, Retention.document_id == Document.id)
```
Which now creates an object at q, which can only be accessed by id.

So to review, 

* The first query(A) specifies what the end object is going to include.
* If we query(A.attribute), that end object will only include that one attribute.

However, if we actually pull precisely what we are looking for, and filter for the document in question, in one pull, we get an object that includes precisely the information we want, and we can create a count on that information:

```
q = db.session.query(Document).join(Retention, Retention.document_id == Document.id).filter(Retention.sponsor_id == 1)

>>> q[0].document_name
'Document Name 1'

>>> q[1].document_body
'This is the second document.'

>>> q[2].document_name
'Document Name 5'

>>> q[1].document_name
'Document Name 2'

>>> q.count()
3
```
So basically, we can convert this into a list, per user, in the same way we did above, but without using a for loop, and while only using one query into the database, rather than two.

```
    # get the current user id
    user_id = current_user.id

    # get document objects filtered by the current user
    document_objects = db.session.query(Document).join(Retention, Retention.document_id == Document.id).filter(Retention.sponsor_id == user_id)
    # get a count of the document objects
    document_count = document_objects.count()
    # blank list to append to
    documentname_list=[]
    # loop through document objects
    for counter in range(0,document_count):
        documentname_list.append(document_objects[counter].document_name)

    # show list of document names
    documents = documentname_list

```
The above code worked immediately without having to debug. Excellent!

#### Populating Items into a Grid

Now that I have successfully been able to populate items in general, as a list, into Jinja2, after creating them, on a user by user basis, it will be helpful to be able to populate these items into more of a readable grid-like structure.

So the first thing to do is figure out what exact type of grid we want, which gets designed on an HTML level, and then figure out how to generate this within Jinja2.

To quickly design a table, there are tons of different online table generators, such as [this one](https://www.tablesgenerator.com/html_tables#).

We can generate a table as we would like, and then insert our Jinja2 expressions and statements into the table, eliminating the rows in exchange for Jinja logic.

So for example, the styled table below:

```
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-73oq{border-color:#000000;text-align:left;vertical-align:top}
</style>
<table class="tg" style="undefined;table-layout: fixed; width: 580px">
<colgroup>
<col style="width: 243px">
<col style="width: 337px">
</colgroup>
<thead>
  <tr>
    <th class="tg-73oq">Document Name</th>
    <th class="tg-73oq">Document Body<br></th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-73oq">Doc1</td>
    <td class="tg-73oq">Doc1 Text<br></td>
  </tr>
  <tr>
    <td class="tg-73oq">Doc2</td>
    <td class="tg-73oq">Doc2 Text<br></td>
  </tr>
</tbody>
</table>
```
We can turn into:

```
    <style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;}
    .tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
      overflow:hidden;padding:10px 5px;word-break:normal;}
    .tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
      font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
    .tg .tg-ea8y{background-color:#ffc5c5;border-color:#000000;font-weight:bold;text-align:left;vertical-align:top}
    .tg .tg-73oq{border-color:#000000;text-align:left;vertical-align:top}
    </style>

    <table class="tg" style="undefined;table-layout: fixed; width: 580px">
    <colgroup>
    <col style="width: 243px">
    <col style="width: 337px">
    </colgroup>
    <thead>
      <tr>
        <th class="tg-73oq">Document Name</th>
        <th class="tg-73oq">Document Body<br></th>
      </tr>
    </thead>
    <tbody>
    {% for document in documents %}
      <tr>
        <td class="tg-73oq">{{ document }}</td>
        <td class="tg-73oq"> Placeholder <br></td>
      </tr>
    {% endfor %}
    </tbody>
    </table>
```

Of course it would be more efficient to store the CSS properly and call the style dynamically, but just to do a quick trial above, this works.

Notice that for the document name, we have a list, "document" which includes the document names.  Reading through the Jinja2 documentation, it seems that certain variables like this may be callable by their attribute within Jinja. So, we can try passing our document as an object and accessing attributes as shown below:

```
    {% for document in documents %}
      <tr>
        <td class="tg-73oq">{{ document.document_name }}</td>
        <td class="tg-73oq">{{ document.document_body }}</td>
      </tr>
    {% endfor %}

```

This of course requires changing our route logic as well, but can be done.  The change to the route logic is as follows:

```
    # blank list to append to
    document_list=[]
    # loop through document objects
    for counter in range(0,document_count):
        document_list.append(document_objects[counter])

    # show list of document names
    documents = document_list
```
This above logic works immediately.

### Editing/Saving, Deleting Documents

The first critical function, now that we have documents, would be the ability to go in and actually change what the document says, and what its title is - basically making the database completely mutable.

This requires several layers of tasks to make happen:

1. Creating a special, "Edit" view which pulls up a form that allows the user to enter in what would be a, "New" version of the old document, to over-write the old document text by inputting into a form.

2. Creating a dynamic link to each individual Document Edit page, to allow the User/Sponsor to dynamically be able to click a link to every individual Document that they own for editing purposes.

3. SQLAlchemy logic that allows individual pieces of data within the database to be overwritten, basically access and then write logic.

#### Creating the Route Function with Dynamic Link

Starting off, we have our capability to look at documents which we have set up at the route for "/sponsor/documents" - so it is therefore logical that we pull up additional documents by using the dynamic route "/sponsor/document/<docnumber>" with the docnumber mapping to the id for that particular document.

We start off by creating a route with the variable in the URL, as follows:

```
@sponsor_bp.route('/sponsor/documents/<document_id>', methods=['GET','POST'])
@login_required
def documentedit_sponsor(document_id):

    return render_template(
        'documentedit_sponsor.jinja2'
    )
```
So where do we get the document_number from?  We know from earlier in this investigation that we can get document_id's from the document object using db.session.query().  The code for that would be:

```
    # get the current user id
    user_id = current_user.id
    # get document objects filtered by the current user
    document_objects = db.session.query(Document).join(Retention, Retention.document_id == Document.id).filter(Retention.sponsor_id == user_id)
    # get a count of the document objects
    document_count = document_objects.count()
    # blank list to append to
    document_list=[]
    # loop through document objects
    for counter in range(0,document_count):
        document_list.append(document_objects[counter])

    # show list of document names
    documents = document_list

```

The variable, "documents" includes a list of objects which have attributes from the documents table, filtered by user.  From these objects we can get the unique document_id within our jinja2 template with:

```
document.id
```
So hypothetically, we can feed back from within Jinja to a dynamically created route, using url_for() with a jinja variable.  This should be doable with the url_for function, in the format: "{{ url_for('function_name', variable=variable) }}"

```
{{ url_for('sponsor_bp.documentedit_sponsor', document_id=document.id) }}
```
So the above line, placed within our template:

* Should create a link using the function documentedit_sponsor().
* the variable passed into the function should be dynamically created per the function's specifications, and be equal to document.id.

We can further turn the, "Document Name" into a link itself by using standard HTML href.

```
        <td class="tg-73oq">
          <a href="{{ url_for('sponsor_bp.documentedit_sponsor', document_id=document.id) }}">{{ document.document_name }}</a>
        </td>
```
The above works to create links, and creates dynamic links flawlessly.  There was one small problem with the newly rendered template, which was that we attempted to pass a variable, "document" in the render_template function which had no definition, but once we took that variable out, it worked.

#### Creating Editing Forms

The next step, now that we have the precision capability to enter into document pages, is to be able to go in and actually edit the documents.  This suggests pre-filled forms, which basically populate with document text, and give the user to, "save" again, essentially re-writing the old database entry with a new entry.

Presumably to create an editing form, we should be able to pre-fill with a specified variable.  However before we go any further, let's figure out if we can tweak our current form, the, "create new document" form in order to make the body text box larger.

##### Grow Size of Body Text Box

So basically, we're using Bootstrap, which should have a bunch of standard CSS styles included in it.  This comes from the, "layout" jinja template, which currently encompasses all of our pages.

```
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
```
The [bootstrap documentation can be found here](https://getbootstrap.com/docs/5.0/getting-started/introduction/) - keep in mind, the version we are using may differ slightly from the documentation.  Looking at the documentation for [forms](https://getbootstrap.com/docs/5.0/forms/input-group/), we can see that there is a class, "input-group" which seems to be for larger text.

```
<div class="input-group">
  <span class="input-group-text">With textarea</span>
  <textarea class="form-control" aria-label="With textarea"></textarea>
</div>
```

Further, there is a way to change the actual text area, as follows:

```
<div class="mb-3">
  <label for="exampleFormControlTextarea1" class="form-label">
  Example textarea
  </label>
  <textarea class="form-control" id="exampleFormControlTextarea1" rows="3">
  </textarea>
</div>
```
Combining the two together, we get:

```
<div class="input-group">
    <span class="input-group-text">With textarea</span>
    <textarea class="form-control" id="exampleFormControlTextarea1" rows="3">
    </textarea>
    <textarea class="form-control" aria-label="With textarea"></textarea>
</div>
```
Unfortunately, none of this works and it just creates a jumble of user interface that doesn't work right.  So, after some quick reading, it turns out that there is a way to work with bootstrap [using a module called, "flask-boostrap," per this tutorial here](https://john.soban.ski/pass-bootstrap-html-attributes-to-flask-wtforms.html).

So, we reverted everything back and we're going to have to life with the forms we have for now.

##### Pre-Populating WTF Forms

So one of the first questions is whether we can actually use the same form, the, "NewDocumentForm" and perhaps rename it, "DocumentForm" and just recycle the same old form, while pre-populating it with strings from our existing database.  This would of course make things the easiest, as we don't have to create an additional form.

We can start off to ensure that we can enter our document into the form itself with:

```
On the route:

# query for the document_id in question to get the object
document = db.session.query(Document).filter_by(id = document_id)[0]


On the documentedit_sponsor.jinja2 template:

<p>Current Document Title: <b>{{ document.document_name }}</b></p>
```
...of course not forgetting to pass the variable, "document" under the render_template function within the route.

So now how do we unobstrusively add the Name and the Document Body Content, pre-populated into the form?

Basically, it sounds like we need to pass variables via jinja to html via "input" and "textarea" elements, indexing to the object that has been passed.

```
<input type="text" class="form-control" documentname=document.document_name value="{{ name[0]["name"] }}">
```
This does not work, so we revert over to the [WTF-flask documentation](https://wtforms.readthedocs.io/en/2.3.x/forms/#using-forms), which says that:

> if request.POST and form.validate():
>    form.populate_obj(article)
>    article.save()
>    return redirect('/articles')

> Inside the gated block, we call populate_obj() to copy the data onto fields on the ‘article’ object. We also then redirect after a successful completion. The reason we redirect after the post is a best-practice associated with the Post/Redirect/Get design pattern.

So it seems that the function populate_obj needs to be used.  Whereas above I'm attempting to populate the form in the Jinja/front end template, it appears that the domain of the form may actually controlled by wtf, so it needs to be on the function/server and backend side, which then gets populated up into Jinja as a part of the form.

This also seems to entail creating a different form, "EditForm" rather than, "NewForm."  However there is documentation on how we can inheret from different forms.

[This Stackoverflow Article](https://stackoverflow.com/questions/42984453/wtforms-populate-form-with-data-if-data-exists) appears to go into greater detail.

##### Writing to Database

After the form is filled out on the frontend, we have to populate it to the back-end, which is done on the function.

The difference is, we are oing to be adding or re-writing over a specific datapoint.  We are not creating an entirely new object, we are not subscripting the object we have, because it's already subscripted, we're just indexing it and commiting changes.

```
    if form.validate_on_submit():
        # take new document
        # edit document parameters
        # index [0], which is the row in question for document name
        document.document_name = form.document_name.data
        document.document_body = form.document_body.data
        
        # commit changes
        db.session.commit()
```

There is no need to change the retentions table at this point.  The document remains owned by the same user.

### Creating a Dropdown for Adding Editors to Documents

To create a dropdown, we use wtf-flask and something called, "SelectField."

There is a list of [BasicFields](https://wtforms.readthedocs.io/en/2.3.x/fields/#basic-fields) which include everything from Boolean, Date, Time, Decimal, File Upload, Multiple File Upload, Float, Integer, Radio Button, Select, SelectMultiple and of course Submit.

SelectMultiple is like a checbox rather than a dropdown.

> Select fields take a choices parameter which is a list of (value, label) pairs. It can also be a list of only values, in which case the value is used as the label. The value can be any type, but because form data is sent to the browser as strings, you will need to provide a coerce function that converts a string back to the expected type.

An example can be foudn below:

```
class PastebinEntry(Form):
    language = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
```

We can start out by putting this on our documentedit_sponsor.jinja2 template and route.  We're just testing this out with static choices to make sure we can make it work first.

Jinja2:

```
      <form>
          {{ selector.language.label }}{{selector.language}}
      </form>
```
Route:
```
from .forms import NewDocumentForm, PastebinEntry

    # editor selector
    selector = PastebinEntry()

        # test out selector form
    if selector.validate_on_submit():
        lang = selector.language.data

```
Forms:
```
class PastebinEntry(FlaskForm):
    language = SelectField(
        u'Programming Language', 
        choices=[('cpp', 'C++'), 
        ('py', 'Python'), 
        ('text', 'Plain Text')]
        )
```
#### Dynamic Entries for Dropdown Form

So now that I have created a dropdown form, the next step is to be able to populate said dropdown form with dynamic entries - basically items from a database.

Something to keep in mind is that there are actually *two* forms plugins that utilize forms, and the documentation for these are in different websites:

* [WTForms at Pypi](https://pypi.org/project/WTForms/), with documentation at [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)
* [Flask-WTF at Pypi](https://pypi.org/project/Flask-WTF/) with documentation at [flask-wtf](https://flask-wtf.readthedocs.io/en/stable/), for which I am using Flask-WTF==0.14.3.

Since Flask-WTF is an integration, all of the documentation for WTForms works the same.  Again, the field used for dropdowns is [SelectField](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.SelectField).

The format, with "PROMPT" being the prompt ahead of the field, and "CHOICES" being a list of value, label pairs.

```
SelectField(
    u'PROMPT',
    CHOICES
    )
```
So our main challenge is creating a list of value, label pairs, which can then be placed in, "CHOICES".

The default setup for fields with dynamic choice values is as follows [from this documentation](https://wtforms.readthedocs.io/en/2.3.x/fields/#wtforms.fields.SelectField):

```
class UserDetails(Form):
    group_id = SelectField(u'Group', coerce=int)

def edit_user(request, id):
    user = User.query.get(id)
    form = UserDetails(request.POST, obj=user)
    form.group_id.choices = [(g.id, g.name) for g in Group.query.order_by('name')]
```
So the first thing we need to do is query for our Editors, and figure out how to get that into a list of pairs with, (id, Name) being the pairs.

```
editors = db.session.query(User).filter_by(user_type = 'editor')

>>> editors[0].name
John Smith

>>> editors[0].id
2

```
Since this works, to create a list of pairs. I want to reduce the number of queries on the database, so a loop through the 'editors' object after having done one query would be best, we could do:

```
# pull table of editors object from database
editors = db.session.query(User).filter_by(user_type = 'editor')

# start a blank list
editorlist = []
# use sqlalchemy count() method to count all editors
editorcount = editors.count()

# loop through editors object, populating (id, Name) into a list
for counter in range(0,editorcount):
    # append tuples of (id, Name)
    editorlist.append((editors[counter].id,editors[counter].name))

```
This successfully creates a list of tuples including the editor name and id.  So, the next task is to integrate it into our, NewDocumentForm, or as we have renamed it, DocumentForm.

```
class DocumentForm(FlaskForm):
    """Create New Document Form."""
    document_name = StringField(
        'Document Name',
        validators=[Optional()]
    )
    document_body = StringField(
        'Document Body',
        validators=[Optional()]
    )
    editorchoice = SelectField(
        u'Editor', 
        coerce=int
    )
    submit = SubmitField('Submit')
    
```

Note that we use coerce=int, this is because data on a webpage is always strings, we are attempting to coerce string numbers back into integers, per the documentation:

> Select fields take a choices parameter which is a list of (value, label) pairs. It can also be a list of only values, in which case the value is used as the label. The value can be any type, but because form data is sent to the browser as strings, you will need to provide a coerce function that converts a string back to the expected type.

For the usage of the actual form, we have to use something along the lines of form.editorchoice.choices, and add this to our route function.

Starting out with our document editor route, we can add:

```
    if form.validate_on_submit():
        # take new document
        # edit document parameters
        # index [0], which is the row in question for document name
        document.document_name = form.document_name.data
        document.document_body = form.document_body.data
        # display choices from list of editors
        form.editorchoice.choices = editorlist

        # commit changes
        db.session.commit()
```
Once we have verified that the above works to create an actual list of editors to select from, we can create logic which writes a new editor_id to the retention database for that document in question.

Now, the problem is of course, once we modify the "DocumentForm" which is our only form, we can no longer use it to submit a new document, meaning our database for documents is empty, so we can't get to the, "View Document" link for any given document anymore.  This means we have to start working with the, "Create New Document" route first, ensure that everything works there, and then pivot back to the "Edit Document" route to finish it up.

So reflecting on this, one of the advantages of code inherentance and building based upon re-use of code, is that less code needs to be written and it's easier to read through. One of the disadvantages is that if there are, "subsequent" functions that happen sequentially in time, one after another, you can't debug the subsequent interface until the starter interface has been built already - unless you have a function that seeds the database!

##### Adding Entries into newdocument_sponsor() Route

The newdocument_sponsor() route starts off with:

```
def newdocument_sponsor():
    
    # new document form
    form = DocumentForm()
```

Basically establishing the form, which was previously only a purely user-input form with stringfields.  However now that we are establishing a list of things for the user to pick from, we have some inputs that are needed into the form and function.

```
def newdocument_sponsor(request):

form = DocumentForm(request.POST,obj=editorchoice)
```

Basically, "request" is an input which goes into the form from the function. Where does the function get the input, "request?"  This may not be the way to set everything up 100%.  Looking at these Stackoverflow discussion on 

* [Flask-WTForms and SQLAlchemy SelectField](https://stackoverflow.com/questions/36180084/flask-wtforms-and-sqlaalchemy-selectfield-with-relation) 
* [Dynamically Populate WTForm SelectField with SQLAlchemy Query](https://stackoverflow.com/questions/52635661/dynamically-populate-wtform-selectfield-with-sqlalchemy-query)
* [How to use wtforms SelectField depending on dynamic attributes with flask/sqlalchemy](https://stackoverflow.com/questions/60628496/how-to-use-wtforms-selectfield-depending-on-dynamic-attributes-with-flask-flas)

we make a few observations:

1. The way lists are made appear consistent with how we make lists, except for turning the integer id into a string with str(). This string might be because the user is possibly interested in printing out the id on the view, however it may also be that a string is required as an input.
2. The Form appears to include a "choices" variable.
3. We may need some kind of initialization function under the DocumentForm class.  For example:

```
  def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.newdocument_sponsor.choices = [(editors[counter].id, editors[counter].name) for counter in Editor.query.order_by(Editor.id)]

```
4.  [QuerySelectField](https://wtforms.readthedocs.io/en/2.3.x/ext/?highlight=queryselectfield#wtforms.ext.sqlalchemy.fields.QuerySelectField) seems to be something that needs to be added on the Forms.py file.  According to the wtforms documentation (version 2.3 mentions the documentation for this is depricated since version 2.0 and we should use [WTForms-SQLAlchemy](https://github.com/wtforms/wtforms-sqlalchemy).


##### Using WTForms-SQLAlchemy to Create a Functioning Dynamic Dropdown List

In this section we are using [WTForms-SQLAlchemy](https://github.com/wtforms/wtforms-sqlalchemy).

> WTForms-SQLAlchemy is a fork of the wtforms.ext.sqlalchemy package from WTForms. The package has been renamed to wtforms_sqlalchemy but otherwise should function the same as wtforms.ext.sqlalchemy did.

This wtforms-sqlalchemy includes:

> SelectField integration with SQLAlchemy models.
> 
>    wtforms_sqlalchemy.fields.QuerySelectField
>    wtforms_sqlalchemy.fields.QuerySelectMultipleField
>
> Generate forms from SQLAlchemy models using wtforms_sqlalchemy.orm.model_form

The versioning for this is stored at PyPi [WTForms-SQLAlchemy](https://pypi.org/project/WTForms-SQLAlchemy/).  So, we could install this in our requirements.  We add this to requirements.txt as, "WTForms-SQLAlchemy==0.2"

From this repo, we see an [example build file](https://github.com/wtforms/wtforms-sqlalchemy/blob/master/examples/flask/basic.py) shown on Github.

1. The first step is to get the import working, which is done with the following:

On forms.py...

```
from wtforms_sqlalchemy.orm import model_form, QuerySelectField
```

Now that we have imported QuerySelectField from the proper location, rather than SQLAlchemy from wtforms, since that is being depricated, we can likely use the [old documentation to set things up, based upon ORM-backed fields](https://wtforms.readthedocs.io/en/stable/ext/#module-wtforms.ext.sqlalchemy).

2. Set up a proper form with QuerySelectField included.

Looking at the various Stackoverflow discussions above, one suggested result was a tutorial on the [usage of QuerySelectField from PrettyPrinted](https://github.com/PrettyPrinted/youtube_video_code/tree/master/2017/09/01/Generating%20Select%20Fields%20in%20Flask-WTF%20From%20SQLAlchemy%20Queries%20(QuerySelectField)).

Note that QuerySelectField() is an actual replacement for SelectField()

```
    editorchoice = QuerySelectField(
        query_factory=choice_query, 
        allow_blank=True, 
        get_label='name'
    )

```
* Note that I set, allow_blank=True to allow a default null option.


3. We also have to set up a function for the query_factory to be able to query our object as needed.  query_factory returns a query, not the results.  

```
# define user_query in order for QuerySelectField query_factory to work
def user_query():
    return User.query
```
Per the documentation

> The query property on the field can be set from within a view to assign a query per-instance to the field. If the property is not set, the query_factory callable passed to the field constructor will be called to obtain a query.


4. We set up an SQLAlchemy class in the same way we would previously, without having to pass an argument into it, or the route function.

Then, in the form object itself, we call editorchoice and do a query on that form, filtering by user type, just as we had done previously when we had set up a db.session.query(User) query and put that information into a list. Presumably, QuerySelectField is formatting the information into a list for us.

Of course we need to know which fields we are going to show on the options.

On routes.py
```
form = DocumentForm()

...

# display choices from list of editors
form.editorchoice.query = User.query.filter(User.user_type == 'editor')

```
5. We pass to the template same as had done previously, because this is part of the form object.

```
return render_template('dashboard_sponsor.jinja2',form=form)
```
6. We pass form.editorchoice to have the results show up on the view.

```
     {{ form.editorchoice }}
```


User QuerySelectField(SelectFieldBase) per [this documentation](https://github.com/wtforms/wtforms-sqlalchemy/blob/e172387992601ab8477d767580e957209ac46ea1/wtforms_sqlalchemy/fields.py#L28) includes additional updates.

After all of the above is implemented and working for our dropdown menu, we can then eliminate the function which used a for loop to query for our editors:

```
    def create_editorlist():
        # create list of editors
        # pull table of editors object from database
        editors = db.session.query(User).filter_by(user_type = 'editor')
        # start a blank list into which we will put tuples (id,Name)
        editorlist = []
        # use sqlalchemy count() method to count all editors
        editorcount = editors.count()
        # loop through editors object, populating (id, Name) into a list
        for counter in range(0,editorcount):
            # append tuples of (id, Name)
            editorlist.append((str(editors[counter].id),editors[counter].name))
    
        return editorlist

    # this will create a list of tuples [(id,name),(id,name)]
    editorlist = create_editorlist()
```
After deleting the above, the application still works.

##### Placing a Record in the Retentions Database

The first thing we have to do in order to be able to assign editors to documents is to update the retentions table to allow another column for editor_id's.

```
    editor_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        unique=False,
        nullable=True
    )
```

From here we have to rebuild the Docker container.  Double checking our database after running the Docker container, we see that editor_id is added to the database.

So since editor_id has been added as an available column, how do we add a selected editor onto the retentions table?  Previously we had added a new retention as follows:

```
# Add Sponsor Retention ------------
# get the current userid
user_id = current_user.id
# create a new retention entry
newretention = Retention(
    sponsor_id=user_id,
    document_id=newdocument_id
    )
```
Now, rather than adding simply the user_id, meaning the sponsor_id, we have to find the id of the selected editor, and add that into the retention table.

The problem is, we seem to have an error with editor_id = db.Column from above.

```
sqlalchemy.exc.AmbiguousForeignKeysError

sqlalchemy.exc.AmbiguousForeignKeysError: Could not determine join condition between parent/child tables on relationship User.documents - there are multiple foreign key paths linking the tables.  Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference to the parent table.

```
Basically, it looks like we can't use users.id as a foreign key in two places. What this means, unfortunately, is that we probably have to have a seperate table for Editor-Users, completely seperate and apart from Sponsor-Users. This is not the end of the world, as Editor-Users will likely never convert to become Sponsor-Users, in the model we are creating.

This is of course, unless we can tell the mapper explicitly how SQLAlchemy should use.  

From [this Stackoverflow article on foreign keys error](https://stackoverflow.com/questions/40110574/sqlalchemy-exc-ambiguousforeignkeyserror-after-inheritance)

> When your tables have multiple possible paths to inherit between them (Sales.EmployeeID or Sales.OldEmployeeID), SqlAlchemy doesn't know which one to use and you'll need to tell it the path explicitly, by using inherit_condition. For instance to inherit by EmployeeID:
>__mapper_args__ = { "inherit_condition": EmployeeID == Employee.EmployeeId }
> For the sake of example, you could also inherit by OldEmployeeID, by entering OldEmployeeID == Employee.EmployeeId - this would mean that both your Sales primary key and the Employee primary key are allowed to be different.

The [SQLAlchemy documentation for __mapper_args__ is here](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/inheritance.html).

However, this does not have to deal with inheritance, this has to deal with multiple join paths - we have 

[From the SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/14/orm/join_conditions.html#handling-multiple-join-paths):

> One of the most common situations to deal with is when there are more than one foreign key path between two tables.

We need to figure out how to change our backreferences potentially:

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

[From the SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/14/orm/join_conditions.html#handling-multiple-join-paths) gives an example where:

> "Consider a Customer class that contains two foreign keys to an Address class"

In our situation, that translates to:

> "Consider a Retentions class that contains two foreign keys to a User Class"

The documentation wants to read the error precisely, to understand how to diagnose the problem. "There are many potential messages that have been carefully tailored to detect a variety of common configurational issues; most will suggest the additional configureation that is needed."  So what does our error suggest?

> Could not determine join condition between parent/child tables on relationship User.documents - there are multiple foreign key paths linking the tables.  Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference to the parent table.

So what the error is talking about is that our documents relationship under the User table has a problem:

```
    """backreferences User class on retentions table"""    
    documents = relationship(
        'Retention',
        back_populates='user'
        )
```
We should specify the, "foreign_keys" providing a list of columns which shouldb e counted as containing a foreign key reference to the parent table (User).

Which columns point to the parent table (User)?  We have two columns within the "Retentions" class that point to this User table.

```
    sponsor_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        primary_key=True,
        unique=False,
        nullable=True
    )

    editor_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        unique=False,
        nullable=True
    )
```
So using the [foreign_keys argument](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship.params.foreign_keys) documentation.  The documentation states:

> In normal cases, the relationship.foreign_keys parameter is not required. relationship() will automatically determine which columns in the relationship.primaryjoin condition are to be considered “foreign key” columns based on those Column objects that specify ForeignKey, or are otherwise listed as referencing columns in a ForeignKeyConstraint construct.

> When specifying foreign_keys with Declarative, we can also use string names to specify, however it is important that if using a list, the list is part of the string: "[list1,list2]"

```
    """backreferences User class on retentions table"""    
    documents = relationship(
        'Retention',
        foreign_keys='[Retention.sponsor_id,Retention.editor_id]',
        back_populates='user'
        )
```
This does not seem to clear the error, so it might be that we have to specify the foreign keys within the Retention class.

If we instead add foreign_keys to the retentions table, as shown:

```
    """backreferences to user and document tables"""
    user_sponsor = db.relationship(
        'User',
        foreign_keys='[users.id]',
        back_populates='documents'
        )

    user_editor = db.relationship(
        'User',
        foreign_keys='[users.id]',
        back_populates='documents'
        )
```
When we add the above, we get a, "mapper failed to initialize" error on User.query.get(user_id):

> sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'mapped class User->users'. Original exception was: Could not determine join condition between parent/child tables on relationship User.documents - there are multiple foreign key paths linking the tables.  Specify the 'foreign_keys' argument, providing a list of those columns which should be counted as containing a foreign key reference to the parent table.

So, perhaps eliminating the foreign_keys argument within the documents = relationship() portion of the User class would solve this. However, when we eliminate that, we still get an AmbiguousForeignKeysError.

Perhaps the error is wrong.  We could go back to the example given at the SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/14/orm/join_conditions.html#handling-multiple-join-paths):

> "Consider a Retentions class that contains two foreign keys to a User Class"

In this example, the Customer class has two columns foreign keys to an Address class, address.id.  Whereas in our scenario, our Retentions table has two columns with ForeignKeys to our user.id.

The solution seems to be to have one relationship argument, which includes a string linking to both mapped keys.

##### Considering Going a Different Route - Editor Table

After removing the following, everything works:

```

    editor_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        unique=False,
        nullable=True
    )
```

Everything works again.  Why can't we have one document pointing to two users?  Why can't we establish shared ownership?  This seems ridiculous.  I phoned a senior developer friend, who agreed with the idea that we should be able to create a workable single-inheretance table.

Probably what I have to do is read through the entire documentation for the relationship() function on SQLAlchemy.  Previous in this project, I read through the SQLAlchemy documentation, but kind of skipped through relationship() because it was fairly long. I may just need to go back in and comb through it.

No problem can withstand the assault of sustained thinking.

###### Combing through SQLAlchemy relationship()

Relationship:

> Provides a relationship between two mapped classes.  This corresponds to a parent-child or associative table relationship. The constructed class is an instance of [RelationshipProperty](https://docs.sqlalchemy.org/en/14/orm/internals.html#sqlalchemy.orm.RelationshipProperty).

Classical mapping:

> mapper(Parent, properties={
> 'children': relationship(Child)
> })

> Some arguments accepted by relationship() optionally accept a callable function, which when called produces the desired value.  The callable is invoked by the parent, "Mapper" at "mapper initialization" time, only when mappers are first used. This can be used to resolve order-of declaration and other dependency issues.

> When using the Declarative Extensions, the Declarative initializer allows string arguments to be passed to, "relationship()". These string arguments are converted into callables that evaluate the string as Python code.

Another consieration, is to think about the parent-child relationship. How does parent-child work?  The parent has a primary id, like user_id, which gets placed on the child table as a column. So with an association table, the association table is always a child of the other two parent tables.

*Parameters*

```
 function sqlalchemy.orm.relationship(argument, secondary=None, primaryjoin=None, secondaryjoin=None, foreign_keys=None, uselist=None, order_by=False, backref=None, back_populates=None, overlaps=None, post_update=False, cascade=False, viewonly=False, lazy='select', collection_class=None, passive_deletes=False, passive_updates=True, remote_side=None, enable_typechecks=True, join_depth=None, comparator_factory=None, single_parent=False, innerjoin=False, distinct_target_key=None, doc=None, active_history=False, cascade_backrefs=True, load_on_pending=False, bake_queries=True, _local_remote_pairs=None, query_class=None, info=None, omit_join=None, sync_backref=None)
```

* argument - a mapped class, or Mapper instance, representing the target of the relationship.

* secondary - for a many-to-many relationship, it specifies the intermediary table, and typicaly is an instance of Table. This may also be passed as a callable function. relationship.secondary keyword argument is applied in the case where the intermediary Table is not expressed in any direct class mapping. If the secondary table is explicitly mapped elsewhere, e.g. an association object, it may cause a conflict.

* active_history=False - when True, indicates that the previous value for a many to one reference should be loaded when replaced, if not already loaded. History tracking logci for many-to-ones normally only needs to be aware of the, "new" value in order to perform a flush. This is available for applications which make use of, "get_history()" to know the previous value of an attribute.

* backref = indicates the string name of a property to be placed in the mapper's class that will handle this relationship in the other direction. Can be passed as a backref() object to control the configuration ofthe new relationship.  The relationship.backref/relationship.back_populates behavior has the advantage that common bidirectional operations can reflect the correct state without requiring a database round trip.

* back_populates - has the same meaning as backref, but the complementing property is not created automatically and must be explicitly created.

* overlaps - target mapper with which this relationship may write to the same foreign keys upon persistence. This eliminates the warning that the relationship will conflict with another upon persistence. This is only to be used for relationships that are truly conflicting with one another.

* bake_queries=True - cache the construction of SQL used in lazy loads. 

* cascade - comma sepearted list of cascade rules which determines how Session operations should be cascaded from parent to child. The default is False, which means the default is used, "save-update, merge."  There are other standard operations, ways to delete orphans, etc.

* cascade_backrefs=True - boolean value indicating if save-update cascade shold operate along an assignment event intercepted by a backref.

* collection_class - returns a list-holding object

* comparator_factory - extends comparator which provides custom SQL clause generation.

* distinct_target_key=None

* doc - Docstring which will be applied to the resulting descriptor.

* foreign_keys - a list of columns which are to be used as foreign key columns, or columns which refer to the value in a remote column, within the context of this relationship() object's relationship.primaryjoin condition.

* info - optional data dictionary which will be populated into MapperPRoperty.info

* innerjoin=False - when true, joined eager loads will use inner join to join against related tables instead of an outer join. The purpose of this option is generally one of performance, as inner joins generally perform better than outer joins.

* order_by - indicatres the orderign that should be applied when loading these items. relationship.order_by is expected to refer to one of the Column objects to which the target class is mapped.

* primaryjoin - used as the primary join of a child object against the parent object, in a many-to-many relationship, the join of the parent object to the association table. By default this value is computed based upon the foreign key relationships of the parent and child tables (or association tables)

* remote_side - used for soft referential relationships, indicates the column or list of columns that form the remote side of the relationship.

* query_class - Query subclass that will be used internally returned by a dynamic relatinship, that is , a relationship that specifies lazy="dynamic"

* secondaryjoin - will be used as the join associaton table to the child object. By default, this value is computed based upon the foreign key relationships of the assocation and child tables.

* single_parent - installs a validator that will prevent objects from being associated with more than one parent at a time

* uselist - boolean that indicates of this property should be loaded as a list or a scalar.

* viewonly=False - when set to true, relationship is used only for loading objects, not for any persistence operation. So basically, a super static record of what's going on in the relationship table.


#### Specifying Alternate Join Conditions

[Specifying alternate join conditions](https://docs.sqlalchemy.org/en/14/orm/join_conditions.html#relationship-primaryjoin).  

> The default behavior of relationship() when constructing a join is that it equates the value of primary key columns on one side to that of foreign-key-referring columns on the other. We can change this criterion to be anything we’d like using the relationship.primaryjoin argument, as well as the relationship.secondaryjoin argument in the case when a “secondary” table is used.

So typically you have a 1:1 relationship between primary keys and foreign keys.  We can change this with primaryjoin and secondaryjoin.  primaryjoin can be used to filter for certain types of data elements within a foreign key address.

From the documentation:

```
class User(Base):
    ...
    boston_addresses = relationship("Address",
                    primaryjoin="and_(User.id==Address.user_id, "
                        "Address.city=='Boston')")

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    ...
    city = Column(String)
    ...

```

* Used the and_() conjunection to construct two predicates for the join condition, joining User.id and Address.user_id to each other, and limiting rows in Address to just city='Boston'.  Typically this only comes into effect at query time, so when someone queries .boston_addresses specifically.

So could we use the following, in the User class, to specify our primary join being sponsor_id and contingent upon string, 'sponsor'?

```
class Retention(db.Model):
    sponsor_user = relationship(primaryjoin="and_"(User.id==Retention.sponsor_id, "
        "User.user_type=='sponsor')")

```
However, we don't want an object strictly called, "sponsor_user," or "editor_user" unless we can eliminate the ambiguous relationship, "user" that we currently have, which looks like this:

```
    user = db.relationship(
        'User',
        back_populates='documents'
        )
```

So we could start off by writing a new relationship to replace sponsor_id to start off with:

```
sponsor_id = db.Column(
    db.Integer
    db.ForeignKey('users.id'),
    primary_key=True,
    unique=False,
    nullable=True
)

sponsor_user = db.relationship(primaryjoin="and_"(User.id==Retention.sponsor_id, "
        "User.user_type=='sponsor')")

```
Attempted to use a primaryjoin relationship on the retentions table as follows, eliminated the "user" relationship.

```

    """backreferences to user and document tables"""

    # type sponsor user, 
    # using primaryjoin to specify the user_type only as sponsor for when the User.id refers to Retention.sponsor_id
    sponsor_user = db.relationship("User",
        primaryjoin="and_(User.id==Retention.sponsor_id, "
        "User.user_type=='sponsor')")

    # opening up to editor_id as well
    editor_user = db.relationship("User",
        primaryjoin="and_(User.id==Retention.editor_id, "
        "User.user_type=='editor')")

```

However, since user is so critical in the login functionality, this doesn't compute.  We need to maintain the "user" backreference to avoid breaking login functionality overall.  The above was meant to replace the need for ForeignKey.

There seems to be a trap between, "ambiguous foreign keys" and "can't find any foreign keys"

#### Self-Referential Many to Many Relationship

[Self Referential Many to Many Relationship](https://docs.sqlalchemy.org/en/14/orm/join_conditions.html#self-referential-many-to-many)

If the association table refers twice to the one of the same classes, for example:

```
class Node(Base)
...

Table(...,
Column("left_id",Integer,ForeignKey("node.id"),primary_key=True),
Column("right_id",Integer,ForeignKey("node.id"),primary_key=True)
)
```
SQLAlchemy can't automatically know which columns should connect to which for the right_nodes and left_nodes relationships.

[relationship.primaryjoin](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship.params.primaryjoin), [relationship.secondaryjoin](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html#sqlalchemy.orm.relationship.params.secondaryjoin) establish how we would like to join the association table.

##### Taking a Shortcut and Eliminating db.ForeignKey from editor_id in Retention

Out of all of the above, the only thing that seems to work is to eliminate the editor_id frmo the Retention table, and to make the relationship very basic.

We could probably write our own custom logic to deal with editor assignments in the Retention table.  Basically we only ever write integers into that column who are editors.

The other route to go would be to create a completely seperate user type, an "Editor_User," with a completely different login function.


#### Adding editor.id to Relations Table

Intersting side note, if we take out the ForeignKey('users.id') from the editor_id column in the Retentions class, the app still seems to work:

```
    editor_id = db.Column(
        db.Integer, 
        primary_key=True,
        unique=False,
        nullable=True
    )

```

Does this column really need to be mapped to a user?  What if this column is just a record of numbers, and we don't really bother to see whether those numbers exist or not?  What would be the disadvantage?

The disadvantage might be that if an editor gets deleted, or if that account no longer exists, then the table might not know what to do, the editor_id might not get notified or updated somehow in our Retentions table automatically.  So, presumably, we would need to write this updating code anyway, right?

There might also be confusions about what is actually available.

So to start off with, when we attempt to add a new value, even if it does not include an editor, we get the following error:

```
sqlalchemy.exc.IntegrityError

sqlalchemy.exc.IntegrityError: (psycopg2.errors.NotNullViolation) null value in column "editor_id" of relation "retentions" violates not-null constraint
DETAIL:  Failing row contains (2, 2, null, 2).
```
Previously we had solved this by inserting an autoincrement function.  We actually do want null values to be a possible answer.  If we populated our, "write" to the database with a string value, this error was cleared.

As to how we populate our database with our actual editor_id, that is another question.

```
form.editorchoice.query = User.query.filter(User.user_type == 'editor')
...

# extract the selected editor choice from the form
selected_editor_id=form.editorchoice.data

# create a new retention entry
newretention = Retention(
    sponsor_id=user_id,
    editor_id=selected_editor_id,
    document_id=newdocument_id
    )
```
In the above, we grab the choice from the form at form.editorchoice.query, which is filtered from the editor user types.

However, when we do this, we get an error: "sqlalchemy.exc.ProgrammingError: <unprintable ProgrammingError object>" - basically, the form.editorchoice.data is an object, and can't be read.

If we look under the flask shell what that object looks like:

```
>>> selected_editor = User.query.filter(User.user_type == 'editor')


>>> selected_editor[0].id 
1

>>> type(selected_editor[0].id)                                                                                                         
<class 'int'>

```
So basically, we can get the id to populate into the Retention table.  However, this might not be the right way to do this.  SQLAlchemy has a get() function.  However, get() is more for grabbing objects and properties of those objects based upon a known identify, so that won't do it.  We need to pull the identity itself.

There is also the problem of datatypes.  editor_id is supposed to be an integer.

```
    editor_id = db.Column(
        db.Integer, 
        unique=False,
        nullable=True
    )
```
Whereas above we see that our query on the shell was an int, data from forms might instead be strings. So, we might need to convert this to an int in order for it to populate.  The following works:

```
# extract the selected editor choice from the form
selected_editor_id=int(form.editorchoice.data.id)
```
Testing it out with a couple different editors:

```
userlevels_flask_dev=# SELECT * FROM retentions;                                                                                        
 id | sponsor_id | editor_id | document_id                                                                                              
----+------------+-----------+-------------                                                                                             
  1 |          2 |         1 |           4                                                                                              
  2 |          2 |         1 |           5                                                                                              
  3 |          2 |         3 |           6 
```
It works.

#### Fixing Indvidual Document Routes and Views

To fix the following:

```
@sponsor_bp.route('/sponsor/documents/<document_id>', methods=['GET','POST'])
@login_required
def documentedit_sponsor(document_id):
```
We need to mimic what we successfully built in the, "newdocument" form above.

We can eliminate our ad-hoc way of creating a list of editors:

```
    # create list of editors
    # pull table of editors object from database
    editors = db.session.query(User).filter_by(user_type = 'editor')
    # start a blank list into which we will put tuples (id,Name)
    editorlist = [(0,'None')]
    # use sqlalchemy count() method to count all editors
    editorcount = editors.count()
    # loop through editors object, populating (id, Name) into a list
    for counter in range(0,editorcount):
        # append tuples of (id, Name)
        editorlist.append((editors[counter].id,editors[counter].name))
```

After cleaning up the sponsor/document/<number> route, we get a working version as shown below:

```
@sponsor_bp.route('/sponsor/documents/<document_id>', methods=['GET','POST'])
@login_required
def documentedit_sponsor(document_id):

    # new document form
    form = DocumentForm()

    # query for the document_id in question to get the object
    document = db.session.query(Document).filter_by(id = document_id)[0]

    # display choices from list of editors
    form.editorchoice.query = User.query.filter(User.user_type == 'editor')


    if form.validate_on_submit():
        # take new document
        # edit document parameters
        # index [0], which is the row in question for document name
        document.document_name = form.document_name.data
        document.document_body = form.document_body.data

        # display choices from list of editors
        form.editorchoice.choices = editorlist

        # commit changes
        db.session.commit()


    return render_template(
        'documentedit_sponsor.jinja2',
        form=form,
        document=document,
        )
```
To display the editor name at the top of the page, we have to do a query. We don't have the editor_id directly, but we can find it from the retention table using a join query:

We have the document_id, and can use document_id=1 as a stand-in.  We want to query the Retention table and filter it for that document_id

```
>>> current_editor_object = db.session.query(Retention).filter_by(document_id=document_id) 

>>> current_editor_object[0]
<Retention 1,2,1>

>>> current_editor_object[0].editor_id                        
1    

>>> editor_id = 1

>>> current_editor = db.session.query(User).filter_by(id=editor_id)


```

Using a join query:

```
>>> q = db.session.query(Retention).join(User, User.id == Retention.editor_id).filter(Retention.document_id == document_id)

>>> q[0]         
<Retention 1, 2, 1>

>>> q[0].editor_id
1

>>> current_editor_id = db.session.query(Retention).join(User, User.id == Retention.editor_id).filter(Retention.document_id == document_id)[0].editor_id

>>> current_editor_id
1

>>> editor_object = db.session.query(User).filter(User.id == current_editor_id)[0]


```
With this information we can pass the editor_object to our view and display the name or any other needed information.

The next step is to go in and edit the, "Retentions" table and add a new editor_id from whatever editor_id might be selected from the dropdown form.

This was done with the following:

```
        # grab the selected_editor_id from the form
        selected_editor_id=int(form.editorchoice.data.id)

        # add new retention
        retention_object.editor_id = selected_editor_id
```
#### Improving the Document List for Better User Feedback

It would be helpful to include the editor attached to each document under the documentlist, for easier reference, in the same way we do on the edit document page.

First, we have to get a list of editors object, which lines up with the document_objects.

```
>>> document_objects = db.session.query(Document).join(Retention, Retention.document_id == Document.id).filter(Retention.sponsor_id == user_id)
```
The above gives a list of document objects filtered by the current sponsor_id.  We want the same thing but for editor objects, filtered by the current sponsor_id.

```
>>> editor_perdocument_objects = db.session.query(User).join(Retention, Retention.editor_id == User.id).filter(Retention.sponsor_id == user_id)

```
Based upon this list of editors per document objects, we should be able to append to an editor list in the same way that we appended to a document list.  This logic will only work if there is a one to one relationship between the editors and documents.  Below is the augmented way of working with documents.

```

    # Document objects and list, as well as Editor objects and list
    # this logic will only work if document_objects.count() = editor_objects.count()
    # get document objects filtered by the current user
    document_objects = db.session.query(Document).join(Retention, Retention.document_id == Document.id).filter(Retention.sponsor_id == user_id)
    # editor per document objects
    editor_perdocument_objects = db.session.query(User).join(Retention, Retention.editor_id == User.id).filter(Retention.sponsor_id == user_id)
    # get a count of the document objects
    document_count = document_objects.count()
    editorobjects_count = editor_perdocument_objects.count()
    # blank list to append to for documents and editors
    document_list=[]
    editor_name_list=[]
    # loop through document objects
    for counter in range(0,document_count):
        document_list.append(document_objects[counter])
        editor_name_list.append(editor_perdocument_objects[counter].name)

    # show list of document names
    documents = document_list

    # Editor objects and list
    # get editor objects filtered by the 
    editors = editor_name_list

```
Finally, populating into jinja is a bit different, because we now have a list of name strings which is parallel to the list of document objects, so we're not combining them into the same object.  Therefore we have to take advantage of jinja's [loop.index0] way of indexing through a loop as shown below.

    {% for document in documents %}
      <tr>
        <td class="tg-73oq">{{ editors[loop.index0] }}</td>

#### Error on Editor Name Display

The following query:

```
editor_perdocument_objects = db.session.query(User).join(Retention, Retention.editor_id == User.id).filter(Retention.sponsor_id == user_id)
```
Creates an error such that the wrong editor is shown on the last document.  The error is not in the for loop, but in the actual query.  If we query the base query:

```
>>> db.session.query(User).join(Retention, Retention.editor_id == User.id)[0].name                                                      
'John Smith'                                                                                                                            
>>> db.session.query(User).join(Retention, Retention.editor_id == User.id)[1].name                                                     
'John Smith'                                                                                                                            
>>> db.session.query(User).join(Retention, Retention.editor_id == User.id)[2].name                                                     
'Second Editor'                                                                                                                         
>>> db.session.query(User).join(Retention, Retention.editor_id == User.id)[3].name                                                     
'Second Editor'                                                                                                                         
>>> db.session.query(User).join(Retention, Retention.editor_id == User.id)[4].name                                                     
'John Smith' 
```
As we can see, the proper names show up.  It is possible that we could filter the sponsor_id previous to the join to see if that clears things up.

```
editor_perdocument_objects = db.session.query(User).filter(Retention.sponsor_id == user_id).join(Retention, Retention.editor_id == User.id)
```

This could be because we set user_id to a fixed value in our flask shell as we were building this earlier.  However, if we check this, we see that we still have the same problem.

Do we really need the filter() to get everything to work properly?  Well, yes because if we have different sponsors, they are going to hypothetically see each other's documents in the documentlist view, or rather editors will not line up properly and a list of all editors will get pulled on the routes function.

What is the following statement really saying?

```
.join(Retention, Retention.editor_id == User.id)
```

What is User.id?  Basically User.id is the primary key we are using to JOIN the Retention table to the User table. Perhaps we shouldn't start off with that. Perhaps we should instead join by the sponsor_id, since that is what we are generating data for.

```
>>> db.session.query(Retention).filter(Retention.sponsor_id == user_id)[0].editor_id                                                                                  
1                                                                                                                                                                     
>>> db.session.query(Retention).filter(Retention.sponsor_id == user_id)[1].editor_id                                                                                 
1                                                                                                                                                                     
>>> db.session.query(Retention).filter(Retention.sponsor_id == user_id)[2].editor_id                                                                                
3                                                                                                                                                                     
>>> db.session.query(Retention).filter(Retention.sponsor_id == user_id)[3].editor_id                                                                                 
3                                                                                                                                                                     
>>> db.session.query(Retention).filter(Retention.sponsor_id == user_id)[4].editor_id                                                                                 
1 
```
The above pattern does give the proper results that we are looking for. However how do we now display the names rather than just the id's, without querying the database in a for loop?

```
# querying for the Retention which will give the proper editor id in the order asked

>>> sponsor_retentions = db.session.query(Retention).filter(Retention.sponsor_id == user_id)

```
Of course this only gives us the Retentions object, with no information about the editors. We need some kind of, "union" function in the database to pull precisely what we are trying to pull into an ordered object.  Or, we may need to reverse the entire quiery.

```
editor_names = db.session.query(Retention).filter(Retention.sponsor_id == user_id).join

# generalized large table where the Retention.sponsor_id is the joining factor

sponsor_objects = db.session.query(User).join(Retention, Retention.sponsor_id == User.id)

# generalized large table where the Retention.editor_id is the joining factor

editor_objects = db.session.query(User).join(Retention, Retention.editor_id == User.id)

# filter down those editor_objects by the sponsor_id 

We can't.


```
Probably the best course of action is to play around with all of this in SQL first, then translate it over to SQLALchemy.  On the other hand, we can just, "talk through" SQLAlchemy and think about the logic on paper in order to build the table.  How do we print out the results of a table?

```
q=db.session.query(User).join(Retention, Retention.editor_id == User.id)

from sqlalchemy import select

r=select('*').select_from(q)

```
##### Building the Query in SQL


```
# SELECT retentions.sponsor_id,users.id,retentions.editor_id,retentions.document_id FROM retentions JOIN users ON users.id=retentions.editor_id;    

 sponsor_id | id | editor_id | document_id

------------+----+-----------+-------------                                                                                                                                       
          1 |  2 |         2 |           2
          1 |  2 |         2 |           3
          1 |  2 |         2 |           4
          4 |  2 |         2 |           5
          4 |  3 |         3 |           6
          4 |  2 |         2 |           7
          4 |  3 |         3 |           8
          4 |  2 |         2 |           9
(8 rows)
```
The above query would hypothetically give us what we need.  If we were able to get that query, we could then filter it down by sponsor_id and get the editor_id in order lining up with the proper document_id for that particular sponsor.

```
 sponsor_id | id | editor_id | document_id

------------+----+-----------+-------------                                                                                                                                       
          4 |  2 |         2 |           5
          4 |  3 |         3 |           6
          4 |  2 |         2 |           7
          4 |  3 |         3 |           8
          4 |  2 |         2 |           9
(8 rows)
```

To mimic the above original query to simply create the table, we can do:

```
>>> q=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id)

>>> q.count()
32
```
To filter this down into our 8 main results, we do:

```
>>> q=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id).join(Retention, User.id==Retention.editor_id)

>>> q.count()
8
```
Inspecting that secondary query, we get the above expected results.  So next the task is to filter by a given sponsor, let's say we filter by sponsor_id=4:

```
>>> q=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id).join(Retention, User.id==Retention.editor_id).filter(Retention.sponsor_id==4)

>>> q.count()
5
```
We are now getting close to our expected result.  Interestingly here we have found that we can filter for both the sponsor_id and the editor_id, as we had been interested earlier.  This suggests that an ultimate query could potentially be built which also queries the document_name and document_body, further reducing load on the database down to one query rather than two.

Note that the .id follows the editor, rather than the sponsor, so we should be able to pull out the editor name with this query.

```
>>> q[0].sponsor_id                                                                                                             
4                                                                                                                               
>>> q[0].editor_id                                                                                                       
2                                                                                                                               
>>> q[0].id                                                                                                                     
2    
```
Pulling out the editor name:

```
q=db.session.query(Retention.sponsor_id,User.name,Retention.editor_id,Retention.document_id).join(Retention, User.id==Retention.editor_id).filter(Retention.sponsor_id==4)

>>> q[0].sponsor_id                                                                                                             
4                                                                                                                               
>>> q[0].editor_id                                                                                                       
2        
>>> q[0].name                                                                                                                   
'Editor Edintarion'

```
So with this query, we should be able to create the proper list of names to display on the view.  Within our routes.py, we set:

```
editor_perdocument_objects=db.session.query(Retention.sponsor_id,User.name,Retention.editor_id,Retention.document_id).join(Retention, User.id==Retention.editor_id).filter(Retention.sponsor_id==user_id)
```
When we enter this into our routes.py, we still get the following error upon accessing the appropriate page:

```
sqlalchemy.exc.ProgrammingError

sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column users.username does not exist
```

This was fixed by adding, "username" column to models (even though we don't use it).  However, the editors still do not show up properly next to the documents, even with our new query.  Perhaps the idea of building one big table which includes document names, and then running a for loop on that object, would be a better idea than doing two seperate for loops on two seperate objects.

#### Creating an Overall SQL Call To Mimic Our Desired View

Firstly we must ask the question, what kind of table do we want to end up with?

The columns of the final table should look like this:

| Sponsor | Editor | Document Name | Document Body |


We can start with:

```
# SELECT retentions.sponsor_id,users.id,retentions.editor_id,retentions.document_id FROM retentions JOIN users ON users.id=retentions.editor_id;  
```

and modify it to:

```
# SELECT retentions.sponsor_id,users.id,retentions.editor_id,retentions.document_id,users.name,documents.document_name,documents.document_body FROM retentions JOIN users ON users.id=retentions.editor_id JOIN documents ON documents.id=retentions.document_id;  
```
This query spits out the type of result that is more consistent and includes the results we are looking for, with:

 sponsor_id | id | editor_id | document_id |      name      | document_name | document_body                        
------------+----+-----------+-------------+----------------+---------------+---------------                       
          1 |  2 |         2 |           1 | Johnny Editor  | Apple         | Red                                  
          1 |  2 |         2 |           2 | Johnny Editor  | Bannana       | Yellow                               
          1 |  3 |         3 |           3 | Rocky Editface | Orange        | Orange                               
          1 |  3 |         3 |           4 | Rocky Editface | Grape         | Purple                               
          1 |  2 |         2 |           5 | Johnny Editor  | Salad         | Green                                

So from there, translating it into an SQLAlchemy Query...our original query was:

```
q=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id).join(Retention, User.id==Retention.editor_id)
```

Modifying to mimic our larger table query, we added a join of the documents table setting the document id's together:

```
q=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id).join(Retention, User.id==Retention.editor_id).join(Document, Document.id==Retention.document_id)
```

Then we pull out the desired information into the query:

```
q=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id,User.name,Document.document_name,Document.document_body).join(Retention, User.id==Retention.editor_id).join(Document, Document.id==Retention.document_id)
```
Looking at the results to ensure our query looks good:

```
>>> q[0].document_name                                                                                             
'Apple'                                                                                                            
>>> q[0].name                                                                                                      
'Johnny Editor' 
>>> q[1].document_name                                                                                             
'Bannana'                                                                                                          
>>> q[1].name                                                                                                      
'Johnny Editor'                                                                                                    
>>> q[2].document_name                                                                                             
'Orange'                                                                                                           
>>> q[2].name                                                                                                      
'Rocky Editface'                                                                                                   
>>> q[3].document_name                                                                                           
'Grape'                                                                                                            
>>> q[3].name                                                                                                      
'Rocky Editface'                                                                                                   
>>> q[4].document_name                                                                                            
'Salad'                                                                                                            
>>> q[4].name                                                                                            
'Johnny Editor' 

```
This lines up perfectly with what we expect to see on the view.  That being said, we have to be able to filter this for a defined sponsor_user id, assuming we have multiple sponsors.  

```
>>> user_id=1                                                                                                      
>>> q=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id,User.name,Document.document_name,Document.document_body).join(Retention, User.id==Retention.editor_id).join(Document, Document.id==Retention.document_id).filter(Retention.sponsor_id == user_id) 

>>> q.count()                                                                                                      
5  
```
...Which is the expected result for user_id set staticly to 1, vs. 9 total documents.  So going back into the route, we can change our overal query and consolidate our code, which was originally:

```
    # Document objects and list, as well as Editor objects and list
    # this logic will only work if document_objects.count() = editor_objects.count()
    # get document objects filtered by the current user
    document_objects = db.session.query(Document).join(Retention, Retention.document_id == Document.id).filter(Retention.sponsor_id == user_id)
    # editor per document objects
    editor_perdocument_objects=db.session.query(Retention.sponsor_id,User.name,Retention.editor_id,Retention.document_id).join(Retention, User.id==Retention.editor_id).filter(Retention.sponsor_id==user_id)

    # get a count of the document objects
    document_count = document_objects.count()
    editorobjects_count = editor_perdocument_objects.count()
    # blank list to append to for documents and editors
    document_list=[]
    editor_name_list=[]
    # loop through document objects
    for counter in range(0,document_count):
        document_list.append(document_objects[counter])
        editor_name_list.append(editor_perdocument_objects[counter].name)

    # show list of document names
    documents = document_list

    # Editor objects and list
    # get editor objects filtered by the 
    editors = editor_name_list


    return render_template(
        'documentlist_sponsor.jinja2',
        documents=documents,
        editors=editors
    )

```
The finalized route code is slimmed down considerably, with only one query to the database:

```
def documentlist_sponsor():
    """Logged-in Sponsor List of Documents."""
    # get the current user id
    user_id = current_user.id
    
    # Document objects list which includes editors for all objects
    # this logic will only work if document_objects.count() = editor_objects.count()
    # get document objects filtered by the current user
    document_objects=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id,User.name,Document.document_name,Document.document_body).join(Retention, User.id==Retention.editor_id).join(Document, Document.id==Retention.document_id).filter(Retention.sponsor_id == user_id) 

    # get a count of the document objects
    document_count = document_objects.count()
    
    # blank list to append to for documents and editors
    document_list=[]

    # loop through document objects
    for counter in range(0,document_count):
        document_list.append(document_objects[counter])

    # show list of document names
    documents = document_list

    return render_template(
        'documentlist_sponsor.jinja2',
        documents=documents,
    )

```
We then modify the view from:

```
    </colgroup>
    <thead>
      <tr>
        <th class="tg-73oq">Editor</th>
        <th class="tg-73oq">Document Name</th>
        <th class="tg-73oq">Document Body</th>
      </tr>
    </thead>
    <tbody>
    {% for document in documents %}
      <tr>
        <td class="tg-73oq">{{ editors[loop.index0] }}</td>
        <td class="tg-73oq">
          <a href="{{ url_for('sponsor_bp.documentedit_sponsor', document_id=document.id) }}">{{ document.document_name }}</a>
        </td>
        <td class="tg-73oq">{{ document.document_body }}</td>
      </tr>
    {% endfor %}
    </tbody>
    </table>

```
to:

```
    </colgroup>
    <thead>
      <tr>
        <th class="tg-73oq">Editor</th>
        <th class="tg-73oq">Document Name</th>
        <th class="tg-73oq">Document Body</th>
      </tr>
    </thead>
    <tbody>
    {% for document in documents %}
      <tr>
        <td class="tg-73oq">{{ document.name }}</td>
        <td class="tg-73oq">
          <a href="{{ url_for('sponsor_bp.documentedit_sponsor', document_id=document.document_id) }}">{{ document.document_name }}</a>
        </td>
        <td class="tg-73oq">{{ document.document_body }}</td>
      </tr>
    {% endfor %}
    </tbody>
    </table>

```

Given the way our new table is structured, we had to change:

* document_id=document.document_id, because document.id now maps to User.id

"<td class="tg-73oq">{{ document.name }}</td>" seems counterintuitive because it seems that we are drawing out the document name, but we are really calling the username.

After implementing the above changes, We have a problem where one documents is showing up twice sequentially (document_id=3) but it is skipping (document=2).  This may have been a problem with the view's logic.  Part of this might be the order in which the documents are appearing on the SQL query, which is as follows:

```
 sponsor_id | id | editor_id | document_id |       name        | document_name | document_body                     
------------+----+-----------+-------------+-------------------+---------------+---------------                    
          3 |  1 |         1 |           1 | Editor Edintarion | Apple         | Red                               
          3 |  1 |         1 |           3 | Editor Edintarion | Cabbage       | Green                             
          3 |  2 |         2 |           4 | Johnny Editor     | Grape         | Purple                            
          3 |  1 |         1 |           5 | Editor Edintarion | Bannana       | Yellow                            
          4 |  2 |         2 |           6 | Johnny Editor     | Car           | Vroom                             
          3 |  2 |         2 |           2 | Johnny Editor     | Carrot        | Orange                            
(6 rows)                                                                                                           
```
Basically since "Carrot" shows up after "Car," it does not seem to show up on the list.  This probablem can likely be mitigated by an, "order_by" subfunction on the .query function.

```
document_objects=db.session.query(Retention.sponsor_id,User.id,Retention.editor_id,Retention.document_id,User.name,Document.document_name,Document.document_body).\
join(Retention, User.id==Retention.editor_id).\
join(Document, Document.id==Retention.document_id).\
order_by(Retention.sponsor_id).\
filter(Retention.sponsor_id == user_id) 

```
After this change, the problem appears to have been resolved. There was a temporary problem with a double entry after the fix, but after re-starting the database and app, everything appears to show up in order and that may have been something dealing with the legacy database or query.

#### Adding Links to List and Dashboard

* On documentlist - create a link to, "createnewdocument" - Done
* On createnewdocument - create a link to, "documentlist" - Done

### Finishing Up Editor Views

#### Editor List of Documents

1. Create View
2. Create Route
3. Route Function, Logic

Basically I was able to copy and paste a lot of code from the sponsor side to create this set of documents.

#### Editing Individual Documents

Same as above.


### Restricting Access

Beyond the capability of simply allowing editing, there must also be logic which actually restricts access to the user who is designated to see a particular page.

Where does this apply?

#### Mapping Out Access Restriction

From the top down...

1. Editors Should Not Be Able to See Sponsor Routes
2. Sponsors Should Not Be Able to See Editor Routes
3. Sponsors Should Not Be Able to Access Each Other's Documents
4. Editors Should Not Be Able to Access Each Other's Documents

#### Creating Editor Restriction Function

We can set up a sponsor_only() function and put it within all sponsor routes.

```
def sponsor_only()
    if not current_user.user_type == 'sponsor'
        flash('You do not have access to view this page.')
        return redirect(url_for('editor_bp.dashboard_editor'))
```
To add this to sponsor routes, use:

```
    # checking if user type is sponsor
    ret = sponsor_only()
    if( not ret ):
        return ret
```

Since this is not easily working, we can cover this in the future when we deal with security and user interface.

### Adding Flash Messages

We can cover this in the future, under, "UX"


## Logical Flows Diagramming - Summarization

To create the logic behind what user can see which dashboard, I used [Lucid online flowcharts](https://lucid.app/documents#/dashboard).

![](/readme_img/logical.png)

## Putting Everything into Production

* [Reference Guide for How We Went into Production Last Time](https://github.com/pwdel/postgresloginapiherokudockerflask#pushing-everything-to-production)
* [With more detailed information here](https://github.com/pwdel/herokudockerflask#logging-into-heroku)


* Copy envrionmental variables over from previous project, since the project is essentially the same on the server side.
* We have to change the Postgres database name

On the docker-compose.prod.yml file:

```
web:
environment:
    - DATABASE_URL=postgresql://userlevels_flask:userlevels_flask@db:5432/userlevels_flask_prod

environment:
      - POSTGRES_USER=userlevels_flask
      - POSTGRES_PASSWORD=userlevels_flask
      - POSTGRES_DB=userlevels_flask_prod
```

Other confusing variables:

Will come back to this if needed.

### Build Production File:

```
sudo docker-compose -f docker-compose.prod.yml up -d --build
```

Log into Heroku CLI

```
$ sudo heroku container:login
```
### Push to Heroku

Check image name

```
$ sudo docker images

~/Documents/Projects/userlevelmodelsflask : sudo docker images                                                                                                        
REPOSITORY                                      TAG                 IMAGE ID            CREATED             SIZE                                                      
userlevels_flask                                latest              c6fc1fa1d23d        3 minutes ago       170MB                                                     

```

1.    Login to Heroku

2.    Login to Heroku Container registry with: 

sudo docker login --username=_ --password=$(heroku auth:token) registry.heroku.com

3.    Create app:

```
heroku create
Creating app... done, ⬢ evening-ravine-99954
https://evening-ravine-99954.herokuapp.com/ | https://git.heroku.com/evening-ravine-99954.git
```

3.    Tag with:              

```
sudo docker tag userlevels_flask registry.heroku.com/evening-ravine-99954/web
```
4.    Push to registry with: 

```
sudo docker push registry.heroku.com/evening-ravine-99954/web
```

5.    Release to web with: 

```
heroku container:release web
```

Once we do this, and set up all of the environmental variables, we are going in the right direction.

### Production Error Diagnosis 

#### R10 Error

```
Error R10 (Boot timeout) -> Web process failed to bind to $PORT within 60 seconds of launch
```

We actually have to get the Postgres variables from the Postgres deployment itself, not just use dummy values.  This is under the Postgres >> Settings >> Database Credentials

* Host (SQL_HOST)
* Database (can remain postgres)
* Database User
* Database Password
* Port
* Endpoint URL
* ...And anything else needed

#### SQLAlchemy Error

```
sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres
```
We notice along our error stream the following message:

```
/util/deprecations.py
```
So it may be that our SQLAlchemy may be depricated.

Looking at our requirements.txt:

```
Flask==1.1.2
Flask-SQLAlchemy==2.4.1
gunicorn==20.0.4
psycopg2-binary==2.8.6
click==7.1.2
Flask-Login==0.5.0
Flask-WTF==0.14.3
email-validator==1.1.2
Flask-Assets==2.0
cssmin==0.2.0
jsmin==2.2.2
WTForms-SQLAlchemy==0.2
```
Flask-SQLAlchemy has been updated to 2.5.1, so we can try that.  Updating the version still resulted in the same error.

After some online research, we hve a couple different new hypotheses:

1. Problem in config.py, around the database path.

Our database path given in Heroku is:

```
postgres://gdsrkgnknuyemx:ebbd981227e0918ab389043f31af7aea0a4fc8f9aab870c5caeb12da351d9358@ec2-54-205-183-19.compute-1.amazonaws.com:5432/dav7sdb2ndvpfm
```
* Based upon a [Stackexchange answer](https://stackoverflow.com/questions/62688256/sqlalchemy-exc-nosuchmoduleerror-cant-load-plugin-sqlalchemy-dialectspostgre), our DATABASE_URL should start with, "postgresql://" not "postgres://"
* However, if we try to change this, we get: "Cannot Overwrite Attachment values for DATABASE_URL"

Basically, in order to re-write it, I had to destroy the database with:

```
heroku addons:destroy heroku-postgresql -a evening-ravine-99954                                                           
 ▸    WARNING: Destructive Action                                                                                                                                     
 ▸    This command will affect the app evening-ravine-99954
 ▸    To proceed, type evening-ravine-99954 or re-run this command with --confirm evening-ravine-99954
```
This did indeed delete the database, but when we attempted to re-create the databse, the DATABASE_URL was forced and reconnected.

Further, if we look at what our codebase in our previous project under config.py, which was successfully deployed, looks like, it shows:

```
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
```
Whereas our new setup is:

```
# Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
```
However changing to sqlite:// seemed to do nothing.

Since we can't seeem to change the DATABASE_URL in Heroku, it seems to be a system-level variable, and since we have the following in our settings...

```
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://")
```
The solution is likely to change this DATABASE_URL to be a different address right within the code, for example:

```
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_PROD", "postgresql://")
```

...and to set the DATABASE_URL_PROD to the proper variable name beginning with postgresql:// rather than postgres://.

That worked!

Unfortunately, to run things in development again, I have to change that variable back to:

```
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://")
```

And then switch back again to DATABASE_URL_PROD before pushing to Heroku one more time.  This is of course annoying.  One solution for that would be to create a /heroku branch off of the working development branch, or perhaps off of main, which contains a dummy environmental variable that doesn't work for either environment, and then a /dev and /heroku branch which has the proper env variable for their respective environments.

Another way to deal with it would be some kind of if statement which detects the environment automatically first, however this is complicated for now.

### Putting Into Production Again After Fixing /sponsor/documents List View

After we put things into production for a second time after fixing the Document per user list view, we got the following error:

```
021-03-26T19:49:50.134958+00:00 app[web.1]: [SQL: SELECT users.id AS users_id, users.name AS users_name, users.username AS users_username, users.user_type AS users_user_type, users.email AS users_email, users.password AS users_password, users.organization AS users_organization, users.created_on AS users_created_on, users.last_login AS users_last_login 

2021-03-26T19:49:50.134959+00:00 app[web.1]: FROM users 

2021-03-26T19:49:50.134959+00:00 app[web.1]: WHERE users.id = %(pk_1)s]

2021-03-26T19:49:50.134959+00:00 app[web.1]: [parameters: {'pk_1': '2'}]

2021-03-26T19:49:50.134960+00:00 app[web.1]: (Background on this error at: http://sqlalche.me/e/14/f405)

2021-03-26T20:25:25.609777+00:00 heroku[web.1]: Idling

2021-03-26T20:25:25.625269+00:00 heroku[web.1]: State changed from up to down

2021-03-26T20:25:27.145873+00:00 heroku[web.1]: Stopping all processes with SIGTERM

2021-03-26T20:25:27.371509+00:00 heroku[web.1]: Process exited with status 143
```
Above we had added, "username" to our "User" class in order to fix another error we were having.  This might have been to compensate for something we introduced, "username" rather than something inherent in the program.

We had created a couple different functions:

```
    """Sponsor vs. Editor Role Functions"""
    def sponsor_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if current_user.role == 'Sponsor':
                return f(*args, **kwargs)
            else:
                flash("You need to be a Sponsor to view this page.")
                return redirect(url_for('index'))

        return wrap

    def editor_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if current_user.role == 'Editor':
                return f(*args, **kwargs)
            else:
                flash("You need to be an Editor to view this page.")
                return redirect(url_for('index'))

        return wrap

    def __repr__(self):
        return '<User {}>'.format(self.username)
```

What does the, '<User {}>'.format(self.username) do?

##### Cleaning Up Code on Local Machine Relating to, "username"


If we delete the def __repr__(self): that we called out above, as well as the decorator functions we get a fully functional app, without any errors from SQLAlchemy.

So, it is possible that we had an error previously because the __repr__(self) function was being checked within the user model by SQLAlchemy which was looking to make sure we had, "username" which was not necessary.  I also removed:

```
    username = db.Column(
        db.String(100),
        unique=False,
        nullable=True
    )
```

From the User schema, after which it is removed, everything still seems to build and work fine.

The "__repr__(self):" function is defined by the designer of a type, in order to provide a means for users of the type to represent values of that type unambiguously, with a string.  So this is likely needed.  However, we don't have a username, so maybe not.

#### Returning to Diagnosing the Deployment

The first thing we can try is actually to delete the database, and then re-run or re-start the app in exactly the same form.  There may have been a legacy problem with the database.  If we destroy the database and then start again, we can see if this resolves the issue.

We destroy the database and then get the following SQLAlchemy Error at https://docs.sqlalchemy.org/en/14/errors.html#error-f405, which says:

> ProgrammingError
> Exception raised for programming errors, e.g. table not found or already exists, syntax error in the SQL statement, wrong number of parameters specified, etc.
> This error is a DBAPI Error and originates from the database driver (DBAPI), not SQLAlchemy itself.
> The ProgrammingError is sometimes raised by drivers in the context of the database connection being dropped, or not being able to connect to the database. For tips on how to deal with this, see the section Dealing with Disconnects.

If we delete the database, we still get the above error, however this could be because we have not re-set the environmental variables.

After replacing our environmental variables we get:

```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) FATAL:  role "egaepatncgvcbk" is not permitted to log in

2021-03-27T00:22:36.798903+00:00 app[web.1]: 
```
So, we likely have to release the code again to re-build the database and everything at start.

Rebuilding everything from the start...we get a different error, which we have seen previously:

```
sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres
```

#### Returning to Diagnosing the Deployment - Dialects

As had been diagnosed earlier in this readme file, we had to change "postgres://" to "postgresql://" at the start of the DATABASE_URL_PROD variable.

```
postgresql://adsfadsfdsf...etc

```

After this was completed, absolutely everything worked in production.

## Conclusion

### Things I Learned

* Don't go into convoluted SQL Tool deep level configuration if you don't have to, it goes really far in the weeds. Just try to design database relational models in a way that will prevent you from having to do custom configuration.
* You have to check your own logic on restricting access between pages, which was fairly intuitive previously anyway - but really though, if you don't sepcify certain users can't access certain pages, then you are opening the door for cross-user editing.
* Using flask-principal rather than creating convoluted new user types is probably desirable. [Flask-principal](https://pythonhosted.org/Flask-Principal/)
* Should also probably use [flask-security](https://pythonhosted.org/Flask-Security/)
* For moving to production, sometimes there may be environmental variable name conflicts, where the new production system might demand that it uses a certain variable name and value, and this could cause problems in running the application.
* Much like in excel, running two seperate for loops on two completely differently generated tables is a disorganized practice and may result in confusing end results. What is probably more effective is creating one overall, "result" table for a view, and then displaying results from that table, including strings and so-fourth.  There should be more confidence that everything is lining up properly.

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
* Fix manage.py so we can operate the app and various other commands from the CLI.
* [Go through the Jinja Documentation](https://jinja.palletsprojects.com/en/2.11.x/templates/) to gain a fuller understanding of how to design the front-end.
* [using a module called, "flask-boostrap," per this tutorial here](https://john.soban.ski/pass-bootstrap-html-attributes-to-flask-wtforms.html) to implement bootstrap designs.

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