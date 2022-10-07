=============================================================================
SANBOX API ODOO\
=============================================================================
Info :
	- 1 user/email di sandbox dapat memiliki banyak merchant. Di Odoo user sebagai user dan merchant sebagai company.
	- Untuk update menggunakan scheduler cron atau bisa klik tombol manual update di menu preferensi user di pojok kanan atas.
	- Data pelanggan dari order sandbox tidak ada id jadi menggunakan nama untuk mencocokan data dengan odoo. Jika nama tidak ditemukan / tidak cocok akan menggunakan default pelanggan di Odoo nya (No Name).
	- Untuk sekarang payment masuk ke jurnal kas untuk tipe "cash" dan bank untuk sisanya (virtual_account, qr_code, dll). Kalau kedepannya ada jurnal berbeda tinggal buat junalnya, fungsi sudah ada.
	- Untuk payment fee (split/owner/customer) sekarang masih mengikuti Setting sandbox, kedepannya mending ambil dari print_invoice karna data setting bisa berubah. (Karna data di invoicenya masih salah jadi dari setting dulu).
	- Untuk Akunting - CoA company baru ambil template dari account.chart.template, defaultnya cuma 1 data "Indonesia". Jika ada template berbeda tinggal tambah template yang baru lalu di filter.
	- Setting "Outstanding Receipts Account" di jurnal untuk otomatisasi payment "Paid" saat cron job (untuk sekarang mengikuti default akun id di jurnalnya).
	- Cash Rounding / Pembulatan Kas sepertinya global jadi cek sekali aja, kalau sudah ada tinggal pakai, kalau belum ada buat (Karna butuh 1 cek apa sudah ada di model atau belum).

=============================================================================
Setting Dari Awal :
	- Install modul "restapi"
	- Instal modul "Sale" dan "Accounting" (Kalau belum ada)
	- Centang Pembulatan Kas / Cash Rounding di pengaturan Akunting
	- Setting Sandbox API di user setting / menu atas preferensi. (Bisa buat user baru / pakai user admin)
	

