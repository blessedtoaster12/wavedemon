from datetime import date
import json
from pathlib import Path

#Streamrip has a dependency conflict with pylint (toml version mismatch) so a venv is used
#Consider taking a look at getting the requirements for the toml version in streamrip updated
import tidalapi # pylint: disable=import-error
import streamrip # pylint: disable=import-error

def _write_login_to_file(session, login_file):
    '''
    Lil helper function to write session to file because I hate copy/pasting blocks of code

    Keyword arguments:
    session - tidalapi session object
    login_file - File object representing data\\login.json
    '''
    session.login_oauth_simple()
    login_file.writelines(json.dumps({
        "token_type": session.token_type,
        "access_token": session.access_token,
        "refresh_token": session.refresh_token
    }))

def tidalapi_login():
    '''
    Login with python-tidal
    Streamrip does supply a suitable login function, but python-tidal is pretty
    much equivalent to the online experience in terms of features so we'll keep
    it around to add expanded functionality later
    '''

    _s = tidalapi.Session()
    login_file = None
    #Only reason this exists is to load the login file for use in the ValueError exception below
    #It pains me
    try:
        login_file = open(file=Path("data\\login.json"), encoding='UTF-8')
    except OSError():
        quit() #Change later to better error message about how the file is borked

    try:
        with login_file as file:
            _d = json.load(file)
        if not _s.load_oauth_session(**_d):
            _write_login_to_file(_s, login_file)
    except ValueError():
        _write_login_to_file(_s, login_file)

    login_file.close()
    return _s

def tidaldl_login(session):
    '''
    Login with streamrip for download

    Keyword arguments:
    session - tidalapi session object to pull user data from
    '''
    tidal_client = streamrip.clients.TidalClient()
    return tidal_client.login(
        session.user.id,
        session.country_code,
        session.access_token,
        (session.expiry_time.date() - date.today()).total_seconds(),
        session.refresh_token)
