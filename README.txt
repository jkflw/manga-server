Install python and pip and run
  pip install -r requirements.txt

Update MANGA_DIR at the bottom of settings.py to the directory you store manga in.

Run
  python3 manage.py update_database
to scan the MANGA_DIR for directories to search for.

Run
  python3 manage.py runserver 0:8000
to start the server at http://localhost:8000.

After the server is started, navigate to http://<server_address>:8000/manga
