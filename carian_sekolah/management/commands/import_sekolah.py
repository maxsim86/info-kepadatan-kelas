import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from carian_sekolah.models import School

class Command(BaseCommand):
    help = 'Import data sekolah dari fail CSV dan hasilkan laporan ralat yang terperinci.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Laluan ke fail CSV')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        self.stdout.write(f"Memulakan import dari {csv_file_path}...")

        error_rows = []
        success_count = 0
        error_file_path = 'import_errors.csv'

        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Dapatkan nama lajur asal dari pembaca CSV
                original_fieldnames = reader.fieldnames or []
                error_fieldnames = original_fieldnames + ['sebab_ralat']

                for row_num, row in enumerate(reader, 2): # Mula dari baris 2
                    try:
                        # === SEMAKAN BARU: Kesan lajur berlebihan ===
                        if None in row:
                            raise ValueError(f"Baris mempunyai lebih banyak lajur daripada pengepala. Data tambahan: {row[None]}")

                        kod_sekolah = row.get('kod_sekolah', '').strip()
                        latitude = row.get('latitude', '').strip()
                        longitude = row.get('longitude', '').strip()

                        if not kod_sekolah or not latitude or not longitude:
                            raise ValueError("Data penting (kod_sekolah, latitude, atau longitude) kosong.")

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
                        error_row_data = row.copy()
                        # Pastikan kunci 'None' tidak dimasukkan ke dalam laporan
                        if None in error_row_data:
                            del error_row_data[None]
                        error_row_data['sebab_ralat'] = f"Baris {row_num}: {e}"
                        error_rows.append(error_row_data)
                        continue
            
            self.stdout.write(self.style.SUCCESS(f"Proses selesai. {success_count} sekolah berjaya diimport/dikemas kini."))

            if error_rows:
                self.stdout.write(self.style.WARNING(f"{len(error_rows)} baris gagal diimport. Laporan ralat disimpan di {error_file_path}"))
                
                with open(error_file_path, mode='w', encoding='utf-8', newline='') as error_file:
                    # Guna 'extrasaction' untuk mengabaikan lajur yang tidak dijangka
                    writer = csv.DictWriter(error_file, fieldnames=error_fieldnames, extrasaction='ignore')
                    writer.writeheader()
                    writer.writerows(error_rows)

        except FileNotFoundError:
            raise CommandError(f'Fail "{csv_file_path}" tidak ditemui.')