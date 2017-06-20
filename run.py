#!flask/bin/python
from app.gct import app
from app import settings

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4000)
