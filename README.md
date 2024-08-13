<h2>Tips<h2>
<h4>You should create a database contains two tables before any other operations<h4>
<h4>the two tables are ↓↓↓<h4>
<h4>create table table_name
(
    id int null,
    filename varchar(255) null
);<h4>

<h4>create table photos
(
    id int null,
    filename varchar(255) null
);<h4>
<h4>create table users
(
    id int autoincrement,
    username varchar(150) null,
    email varchar(150) null,
    password_hash varchar(255) null
);<h4>

<h4>just run app.py you can see the Flask applicatiom.<h4>