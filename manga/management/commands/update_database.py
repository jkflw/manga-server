from django.core.management.base import BaseCommand, CommandError
from manga.models import Directory
from manga.settings import MANGA_DIR
import os

class Command(BaseCommand):
    help = 'Scans the directories for search capability'

    def handle(self, *args, **options):
        insert_num = 0
        for root, dirs, files in os.walk(MANGA_DIR):
            if len(files) > 0:
                try:
                    Directory.objects.create(
                        directory=os.path.basename(root),
                        full_path=root,
                        authors=[],
                        genres=[],
                        related_series=[],
                        tags=[]
                    )
                    print(os.path.basename(root))
                    insert_num = insert_num + 1
                except Exception as e:
                    pass
        print("inserted %s dirs" % insert_num)
