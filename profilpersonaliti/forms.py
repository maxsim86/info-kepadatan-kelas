# profilpersonaliti/forms.py

from django import forms


class PersonalDataForm(forms.Form):
    """Form untuk data peribadi."""

    URUSAN_CHOICES = [
        ("1", "Pilih Urusan 1"),
        ("2", "Pilih Urusan 2"),
        ("3", "Pilih Urusan 3"),
    ]

    JANTINA_CHOICES = [
        ("L", "Lelaki"),
        ("P", "Perempuan"),
    ]

    WARGANEGARA_CHOICES = [
        ("WNI", "Warganegara"),
        ("WNA", "Warga Asing"),
    ]

    AGAMA_CHOICES = [
        ("ISLAM", "Islam"),
        ("KRISTEN", "Kristen"),
        ("BUDHA", "Budha"),
        ("HINDU", "Hindu"),
        ("LAIN", "Lain"),
    ]

    BANGSA_CHOICES = [
        ("MELAYU", "Melayu"),
        ("CINA", "Cina"),
        ("INDIA", "India"),
        ("LAIN", "Lain"),
    ]

    KUMPULAN_PERKHIDMATAN_CHOICES = [
        ("KP1", "Kumpulan Perkhidmatan 1"),
        ("KP2", "Kumpulan Perkhidmatan 2"),
        ("KP3", "Kumpulan Perkhidmatan 3"),
    ]

    KATEGORI_KLIEN_CHOICES = [
        ("KLIEN1", "Kategori Klien 1"),
        ("KLIEN2", "Kategori Klien 2"),
        ("KLIEN3", "Kategori Klien 3"),
    ]
    no_kad_pengenalan = forms.CharField(
        label="No. Kad Pengenalan",
        widget=forms.TextInput(attrs={"placeholder": "Contoh: 880808001111"}),
    )
    nama_penuh = forms.CharField(label="Nama Penuh")
    jantina = forms.ChoiceField(
        label="Jantina",
        choices=JANTINA_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    warganegara = forms.ChoiceField(
        label="Warganegara",
        choices=WARGANEGARA_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    tarikh_lahir = forms.DateField(
        label="Tarikh Lahir", widget=forms.DateInput(attrs={"type": "date"})
    )
    agama = forms.ChoiceField(
        label="Agama",
        choices=AGAMA_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    bangsa = forms.ChoiceField(
        label="Bangsa",
        choices=BANGSA_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    kumpulan_perkhidmatan = forms.ChoiceField(
        label="Kumpulan Perkhidmatan",
        choices=KUMPULAN_PERKHIDMATAN_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    gred_jawatan = forms.CharField(label="Gred Jawatan")
    jawatan = forms.CharField(label="Jawatan")
    no_telefon_pejabat = forms.CharField(
        label="No. Telefon Pejabat",
        widget=forms.TextInput(attrs={"placeholder": "Contoh: 0368881111"}),
    )
    no_telefon_bimbit = forms.CharField(
        label="No. Telefon Bimbit",
        widget=forms.TextInput(attrs={"placeholder": "Contoh: 0192233445"}),
    )
    alamat_e_mel = forms.EmailField(label="Alamat E-Mel")
    kategori_klien = forms.ChoiceField(
        label="Kategori Klien",
        choices=KATEGORI_KLIEN_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    tempat_berkhidmat_pengajian = forms.CharField(
        label="Tempat Berkhidmat/Pengajian",
        widget=forms.TextInput(attrs={"placeholder": "Sila klik butang kemaskini"}),
    )
    urusan = forms.ChoiceField(
        label="Urusan",
        choices=URUSAN_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
