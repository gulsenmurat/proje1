# Banka Müşterisi Kaybı: Hangi Müşteriler Ayrılma Riski Taşıyor?

**BIL545 – Veri Madenciliğinde İleri Konular**  
**Üsküdar Üniversitesi · 2026–2027 Güz · Grup 01**  
**Konu:** 9.28 – Banka müşterisi kaybı  
**Depo:** https://github.com/gulsenmurat/proje1

## 1. Grup bilgileri

| Üye | Öğrenci numarası |
|---|---|
| Murat Gülşen | 264309500 |
| Halil Çankaroğlu | 264329016 |
| Mesut İşsever | 264329015 |
| Alp Aydın Özçelik | 244312033 |
| Melih Turgut | 244309019 |

- **Grup adı:** Grup 01
- **Grup tipi:** 5 kişi; Bölüm 1–3 ile Ek Paket 1 ve Ek Paket 2
- **İletişim sorumlusu:** Murat Gülşen — murat.gulsen@st.uskudar.edu.tr
- **Sunum ve teslim:** Ders yönergesine göre 8. hafta; GitHub ve STIX

## 2. Araştırma sorusu

*Bank Customer Churn* veri kümesindeki müşteri özellikleri kullanılarak bankadan ayrılma riski tahmin edilebilir mi ve elde tutma ekibinin hangi müşteri gruplarına öncelik vermesi gerektiği güvenilir biçimde değerlendirilebilir mi?

Çalışma yalnızca model başarımına odaklanmaz; veri sızıntısının önlenmesi, dürüst çapraz doğrulama, istatistiksel karşılaştırmalar, açıklanabilirlik, birliktelik kuralları ve öznitelik seçiminin güvenilirliği de incelenir.

## 3. Veri kümesi

| Alan | Açıklama |
|---|---|
| **Veri kümesi** | Bank Customer Churn / `Churn_Modelling.csv` |
| **Kaynak** | [Aakash Aggrawal — Kaggle veri kümesi](https://www.kaggle.com/datasets/aakash50897/churn-modellingcsv) |
| **Erişim tarihi** | İlk erişim: 10 Ekim 2026; kaynak dosyasının yeniden indirilip doğrulanması: 2 Kasım 2026 |
| **Lisans** | **Unknown / belirtilmemiş.** Açık yeniden dağıtım izni varsayılmaz. |
| **Boyut** | **10.000 müşteri × 14 sütun** |
| **Hedef** | `Exited`: **1 = bankadan ayrıldı**, **0 = bankada kaldı** |
| **Sınıf dağılımı** | 2.037 ayrılan (**%20,37**), 7.963 kalan (**%79,63**) |
| **Analizde kullanılan özellikler** | CreditScore, Age, Tenure, Balance, NumOfProducts, EstimatedSalary, HasCrCard, IsActiveMember, Geography, Gender |
| **Ana modele alınmayan sütunlar** | `RowNumber`, `CustomerId`, `Surname` |

**Veri dosyası bu GitHub deposunda yayımlanmamaktadır.** Projeyi çalıştırmak için Kaggle bağlantısından `Churn_Modelling.csv` dosyasını indirin. Google Colab defteri dosyayı ilk veri yükleme hücresinde sizden ister. `CustomerId` yalnızca gerekli satır eşleştirmelerinde tutulur; tahmin özelliği olarak kullanılmaz.

Verinin toplanma zamanı, ilk üreticisi ve örneklemin temsiliyeti yeterince belgelenmediğinden sonuçların bütün banka müşterilerine genellenebileceği varsayılmaz. Ders yönergesindeki bilinen ve akademik yeniden paylaşıma izin veren lisans koşulu, kaynağın **Unknown** lisansıyla doğrulanamamaktadır; bu koşulun sağlandığı iddia edilmez.

## 4. Proje 1 kapsamı

| Bölüm | Kapsam |
|---|---|
| **1. Veri, ön işleme ve sızıntı** | Veri künyesi, keşifsel analiz, eksiklik ve sıfır değerler, soyadı kodlama, veri sızıntısı deneyi, Baseline/Lojistik Regresyon, Weka ZeroR–J48 kontrolü |
| **2. Sınıflandırma ve dürüst değerlendirme** | Beş modelin karşılaştırılması, karar ağacı kuralları, GridSearchCV ve iç içe çapraz doğrulama, McNemar ve 5×2cv testleri, model ve OOF çıktıların hazırlanması |
| **3. Veri küpü ve birliktelik** | Roll-up/drill-down ve alt gruplar, ayrıklaştırma, FP-Growth, support/confidence/lift/Kulczynski/IR, Weka Apriori kontrolü |
| **Ek Paket 1** | Karar ağacı budama eğrisi, Rastgele Orman OOB–test doyum eğrisi, Gini–permütasyon öznitelik önemi |
| **Ek Paket 2** | Filtre/sarmalayıcı/gömülü öznitelik seçimi, 100 alt örneklemde kararlılık ve gürültü kontrolü, seçimin katkısının düzeltilmiş t-testiyle değerlendirilmesi |

Deneylerde temel rasgelelik tohumu `SEED = 42`'dir. Ana model karşılaştırmalarında **5 kat × 5 tekrar tabakalı çapraz doğrulama** kullanılır. Ana ölçüt **ROC AUC**; yardımcı ölçütler Average Precision, F1, Balanced Accuracy ve Accuracy'dir.

## 5. Proje 1 sonuçlarının özeti

### 5.1 Sınıflandırma modelleri

Aşağıdaki sonuçlar, 5 katlı ve 5 tekrarlı çapraz doğrulamadaki **ROC AUC ortalaması ± standart sapmasıdır**:

| Model | ROC AUC | F1 | Average Precision |
|---|---:|---:|---:|
| Baseline (DummyClassifier) | 0,500 ± 0,000 | 0,000 | 0,204 |
| Karar Ağacı | 0,822 ± 0,010 | 0,567 | 0,628 |
| k-NN (k=25) | 0,835 ± 0,009 | 0,482 | 0,620 |
| Rastgele Orman | 0,859 ± 0,008 | 0,574 | 0,688 |
| **Gradyan Artırma (seçilen)** | **0,859 ± 0,009** | **0,594** | **0,698** |

**Nihai tercih:** Gradyan Artırma (*HistGradientBoostingClassifier*). ROC AUC bakımından Rastgele Orman'a çok yakınken F1, Average Precision ve Balanced Accuracy (0,726) açısından daha iyi sonuç vermiştir. **Bu fark istatistiksel olarak kanıtlanmış bir üstünlük değildir:** 5×2cv t-testinde `p = 0,6352` (2 Kasım 2026 sıralı yeniden çalıştırma) elde edilmiştir.

Kaydedilen `p1_hat.joblib`, **2.1 bölümündeki varsayılan parametreli** Gradyan Artırma hattıdır; 2.3'te yapılan optimizasyonun sonucu değildir. GridSearchCV için 0,8666 ve iç içe çapraz doğrulama için yaklaşık 0,866 ± 0,007 ROC AUC ayrıca raporlanmıştır.

### 5.2 Veri sızıntısının etkisi

- **Yanlış kurulum (hedef kodlama + seçim tüm veri üzerinde):** ROC AUC **0,898 ± 0,006**.
- **Doğru kurulum (işlemler çapraz doğrulama içinde):** ROC AUC **0,775 ± 0,012**.
- **Yorum:** Yaklaşık **0,123 ROC AUC puanlık yapay iyileşme**, veri sızıntısının başarıyı olduğundan yüksek gösterebildiğini ortaya koyar. Ana analizlerde ön işleme adımları `Pipeline` içinde yapılır.

### 5.3 Veri küpü ve birliktelik kuralları

- Genel müşteri ayrılma oranı **%20,37**; ayrılma oranları yaş, ülke ve aktif üyelik durumuna göre farklılaşır.
- FP-Growth (`mlxtend==0.25.0`, `min_support=0,02`, `max_len=4`) ile **7.927 sık öğe kümesi** bulunmuştur. Tüm genel kuralları oluşturmadan, sık öğe kümelerinin desteklerinden `Exited=Ayrildi` sonucuna yönelik **116 kural** hesaplanmıştır (`min_confidence=0,30`). Eski sürümde üretilen 26.657 genel kurala yeni hesaplama yönteminde ihtiyaç yoktur.
- **Weka 3.8.7 Apriori** karşılaştırmasında Python'daki **116 hedef kuralının tamamı** eşleşmiştir. Weka'da toplam **132 hedef kuralı** olup, bunların **16'sı** Python analizinin `max_len=4` sınırını aşmaktadır. Ortak kuralların hesaplanan güven ve lift değerleri uyumludur.
- En dikkat çekici birlikteliklerden biri, **50–59 yaş, pasif üyelik ve tek ürün** grubunda yaklaşık **%86,9 güven** ve **4,264 lift** değeridir. Bu ilişkiler nedensellik göstermez.

### 5.4 Ek paketler: model karmaşıklığı ve öznitelik seçimi

- **E1.1 – Budama:** En yüksek test ROC AUC **0,8402** (yaklaşık 55 yaprak); 1-SE kuralıyla **0,8362** (yaklaşık 28 yaprak).
- **E1.2 – OOB doyum:** 500 ağaçta yaklaşık **0,1387 OOB hatası** ve **0,1327 test hatası**. 150 ağaçtan sonraki kazanım sınırlıdır.
- **E1.3 – Öznitelik önemi:** Bağımsız rastgele değişkenin Gini önemi **0,09255**, test verisindeki permütasyon önemi **0,00161**; Gini öneminin sürekli değişkenlere yanlı olabileceği görülmüştür.
- **E2.1 – Seçim yöntemleri:** ROC AUC değerleri seçimsiz **0,765**, filtre **0,760**, sarmalayıcı **0,763**, gömülü **0,745**.
- **E2.2 – Kararlılık:** Gömülü yöntemde rastgele üç gürültü değişkeni **%93, %100 ve %85** oranlarında seçilmiştir. Yüksek seçim sıklığı tek başına gerçek fayda kanıtı değildir.
- **E2.3 – İstatistiksel katkı:** Filtre ve sarmalayıcı yöntemlerde seçimsiz modele göre anlamlı fark tespit edilmezken, gömülü yöntemde performans düşüşü anlamlı bulunmuştur (**p < 0,0001**).

## 6. Depo yapısı ve dosyalar

Ders yönergesine uygun olarak her projenin dosyaları kendi klasöründedir:

```text
.
├── README.md
├── proje1/
│   ├── BIL545_Proje1_Grup01.ipynb
│   ├── p1_hat.joblib
│   ├── p1_meta.json
│   ├── p1_model_tum_veri.joblib
│   ├── p1_kural_kanit.csv
│   ├── alp_dogrulama.json
│   └── sunum/
│       ├── Alp_Aydin_Ozcelik_Banka_Musteri_Kaybi.pptx
│       ├── Alp_Aydin_Ozcelik_Banka_Musteri_Kaybi.docx
│       ├── p1_sunum_kanit.json
│       └── sunum_kanitlarini_uret.py
└── proje2/                      (final teslimiyle eklenecek)
```

| Dosya | Açıklama |
|---|---|
| [`proje1/BIL545_Proje1_Grup01.ipynb`](./proje1/BIL545_Proje1_Grup01.ipynb) | Proje 1'in kodları, çalıştırma çıktıları, grafikler, okuma notları, yorumlar, Weka karşılaştırmaları ve beyanları |
| [`proje1/p1_hat.joblib`](./proje1/p1_hat.joblib) | 2.5'te oluşturulan **henüz eğitilmemiş** ön işleme + Gradyan Artırma `Pipeline`'ı; Proje 2'de ilgili veri üzerinde yeniden eğitilmek üzere |
| [`proje1/p1_model_tum_veri.joblib`](./proje1/p1_model_tum_veri.joblib) | Aynı hattın **tüm veriyle eğitilmiş** örneği; yalnızca açıklama/inceleme amacıyla; çapraz doğrulama başarımının kanıtı veya bağımsız test modeli değildir |
| [`proje1/p1_meta.json`](./proje1/p1_meta.json) | Tohum, özellikler, dışlanan sütunlar, seçilen model ve parametreleri, CV/OOF protokolleri, ROC AUC özeti, veri SHA-256 özeti ve çalışma sürümleri |
| [`proje1/p1_kural_kanit.csv`](./proje1/p1_kural_kanit.csv) | 116 hedef kuralı için toplulaştırılmış müşteri sayıları, ölçütler ve hedef kapsama oranı |
| [`proje1/alp_dogrulama.json`](./proje1/alp_dogrulama.json) | Sıralı çalıştırılan 28 kod hücresinin kontrol kaydı ve kapsamı |
| [`PowerPoint sunumu`](./proje1/sunum/Alp_Aydin_Ozcelik_Banka_Musteri_Kaybi.pptx) | Son görev dağılımındaki **Slayt 11–14** için dört slaytlık Alp bölümü; düzenlenebilir tablolar ve konuşmacı notları |
| [`Word sunumu ve konuşma notları`](./proje1/sunum/Alp_Aydin_Ozcelik_Banka_Musteri_Kaybi.docx) | Dört slaytın görselleri, yaklaşık 3–4 dakikalık düzenlenebilir konuşma metni, rakamların yorumu, yöntem gerekçeleri ve soru-cevap hazırlığı |
| [`Sunum kanıtları`](./proje1/sunum/p1_sunum_kanit.json) | 30 küp hücresi, yaş/ülke/aktiflik özetleri, Simpson taraması, üç profil ve Weka eşleşmelerinin toplulaştırılmış sayıları |
| [`Kanıtları yeniden üret`](./proje1/sunum/sunum_kanitlarini_uret.py) | Yalnızca Python standart kütüphanesiyle aynı ham CSV'den sayıları yeniden hesaplar ve kayıtlı Weka çıktısıyla 116 kuralı karşılaştırır |

`p1_meta.json` içindeki `cv_roc_auc_ort=0.8593316162707018`, `cv_roc_auc_std=0.008677503913869976`, `seed=42` ve `sklearn_surumu=1.6.1` değerleri notebook'un 2.5 bölümünde kaydedilen bilgilerle tutarlıdır. Model dosyaları aynı bölümde `joblib.dump` aracılığıyla üretilir.

**Veri paylaşımı:** `Churn_Modelling.csv`, `p1_temiz_veri.csv` ve müşteri düzeyinde `CustomerId`, `y_true`, `oof_proba` içeren `p1_oof.csv` dosyaları genel erişime açık GitHub deposuna yüklenmez. Proje 2'de ihtiyaç duyulursa kısıtlı erişimli bir ortamda tutulur. `joblib`/pickle model dosyaları yalnızca güvenilen kaynaktan yüklenmelidir; ayrıca scikit-learn sürümleri farklıysa yeniden üretmek tercih edilmelidir.

**Not:** Notebook 2.5, müşteri düzeyindeki temiz veri ve OOF dosyalarının açık depoya yüklenmemesi gerektiğini açıkça belirtir. Proje 2 (final) henüz bu depoda bulunmamaktadır; teslim edildiğinde `proje2/` klasörüne eklenecektir.

## 7. Google Colab'da çalıştırma

**[Proje 1 notebook'unu Colab'da aç](https://colab.research.google.com/github/gulsenmurat/proje1/blob/main/proje1/BIL545_Proje1_Grup01.ipynb)**

1. [Kaggle veri kümesini](https://www.kaggle.com/datasets/aakash50897/churn-modellingcsv) indirin; dosya adı `Churn_Modelling.csv` olmalıdır.
2. Notebook'u Colab'da açın. Hazırlık hücresindeki iki kurulum komutunu sırayla çalıştırın. İlk komut doğrulamada kullanılan NumPy, pandas, SciPy, scikit-learn, Matplotlib, joblib ve statsmodels sürümlerini kurar; ikinci komut `!pip install -q --no-deps mlxtend==0.25.0` şeklindedir. `mlxtend 0.25.0` paket metaverisi scikit-learn ≥1.8.0 istediğinden, kaydedilmiş modellerin 1.6.1 sürümünü korumak için otomatik bağımlılık yükseltmesi kapatılmıştır. Projede kullanılan FP-Growth işlevi bu sabitlenmiş ortamda çalıştırılarak doğrulanmıştır; mlxtend paketinin tüm işlevlerinin uyumlu olduğu iddia edilmez. Kurulum mevcut oturumdaki paketi değiştirdiyse **Çalışma Zamanı → Oturumu yeniden başlat** seçeneğini kullanın.
3. **Çalışma Zamanı → Tümünü çalıştır** deyin; yükleme ekranında `Churn_Modelling.csv` dosyasını seçin.
4. `mlxtend` sürümünün **0.25.0**, veri boyutunun **10.000 × 14**, sık öğe kümesi sayısının **7.927** ve yalnızca hedef kurallarının sayısının **116** olduğunu kontrol edin. Kod hücreleri, grafikler ve açıklama bölümleri tamamlandıktan sonra notebook'u kaydedin.
5. Proje 2 için kullanılacak model ve meta veriyi yeniden üretmek gerektiğinde 2.5 hücresinin oluşturduğu dosyalardan uygun olanları indirin. Müşteri düzeyindeki veri/OOF CSV'lerini **açık depoya** yüklemeyin.

**Çalıştırma kayıtlarının kapsamı:** Önceden kaydedilmiş Colab çıktılarında Python 3.13.18, NumPy 2.1.3, pandas 2.2.3, scikit-learn 1.6.1, SciPy 1.16.3, Matplotlib 3.10.0, mlxtend 0.25.0 ve statsmodels 0.15.0 yazmaktadır. Bu bilgi eski hücre çıktılarının kaydıdır; bütün defterin güncel ortamda yeniden çalıştırıldığı anlamına gelmez.

**2 Kasım 2026 sıralı çalıştırma:** Defterin **28 kod hücresinin tamamı**, bağımlılıkları önceden kurulmuş taze bir yerel IPython sürecinde, aynı kaynak CSV ile sırayla hatasız çalıştırıldı (169,4 saniye). Hazırlık ve Alp bölümlerindeki altı kod hücresinin çıktıları yenilendi; diğer üyelerin kaydedilmiş çıktıları korundu. Çalışma ortamı Python 3.13.9, NumPy 2.3.5, pandas 2.3.3, scikit-learn 1.6.1, SciPy 1.16.3, mlxtend 0.25.0, statsmodels 0.14.5 ve Matplotlib 3.10.6'dır. Grafik gösterimi Agg ile yapıldı. Hücre bazında durumlar, süreler ve veri dosyasının SHA-256 özeti [`alp_dogrulama.json`](./proje1/alp_dogrulama.json) dosyasındadır. Bu kayıt yerel çalıştırmanın kanıtıdır; Google Colab oturumunun veya Weka masaüstü deneylerinin yeniden çalıştırıldığı iddia edilmez. Teslim öncesi sıfırlanmış Colab oturumunda **Tümünü çalıştır** kontrolü ayrıca yapılmalıdır.

- 5×2 testinde `t=-0,505`, `p=0,6352`, ortalama hata farkı `0,0016` bulundu. Eski kayıtta `p=0,8416` idi; anlamlı fark olmadığı kararı değişmedi. Beş McNemar bölmesi için Holm düzeltmesi eklendi; en küçük düzeltilmiş p-değeri `0,2637`.
- 116 kuralın destek, güven, lift, Kulczynski ve IR değerleri müşteri maskelerinden bağımsız olarak yeniden hesaplanıp doğrulandı. Nadir kategori sıralaması ve null-invariance duyarlılık hesabı açıklandı. [`p1_kural_kanit.csv`](./proje1/p1_kural_kanit.csv) yalnızca toplulaştırılmış ölçütler ve sayılar içerir.
- Her müşteri bir kez OOF test katında yer aldı; eğitim/test ayrılığı, olasılık aralığı ve dosya satır eşleştirmeleri kontrol edildi. Meta dosyasına ham veri özeti, model parametreleri, OOF protokolü ve çalışma sürümleri eklendi. Mevcut eğitilmiş modelin tahminleri yeniden üretilen modelle kaynak veride karşılaştırıldı; en büyük mutlak olasılık farkı **0,0** bulundu. İki mevcut model dosyası korundu.
- Weka masaüstü deneyleri yeniden çalıştırılmadı. Kayıtlı Weka çıktısıyla 116 ortak kural yeniden eşleştirildi; güven ve lift farkı sıfır bulundu.


**Weka:** Weka 3.8.7 ile ZeroR, J48 ve Apriori karşılaştırmaları ayrıca yapılmıştır. Notebook'ta Weka'nın gerçek çıktı metinleri bulunmaktadır; Colab'da **Tümünü çalıştır** komutu Weka masaüstü uygulamasındaki deneyleri yeniden çalıştırmaz.

## 8. Proje 2 (final): planlanan çalışma

Proje 2 hazırlık aşamasındadır. Kapsamında kümeleme, aykırı gözlem analizi, alt grup incelemeleri, adillik/yanlılık değerlendirmeleri ve ilgili ek paketler yer almaktadır. Bu aşama için henüz deney sonucu raporlanmamıştır.

## 9. Varsayımlar ve sınırlılıklar

- Veri kümesinin özgün toplama süreci, dönem bilgisi ve hedef etiketinin gerçek banka kayıtlarıyla doğrulanması belgelenmemiştir.
- Sınıf dağılımı dengesizdir (ayrılma **%20,37**); bu nedenle tek başına accuracy yanıltıcı olabilir.
- `Balance = 0` otomatik olarak eksik veri kabul edilmemiş, alternatifleri deneysel olarak incelenmiştir.
- `Surname`, `RowNumber`, `CustomerId` ana modelin girdileri arasında değildir; aynı aileden kişilerin farklı katlara düşme olasılığı dışlanamamaktadır.
- Veri küpü ve birliktelik kuralları **ilişki** gösterir; nedensellik veya gerçek bankacılık süreçlerinde doğrudan uygulanabilirlik kanıtı değildir.
- Modellerde eşik optimizasyonu, bağımsız zamansal sınama ve müdahalenin maliyet/fayda hesabı yapılmadığından müşteri iletişim kararı otomatikleştirilmemelidir.
- Öznitelik önemleri, öznitelik seçimi sonuçları ve testlerdeki p-değerleri ilgili deney düzenine bağlıdır; sınırlılıkları ayrıntılı olarak notebook'un **Varsayım Defteri** bölümünde açıklanır.

## 10. Katkı beyanı ve sunum

| Üye | Proje 1 sorumluluk alanları | Proje 1 sunum başlığı |
|---|---|---|
| Murat Gülşen | Hazırlık, 1.1–1.3, 3.1, E1.1; veri kontrolü, analiz/yorum ve koordinasyon | Slayt 2–4 – Amaç, veri kümesi ve eksiklik analizi |
| Halil Çankaroğlu | 1.4–1.7, 3.4; kodlama/kontrol, Weka karşılaştırmaları, README ve GitHub | Slayt 5–6 – Veri sızıntısı |
| Mesut İşsever | 2.1–2.3, E1.3; model karşılaştırması, ayar ve öznitelik önemleri | Slayt 7–10 – Model karşılaştırması, model tercihi ve istatistiksel testler |
| Alp Aydın Özçelik | 2.4–2.5, 3.2–3.3; istatistiksel testler, çıktıların derlenmesi, kaynaklar/teslim; 3.1–3.4 bulgularının sunuma derlenmesi | **Slayt 11–14 – Veri küpü, yaş/ülke/aktiflik, birliktelik kuralları ve Python–Weka** |
| Melih Turgut | E1.2, E2.1–E2.3; OOB, öznitelik seçimi, kararlılık ve varsayım defteri | Slayt 15–17 – Öznitelik önemi ve seçimi |

**Son sunum dağılımı:** Yukarıdaki sunum sütunu, Alp'in paylaştığı 20 slaytlık grup sunumu görev dağılımını yansıtır. Kod/analiz katkıları kendi sütununda korunmuştur. Slayt 18–20 genel sonuçlar, akademik kaynaklar ve kapanış için ortak kapsamdır. Depodaki Alp dosyası **yalnızca Slayt 11–14 için dört slaytlık bölümdür**; grubun tamamının 20 slaytlık ana dosyası olduğu iddia edilmez.

**Alp bölümünün kapsamı:** [PowerPoint](./proje1/sunum/Alp_Aydin_Ozcelik_Banka_Musteri_Kaybi.pptx) ve [Word](./proje1/sunum/Alp_Aydin_Ozcelik_Banka_Musteri_Kaybi.docx) son dağılıma göre güncellendi:

| Slayt | Anlatılacak konu | Defterdeki kaynak |
|---|---|---|
| 11 | Olgu ve üç boyut, 30 küp hücresi, ülke × yaş özeti, roll-up | 3.1 |
| 12 | Ülke oranları, Almanya 50–59 yaş drill-down, aktiflik ve Simpson taraması | 3.1 |
| 13 | B seçeneğinin gerekçesi, ayrıklaştırma, eşikler, üç kural ve ölçütlerin yorumu | 3.2–3.3 |
| 14 | Python–Weka eşleşmesi, 16 ek kuralın nedeni, model önemleriyle örtüşme ve sınırlılıklar | 3.3–3.4 |

Word'de dört konuşma metni toplam 380 kelimedir; yaklaşık 3–4 dakika için hazırlanmıştır. Son iki sayfa hesaplar, yöntem gerekçeleri ve soru-cevap hazırlığıdır. Örneğin genel 50–59 yaş grubunda **487/869 = %56,04**, Almanya 50–59 yaş grubunda **194/277 = %70,04**; 50–59 yaş, pasif ve tek ürün profilinde **218/251 = %86,85** bulunmuştur. Bu farklı paydalar sunumda açıkça ayrılır. Bütün rakamlar aynı kaynak CSV'deki sayımlara dayanır. Kurallar ve alt grup oranları nedensellik kanıtı olarak sunulmaz.

Sunum kanıtlarını yeniden üretmek için depo kökünde çalıştırın (Python 3.10 veya üzeri, ek paket gerektirmez):

```bash
python proje1/sunum/sunum_kanitlarini_uret.py /dosyanin/yolu/Churn_Modelling.csv
```

Betik CSV'nin SHA-256 özetini `p1_meta.json` ile karşılaştırır; 30 küp hücresinin sayımlarını, üç profilin ham müşteri sayılarını ve ölçütlerini, ayrıca 116 ortak Weka kuralını doğrular. Yalnızca toplulaştırılmış JSON üretir. Weka masaüstü uygulamasını veya model eğitimini yeniden çalıştırmaz.

## 11. Yapay zekâ kullanım beyanı

- **ChatGPT (OpenAI):** Python ve Colab kodlarının hatalarının giderilmesi ve dosya kontrolünde kullanılmıştır.
- **Claude (Anthropic):** Proje 1 defterinin ve README'nin ders yönergesine göre gözden geçirilmesinde, deponun `proje1/` klasör yapısına taşınmasında ve README güncellemelerinin hazırlanmasında kullanılmıştır. Önerilen değişiklikler grup üyesi tarafından kontrol edilip onaylanmıştır.


- **Codex (OpenAI), 1 Kasım 2026:** Alp Aydın Özçelik'in talebiyle 2.4–2.5 ve 3.2–3.3 kontrollerinin geliştirilmesi, gerçek veriyle hedefli çalıştırma, kural kanıt tablosu ve bireysel Word sunum metninin hazırlanmasında kullanıldı. Kullanıcı adına kaynakları okuduğu veya sözlü savunma yaptığı iddia edilmez.
- **Codex (OpenAI), 2 Kasım 2026:** Alp'in aynı bölümlerindeki hesapların izlenebilirliğinin geliştirilmesi, tüm kod hücrelerinin yerel ortamda sıralı çalıştırılması, kullanıcı tarafından hazırlanan sunumun veri/kod çıktılarıyla düzeltilmesi ve Word dönüşümünde kullanıldı.
- **Codex (OpenAI), son sunum dağılımı güncellemesi:** Slayt 11–14 için 3.1–3.4 bulgularının derlenmesinde, ham CSV'den toplulaştırılmış küp ve profil sayımlarının yeniden kontrolünde, Weka eşleşmelerinin doğrulanmasında ve Word konuşma/soru-cevap metninin hazırlanmasında kullanıldı. Mevcut kod/analiz sahiplikleri korundu.

## 12. Kaynaklar

### Veri kaynağı

- Aggrawal, A. (t.y.). *Churn_Modelling.csv*. Kaggle. https://www.kaggle.com/datasets/aakash50897/churn-modellingcsv (Erişim: 10.10.2026; lisans: **Unknown**).

### Proje 1'de kullanılan akademik kaynaklar

- Kaufman, S., Rosset, S., Perlich, C. ve Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. *ACM Transactions on Knowledge Discovery from Data*, 6(4), Article 15. https://doi.org/10.1145/2382577.2382579
- Dietterich, T. G. (1998). Approximate statistical tests for comparing supervised classification learning algorithms. *Neural Computation*, 10(7), 1895–1923. https://doi.org/10.1162/089976698300017197
- Han, J., Kamber, M. ve Pei, J. (2012). *Data Mining: Concepts and Techniques* (3. baskı). Morgan Kaufmann.
- Wu, T., Chen, Y. ve Han, J. (2010). Re-examination of interestingness measures in pattern mining: A unified framework. *Data Mining and Knowledge Discovery*, 21(3), 371–397. https://doi.org/10.1007/s10618-009-0161-2
- Meinshausen, N. ve Bühlmann, P. (2010). Stability selection. *Journal of the Royal Statistical Society: Series B*, 72(4), 417–473. https://doi.org/10.1111/j.1467-9868.2010.00740.x
- Pedregosa, F. ve diğerleri (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830. https://www.jmlr.org/papers/v12/pedregosa11a.html
- Raschka, S. (2018). MLxtend: Providing machine learning and data science utilities and extensions to Python's scientific computing stack. *Journal of Open Source Software*, 3(24), 638. https://doi.org/10.21105/joss.00638
- Hall, M., Frank, E., Holmes, G., Pfahringer, B., Reutemann, P. ve Witten, I. H. (2009). The WEKA data mining software: An update. *ACM SIGKDD Explorations Newsletter*, 11(1), 10–18. https://doi.org/10.1145/1656274.1656278
