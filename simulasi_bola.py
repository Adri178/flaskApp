from vpython import *

# Ukuran frame
panjang = 15  # Memperbesar frame
tinggi = 15   # Memperbesar frame
tebal = 0.2

# Setup scene dengan ukuran yang lebih besar
scene.width = 800
scene.height = 600
scene.range = 10  # Menyesuaikan jarak pandang kamera

# Membuat dinding kotak 2D (persegi panjang) di bidang horizontal (x-y)
dinding_atas = box(pos=vector(0, tinggi/2, 0), size=vector(panjang, tebal, tebal), color=color.white)
dinding_bawah = box(pos=vector(0, -tinggi/2, 0), size=vector(panjang, tebal, tebal), color=color.white)
dinding_kiri = box(pos=vector(-panjang/2, 0, 0), size=vector(tebal, tinggi, tebal), color=color.white)
dinding_kanan = box(pos=vector(panjang/2, 0, 0), size=vector(tebal, tinggi, tebal), color=color.white)

# Membuat bola dengan warna berbeda
bolas = [
    sphere(pos=vector(-4, -4, 0), radius=0.5, color=color.red, velocity=vector(0.025, 0.035, 0)),
    sphere(pos=vector(-3, -3, 0), radius=0.5, color=color.green, velocity=vector(0.035, 0.025, 0)),
    sphere(pos=vector(-2, -2, 0), radius=0.5, color=color.blue, velocity=vector(0.05, 0.035, 0)),
    sphere(pos=vector(-1, -1, 0), radius=0.5, color=color.yellow, velocity=vector(0.05, 0.05, 0)),
    sphere(pos=vector(0, 0, 0), radius=0.5, color=color.cyan, velocity=vector(0.025, 0.05, 0)),
    sphere(pos=vector(2, 2, 0), radius=0.5, color=color.purple, velocity=vector(0, 0, 0))  # Bola ungu
]

bola_pengguna = bolas[-1]  # Menggunakan bola ungu sebagai bola pengguna
kecepatan_gerak = 0.05  # Mengurangi kecepatan gerakan bola ungu

# Mode bola ungu: 0 untuk mode memantul, 1 untuk mode berhenti
mode_bola_ungu = 0

# Label di sebelah frame
label_mode = label(pos=vector(0, tinggi/2 + 1, 0), text="Mode: Memantul", height=15, border=4, color=color.black, background=color.white)
label_tabrakan = label(pos=vector(0, tinggi/2 + 2, 0), text="Tabrakan: 0", height=15, border=4, color=color.black, background=color.white)

# Variabel untuk menghitung jumlah tabrakan bola ungu
jumlah_tabrakan = 0

def cek_tabrakan(bola1, bola2):
    # Menghitung jarak antara dua bola
    jarak = mag(bola1.pos - bola2.pos)
    return jarak < (bola1.radius + bola2.radius)

def tangani_tabrakan(bola1, bola2):
    global jumlah_tabrakan
    # Vektor normal dan tangent
    normal = (bola1.pos - bola2.pos).norm()
    tangent = vector(-normal.y, normal.x, 0)

    # Kecepatan dalam arah normal dan tangent
    v1n = bola1.velocity.dot(normal)
    v1t = bola1.velocity.dot(tangent)
    v2n = bola2.velocity.dot(normal)
    v2t = bola2.velocity.dot(tangent)

    # Bertukar kecepatan dalam arah normal
    v1n, v2n = v2n, v1n

    # Kecepatan akhir
    bola1.velocity = v1n * normal + v1t * tangent
    bola2.velocity = v2n * normal + v2t * tangent

    # Menghindari tumpang tindih antara bola ungu dan bola lain
    if bola1 == bola_pengguna or bola2 == bola_pengguna:
        if bola1 != bola_pengguna or bola2 != bola_pengguna:
            overlap = bola1.radius + bola2.radius - mag(bola1.pos - bola2.pos)
            direction = norm(bola1.pos - bola2.pos)
            if bola1 != bola_pengguna:
                bola1.pos += direction * overlap / 2
            if bola2 != bola_pengguna:
                bola2.pos -= direction * overlap / 2

            jumlah_tabrakan += 1
            label_tabrakan.text = f"Tabrakan: {jumlah_tabrakan}"  # Update teks label jumlah tabrakan

            # Jika bola bukan bola pengguna, dan mode berhenti aktif, maka hentikan bola tersebut
            if bola1 != bola_pengguna and mode_bola_ungu == 1:
                bola1.velocity = vector(0, 0, 0)
            if bola2 != bola_pengguna and mode_bola_ungu == 1:
                bola2.velocity = vector(0, 0, 0)

def gerak_bola_pengguna():
    global mode_bola_ungu

    # Mengambil input dari keyboard
    if 'left' in keysdown():
        bola_pengguna.pos.x -= kecepatan_gerak
    if 'right' in keysdown():
        bola_pengguna.pos.x += kecepatan_gerak
    if 'up' in keysdown():
        bola_pengguna.pos.y += kecepatan_gerak
    if 'down' in keysdown():
        bola_pengguna.pos.y -= kecepatan_gerak

    # Memantulkan bola pengguna dari dinding
    if bola_pengguna.pos.x > panjang/2 - bola_pengguna.radius:
        bola_pengguna.pos.x = panjang/2 - bola_pengguna.radius
    if bola_pengguna.pos.x < -panjang/2 + bola_pengguna.radius:
        bola_pengguna.pos.x = -panjang/2 + bola_pengguna.radius
    if bola_pengguna.pos.y > tinggi/2 - bola_pengguna.radius:
        bola_pengguna.pos.y = tinggi/2 - bola_pengguna.radius
    if bola_pengguna.pos.y < -tinggi/2 + bola_pengguna.radius:
        bola_pengguna.pos.y = -tinggi/2 + bola_pengguna.radius

    # Memeriksa tabrakan dengan bola lain
    for bola in bolas:
        if bola != bola_pengguna and cek_tabrakan(bola_pengguna, bola):
            if bola != bola_pengguna:  # Hanya pengaruhkan bola lain, bukan bola pengguna
                if mode_bola_ungu == 0:  # Mode memantul
                    tangani_tabrakan(bola_pengguna, bola)
                elif mode_bola_ungu == 1:  # Mode berhenti
                    # Hindari menempel pada bola lain
                    overlap = bola_pengguna.radius + bola.radius - mag(bola_pengguna.pos - bola.pos)
                    direction = norm(bola_pengguna.pos - bola.pos)
                    bola_pengguna.pos += direction * overlap / 2

def ganti_mode(evt):
    global mode_bola_ungu
    if evt.key == 'm':
        mode_bola_ungu = (mode_bola_ungu + 1) % 2  # Ganti mode antara 0 dan 1
        if mode_bola_ungu == 0:
            label_mode.text = "Mode: Memantul"  # Update teks label saat mode memantul
            print("Mode Bola Ungu: Memantul")
        elif mode_bola_ungu == 1:
            label_mode.text = "Mode: Berhenti"  # Update teks label saat mode berhenti
            print("Mode Bola Ungu: Berhenti")

def gerak_bola_ungu(evt):
    global bola_pengguna, kecepatan_gerak
    if evt.key == 'w':
        bola_pengguna.pos.y += kecepatan_gerak
    elif evt.key == 's':
        bola_pengguna.pos.y -= kecepatan_gerak
    elif evt.key == 'a':
        bola_pengguna.pos.x -= kecepatan_gerak
    elif evt.key == 'd':
        bola_pengguna.pos.x += kecepatan_gerak

    # Memantulkan bola pengguna dari dinding
    if bola_pengguna.pos.x > panjang/2 - bola_pengguna.radius:
        bola_pengguna.pos.x = panjang/2 - bola_pengguna.radius
    if bola_pengguna.pos.x < -panjang/2 + bola_pengguna.radius:
        bola_pengguna.pos.x = -panjang/2 + bola_pengguna.radius
    if bola_pengguna.pos.y > tinggi/2 - bola_pengguna.radius:
        bola_pengguna.pos.y = tinggi/2 - bola_pengguna.radius
    if bola_pengguna.pos.y < -tinggi/2 + bola_pengguna.radius:
        bola_pengguna.pos.y = -tinggi/2 + bola_pengguna.radius

    # Memeriksa tabrakan dengan bola lain
    for bola in bolas:
        if bola != bola_pengguna and cek_tabrakan(bola_pengguna, bola):
            if bola != bola_pengguna:  # Hanya pengaruhkan bola lain, bukan bola pengguna
                if mode_bola_ungu == 0:  # Mode memantul
                    tangani_tabrakan(bola_pengguna, bola)
                elif mode_bola_ungu == 1:  # Mode berhenti
                    # Hindari menempel pada bola lain
                    overlap = bola_pengguna.radius + bola.radius - mag(bola_pengguna.pos - bola.pos)
                    direction = norm(bola_pengguna.pos - bola.pos)
                    bola_pengguna.pos += direction * overlap / 2

# Menghubungkan event keydown untuk menggerakkan bola ungu
scene.bind('keydown', gerak_bola_ungu)

# Menghubungkan event keydown dengan fungsi ganti_mode
scene.bind('keydown', ganti_mode)

# Loop animasi
while True:
    rate(100)  # Mengatur kecepatan animasi
    
    # Gerak bola pengguna
    gerak_bola_pengguna()

    for i in range(len(bolas)):
        bola = bolas[i]
        bola.pos += bola.velocity
        
        # Memantulkan bola dari dinding
        if bola.pos.x > panjang/2 - bola.radius or bola.pos.x < -panjang/2 + bola.radius:
            bola.velocity.x = -bola.velocity.x
        if bola.pos.y > tinggi/2 - bola.radius or bola.pos.y < -tinggi/2 + bola.radius:
            bola.velocity.y = -bola.velocity.y

        # Memeriksa tabrakan dengan bola lain
        for j in range(i + 1, len(bolas)):
            bola_lain = bolas[j]
            if cek_tabrakan(bola, bola_lain):
                tangani_tabrakan(bola, bola_lain)

        # Memeriksa tabrakan dengan bola pengguna
        if bola != bola_pengguna and cek_tabrakan(bola, bola_pengguna):
            if bola != bola_pengguna:  # Hanya pengaruhkan bola lain, bukan bola pengguna
                if mode_bola_ungu == 0:  # Mode memantul
                    tangani_tabrakan(bola, bola_pengguna)
                elif mode_bola_ungu == 1:  # Mode berhenti
                    # Hindari menempel pada bola lain
                    overlap = bola_pengguna.radius + bola.radius - mag(bola_pengguna.pos - bola.pos)
                    direction = norm(bola_pengguna.pos - bola.pos)
                    bola_pengguna.pos += direction * overlap / 2
