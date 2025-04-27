# Techmen Documentation System

A Django-based documentation system for managing maintenance records and machine documentation.

## Features

- Track and manage production line maintenance records
- Generate PDF reports for maintenance activities 
- Maintain machine documentation and specifications
- Track machine issues and resolutions
- Monitor component replacements and repairs
- Create and export service reports
- Manage work lists and item descriptions

## Requirements

- Python 3.9+
- Django 4.0+
- Additional dependencies in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/techmen-app.git
cd techmen-app
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash 
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

## Usage

1. Log in to the admin interface at `/admin`
2. Add production lines and their specifications
3. Create maintenance records for the lines
4. Generate PDF reports and Excel exports
5. Track issues and maintenance activities

## Project Structure

- `core/` - Main application code
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JS, images)
  - `techdocs/` - Views and business logic
- `app_settings/` - Application settings and configurations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
