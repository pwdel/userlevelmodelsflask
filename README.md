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
5. Build "Messaging" Protocol which includes saves and submits and requests back and fourth.

## Getting Started

We have previous work already done having built a 


## References

[Stack Overflow: Implementing Flask Login with Multiple User Classes](https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes)
[Using Flask Blueprint to Architect Your Applications](https://realpython.com/flask-blueprint/)