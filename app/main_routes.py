from flask import Blueprint, render_template

bp = Blueprint('main', __name__)

@bp.route('/start')
def home():
    return render_template('home.html')
