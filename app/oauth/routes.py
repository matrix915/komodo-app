import json
from flask import current_app
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from app.oauth import bp # import blueprint
from app import auth0
from app.decorators import requires_auth
from six.moves.urllib.parse import urlencode

@bp.route('/callback')
def callback_handling():
	 # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')




# /server.py

@bp.route('/login')
def login():
    # return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')
    return auth0.authorize_redirect(redirect_uri=current_app.config['AUTH0_CALLBACK_URL'])


@bp.route('/home')
def home():
    return render_template('oauth/home.html')


@bp.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('oauth/dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))


@bp.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('oauth.home', _external=True), 'client_id': current_app.config['AUTH0_CLIENT_ID']}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))