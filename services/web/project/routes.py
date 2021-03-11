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

@main_bp.route('/', methods=['GET'])
@login_required


@sponsor_bp.route('/', methods=['GET'])
@login_required
def dashboard_sponsor():
    """Logged-in User Dashboard."""
    return redirect(url_for('sponsor_bp.dashboard_sponsor'))

