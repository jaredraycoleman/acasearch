from typing import Dict, List, Tuple
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_pymongo import PyMongo
from forms import ConferenceForm
import dotenv
import os
import datetime

from app_base import app, bp, FLASK_ENV, SECRET_KEY
from app_oauth import get_app_metadata, requires_role

dotenv.load_dotenv()

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

@bp.route('/')
def index():
    conferences = list(mongo.db.conferences.find())
    # add days_until_deadline field to each conference
    for conference in conferences:
        if conference['deadline']:
            conference['days_until_deadline'] = (conference['deadline'] - datetime.datetime.now()).days
            if conference['days_until_deadline'] < 0:
                conference['days_until_deadline'] = 365 + conference['days_until_deadline']
        else:
            conference['days_until_deadline'] = None
    is_editor = False
    if 'acasearch_roles' in get_app_metadata():
        is_editor = 'editor' in get_app_metadata()['acasearch_roles']
    return render_template('index.html', conferences=conferences, is_editor=is_editor)

# @bp.route('/user')
# def user():
#     return render_template('user.html', user=get_app_metadata())

@bp.route('/add', methods=['GET', 'POST'])
def add_conference():
    form = ConferenceForm()
    if form.validate_on_submit():
        conference = {
            'acronym': form.acronym.data,
            'h5_index': form.h5_index.data,
            'core_rank': form.core_rank.data,
            'era_rank': form.era_rank.data,
            'qualis_rank': form.qualis_rank.data,
            'deadline': datetime.datetime.combine(form.deadline.data, datetime.datetime.min.time()) if form.deadline.data else None,
            'notification_date': datetime.datetime.combine(form.notification_date.data, datetime.datetime.min.time()) if form.notification_date.data else None,
            'start_date': datetime.datetime.combine(form.start_date.data, datetime.datetime.min.time()) if form.start_date.data else None,
            'end_date': datetime.datetime.combine(form.end_date.data, datetime.datetime.min.time()) if form.end_date.data else None,
            'location': form.location.data,
            'name': form.name.data,
            'description': form.description.data
        }
        mongo.db.conferences.insert_one(conference)
        return redirect(url_for('acasearch.index'))
    return render_template('add_conference.html', form=form)

@bp.route('/edit/<acronym>', methods=['GET', 'POST'])
@requires_role('editor')
def edit_conference(acronym):
    conference = mongo.db.conferences.find_one({'acronym': acronym})
    form = ConferenceForm(data=conference)
    if form.validate_on_submit():
        updated_conference = {
            'acronym': form.acronym.data,
            'h5_index': form.h5_index.data,
            'core_rank': form.core_rank.data,
            'era_rank': form.era_rank.data,
            'qualis_rank': form.qualis_rank.data,
            'deadline': datetime.datetime.combine(form.deadline.data, datetime.datetime.min.time()) if form.deadline.data else None,
            'notification_date': datetime.datetime.combine(form.notification_date.data, datetime.datetime.min.time()) if form.notification_date.data else None,
            'start_date': datetime.datetime.combine(form.start_date.data, datetime.datetime.min.time()) if form.start_date.data else None,
            'end_date': datetime.datetime.combine(form.end_date.data, datetime.datetime.min.time()) if form.end_date.data else None,
            'location': form.location.data,
            'name': form.name.data,
            'description': form.description.data
        }
        mongo.db.conferences.update_one({'acronym': acronym}, {'$set': updated_conference})
        return redirect(url_for('acasearch.index'))
    return render_template('edit_conference.html', form=form, conference=conference)

@bp.route('/get/<acronym>', methods=['GET'])
def get_conference(acronym):
    # get_conference.html
    conference = mongo.db.conferences.find_one({'acronym': acronym})
    return render_template('get_conference.html', conference=conference)


def search_venues(query: str) -> List[Dict]:
    """
    Search for venues in the MongoDB database using the $search aggregation pipeline.

    Args:
        query: The search query.

    Returns:
        A list of venues that match the search query.
    """
    pipeline = [
        {
            '$search': {
                'index': 'default',
                'text': {
                    'query': query,
                    'path': {
                        'wildcard': '*'
                    }
                }
            }
        }
    ]
    return list(mongo.db.conferences.aggregate(pipeline))



app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
