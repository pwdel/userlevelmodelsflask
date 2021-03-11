"""Database models."""
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


"""User Object"""
class User(db.Model):
    """User account model."""

    __tablename__ = 'users'

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

    """backreferences User class on retentions table"""    
    documents = relationship(
        'Retentions',
        back_populates='user'
        )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

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


"""Document Object"""
class Document(db.Model):
    """Document model."""
    """Describes table which includes documents."""

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
    """backreferences User class on retentions table"""
    users = relationship(
        'Retentions',
        back_populates='document'
        )


"""Association Object - User Retentions of Documents"""
class Retentions(db.Model):
    """Model for who retains which document"""
    """Associate database."""
    __tablename__ = 'retentions'

    id = db.Column(
        db.Integer, 
        primary_key=True
    )

    sponsor_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'),
        primary_key=True,
        unique=False,
        nullable=False
    )

#    editor_id = db.Column(
#        db.Integer, 
#        db.ForeignKey('users.id'),
#        unique=False,
#        nullable=True
#    )

    document_id = db.Column(
        db.Integer, 
        db.ForeignKey('documents.id'),
        primary_key=True,
        unique=False,
        nullable=False
    )

        """backreferences to user and document tables"""
    user = db.relationship(
        'User', 
        back_populates='documents'
        )

    document = db.relationship(
        'Document', 
        back_populates='users'
        )