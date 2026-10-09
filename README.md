# Banka müşterisi kaybı: hangi müşteriler ayrılma riski taşıyor?

Depo: https://github.com/gulsenmurat/proje1

> BIL545 · Veri Madenciliğinde İleri Konular · 2026–2027 Güz · Üsküdar Üniversitesi
> Bu dosya grubun GitHub deposunun ana sayfasıdır. Köşeli parantez içindeki yerleri doldurun ve her proje tesliminde güncelleyin.

## Grup

| Üye | Öğrenci no |
|---|---|
| Murat Gülşen | 264309500 |
| Halil Çankaroğlu | 264329016 |
| Mesut İşsever | 264329015 |
| Alp Aydın Özçelik | 244312033 |
| Melih Turgut | 244309019 |

- **Grup adı:** Grup 01
- **İletişim sorumlusu:** Murat Gülşen, murat.gulsen@st.uskudar.edu.tr
- **Grup tipi:** 5 kişi (+ Ek paket 1 ve 2)
- **Seçilen konu:** 9.28 — Banka müşterisi kaybı

## Soru

[Taslak, ekip kesinleştirsin] Bankanın elde tutma ekibi, hangi müşterilerin ayrılma riski taşıdığını önceden belirleyip önce hangilerine ulaşacağına karar verebilir mi?

## Veri

| | |
|---|---|
| **Veri kümesi** | Bank Customer Churn (`Churn_Modelling.csv`) |
| **Kaynak** | [bağlantı] |
| **Lisans** | [kaynak sayfasından doğrulayın] |
| **Boyut** | ≈10.000 müşteri × 14 sütun [doğrulayın] |
| **Hedef değişken** | `Exited`: müşteri bankadan ayrıldı mı (1 = ayrıldı) [anlamını kaynaktan doğrulayın] |

**Verinin indirilmesi:** Veri bu depoda yoktur. [Kaynak bağlantısından `Churn_Modelling.csv` dosyasını indirin.] Defterler Colab'da ilk çalıştırmada dosya seçtirir; dosyayı o pencereden yükleyin.

## Depo yapısı

```
.
├── README.md
├── proje1/
│   └── BIL545_Proje1_Grup01.ipynb
└── proje2/
    └── BIL545_Proje2_Grup01.ipynb
```

## Çalıştırma

1. Defteri Colab'da açın: [Proje 1](https://colab.research.google.com/github/gulsenmurat/proje1/blob/main/proje1/BIL545_Proje1_Grup01.ipynb) · [Proje 2](https://colab.research.google.com/github/gulsenmurat/proje1/blob/main/proje2/BIL545_Proje2_Grup01.ipynb) *(dal adı `main` varsayıldı; farklıysa düzeltin)*
2. Veriyi yukarıdaki adımlarla yükleyin.
3. **Çalışma Zamanı → Tümünü çalıştır.** Kütüphane sürümleri defterin ilk hücresinde yazdırılır.

## Sonuç özeti

### Proje 1 (vize)
- **Baseline:** [ölçüt: ortalama ± std]
- **En iyi model:** [model; ölçüt: ortalama ± std]
- **Sızıntı deneyi:** [yanlış kurulum ve doğru kurulum skorları; tek cümlelik yorum]
- **Önemli bulgular:** [2–3 madde]

### Proje 2 (final)
- **Proje 1'den düzeltilenler:** [kısa liste]
- **Bölüm bulguları:** [kümeleme, aykırı gözlem, alt grup analizi için birer cümle; Ek paket 1 ve 2 için de]
- **Sınırlılıklar:** [2–3 madde]

## Katkı beyanı

<!-- TASLAK: Aşağıdaki dağılım planlanan işleri gösterir. Teslimden önce GitHub commit geçmişine bakarak gerçekte yapılanlara göre güncelleyin; iş türlerini (kod, analiz, yorum, sunum hazırlığı) ve ürünü yazın. -->

| Üye | Çalıştığı alt başlıklar ve işler | Sunumda anlattığı alt başlık |
|---|---|---|
| Murat Gülşen | P1: Hazırlık, 1.1, 1.2, 1.3, 3.1, E1.1. P2: 1.1, 1.2, E1.1, Proje 1'den devralınanlar. İletişim sorumlusu. [kod / analiz / yorum / sunum hazırlığı ayrıntısı] | P1: 1.3 · P2: 1.2 |
| Halil Çankaroğlu | P1: 1.4, 1.5, 1.6, 1.7, 3.4, README ve GitHub, Weka. P2: 1.3, 1.4, E1.2, Sonuç ve sınırlılıklar, Varsayım defteri derlemesi. [ayrıntı] | P1: 1.5 · P2: 1.4 |
| Mesut İşsever | P1: 2.1, 2.2, 2.3, E1.3. P2: 2.1, 2.2, 2.3, README ve GitHub. [ayrıntı] | P1: 2.1 · P2: 2.2 |
| Alp Aydın Özçelik | P1: 2.4, 2.5, 3.2, 3.3, katkı/YZ/kaynaklar derlemesi, teslim kontrolü. P2: 3.0, 3.1, 3.2, E1.3, katkı/YZ/kaynaklar derlemesi, teslim kontrolü. [ayrıntı] | P1: 3.3 · P2: 3.1 |
| Melih Turgut | P1: E1.2, E2.1, E2.2, E2.3, Varsayım defteri derlemesi. P2: E2.0, E2.1, Model kartı, Tez ve araştırma yönleri. [ayrıntı] | P1: E2.2 · P2: E2.1 |

## Yapay zekâ beyanı

<!-- TASLAK: gerçeğe göre düzeltin. -->
Claude (Anthropic) ile çalışma planı, Proje 1 defterinin kod iskeleti ve yorum yönlendirmelerinin taslağı hazırlandı; gerçek veri üzerindeki çıktılar, yorumlar, gerekçeler ve okuma notları üyeler tarafından yazıldı [doğrulayın]. [Başka araç kullanıldıysa araç adı, aşama ve amaç.]

## Kaynaklar

- [Veri kümesinin kaynağı: ad, bağlantı, erişim tarihi, lisans]
- Kaufman, S., Rosset, S., Perlich, C. ve Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. *ACM TKDD*, 6(4).
- Dietterich, T. G. (1998). Approximate statistical tests for comparing supervised classification learning algorithms. *Neural Computation*, 10(7), 1895–1923.
- Wu, T., Chen, Y. ve Han, J. (2010). Re-examination of interestingness measures in pattern mining: A unified framework. *Data Mining and Knowledge Discovery*, 21(3), 371–397.
- Meinshausen, N. ve Bühlmann, P. (2010). Stability selection. *JRSS: Series B*, 72(4), 417–473.
- Ben-Hur, A., Elisseeff, A. ve Guyon, I. (2002). A stability based method for discovering structure in clustered data. *Pacific Symposium on Biocomputing*, 7, 6–17.
- Liu, F. T., Ting, K. M. ve Zhou, Z.-H. (2008). Isolation forest. *IEEE ICDM*, 413–422.
- Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K. ve Galstyan, A. (2021). A survey on bias and fairness in machine learning. *ACM Computing Surveys*, 54(6), 1–35.
- [Diğer kaynaklar]
