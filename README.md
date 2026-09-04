# Network Scanner

Network Scanner, yerel ağ üzerindeki cihazları keşfetmek, temel TCP port taraması yapmak ve elde edilen sonuçları web tabanlı bir dashboard üzerinden görüntülemek amacıyla geliştirilmiş bir ağ tarama uygulamasıdır.

Proje; ağ programlama, REST API, veritabanı, backend ve frontend teknolojilerini tek bir uygulama içerisinde bir araya getirmek amacıyla geliştirilmiştir.

---

## Projenin Amacı

Bu projenin temel amacı, belirli bir yerel ağ içerisindeki cihazları otomatik olarak tespit etmek ve bu cihazlar hakkında temel ağ bilgilerini kullanıcıya sunmaktır.

Uygulama aşağıdaki işlemleri gerçekleştirebilir:

- Yerel ağdaki cihazları keşfetme
- IP adreslerini tespit etme
- MAC adreslerini tespit etme
- Hostname çözümleme
- Belirli TCP portlarının açık olup olmadığını kontrol etme
- Cihazların aktif veya pasif durumunu takip etme
- Tarama sonuçlarını veritabanında saklama
- Sonuçları web arayüzünde görüntüleme
- Sonuçları CSV formatında dışa aktarma

---

## Özellikler

- ARP tabanlı yerel ağ taraması
- IP ve MAC adresi tespiti
- Hostname çözümleme
- TCP port taraması
- Aktif / pasif cihaz takibi
- SQLite veritabanı desteği
- FastAPI tabanlı REST API
- Web tabanlı dashboard
- Son tarama zamanının saklanması
- IP/CIDR doğrulaması
- Hatalı IP aralıklarının kontrol edilmesi
- Büyük ağ taramalarının sınırlandırılması
- CSV dışa aktarma
- IP, MAC ve hostname ile cihaz arama
- Aktif / pasif cihaz filtreleme
- Cihaz detay görüntüleme
- Responsive dashboard tasarımı

---

## Kullanılan Teknolojiler

### Backend

- Python
- FastAPI
- Uvicorn

### Ağ İşlemleri

- Scapy
- Python `socket` modülü

### Veritabanı

- SQLite
- Python `sqlite3` modülü

### Frontend

- HTML
- CSS
- JavaScript

### Diğer

- Git
- GitHub
- CSV

---

## Proje Yapısı

```text
network-scanner/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── scanner.py
├── port_scanner.py
├── database.py
├── check_database.py
└── index.html