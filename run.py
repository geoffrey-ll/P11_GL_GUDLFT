from decouple import config

from server import app


if __name__ == "__main__":
    app.run(debug=config("DEBUG", cast=bool))
