"""
    Created by Amirk on 2018-07-26.
"""
from app.app import created_app

app = created_app()

if __name__ == '__main__':
    app.run(debug=True)
