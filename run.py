#!flask/bin/python
from app.gct import app
from app import settings

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
