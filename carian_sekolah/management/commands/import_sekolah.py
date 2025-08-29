# dalam carian_sekolah/management/commands/import_sekolah.py

import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from carian_sekolah.models import School

class Command(BaseCommand):
    help = 'Import data sekolah dari fail CSV dengan data PPD dan Kod Sekolah'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Laluan ke fail CSV')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        self.stdout.write(f"Memulakan import dari {csv_file_path}...")

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                sekolah_untuk_dikemas_kini = []
                sekolah_untuk_dicipta = []
                
                for row in reader:
                    try:
                        kod_sekolah = row['kod_sekolah'].strip()
                        lokasi = Point(float(row['longitude']), float(row['latitude']), srid=4236)
                        
                        # Data untuk dicipta atau dikemas kini
                        data_sekolah = {
                            'name': row['name'].strip(),
                            'address': row['address'].strip(),
                            'ppd': row['ppd'].strip(),
                            'school_type': row['school_type'].strip().upper(),
                            'location': lokasi,
                        }

                        # Semak jika sekolah sudah wujud berdasarkan kod sekolah
                        sekolah, dicipta = School.objects.update_or_create(
                            kod_sekolah=kod_sekolah,
                            defaults=data_sekolah
                        )

                        if dicipta:
                            self.stdout.write(f"Mencipta: {sekolah.name}")
                        else:
                            self.stdout.write(f"Mengemas kini: {sekolah.name}")

                    except (ValueError, KeyError) as e:
                        self.stdout.write(self.style.ERROR(f"Baris dilangkau kerana ralat data: {row} - {e}"))
                        continue
                
                self.stdout.write(self.style.SUCCESS("Proses import selesai."))

        except FileNotFoundError:
            raise CommandError(f'Fail "{csv_file_path}" tidak ditemui.')