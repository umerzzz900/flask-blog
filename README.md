Flask Blog & Admin Panel
A simple blog application built with Flask, MySQL, and Bootstrap templates.
It includes:

- Public blog post listing
- Single post view
- Admin login & dashboard
- Create, edit, and delete posts
- File uploads with validation
- Contact form submissions

Features
- Homepage with pagination – Displays blog posts with configurable number per page.
- Admin authentication – Login with bcrypt password hashing.
- Post management – Add, edit, and delete posts from the dashboard.
- File uploads – Upload images or other files with size/type restrictions.
- Contact form – Stores submitted messages in the database.
- Error handling – Custom 404 page.
- Configurable settings – Stored in config.json.

Requirements
- Python 3.x
- MySQL server
- Required Python packages (see below)

Installation
1️⃣ Clone this repository
git clone https://github.com/yourusername/flask-blog.git
cd flask-blog

2️⃣ Install dependencies
pip install flask flask-mysqldb bcrypt

3️⃣ Create MySQL database
CREATE DATABASE flaskapp;

USE flaskapp;

CREATE TABLE posts (
    sno INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    slug VARCHAR(255) UNIQUE,
    content TEXT,
    img_file VARCHAR(255),
    author VARCHAR(255),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sub VARCHAR(255)
);

CREATE TABLE contacts (
    sno INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    phone_num VARCHAR(50),
    msg TEXT,
    email VARCHAR(255),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE admin_access (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255)
);

4️⃣ Configure settings in config.json
Example:
{
    "urls": {
        "no_posts": 5,
        "upload_location": "static/uploads",
        "allowed_extensions": ["jpg", "png", "gif"],
        "max_file_size_mb": 5
    }
}

5️⃣ Create an admin account
Uncomment the /create-admin route in the code, run the app once, and visit:
http://127.0.0.1:5000/create-admin
Then comment it back to avoid leaving it publicly accessible.

Running the App
python app.py
The app will run at:
http://127.0.0.1:5000

File Upload Rules
- Allowed extensions: Configurable in config.json
- Max size: Configurable in config.json
- Files stored in: UPLOAD_FOLDER path from config

Routes Overview
Route          Method     Description
/              GET        Homepage with paginated posts
/about         GET        About page
/login         GET/POST   Admin login
/dashboard     GET        Admin dashboard (requires login)
/logout        GET        Logout admin
/edit/<int:sno> GET/POST  Add/edit post
/delete/<int:sno> GET/POST Delete post
/contact       GET        Contact form page
/submit        POST       Submit contact form
/posts         GET        All posts list
/post/<slug>   GET        Single post view
/uploader      POST       File upload (requires login)
/error         GET        Error page
404 handler    GET        Custom not found page

Security Notes
- Always remove or comment out /create-admin after creating your admin account.
- Store app.secret_key in an environment variable for production.
- Restrict file uploads to safe types and scan files before serving.

License
This project is open-source under the MIT License.
