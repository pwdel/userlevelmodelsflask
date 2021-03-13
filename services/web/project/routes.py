"""Logged-in page routes."""
from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from flask_login import current_user, login_required
from flask_login import logout_user
from .forms import NewDocumentForm
from .models import db, Document

# Blueprint Configuration
# we define __name__ as the main blueprint, and the templates/static folder.
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

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

# when any user goes to /, they get redirected to /login
@main_bp.route('/', methods=['GET'])
@login_required


# ---------- sponsor user routes ----------

@sponsor_bp.route("/sponsor/logout")
@login_required
def logoutsponsor():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))

@sponsor_bp.route('/sponsor/dashboard', methods=['GET','POST'])
@login_required
def dashboard_sponsor():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard_sponsor.jinja2',
        title='Sponsor Dashboard',
        template='layout',
        body="Welcome to the Sponsor Dashboard."
    )

@sponsor_bp.route('/sponsor/newdocument', methods=['GET','POST'])
@login_required
def newdocument_sponsor():
    
    # new document form
    form = NewDocumentForm()
    
    if form.validate_on_submit():
        # take new document
        # create new document
        newdocument = Document(
            document_name=form.document_name.data,
            document_body='world'
            )
        # add and commit new document
        db.session.add(newdocument)
        db.session.commit()
         # message included in the route python function
        message = "New Document saved. Create another document if you would like."
        # if everything goes well, they will be redirected to newdocument
            return render_template('dashboard_sponsor.jinja2',
                form=form
                )

    return render_template('newdocument_sponsor.jinja2',
        form=form
        )

# ---------- editor user routes ----------

@editor_bp.route("/editor/logout")
@login_required
def logouteditor():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))

@editor_bp.route('/editor/dashboard', methods=['GET'])
@login_required
def dashboard_editor():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard_editor.jinja2',
        title='Editor Dashboard',
        template='layout',
        body="Welcome to the Editor Dashboard."
    )