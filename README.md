# Todo_app
Here is my Todo Web application using popular technologies and frameworks:- flask, bootstrap, jinja2, SQLAlchamey, CSS3, HTML5

## Folder Structure
```
--Todo_app
    |
    |--__pycache__
    |
    |--instance
    |    |--Todo.db
    |
    |--static
    |    |--css
    |    |   |--style.css
    |    |
    |    |--script
    |
    |--templates
    |    |--base.html
    |    |--index.html
    |    |--update.html
    |    |--about.html
    |
    |--app.py
    |
    |--.gitignore
    |
    |--LICENSE
    |
    |--README.md
    |
    |--requirments.txt

```
you can run this web-app in either local env or virtual env.

To run this app on local env
```sh
python app.py
```

To run this app in virtual env

1. Create a virtual env
```sh
python -m venv <env_name>
```

2. Activate the virtual env
```sh
.\env\Scripts\Activate
```

3. Make sure you have downloaded packages and frameworks used in this app
```sh
pip install Flask gunicorn SQLAlchemy
```

4. Now Run this app
```sh
python app.py
```