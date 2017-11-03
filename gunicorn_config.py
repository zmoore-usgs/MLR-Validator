import os

import gunicorn

bind_ip = os.getenv('bind_ip', '0.0.0.0')
bind_port = os.getenv('bind_port', '7010')
bind = '{0}:{1}'.format(bind_ip, bind_port)
capture_output = True

# ssl_key_path and ssl_cert_path environment variables are defined when secrets are created
ssl_keyfile = os.getenv('ssl_key_path')
ssl_certfile = os.getenv('ssl_cert_path')
if ssl_keyfile is not None and os.path.isfile(ssl_keyfile):
    keyfile = ssl_keyfile
if ssl_certfile is not None and os.path.isfile(ssl_certfile):
    certfile = ssl_certfile

gunicorn.SERVER_SOFTWARE = ''
