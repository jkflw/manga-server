from django.core.management.base import BaseCommand, CommandError
from manga.models import Directory
from manga.settings import MANGA_DIR
import os
import json

class Command(BaseCommand):
    help = 'Updates database with updated json file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='File to import')

    def handle(self, *args, **kwargs):
        file = open(kwargs['file'], 'r')
        fileData = file.read()
        jsonData = json.loads(fileData)
        print(f"Total number of items to process: {len(jsonData)}")
        count = 0
        for key, value in jsonData.items():
            count = count + 1
            if count % 100 == 0:
                print(f"{100*count/len(jsonData)}%")
            try:
                dir = Directory.objects.get(full_path = key)
                dir.title = value['title']
                dir.year = value['year']
                dir.authors = value['authors']
                dir.tags = value['tags']
                dir.genres = value['genres']
                dir.manga_updates_link = value['mangaUpdatesLink']
                dir.completely_scanlated = True if value['scanStatus'] == "Yes" else False
                dir.manga_image = value['manga_image']
                dir.save()
            except Exception as e:
                #print(f"{e}: {key}")
                pass
        file.close()
        print("100%")
