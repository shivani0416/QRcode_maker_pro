# QR Code Generator Web App

A Flask-based application that allows registered users to generate QR codes from URLs and manage them through a personal dashboard.

## Features

* User signup and login (session-based authentication)
* Generate QR codes from any valid URL
* Dashboard displaying all previously generated QR codes
* QR images stored in a static folder and linked in an SQLite database

## Technologies Used

* **Python / Flask** – Backend framework
* **SQLite** – Lightweight relational database
* **qrcode** – Python library for creating QR images
* **HTML (Jinja templates)** – Frontend interface

## Folder Structure

```
QRcode_maker_pro/
│
├── static/
│   └── qrcodes/         # generated QR images
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   └── generate.html
│
├── app.py               # main Flask application
├── database.db          # SQLite database
└── requirements.txt
```

## How to Run

1. Create a virtual environment and activate it.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:

   ```bash
   python app.py
   ```
4. Open a browser and go to `http://127.0.0.1:5000`.

## Future Improvements

* Make QR codes clickable in the dashboard
* Add delete/download options for each QR
* Add custom styling and themes for the QR output
