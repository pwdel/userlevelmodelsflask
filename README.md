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

![Initial Database](/readme_img/initialdatabase.png)


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

## Dashboards for Different Users

## References

[How to Make a Flask Blog in One Hour or Less](https://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/)
[Flask Markdown Editor Plugin](https://pypi.org/project/Flask-MDEditor/)
[Example Creation of Table Data - Cars](https://stackabuse.com/using-sqlalchemy-with-flask-and-postgresql/)
[Proper way to handle two different types of user session in one app in flask](https://stackoverflow.com/questions/33575918/proper-way-to-handle-two-different-types-of-user-session-in-one-app-in-flask)
[Stack Overflow: Implementing Flask Login with Multiple User Classes](https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes)
[Using Flask Blueprint to Architect Your Applications](https://realpython.com/flask-blueprint/)