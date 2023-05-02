import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Title, Category, Genre, GenreTitle


class Command(BaseCommand):
    help = 'Loads data from csv-files. Use: python manage import_csv'

    MODELS_FILES = {
        Category: 'category.csv',
        Genre: 'genre.csv',
        Title: 'titles.csv',
        GenreTitle: 'genre_title.csv',
    }

    def start_import(self):
        directory = f'{settings.DATA_PATH}\n'
        file_names = "\n".join(list(self.MODELS_FILES.values()))
        info = ('Data will be added from the following directory:\n'
                + directory
                + 'List of files:\n'
                + file_names)

        self.stdout.write(
            self.style.MIGRATE_HEADING('Start importing data from csv-files')
        )
        self.stdout.write(
            self.style.HTTP_INFO(info)
        )

    def database_cleanup(self):
        Category.objects.all().delete()
        Genre.objects.all().delete()
        Title.objects.all().delete()
        GenreTitle.objects.all().delete()
        self.stdout.write(
            self.style.HTTP_INFO(
                'Performing a preliminary database cleanup...'
            )
        )

    def load_data(self):
        self.stdout.write(
            self.style.HTTP_INFO(
                'Loading data to the database...'
            )
        )
        try:
            for model, file_name in self.MODELS_FILES.items():
                file_path = os.path.join(
                    settings.DATA_PATH,
                    f'{file_name}'
                )
                with open(file_path, 'r', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file)
                    next(reader)
                    data = [model(*row) for instance_id, row in
                            enumerate(reader)]
                    model.objects.bulk_create(data)
            self.stdout.write(
                self.style.SUCCESS(
                    'Success! Data from csv-files uploaded to the database.'
                )
            )
        except Exception as error:
            self.stdout.write(
                self.style.ERROR(
                    f'Error while uploading: {error}'
                )
            )

    def handle(self, *args, **options):
        self.start_import()
        self.database_cleanup()
        self.load_data()
