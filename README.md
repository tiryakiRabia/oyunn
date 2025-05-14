# Balon Patlatan Okçu Oyunu

## Oyun Tanımı
Balon Patlatan Okçu, Python’un `pygame` kütüphanesi kullanılarak geliştirilen bir 2D okçuluk oyunudur. Oyuncu, dönen bir yayla açı belirler, ardından hız ibresi yardımıyla oku fırlatarak balonları patlatmaya çalışır. Her vurulan balon bir kalbi doldurur. Tüm balonlar patlatılırsa oyun kazanılır, oklar biterse ve tüm balonlar vurulmamışsa oyun kaybedilir.

---

## Oyun Özellikleri
- Dönen yay ile dinamik **açı belirleme**
- Hareketli hız ibresi ile **hız kontrolü**
- Gerçekçi **ok simülasyonu** (yerçekimi etkili)
- **Balon patlama animasyonları**
- 10 ok hakkı ile sınırlı deneme
- 5 kalp sistemiyle kazanma durumu
- **Ses efektleri** ve **arka plan müziği**
- Kazanma/kaybetme ekranı
- Oyuna başlangıçta “ARE YOU READY?” animasyonu
- Ok simgeleriyle kalan hak gösterimi

---

## Kurulum ve Çalıştırma

### 1. Gereksinimler
- Python 3.x
- Pygame kütüphanesi (Yüklü değilse aşağıdaki komutu girin)

```bash
pip install pygame
```

### 2. Oyunu Başlatmak

Terminal ya da komut satırına şu komutu yazın:

```bash
python main.py
```

> Not: Görsel ve ses dosyalarının doğru klasörlerde olduğundan emin olun.

---

## Oyun Kontrolleri

| Tuş | Görev |
|-----|-------|
| `A` | Dönen yayı durdurur ve açıyı kilitler |
| `S` veya `SPACE` | Hız ibresini durdurur ve oku fırlatır |
| `ESC` | Oyunu kapatır |

---

## Oyun Akışı
1. Oyun başladığında “ARE YOU READY?” yazısı görünür.
2. Oyuncu `A` tuşuna basarak dönen yayı durdurur ve atış açısını kilitler.
3. Ardından `S` veya `SPACE` tuşuna basarak hız ibresini durdurur ve oku fırlatır.
4. Ok, seçilen açı ve hıza göre hareket eder ve hedefe ulaşmaya çalışır.
5. Eğer ok bir balona çarparsa:
   - Balon animasyonla patlar
   - Ses efekti çalar
   - Bir kalp dolar
6. Tüm kalpler dolarsa kazanma ekranı gösterilir.
7. Tüm oklar biterse ve tüm kalpler dolmamışsa kaybetme ekranı gösterilir.

---

## Kullanılan Görseller ve Açıklamaları

### Arka Plan
- `backgroundd.png` → Oyun arka plan görseli

### Okçu ve Yay
- `okcu.png` → Oyuncu karakteri
- `acı_oku.png` → Dönen yayın görseli
- `ok.png` → Ok görseli (iki boyutta kullanılır: 90x30 ve 150x50)

### Hız İbresi
- `hız_ibresi.png` → İbrenin bulunduğu panel
- `ibre_altındaki_cizgi.png` → İbre çizgisi
- `ibre_belirtec.png` → Hareketli ibre oku

### Balonlar
- `balon1.png` → Sağlam balon
- `balon2.png` → Patlamış balon animasyonu
- `balon3.png` → Parçalanmış ve düşen balon

### Kalpler (Can Sistemi)
- `bos_kalp.png` → Boş kalp (vurulmamış balon)
- `dolu_kalp.png` → Dolu kalp (vurulmuş balon)

### Kazanma Ekranı
- `win_yazisi.png` → “Kazandın” yazısı
- `winkalp.png` → Kutlama kalbi

### Kaybetme Ekranı
- `lost_yazisi.png` → “Kaybettin” yazısı
- `lostkalp.png` → Üzgün kalp

---

## Kullanılan Ses Dosyaları

| Dosya Adı | Açıklama |
|-----------|----------|
| `arkaplan.mp3` | Oyunun arka plan müziği (sürekli çalar) |
| `atış.mp3` | Ok fırlatıldığında çalınır |
| `pop.mp3` | Balon vurulduğunda çalınır |
| `oyunukazandı.mp3` | Oyun kazanıldığında çalınır |
| `oyunukaybetti.mp3` | Oyun kaybedildiğinde çalınır |

> Tüm sesler uygun ses seviyesinde (`set_volume`) ayarlanmıştır.

---

## Geliştiriciler

- **Zeren Karataş**
- **Rabia Tiryaki**
- **Dilanur Bal**

Pamukkale Üniversitesi – Bilgisayar Mühendisliği 2. sınıf öğrencileri  
2025

---

## Lisans ve Kullanım
Bu proje yalnızca eğitim ve gösterim amaçlıdır.  
Telif hakkı geliştiricilere aittir.

