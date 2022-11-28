# inspired by https://www.cs.princeton.edu/~cmoretti/cos333/CAS/


import urllib
import re
from flask import request, session, redirect, abort

class CASClient:
    # Initialize a new CASClient object so it uses the given CAS
    # server, or fed.princeton.edu if no server is given.

    def __init__(self, url='https://fed.princeton.edu/cas/'):
        self.cas_url = url

    # URL of current request without ticket
    def ServiceURL(self):
        url = request.url
        if url:
            url = re.sub(r'ticket=[^&]*&?', '', url)
            url = re.sub(r'\?&?$|&$', '', url)
            return url
        else:
            return "something is wrong"

    # if cas server says this is accepted, return netid otherwise return null
    def Validate(self, ticket):
        val_url = self.cas_url + 'validate' + \
            '?service=' + urllib.parse.quote(self.ServiceURL()) + \
            '&ticket=' + urllib.parse.quote(ticket)
        with urllib.request.urlopen(val_url) as flo:
            r = flo.readlines()  # returns 2 lines
        if len(r) != 2:
            return None
        if r[0].decode('utf-8').startswith('yes'):
            return r[1].decode('utf-8')
        else:
            return None


    # Return username of authenticated user
    def Authenticate(self):

        # see if session already has a user (save some complexity)
        if 'username' in session:
            print(f'getting session username {session.get("username")}')
            return session.get('username')

        # If the request contains a login ticket, then try to
        # validate it.
        ticket = request.args.get('ticket')
        if ticket is None:
            # need a login ticket
            login_url = self.cas_url + 'login' \
            + '?service=' + urllib.parse.quote(request.url)
            # send user to the login page if they didn't have a ticket
            abort(redirect(login_url))
            
        username = self.Validate(ticket)
        if username is None:
            # need a login ticket
            login_url = self.cas_url + 'login' \
            + '?service=' + urllib.parse.quote(self.ServiceURL())
            # send user to the login page if they didn't have a ticket
            abort(redirect(login_url))
        
        username = username.strip()
        session['username'] = username
        return username

        


# -----------------------------------------------------------------------


def main():
    print('CASClient does not run standalone')


if __name__ == '__main__':
    main()
