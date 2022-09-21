from flask import session

# Return true if we've set both user_id and first_name on the session
def logged_in():
    return session.get('user_id') and session.get('first_name') and session.get('last_name')