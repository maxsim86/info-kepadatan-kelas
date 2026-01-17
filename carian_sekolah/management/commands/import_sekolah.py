import csv
import re
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Point
from carian_sekolah.models import School

class Command(BaseCommand):
    help = "Import data sekolah dan auto-esan Poskod/Bandar jika tiada."

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Laluan ke fail CSV")

    def handle(self, *args, **options):
        csv_file_path = options["csv_file"]
        self.stdout.write(f"Memulakan import dari {csv_file_path}...")

        success_count = 0
        error_count = 0

        try:
            # Gunakan utf-8-sig untuk handle BOM
            with open(csv_file_path, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                
                # 1. NORMALISASI HEADER: Tukar semua header ke huruf kecil & buang jarak
                # Ini selesaikan masalah jika header anda "Bandar" atau " BANDAR "
                reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]
                
                # Debug: Tunjukkan header yang dikesan
                self.stdout.write(f"Lajur dikesan: {reader.fieldnames}")

                for row_num, row in enumerate(reader, 2):
                    try:
                        # Ambil data wajib
                        kod_sekolah = row.get("kod_sekolah", "").strip()
                        nama_sekolah = row.get("name", "").strip()
                        alamat = row.get("address", "").strip()
                        
                        # --- LOGIK KOORDINAT ---
                        raw_lat = row.get("latitude", "").strip()
                        raw_lon = row.get("longitude", "").strip()

                        if not raw_lat or not raw_lon:
                            # Cuba cari column 'location' jika lat/lon tak jumpa
                            self.stdout.write(self.style.WARNING(f"Baris {row_num}: Tiada koordinat. Skip."))
                            continue

                        val_1 = float(raw_lat)
                        val_2 = float(raw_lon)

                        # Pastikan Lat/Lon betul (Malaysia: Lat ~1-7, Lon ~100-119)
                        if val_1 > 90: 
                            lon = val_1
                            lat = val_2
                        else:
                            lat = val_1
                            lon = val_2
                        
                        lokasi = Point(lon, lat, srid=4326)

                        # --- LOGIK POSKOD & BANDAR ---
                        # 1. Cuba ambil dari CSV dulu (sokong 'postcode' atau 'poskod')
                        postcode = row.get("postcode", row.get("poskod", "")).strip()
                        
                        # 2. Cuba ambil dari CSV (sokong 'bandar' atau 'city')
                        bandar = row.get("bandar", row.get("city", "")).strip()

                        # 3. AUTO-EXTRACT: Jika kosong, cuba teka dari Alamat
                        if not postcode and alamat:
                            match = re.search(r'\b\d{5}\b', alamat)
                            if match:
                                postcode = match.group(0)
                        
                        if not bandar and alamat and postcode:
                            # Cuba ambil perkataan selepas poskod sebagai bandar
                            # Cth: "... 41200 KLANG ..." -> Ambil KLANG
                            parts = alamat.split(postcode)
                            if len(parts) > 1:
                                # Ambil bahagian selepas poskod, buang koma, ambil perkataan pertama/kedua
                                after_postcode = parts[1].strip(" ,.")
                                # Ambil bandar (biasanya huruf besar semua atau dipisahkan koma)
                                bandar_parts = after_postcode.split(",")[0]
                                bandar = bandar_parts.strip()

                        # --- SIMPAN KE DB ---
                        School.objects.update_or_create(
                            kod_sekolah=kod_sekolah,
                            defaults={
                                "name": nama_sekolah,
                                "address": alamat,
                                "postcode": postcode,
                                "city": bandar,
                                "ppd": row.get("ppd", "").strip(),
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
