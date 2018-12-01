import os
import sys
import SGCM

from flask import g
from SGCM import app
from SGCM.models.dao import init_db

if len(sys.argv) > 1 and sys.argv[1] == 'initdb':
    init_db()
elif __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run('0.0.0.0', port=port)