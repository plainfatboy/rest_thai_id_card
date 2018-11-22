# REST server for fetching information from Thai national ID card
สร้าง REST server เพื่ออ่านค่าจากบัตรประชาชนไทย โดยใช้ Python 3.x
This project is reimplemented to read information from Thai national ID card by using Python 3.x.

ผมทดลองCodeของผมบน Windows 10 และใช้ Python 3.7
This project has been tested on Windows 10. In addition, it has been implemented with Python 3.7.

Smartcard reader: https://online.advice.co.th/product/barcode-product/scanner/barcode-scanner-smart-card-reader-scr-n3300-

หาก Advice เห็นว่า Code ส่งเสริมการขายของคุณ ส่งของเล่นสนุกๆมาให้ผมบ้างก็ดีนะครับ :D

Refs:
 - Flask: http://flask.pocoo.org/docs/1.0/quickstart/#quickstart
 - ADPU commands: https://github.com/chakphanu/ThaiNationalIDCard/blob/master/APDU.md
 - Python example: https://freeshell.de/~jirawat/blog/?p=69

Dependencies:
 - flask
 - flask_cors
 - pyscard

Quick guide:
1. main.py ใช้เพื่อดึงข้อมูลและรูปภาพและเขียนลงบน photo.jpeg และ temp.txt
run main.py for fetching photo and information from Thai national ID card.

2. run.bat ใช้เพื่อนการสร้าง REST server
run run.bat in CMD for serving REST server
  - /get_status คืนค่าสถานะของเครื่องอ่าน (return the status of smartcard reader)
  - /get_data คืนข้อมูลทุกอย่างบน smartcard (return all text information)
  - /get_photo_byte คืนค่ารูปภาพเป็น bytes (return jpeg photo as bytes)
  - /get_photo_json คืนค่ารูปภาพเป็น array of ints (return jpeg photo as array of integers)


ผมเป็นมือใหม่หากมีข้อสงสัยหรืออยากแนะนำวิธีการเขียนCodeให้ปลอดภัยขึ้นหรือประสิทธิภาพดีขึ้นหรืออยากชวนทำไปทำอะไรสนุกๆติดต่อมาที่ wasuwatp18@gmail.com ครับ
Contact me via email (wasuwatp18@gmail.com)

I hope my code contribute to something new.

Cheers,

PlainFatBoy

Asura Dev Team
