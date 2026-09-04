# Network Scanner

Yerel ağ üzerindeki cihazları keşfetmek, temel port taraması yapmak ve elde edilen sonuçları web tabanlı bir dashboard üzerinden görüntülemek için geliştirilmiş bir ağ tarama uygulamasıdır.

Bu proje ağ programlama, REST API, veritabanı ve temel frontend teknolojilerini bir arada kullanmak amacıyla geliştirilmiştir.

## Özellikler

- ARP kullanarak yerel ağdaki cihazları keşfetme
- IP ve MAC adreslerini tespit etme
- Hostname çözümleme
- TCP port taraması
- Aktif ve pasif cihaz takibi
- Tarama sonuçlarını SQLite veritabanında saklama
- FastAPI tabanlı REST API
- Web tabanlı dashboard
- Son tarama zamanını görüntüleme
- IP/CIDR doğrulaması
- CSV olarak sonuçları dışa aktarma

## Kullanılan Teknolojiler

- Python
- Scapy
- FastAPI
- Uvicorn
- SQLite
- HTML
- CSS
- JavaScript

## Proje Yapısı

    network-scanner/
    ├── main.py
    ├── scanner.py
    ├── port_scanner.py
    ├── database.py
    ├── check_database.py
    ├── index.html
    ├── requirements.txt
    ├── .gitignore
    └── README.md

## Kurulum

Projeyi bilgisayarınıza klonlayın:

    git clone <repository-url>

Proje klasörüne girin:

    cd network-scanner

Gerekli Python paketlerini yükleyin:

    py -m pip install -r requirements.txt

Windows üzerinde Scapy ile ARP taraması yapabilmek için Npcap kurulu olmalıdır.

## Çalıştırma

Uygulamayı başlatmak için:

    py -m uvicorn main:app --reload --port 8001

Daha sonra tarayıcıdan:

    http://127.0.0.1:8001

adresine gidin.

## Kullanım

Dashboard üzerindeki IP aralığı alanına taranacak ağı CIDR formatında girin.

Örnek:

    192.168.1.0/24

Ardından **Ağı Tara** butonuna basın.

Tarama sonucunda bulunan cihazların:

- IP adresi
- MAC adresi
- Hostname bilgisi
- Açık portları
- Aktif/Pasif durumu

dashboard üzerinde görüntülenir.

Sonuçlar **CSV İndir** butonu kullanılarak CSV formatında dışa aktarılabilir.

## API Endpointleri

| Method | Endpoint | Açıklama |
|---|---|---|
| GET | `/` | Dashboard |
| GET | `/devices` | Tüm cihazları getirir |
| GET | `/devices/{id}` | ID ile cihaz getirir |
| GET | `/devices/ip/{ip}` | IP adresine göre cihaz getirir |
| GET | `/last-scan` | Son tarama zamanını getirir |
| POST | `/scan` | Ağ taraması başlatır |
| GET | `/export` | Sonuçları CSV olarak dışa aktarır |

## Tarama Mantığı

Uygulamanın temel çalışma akışı:

    Kullanıcı
        ↓
    Web Dashboard
        ↓
    FastAPI
        ↓
    Scapy ARP Tarama
        ↓
    Cihaz Keşfi
        ↓
    TCP Port Tarama
        ↓
    SQLite
        ↓
    Dashboard

ARP taraması ile yerel ağdaki cihazlar keşfedilir. Bulunan cihazların belirlenen TCP portları kontrol edilir ve sonuçlar SQLite veritabanına kaydedilir.

## Güvenlik

Bu proje eğitim ve geliştirme amacıyla hazırlanmıştır.

Yalnızca sahibi olduğunuz veya tarama izniniz bulunan ağlarda kullanılmalıdır.

## Geliştirilebilecek Özellikler

- Daha geniş port aralığı desteği
- Tarama geçmişi
- Cihaz detay sayfası
- Dashboard filtreleme ve arama
- Daha gelişmiş hata yönetimi
- Docker desteği