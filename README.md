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
| **Erişim tarihi** | 10 Ekim 2026 |
| **Lisans** | **Unknown / belirtilmemiş.** Açık yeniden dağıtım izni varsayılmaz. |
| **Boyut** | **10.000 müşteri × 14 sütun** |
| **Hedef** | `Exited`: **1 = bankadan ayrıldı**, **0 = bankada kaldı** |
| **Sınıf dağılımı** | 2.037 ayrılan (**%20,37**), 7.963 kalan (**%79,63**) |
| **Analizde kullanılan özellikler** | CreditScore, Age, Tenure, Balance, NumOfProducts, EstimatedSalary, HasCrCard, IsActiveMember, Geography, Gender |
| **Ana modele alınmayan sütunlar** | `RowNumber`, `CustomerId`, `Surname` |

**Veri dosyası bu GitHub deposunda yayımlanmamaktadır.** Projeyi çalıştırmak için Kaggle bağlantısından `Churn_Modelling.csv` dosyasını indirin. Google Colab defteri dosyayı ilk veri yükleme hücresinde sizden ister. `CustomerId` yalnızca gerekli satır eşleştirmelerinde tutulur; tahmin özelliği olarak kullanılmaz.

Verinin toplanma zamanı, ilk üreticisi ve örneklemin temsiliyeti yeterince belgelenmediğinden sonuçların bütün banka müşterilerine genellenebileceği varsayılmaz.

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

**Nihai tercih:** Gradyan Artırma (*HistGradientBoostingClassifier*). ROC AUC bakımından Rastgele Orman'a çok yakınken F1, Average Precision ve Balanced Accuracy (0,726) açısından daha iyi sonuç vermiştir. **Bu fark istatistiksel olarak kanıtlanmış bir üstünlük değildir:** 5×2cv t-testinde `p = 0,8416` elde edilmiştir.

Kaydedilen `p1_hat.joblib`, **2.1 bölümündeki varsayılan parametreli** Gradyan Artırma hattıdır; 2.3'te yapılan optimizasyonun sonucu değildir. GridSearchCV için 0,8666 ve iç içe çapraz doğrulama için yaklaşık 0,866 ± 0,007 ROC AUC ayrıca raporlanmıştır.

### 5.2 Veri sızıntısının etkisi

- **Yanlış kurulum (hedef kodlama + seçim tüm veri üzerinde):** ROC AUC **0,898 ± 0,006**.
- **Doğru kurulum (işlemler çapraz doğrulama içinde):** ROC AUC **0,775 ± 0,012**.
- **Yorum:** Yaklaşık **0,123 ROC AUC puanlık yapay iyileşme**, veri sızıntısının başarıyı olduğundan yüksek gösterebildiğini ortaya koyar. Ana analizlerde ön işleme adımları `Pipeline` içinde yapılır.

### 5.3 Veri küpü ve birliktelik kuralları

- Genel müşteri ayrılma oranı **%20,37**; ayrılma oranları yaş, ülke ve aktif üyelik durumuna göre farklılaşır.
- FP-Growth ile **7.927 sık öğe kümesi**, **26.657 birliktelik kuralı** ve `Exited=Ayrildi` sonucuna yönelik **116 kural** elde edilmiştir.
- **Weka 3.8.7 Apriori** karşılaştırmasında Python'daki **116 hedef kuralının tamamı** eşleşmiş; Weka'da daha uzun öncüllere sahip **16 ek hedef kuralı** bulunmuştur. Ortak kuralların hesaplanan güven ve lift değerleri uyumludur.
- En dikkat çekici birlikteliklerden biri, **50–59 yaş, pasif üyelik ve tek ürün** grubunda yaklaşık **%86,9 güven** ve **4,264 lift** değeridir. Bu ilişkiler nedensellik göstermez.

### 5.4 Ek paketler: model karmaşıklığı ve öznitelik seçimi

- **E1.1 – Budama:** En yüksek test ROC AUC **0,8402** (yaklaşık 55 yaprak); 1-SE kuralıyla **0,8362** (yaklaşık 28 yaprak).
- **E1.2 – OOB doyum:** 500 ağaçta yaklaşık **0,1387 OOB hatası** ve **0,1327 test hatası**. 150 ağaçtan sonraki kazanım sınırlıdır.
- **E1.3 – Öznitelik önemi:** Bağımsız rastgele değişkenin Gini önemi **0,09255**, test verisindeki permütasyon önemi **0,00161**; Gini öneminin sürekli değişkenlere yanlı olabileceği görülmüştür.
- **E2.1 – Seçim yöntemleri:** ROC AUC değerleri seçimsiz **0,765**, filtre **0,760**, sarmalayıcı **0,763**, gömülü **0,745**.
- **E2.2 – Kararlılık:** Gömülü yöntemde rastgele üç gürültü değişkeni **%93, %100 ve %85** oranlarında seçilmiştir. Yüksek seçim sıklığı tek başına gerçek fayda kanıtı değildir.
- **E2.3 – İstatistiksel katkı:** Filtre ve sarmalayıcı yöntemlerde seçimsiz modele göre anlamlı fark tespit edilmezken, gömülü yöntemde performans düşüşü anlamlı bulunmuştur (**p < 0,0001**).

## 6. Depo yapısı ve dosyalar

```text
.
├── README.md
├── proje1/
│   ├── BIL545_Proje1_Grup01.ipynb
│   ├── p1_hat.joblib
│   ├── p1_model_tum_veri.joblib
│   └── p1_meta.json
└── proje2/
```

| Dosya | Açıklama |
|---|---|
| `proje1/BIL545_Proje1_Grup01.ipynb` | Proje 1'in kodları, tabloları, grafikler, okuma notları, yorumlar ve beyanları |
| `proje1/p1_hat.joblib` | Proje 2'de yeniden eğitilebilecek, henüz eğitilmemiş model Pipeline'ı |
| `proje1/p1_model_tum_veri.joblib` | Yalnızca açıklama/inceleme amaçlı tüm veriyle eğitilmiş model; başarım raporlamasında kullanılmaz |
| `proje1/p1_meta.json` | Özellikler, dışlanan sütunlar, seçilen model, tohum, çapraz doğrulama protokolü ve sürüm bilgisi |

`Churn_Modelling.csv`, `p1_temiz_veri.csv` ve müşteri düzeyinde `CustomerId`, `y_true`, `oof_proba` içeren `p1_oof.csv` dosyaları **genel erişime açık GitHub deposuna yüklenmez**. Proje 2 için gerekli özel kopyalar grup erişimi sınırlandırılmış bir ortamda saklanır.

## 7. Google Colab'da çalıştırma

**[Proje 1 notebook'unu Colab'da aç](https://colab.research.google.com/github/gulsenmurat/proje1/blob/main/proje1/BIL545_Proje1_Grup01.ipynb)**  
1. [Kaggle veri kümesini](https://www.kaggle.com/datasets/aakash50897/churn-modellingcsv) indirin; dosya adı **`Churn_Modelling.csv`** olmalıdır.
2. Notebook'u Google Colab ortamında açın.
3. **Çalışma Zamanı → Tümünü çalıştır** komutunu kullanın.
4. Dosya yükleme ekranında `Churn_Modelling.csv` dosyasını seçin.

**Kullanılan ortam (notebook'un kaydettiği sürümler):** Python 3.13.16, NumPy 2.1.3, pandas 2.2.3, scikit-learn 1.6.1, SciPy 1.16.3, Matplotlib 3.10.0 ve statsmodels 0.15.0. Notebook ayrıca `mlxtend` ve `joblib` kullanır; gerekli kurulumlar notebook içinde yer alır veya Colab ortamında hazır bulunabilir.

**Weka:** Weka 3.8.7 ile ZeroR, J48 ve Apriori karşılaştırmaları ayrıca yapılmıştır. Notebook'ta Weka'nın gerçek çıktı metinleri bulunmaktadır; tüm notebook'u tekrar çalıştırmak Weka'nın masaüstü uygulamasını Colab içinde otomatik çalıştırmaz.

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
| Murat Gülşen | Hazırlık, 1.1–1.3, 3.1, E1.1; veri kontrolü, analiz/yorum ve koordinasyon | 1.3 – Eksiklik Analizi |
| Halil Çankaroğlu | 1.4–1.7, 3.4; kodlama/kontrol, Weka karşılaştırmaları, README ve GitHub | 1.5 – Veri Sızıntısı |
| Mesut İşsever | 2.1–2.3, E1.3; model karşılaştırması, ayar ve öznitelik önemleri | 2.1 – Model Karşılaştırması |
| Alp Aydın Özçelik | 2.4–2.5, 3.2–3.3; istatistiksel testler, çıktıların derlenmesi, kaynaklar/teslim | 3.3 – Birliktelik Kuralları |
| Melih Turgut | E1.2, E2.1–E2.3; OOB, öznitelik seçimi, kararlılık ve varsayım defteri | E2.2 – Kararlılık Seçimi |

## 11. Yapay zekâ kullanım beyanı

- **Claude (Anthropic):** Çalışma planı ve kod iskeleti hazırlığında çok az düzeyde yardımcı araç olarak kullanılmıştır.
- **ChatGPT (OpenAI):** Bazı Python hatalarının giderilmesi ve metinlerin düzenlenmesinde çok az düzeyde yardımcı araç olarak kullanılmıştır.

Yapay zekâ araçlarından kod, analiz ve akademik metin oluşturma aşamalarında destek alınmıştır. Nihai deney sonuçları notebook çıktılarında kayıtlıdır; çalışmanın akademik sorumluluğu grup üyelerine aittir.

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
