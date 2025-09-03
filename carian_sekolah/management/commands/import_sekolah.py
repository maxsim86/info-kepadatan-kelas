# carian_sekolah/management/commands/import_sekolah.py

import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from carian_sekolah.models import School

class Command(BaseCommand):
    help = 'Import data sekolah dari fail CSV dan hasilkan laporan ralat.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Laluan ke fail CSV')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        self.stdout.write(f"Memulakan import dari {csv_file_path}...")

        error_rows = []
        success_count = 0

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        # Semak jika lajur penting wujud dan tidak kosong
                        kod_sekolah = row.get('kod_sekolah', '').strip()
                        latitude = row.get('latitude', '').strip()
                        longitude = row.get('longitude', '').strip()

                        if not kod_sekolah or not latitude or not longitude:
                            raise ValueError("Kod sekolah, latitude, atau longitude kosong.")

                        lokasi = Point(float(longitude), float(latitude), srid=4326)
                        
                        data_sekolah = {
                            'name': row.get('name', '').strip(),
                            'address': row.get('address', '').strip(),
                            'ppd': row.get('ppd', '').strip(),
                            'school_type': row.get('school_type', 'RENDAH').strip().upper(),
                            #'postcode': row.get('postcode', '').strip(),
                            'location': lokasi,
                        }

                        _, dicipta = School.objects.update_or_create(
                            kod_sekolah=kod_sekolah,
                            defaults=data_sekolah
                        )
                        success_count += 1

                    except (ValueError, KeyError) as e:
                        # Jika berlaku ralat, simpan baris dan sebabnya
                        row['sebab_ralat'] = str(e)
                        error_rows.append(row)
                        continue
            
            self.stdout.write(self.style.SUCCESS(f"Proses selesai. {success_count} sekolah berjaya diimport/dikemas kini."))

            # Jika terdapat ralat, hasilkan fail laporan
            if error_rows:
                error_file_path = 'import_errors.csv'
                self.stdout.write(self.style.WARNING(f"{len(error_rows)} baris gagal diimport. Laporan ralat disimpan di {error_file_path}"))
                
                with open(error_file_path, mode='w', encoding='utf-8', newline='') as error_file:
                    # Ambil pengepala dari baris pertama yang ralat
                    fieldnames = error_rows[0].keys()
                    writer = csv.DictWriter(error_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(error_rows)

        except FileNotFoundError:
            raise CommandError(f'Fail "{csv_file_path}" tidak ditemui.')
