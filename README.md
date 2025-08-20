# XRS Django App Setup Guide

Repository: [https://github.com/stirlingv/xrs.git](https://github.com/stirlingv/xrs.git)

This guide will help you set up and run the XRS Django app locally, even if you have never used Django or Python virtual environments before.

## Prerequisites

- Python 3.13.1 (recommended) installed on your system
- Git installed on your system

## Contributing

Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Step 1: Clone the Repository

Open your terminal and run:

```sh
git clone https://github.com/stirlingv/xrs.git
cd xrs
```

## Step 2: Create a Virtual Environment

A virtual environment keeps your project dependencies isolated.

```sh
python3 -m venv venv
```

## Step 3: Activate the Virtual Environment

- On macOS/Linux:

  ```sh
  source venv/bin/activate
  ```

- On Windows:

  ```sh
  venv\Scripts\activate
  ```

## Step 4: Upgrade pip (Recommended)

```sh
pip install --upgrade pip
```

## Step 5: Install Project Dependencies

Install all required Python packages using the provided `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Step 6: Run Database Migrations

```sh
python manage.py migrate
```

## Step 7: Run the Development Server

```sh
python manage.py runserver
```

## Step 8: View the App

Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
You should see the XRS homepage with the integrated HTML5 template.

## Troubleshooting

- If you see errors about missing static files, make sure you have activated your virtual environment and installed dependencies.
- If you see a TemplateSyntaxError about `{% static %}`, ensure your templates have `{% load static %}` at the top.

## Next Steps

- To stop the server, press `Ctrl+C` in your terminal.
- To deactivate the virtual environment, type:

  ```sh
  deactivate
  ```

For further help, contact the project maintainer or check the official Django documentation: <https://docs.djangoproject.com/en/5.2/>
