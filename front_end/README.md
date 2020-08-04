LOG IN
### Step 1: Creating the Database Table
Execute the following SQL query to create the users table inside your MySQL database.

CREATE TABLE users (
    <br>&emsp;&emsp;id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    <br>&emsp;&emsp;username VARCHAR(50) NOT NULL UNIQUE,
    <br>&emsp;&emsp;password VARCHAR(255) NOT NULL,
    <br>&emsp;&emsp;created_at DATETIME DEFAULT CURRENT_TIMESTAMP
<br>);

### Step 2: Creating the Config File
Database configuration in config.php

define('DB_SERVER', '127.0.0.1');
<br>define('DB_USERNAME', 'root');
<br>define('DB_PASSWORD', '');
<br>define('DB_NAME', '');

### Step 3: how to run php script
<br>cd your_directory
<br>php -S localhost:8000
<br>http://localhost:8000/login.php
