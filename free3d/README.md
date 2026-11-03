# Vellessa: ücretsiz ayakkabı fotogrametrisi

Bu yol ücretli API/kredi kullanmaz. Meshroom ve Blender ücretsiz, açık kaynaklı masaüstü yazılımlardır. İşlem için Windows/Linux/macOS bilgisayar gerekir; iPhone tarayıcısında ağır 3D rekonstrüksiyon çalıştırılamaz.

## 1. Çekim
- Aynı ayakkabıyı sabit, mat ve dokulu bir zeminde tut.
- 8 fotoğraf minimumdur; daha iyi sonuç için 20-40 fotoğraf çek.
- Ayakkabının çevresinde küçük adımlarla dön; ardışık kareler en az %70 örtüşsün.
- Kamera mesafesi ve pozlamayı sabit tut. Bulanık fotoğraf kullanma.
- Üst, iki yan, burun ve topuk bölgelerini kapsa. Alt yüzey için ayakkabıyı dikkatlice ters çevirip ayrı bir set çek; iki seti aynı sahnede hizalamak zor olabilir.

## 2. Ücretsiz yazılımlar
- Meshroom (AliceVision): https://alicevision.org/#meshroom
- Blender: https://www.blender.org/download/

## 3. Fotoğraf paketini hazırla
Reels Atölyesi'nde fotoğrafları seçip **Ücretsiz 3D paketini indir** düğmesine bas. ZIP'i bilgisayarda aç.

## 4. GLB üret
Python 3 kurulu olsun. Meshroom ve Blender kurulumları PATH'e eklenmiş olmalı. Bu klasörde terminal aç:
```bash
python photogrammetry.py ./vellessa-ayakkabi-fotograflari --output ./vellessa-output
```
İstersen yürütülebilir yollarını `--meshroom` ve `--blender` ile ver. İşlem bilgisayarın CPU/GPU ve RAM kapasitesine göre uzun sürebilir.

## 5. Reels videosu
Oluşan `vellessa-output/vellessa-ayakkabi.glb` dosyasını Reels Atölyesi'nde **Hazır 3D modelim var** alanından yükle. Gerçek 3D kamera motoruyla 10/15/20 saniyelik kesintisiz video al.

## Önemli doğruluk notu
Fotogrametri, çekilen yüzeyleri yeniden kurar; fotoğraflarda görünmeyen bölgeleri tahmin edemez. Parlak, tek renkli, şeffaf ayakkabılarda sonuç zayıflayabilir. Meshroom çıktısını orijinal ürünle karşılaştır; logo, dikiş, taban ve burun formu değişmişse reklamda kullanma. Ücretsiz yazılım, kusursuz geometri garantisi değildir.
