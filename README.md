# Todo_app
Here is my Todo Web application using popular technologies and frameworks:- flask, bootstrap, jinja2, SQLAlchamey, CSS3, HTML5

## Folder Structure
```
--Todo_app
    |
    |--instance
    |    |--Todo.db
    |
    |--static
    |    |--css
    |    |   |--style.css
    |    |   |--login.css
    |    |
    |    |--script
    |    |   |--login.js
    |    |    |--script.js
    |    |
    |    |--icons
    |         |--male.png
    |         |--female.png
    |
    |
    |--templates
    |    |--base.html
    |    |--home.html
    |    |--update.html
    |    |--about.html
    |    |--login.html
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

1. install Virtualenv for python
```sh
pip install virtualenv
```

2. Create a virtual env
```sh
virtualenv <name>
```

3. Activate the virtual env
```sh
.\env\Scripts\Activate
```

4. install all the dependencies used in app
```sh
pip install -r requirements.txt
```

5. Now Run this app
```sh
python app.py
```
