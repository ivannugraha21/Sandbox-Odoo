{\rtf1\ansi\ansicpg1252\cocoartf2513
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 =============================================================================\
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0
\cf0 SANBOX API ODOO\
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0
\cf0 =============================================================================\
Info :\
	- 1 user/email di sandbox dapat memiliki banyak merchant. Di Odoo user sebagai user dan merchant sebagai company.\
	- Untuk update menggunakan scheduler cron atau bisa klik tombol manual update di menu preferensi user di pojok kanan atas.\
	- Data pelanggan dari order sandbox tidak ada id jadi menggunakan nama untuk mencocokan data dengan odoo. Jika nama tidak ditemukan / tidak cocok akan menggunakan default pelanggan di Odoo nya (No Name).\
	- Untuk sekarang payment masuk ke jurnal kas untuk tipe \'93cash\'94 dan bank untuk sisanya (virtual_account, qr_code, dll). Kalau kedepannya ada jurnal berbeda tinggal buat junalnya, fungsi sudah ada\
	- Untuk payment fee (split/owner/customer) sekarang masih mengikuti Setting sandbox, kedepannya mending ambil dari print_invoice karna data setting bisa berubah\'94. (Karna data di invoicenya masih salah jadi dari setting dulu)\
	- Untuk Akunting - CoA company baru ambil template dari account.chart.template, defaultnya cuma 1 data \'93indonesia\'94. Jika ada template berbeda tinggal tambah template yang baru lalu di filter.\
	- Setting \'93Outstanding Receipts Account\'94 di jurnal untuk otomatisasi payment \'93Paid\'94 saat cron job (untuk sekarang mengikuti default akun id di jurnalnya)\
	- Cash Rounding / Pembulatan Kas sepertinya global jadi cek sekali aja, kalau sudah ada tinggal pakai, kalau belum ada buat (Karna butuh 1 cek apa sudah ada di model atau belum)\
\
=============================================================================\
Setting Dari Awal :\
	- Install modul \'93restapi\'94\
	- Instal modul \'93Sale\'94 dan \'93Accounting\'94 (Kalau belum ada)\
	- Centang Pembulatan Kas / Cash Rounding di pengaturan Akunting\
	- Setting Sandbox API di user setting / menu atas preferensi. (Bisa buat user baru / pakai user admin)	\
	\
\
}