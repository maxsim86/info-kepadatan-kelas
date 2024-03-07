from django.db import models


class Classroom(models.Model):
    SCHOOL_CHOICES = [
        ("SK KLANG ", "SK KLANG"),
        ("SK TELOK GADONG", "SK TELOK GADONG"),
        ("SK PELABUHAN KELANG", "SK PELABUHAN KELANG"),
        ("SK TELOK MENEGON", "SK TELOK MENEGON"),
        ("SK BUKIT NAGA", "SK BUKIT NAGA "),
        ("SK JALAN KEBUN", "SK JALAN KEBUN"),
        ("SK BATU BELAH", "SK BATU BELAH"),
        ("SK SEMENTA ", "SK SEMENTA"),
        ("SK KAPAR", "SK KAPAR"),
        ("SK BUKIT KAPAR", "SK BUKIT KAPAR"),
        ("SK SUNGAI BINJAI", "SK SUNGAI BINJAI"),
        ("SK PULAU INDAH", "SK PULAU INDAH"),
        ("SK TOK MUDA", "SK TOK MUDA"),
        ("SK BUKIT KUDA", "SK BUKIT KUDA"),
        ("SK PANDAMARAN JAYA", "SK PANDAMARAN JAYA"),
        ("SK KG JOHAN SETIA", "SK KG JOHAN SETIA"),
        ("SK SUNGAI SERDANG", "SK SUNGAI SERDANG"),
        ("SK KG PENDAMAR", "SK KG PENDAMAR"),
        ("SK TELOK GONG", "SK TELOK GONG"),
        ("SK TAMAN KLANG JAYA", "SK TAMAN KLANG JAYA"),
        ("SK SUNGAI UDANG", "SK SUNGAI UDANG"),
        ("SK PELABUHAN UTARA", "SK PELABUHAN UTARA"),
        ("SK ABDUL SAMAT", "SK ABDUL SAMAT"),
        ("SK MERU", "SK MERU"),
        ("SK KAMPUNG IDAMAN", "SK KAMPUNG IDAMAN"),
        ("SK TAMAN KLANG UTAMA", "SK TAMAN KLANG UTAMA"),
        ("SK KAMPUNG JAWA", "SK KAMPUNG JAWA"),
        ("SK TAMAN GEMBIRA", "SK TAMAN GEMBIRA"),
        ("SK BUKIT TINGGI ", "SK BUKIT TINGGI"),
        ("SK BUKIT KEMUNING 2", "SK BUKIT KEMUNING 2"),
        ("SK MERU (2)", "SK MERU (2)"),
        ("SK SUNGAI KAPAR INDAH", "SK SUNGAI KAPAR INDAH"),
        ("SK KOTA KEMUNING", "SK KOTA KEMUNING "),
        ("SK PULAU INDAH (2)", "SK PULAU INDAH (2)"),
        ("SK BUKIT RIMAU ", "SK BUKIT RIMAU"),
        ("SK BUKIT CERAKAH ", "SK BUKIT CERAKAH"),
        ("SK METHODIST ACS", "SK METHODIST ACS"),
        ("SK (1) JALAN BATU TIGA ", "SK (1) JALAN BATU TIGA "),
        ("SK (1) JALAN BATU TIGA", "SK (1) JALAN BATU TIGA "),
        ("SK CONVENT (1) (M)", "SK CONVENT (1) (M) "),
        ("SK CONVENT (2) (M)  ", "SK CONVENT (2) (M)"),
        ("SK (1) JALAN MERU", "SK (1) JALAN MERU "),
        ("SK (2) JALAN MERU", "SK (2) JALAN MERU "),
        ("SK METHODIST ( M )", "SK METHODIST ( M )"),
        ("SK (P) METHODIST MGS", "SK (P) METHODIST MGS "),
        ("SK TENGKU BENDAHARA AZMAN (1)", "SK TENGKU BENDAHARA AZMAN (1)"),
        ("SK TENGKU BENDAHARA AZMAN (2) ", "SK TENGKU BENDAHARA AZMAN (2)"),
        ("SK (P) BUKIT KUDA", "SK (P) BUKIT KUDA"),
        ("SK (2) SIMPANG LIMA ", "SK (2) SIMPANG LIMA      "),
        ("SK ST ANNE'S CONVENT", "SK ST ANNE'S CONVENT"),
        ("SJK(C) PEREMPUAN", "SJK(C) PEREMPUAN"),
        ("SJK(C) CHUEN MIN", "SJK(C) CHUEN MIN"),
        ("SJK(C) CHUNG HUA", "SJK(C) CHUNG HUA "),
        ("SJK(C) HIN HUA ", "SJK(C) HIN HUA "),
        ("SJK(C) HWA LIEN", "SJK(C) HWA LIEN"),
        ("SJK(C) KHE BENG", "SJK(C) KHE BENG"),
        ("SJK(C) KONG HOE", "SJK(C) KONG HOE"),
        ("SJK(C) LEE MIN", "SJK(C) LEE MIN"),
        ("SJK(C) PANDAMARAN 'A'", "SJK(C) PANDAMARAN 'A'"),
        ("SJK(C) PANDAMARAN 'B'", "SJK(C) PANDAMARAN 'B'"),
        ("SJK(C) PIN HWA (1)", "SJK(C) PIN HWA (1)"),
        ("SJK(C) PUI YING", "SJK(C) PUI YING"),
        ("SJK(C) SOO JIN", "SJK(C) SOO JIN"),
        ("SJK(C) TIONG HUA KOK BIN", "SJK(C) TIONG HUA KOK BIN"),
        ("SJK(C) TSHING NIAN", "SJK(C) TSHING NIAN"),
        ("SJK(C) WU TECK ", "SJK(C) WU TECK"),
        ("SJK(C) YING WAH", "SJK(C) YING WAH "),
        ("SJK(C) PIN HWA (2)", "SJK(C) PIN HWA (2) "),
        ("SJK(C) TAMAN RASHNA", "SJK(C) TAMAN RASHNA"),
        ("SJK(T) LADANG BRAFFERTON", "SJK(T) LADANG BRAFFERTON"),
        ("SJK(T) LADANG BUKIT RAJAH", "SJK(T) LADANG BUKIT RAJAH"),
        ("SJK(T) LADANG EMERALD", "SJK(T) LADANG EMERALD"),
        ("SJK(T) LADANG HIGHLANDS", "SJK(T) LADANG HIGHLANDS "),
        ("SJK(T) LADANG JALAN ACOB ", "SJK(T) LADANG JALAN ACOB "),
        ("SJK(T) JALAN TEPI SUNGAI", "SJK(T) JALAN TEPI SUNGAI"),
        ("SJK(T) JALAN MERU", "SJK(T) JALAN MERU"),
        ("SJK(T) METHODIST", "SJK(T) METHODIST "),
        ("SJK(T) SIMPANG LIMA", "SJK(T) SIMPANG LIMA"),
        ("SJK(T) LDG VALLAMBROSA", "SJK(T) LDG VALLAMBROSA "),
        ("SJK(T) TAMAN SENTOSA", "SJK(T) TAMAN SENTOSA"),
        ("SJK(T) LADANG NORTH HUMMOCK", "SJK(T) LADANG NORTH HUMMOCK"),
    ]
    YEAR_CHOICES = [
        ("PPKI", "PPKI"),
        ("TAHUN SATU", "TAHUN SATU"),
        ("TAHUN DUA", "TAHUN DUA"),
        ("TAHUN TIGA", "TAHUN TIGA"),
        ("TAHUN EMPAT", "TAHUN EMPAT"),
        ("TAHUN LIMA", "TAHUN LIMA"),
        ("TAHUN ENAM", "TAHUN ENAM"),
    ]

    school = models.CharField(
        max_length=50, choices=SCHOOL_CHOICES, verbose_name="Pilihan Sekolah"
    )
    year = models.CharField(
        max_length=50, choices=YEAR_CHOICES, verbose_name="tahun kelas"
    )
    average = models.IntegerField(verbose_name="purata")

    class Meta:
        verbose_name = "Enrolmen Sekolah"
        verbose_name_plural = "Enrolmen Sekolah"

    def __str__(self):
        return f"{self.school} - {self.year} - {self.average}"


class Contact_us(models.Model):
    name = models.CharField(max_length=200, verbose_name="nama")
    email = models.EmailField()
    message = models.CharField(max_length=300, verbose_name="mesej")

    class Meta:
        verbose_name = "Maklum Balas"
        verbose_name_plural = "Maklum Balas"

    def __str__(self):
        return f"{self.name} - {self.message}"
