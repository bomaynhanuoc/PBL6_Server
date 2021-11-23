# AI Contest

<h1>Hướng dẫn cài đặt</h1>

<h2>Git clone</h2>
<h3>Tại thư mục dự án:</h3>
<ul>
<li>git clone https://github.com/bomaynhanuoc/PBL6_Server</li>
</ul>

<h2>Cài đặt venv</h2>
<h3>Tại thư mục dự án:</h3>
<ul>
<li>sudo apt install python3-venv</li>
<li>python -m venv venv</li>
</ul>

<h2>Cài đặt mongod</h2>
<h3>Tạo terminal:</h3>
<ul>
<li>sudo apt-get install gnupg</li>
<li>wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -</li>
<li>echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list</li>
<li>sudo apt-get update</li>
<li>sudo apt-get install -y mongodb-org</li>
<li>sudo systemctl start mongod</li>
<li>mongo</li>
<li>use aicontest</li>
<li>exit</li>
</ul>

<h2>Khởi tạo django</h2>
<h3>Tại thư muc dự án:</h3>
<h4>Chạy venv</h4>
<ul><li>source venv/bin/activate</li></ul>
<h4>Cài đặt thư viện</h4>
<ul><li>pip install -r requirements.txt</ul></li>
<h4>Migrate db</h4>
<ul><li>python manage.py migrate</ul></li>
<h4>Chạy server</h4>
<ul><li>python manage.py runserver</ul></li>
</ul>

<h2>Public server</h2>
<h3>Tạo tài khoản pagekite</h3>
<ul>
<li>Nhập email</li>
<li>Nhập tên miền đăng ký</li>
<li>Vào mail đã đăng ký để lấy password</li>
</ul>
<h3>Tạo terminal ở thư mục dự án</h3>
<ul>
<li>source venv/bin/activate</li>
<li>python pagekite.py 8000 ten-mien-be AND 3000 ten-mien-fe</li>
</ul>

<h1>Hướng dẫn cải tiến</h1>
<a href="https://github.com/bomaynhanuoc/PBL6_Server" target="_blank">Xem thêm</a>
