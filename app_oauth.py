from functools import wraps
import os
from urllib.parse import urlencode
from app_base import bp, mongo

from auth0.authentication import Users, GetToken
from flask import session, url_for, flash, g
from flask_oauthlib.client import OAuth
from flask import Blueprint, render_template, redirect, request


auth0_bp = Blueprint('auth0', __name__)

AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')

oauth = OAuth(bp)
auth0 = oauth.remote_app(
    'auth0',
    consumer_key=AUTH0_CLIENT_ID,
    consumer_secret=AUTH0_CLIENT_SECRET,
    request_token_params={
        'scope': 'openid profile',
        'audience': f'https://{AUTH0_DOMAIN}/userinfo'
    },
    base_url=f'https://{AUTH0_DOMAIN}/',
    access_token_method='POST',
    access_token_url='/oauth/token',
    authorize_url='/authorize',
)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect('/auth0/login')
        return f(*args, **kwargs)
    return decorated

def requires_editor(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_user_metadata()
        if not user.get('is_editor', False):
            return redirect(url_for('acasearch.index'))
        return f(*args, **kwargs)
    return decorated

def requires_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_user_metadata()
        if not user.get('is_admin', False):
            return redirect(url_for('acasearch.index'))
        return f(*args, **kwargs)
    return decorated

# set global current_user variable
@bp.before_request
def before_request():
    g.current_user = session.get('profile', None)

@auth0_bp.route('/login')
def login():
    callback_url = url_for('acasearch.auth0.callback_handling', _external=True)
    callback_url = callback_url.replace('127.0.0.1', 'localhost') # hack for auth0
    return auth0.authorize(callback=callback_url)

@auth0_bp.route('/callback')
def callback_handling():
    resp = auth0.authorized_response()
    if resp is None or resp.get('access_token') is None:
        error_reason = request.args.get('error_reason', 'No error reason provided')
        error_description = request.args.get('error_description', 'No error description provided')
        return f'Access denied: reason={error_reason} error={error_description}'
    
    # Log the response for debugging
    print("Auth0 response:", resp)

    # Store user info and tokens
    session['access_token'] = resp['access_token']
    user_info = Users(AUTH0_DOMAIN).userinfo(session['access_token'])
    session['profile'] = user_info
    
    # Check if user exists in MongoDB, if not create a new entry
    if not mongo.db.users.find_one({"sub": user_info['sub']}):
        mongo.db.users.insert_one(
            {
                "sub": user_info['sub'], 
                "metadata": {
                    "is_admin": False,
                    "is_editor": False
                }
            }
        )
    
    return redirect(url_for('acasearch.index'))

@auth0_bp.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('acasearch.index', _external=True), 'client_id': AUTH0_CLIENT_ID}
    logout_url = auth0.base_url + 'v2/logout?' + urlencode(params)
    print(f'logout_url: {logout_url}')
    return redirect(logout_url)

@bp.route('/user', methods=['GET', 'POST'])
@requires_auth
def user():
    error_message, success_message = None, None
    return render_template(
        'user.html', user=get_user_metadata(), 
        error_message=error_message, success_message=success_message
    )
    
def get_management_api_token():
    get_token = GetToken(AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET)
    token = get_token.client_credentials(audience=f'https://{AUTH0_DOMAIN}/api/v2/')
    return token['access_token']

def update_user_metadata(is_admin, is_editor):
    metadata = {
        'is_admin': is_admin,
        'is_editor': is_editor
    }
    sub = session['profile']['sub']
    mongo.db.users.update_one({"sub": sub}, {"$set": {"metadata": metadata}})
    session['profile']['metadata'] = metadata

def get_user_metadata():
    if 'profile' not in session:
        return {}
    data = session['profile']
    user = mongo.db.users.find_one({"sub": session['profile']['sub']},
                                   {"metadata": 1})
    if user:
        data.update(user['metadata'])
    return data

@auth0_bp.route('/delete_account', methods=['POST'])
def delete_account():
    sub = session['profile']['sub']
    mongo.db.users.delete_one({"sub": sub})
    session.clear()
    flash('Account deleted successfully!', 'success')
    return redirect('/')


bp.register_blueprint(auth0_bp, url_prefix='/auth0')
