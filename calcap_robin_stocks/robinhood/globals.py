"""Holds the session header and other global variables."""
import sys
import os
from contextvars import ContextVar

from requests import Session

# Keeps track on if the user is logged in or not.
LOGGED_IN = False
# The session object for making get and post requests.
SESSION = Session()
SESSION.headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate,br",
    "Accept-Language": "en-US,en;q=1",
    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    "X-Robinhood-API-Version": "1.431.4",
    "Connection": "keep-alive",
    "User-Agent": "*"
}

# Calcap: the session of the client whose account is being read right now, set
# by clients.client_session(). Each thread and asyncio task has its own value,
# so several clients can be read at once. None means the shared SESSION above.
CLIENT_SESSION = ContextVar("calcap_client_session", default=None)

#All print() statement direct their output to this stream
#by default, we use stdout which is the existing behavior
#but a client can change to any normal Python stream that
#print() accepts.  Common options are
#sys.stderr for standard error
#open(os.devnull,"w") for dev null
#io.StringIO() to go to a string for the client to inspect
OUTPUT=sys.stdout
