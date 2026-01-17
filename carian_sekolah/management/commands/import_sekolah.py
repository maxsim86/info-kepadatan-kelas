import csv
import re
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from carian_sekolah.models import School

class Command(BaseCommand):
    help = "Import data sekolah dari fail CSV (Versi Pembaikan Ralat)"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Laluan ke fail CSV")

    def handle(self, *args, **options):
        csv_file_path = options["csv_file"]
        self.stdout.write(f"Memulakan import dari {csv_file_path}...")

        success_count = 0
        error_count = 0

        try:
            # Gunakan utf-8-sig untuk membuang BOM
            with open(csv_file_path, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                
                # Bersihkan header: lower case, strip space
                reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]
                self.stdout.write(f"Header dikesan: {reader.fieldnames}")

                for row_num, row in enumerate(reader, 2):
                    kod_sekolah = row.get("kod_sekolah", "").strip()
                    
                    try:
                        # --- 1. VALIDASI LATITUD & LONGITUD ---
                        raw_lat = row.get("latitude", "").strip()
                        raw_lon = row.get("longitude", "").strip()

                        # Debug: Jika nilai nampak pelik (bukan nombor), cetak ralat jelas
                        if not self.is_valid_coordinate(raw_lat) or not self.is_valid_coordinate(raw_lon):
                            raise ValueError(f"Koordinat tidak sah. Lat: '{raw_lat}', Lon: '{raw_lon}'")

                        val_1 = float(raw_lat)
                        val_2 = float(raw_lon)

                        # --- 2. LOGIK PINTAR: TENTUKAN LAT vs LON ---
                        # Malaysia: Longitud (X) > 90, Latitud (Y) < 10
                        if val_1 > 90: 
                            lon = val_1
                            lat = val_2
                        else:
                            lat = val_1
                            lon = val_2
                        
                        # Pastikan Latitud dalam julat Malaysia (lebih kurang)
                        if not (0 < lat < 10):
                             self.stdout.write(self.style.WARNING(f"Amaran Baris {row_num}: Latitud {lat} mungkin di luar Malaysia?"))

                        lokasi = Point(lon, lat, srid=4326)

                        # --- 3. PROSES DATA LAIN ---
                        # Auto-extract poskod jika lajur kosong
                        postcode = row.get("postcode", row.get("poskod", "")).strip()
                        alamat = row.get("address", "").strip()
                        
                        if not postcode and alamat:
                            match = re.search(r'\b\d{5}\b', alamat)
                            if match:
                                postcode = match.group(0)

                        bandar = row.get("city", row.get("bandar", "")).strip()

                        # --- 4. SIMPAN KE DB ---
                        School.objects.update_or_create(
                            kod_sekolah=kod_sekolah,
                            defaults={
                                "name": row.get("name", "").strip(),
                                "address": alamat,
                                "ppd": row.get("ppd", "").strip(),
                                "city": bandar,
                                "postcode": postcode,
                                "school_type": row.get("school_type", "RENDAH").strip(),
                                "location": lokasi,
                            }
                        )
                        success_count += 1

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Ralat Baris {row_num} ({kod_sekolah}): {e}"))
                        error_count += 1
                        continue

            self.stdout.write(self.style.SUCCESS(f"SELESAI! Berjaya: {success_count}, Gagal: {error_count}"))

        except FileNotFoundError:
            raise CommandError(f'Fail "{csv_file_path}" tidak ditemui.')

    def is_valid_coordinate(self, value):
        """Helper untuk semak jika string boleh ditukar jadi float"""
        try:
            float(value)
            return True
        except ValueError:
            return False
