# Project E3 Studio 

This project was initiated in 2019 when I was learning about software development for web applications.
It was later terminated in 2022 and replaced by [Havkon Studio](www.havkonstudio.com) to showcase my profile. 
It was meant for practicing and enhancing my knowledge in building full stack web applications.
It has been out of maintenance, but I can use it as a reference for the work I did in the past.

This project mainly consists of the Django and React components.

## Django Component

The following folders and files are for the Django component
```
|-- apps
|-- apps_arithmetic
|-- apps_math
|-- apps_physics
|-- courses
|-- e3studio
    |-- __init__.py
    |-- asgi.py
    |-- settings.py
    |-- urls.py
    |-- wsgi.py
|-- probability
|-- quantum_mechancs
|-- registration
|-- static
|-- templates
|-- userprofile
|-- manage.py
|-- requirements.txt
```

Folders `apps`, `apps_arithmetic`, `apps_math`, `apps_physics`, `courses`, `probability`,
`quantum_mechanics`, `registration`, `templates` and `userprofile` are appplication folders
created by the command `python manage.py startapp $app_name`, where `$app_name` is the
application name. These folders follow the following pattern for organizing files and folders.
```
|-- api
|-- migrations
|-- __init__.py
|-- admin.py
|-- apps.py
|-- models.py
|-- tests.py
|-- utilities.py
|-- urls.py
|-- views.py
```

These application folders have their own functionalities in their corresponding `views.py` file under the `api`
directory. For instance, the view class `SubtractionInputView` checks the key `answer` with the key `check` 
from the request payload data depending on the grade. 

The steps to run the Django server is as follows:
1. Create a Python virtual environment folder with `python -m venv venv`
2. Activate the virtual environment with `venv/scripts/activate` (`venv/bin/activate` for MacOS).
3. Go to the `e3studio` folder and do `pip install -r requirements.txt` to install dependency packages.
4. Run database migration command first with `python manage.py migrate`
5. Run the server with the `python manage.py runserver 8000`.
6. Open your web browser and navigate to `http://localhost:8000` to verify the server is running.

In case there is an error on the web browser, it is possible that it is missing files to render the frontend
from the `staticfiles` folder. To create the `staticfiles` folder, you will need to build the build folder
from the React component first, then run `python manage.py collectstatic --noinput` to put collect all 
frontend files for rendering.


## React Component

The following folders and files are for the React component
```
|-- src
    |-- apps_arithmetic
    |-- apps_math
    |-- apps_physics
    |-- e3studio
    |-- machinelearning
    |-- physics11
    |-- registration
    |-- store
    |-- url
    |-- App.js
    |-- index.js
    |-- reportWebVitals.js
    |-- routes.js
    |-- servieWorker.js
    |-- setupTests.js
|-- package-lock.json
|-- package.json
```

The steps to run the React component is as follows:
1. Install dependency packages in the `node_modules` folder with `npm install`
2. Build the frontend files in the `build` folder with `npm run build`. This
step is neccessary for the Django server to collect static files.
3. Run the React server with `npm run start`

