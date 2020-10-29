# reservation-system
The application for making conference room reservations. It allows users to add, edit and delete rooms. It allows booking a selected conference room for the whole day. The reserved conference room does not appear in the search results. On the main page of the application users see two lists with information about available or reserved conference rooms on a given day.

## Technologies
* Python 3.8.5
* Django >= 2.2.5
* psycopg2-binary 2.8.6

## LocalSetup
1) Install All Dependencies  
`pip3 install -r requirements.txt`
2) Database cofiguration  
To make you work easier, find **local_setings.py.example** file, complete it 
with your PostgreSQL data and rename file to **local_setings.py**.  
**Remember!** Do not keep sensitive data under Git's control! (**local_settings.py** file is added to **.gitignore**).   
3) Run the File  
`python manage.py runserver`