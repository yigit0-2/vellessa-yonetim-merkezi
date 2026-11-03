# Vellessa Milano - Yönetim Merkezi

Vellessa Milano için mobil uyumlu işletme paneli.

## Modüller
- `index.html`: Satış paneli (demo veriler; Shopier canlı verisi değildir).
- `reels.html`: Reels içerik akışı ve açıklama taslağı.
- `analytics.html`: Windsor.ai üzerinden daha önce alınmış Instagram örnek raporu. Gösterilen tarih/saat canlı yenileme anlamına gelmez.
- `musteri-takip.html`: Müşteri talebi, ürün, numara ve durum takibi. Kayıtlar kullanıcının tarayıcısında localStorage içinde saklanır; cihazlar arasında senkron değildir.
- `automation.html`: Entegrasyon ve otomasyon durumları.

## Açma
`index.html` dosyasını tarayıcıda açın. Mobil ekrana uyumludur.

## Entegrasyon durumu
Shopier sipariş/ciro ve WhatsApp mesaj bağlantıları kurulmuş değildir. Instagram rapor sayfasındaki sayılar önceki bir veri çekiminin anlık olmayan görüntüsüdür. API anahtarlarını GitHub deposuna koymayın; gerçek entegrasyonlar güvenli sunucu tarafında yapılmalıdır.

## GitHub Pages
Depoda Settings → Pages bölümünden Deploy from a branch seçip `main` ve `/ (root)` seçilebilir. Depo şu anda private olduğundan yayın koşulları GitHub planına ve ayarlarına bağlıdır.