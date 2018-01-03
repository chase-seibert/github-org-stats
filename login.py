from functools import partial
import time
from github3 import authorize, login


_CREDENTIALS_FILE = '.credentials'


def login_from_credentials():
    with open(_CREDENTIALS_FILE, 'r') as fd:
        token = fd.readline().strip()
        id = fd.readline().strip()
    gh = login(token=token)
    return gh


if __name__ == '__main__':
    try:
        auth = authorize(
            raw_input('GitHub username: '),
            password=raw_input('GitHub password: '),
            scopes=['repo', 'read:org'],
            note='github-org-stats %s' % time.time(),
            two_factor_callback=partial(raw_input, 'GitHub 2FA code: '))
    except Exception as e:
        print e.response.text
        exit(1)
    print 'Success, writing authorization token for %s to %s' % (
        auth.id,
        _CREDENTIALS_FILE
        )
    with open(_CREDENTIALS_FILE, 'w') as fd:
        fd.write(auth.token + '\n')
        fd.write(str(auth.id))
