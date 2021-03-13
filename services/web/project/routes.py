"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from flask_login import logout_user

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

# ---------- editor user routes ----------

@editor_bp.route("/logouteditor")
@login_required
def logouteditor():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))

@sponsor_bp.route('/editordashboard', methods=['GET'])
@login_required
def dashboard_editor():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard_editor.jinja2',
        title='Editor Dashboard',
        template='layout',
        body="Welcome to the Editor Dashboard."
    )