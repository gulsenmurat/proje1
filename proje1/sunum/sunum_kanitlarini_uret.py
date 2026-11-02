"""Slayt 11–14 için toplulaştırılmış kanıtları aynı ham CSV'den yeniden üret.

Kullanım: python proje1/sunum/sunum_kanitlarini_uret.py /yol/Churn_Modelling.csv
Yalnızca Python standart kütüphanesini kullanır. Ham müşteri kayıtlarını yazmaz.
Weka'yı çalıştırmaz; deftere gömülü Apriori çıktı metnini ayrıştırır.
"""
import argparse
import ast
import csv
import hashlib
import json
import math
import re
from collections import defaultdict
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("p1_sunum_kanit.json"))
    args = parser.parse_args()
    project = Path(__file__).resolve().parent.parent
    digest = hashlib.sha256(args.csv_path.read_bytes()).hexdigest()
    meta = json.loads((project / "p1_meta.json").read_text())
    assert digest == meta["veri_sha256"], "CSV, doğrulanmış kaynakla aynı değil."
    with args.csv_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    assert len(fields) == 14 and len(rows) == 10000

    def age(row):
        value = int(row["Age"])
        for end, label in [(29, "18–29"), (39, "30–39"),
                           (49, "40–49"), (59, "50–59"), (100, "60+")]:
            if value <= end:
                return label
        raise ValueError("Yaş aralık dışında")

    dimensions = {
        "ulke": lambda r: r["Geography"],
        "cinsiyet": lambda r: r["Gender"],
        "yas": age,
        "aktiflik": lambda r: "Aktif" if r["IsActiveMember"] == "1" else "Pasif",
        "bakiye": lambda r: "Sifir" if float(r["Balance"]) == 0 else "Bakiyeli",
        "kart": lambda r: r["HasCrCard"],
        "urun": lambda r: str(min(int(r["NumOfProducts"]), 3)),
    }

    def group(names, records=None):
        counts = defaultdict(lambda: [0, 0])
        for row in rows if records is None else records:
            key = tuple(dimensions[name](row) for name in names)
            counts[key][0] += 1
            counts[key][1] += int(row["Exited"])
        return [dict(zip(names, key), musteri=n, ayrilan=e, oran=e/n)
                for key, (n, e) in sorted(counts.items())]

    total = group([])[0]
    assert total == {"musteri": 10000, "ayrilan": 2037, "oran": .2037}
    cube = group(["ulke", "cinsiyet", "yas"])
    assert len(cube) == 30
    assert sum(v["musteri"] for v in cube) == total["musteri"]
    assert sum(v["ayrilan"] for v in cube) == total["ayrilan"]

    # Defterdeki 3.1 taramasının yön karşılaştırması, ham sayılardan bağımsız kontrol.
    simpson = []
    for binary in ["cinsiyet", "aktiflik", "bakiye", "kart"]:
        levels = sorted({dimensions[binary](r) for r in rows})
        overall = {v[binary]: v["oran"] for v in group([binary])}
        overall_gap = overall[levels[1]] - overall[levels[0]]
        for layer in ["ulke", "yas", "urun"]:
            grouped = group([layer, binary])
            layer_values = sorted({v[layer] for v in grouped})
            reversed_layers = []
            for level in layer_values:
                rates = {v[binary]: v["oran"] for v in grouped if v[layer] == level}
                if set(rates) != set(levels):
                    continue
                gap = rates[levels[1]] - rates[levels[0]]
                if math.copysign(1, gap) != math.copysign(1, overall_gap):
                    reversed_layers.append(level)
            simpson.append({"ikili": binary, "katman": layer,
                            "fark_tanimi": levels[1]+" − "+levels[0],
                            "toplam_fark": overall_gap,
                            "ters_katmanlar": reversed_layers,
                            "katman_sayisi": len(layer_values),
                            "tum_katmanlarda_ters": len(reversed_layers) == len(layer_values)})

    notebook = json.loads((project / "BIL545_Proje1_Grup01.ipynb").read_text())
    weka_text = None
    weka_code = None
    for cell in notebook["cells"]:
        source = "".join(cell.get("source", []))
        if cell["cell_type"] == "code" and "weka_apriori =" in source:
            weka_code = source
            for statement in ast.parse(source).body:
                if isinstance(statement, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "weka_apriori"
                    for t in statement.targets
                ):
                    weka_text = ast.literal_eval(statement.value)
    assert isinstance(weka_text, str), "Kayıtlı Weka çıktısı bulunamadı."
    pattern = re.compile(r"^\s*\d+\.\s+(.*?)\s+(\d+)\s+==>\s+(.*?)\s+(\d+)\s+conf:\(([\d.]+)\)")
    weka = {}
    all_weka_count = 0
    for line in weka_text.splitlines():
        match = pattern.match(line)
        if not match:
            continue
        all_weka_count += 1
        if match.group(3).strip() == "Exited=Ayrildi":
            key = " & ".join(sorted(match.group(1).split()))
            assert key not in weka
            weka[key] = {"oncul": int(match.group(2)),
                         "birlikte": int(match.group(4)),
                         "oncul_oge_sayisi": len(match.group(1).split())}

    with (project / "p1_kural_kanit.csv").open(newline="") as f:
        python_rules = list(csv.DictReader(f))
    python_keys = {v["kural"] for v in python_rules}
    common = python_keys & weka.keys()
    extras = weka.keys() - python_keys
    assert len(python_keys) == len(common) == 116
    assert all_weka_count == 4731 and len(weka) == 132 and len(extras) == 16
    assert all(weka[key]["oncul_oge_sayisi"] == 4 for key in extras)
    confidence_diff = []
    lift_diff = []
    for rule in python_rules:
        counterpart = weka[rule["kural"]]
        assert int(rule["oncul_musteri"]) == counterpart["oncul"]
        assert int(rule["ayrilan_musteri"]) == counterpart["birlikte"]
        confidence = counterpart["birlikte"] / counterpart["oncul"]
        confidence_diff.append(abs(float(rule["confidence"]) - confidence))
        lift_diff.append(abs(float(rule["lift"]) - confidence/total["oran"]))
    assert max(confidence_diff) < 1e-12 and max(lift_diff) < 1e-12

    profiles = [
        ("50–59 pasif tek ürün", "Aktiflik=pasif & Urun=1 & Yas=50_59",
         lambda r: age(r) == "50–59" and r["IsActiveMember"] == "0" and r["NumOfProducts"] == "1"),
        ("3+ ürün", "Urun=3_ve_uzeri", lambda r: int(r["NumOfProducts"]) >= 3),
        ("50–59 pasif", "Aktiflik=pasif & Yas=50_59",
         lambda r: age(r) == "50–59" and r["IsActiveMember"] == "0"),
    ]
    verified_profiles = []
    for label, key, predicate in profiles:
        subset = [r for r in rows if predicate(r)]
        a, ab, b, n = len(subset), sum(int(r["Exited"]) for r in subset), 2037, 10000
        values = {"support": ab/n, "confidence": ab/a, "lift": ab*n/(a*b),
                  "kulc": .5*(ab/a+ab/b), "IR": abs(a-b)/(a+b-ab), "hedef_kapsama": ab/b}
        rule = next(v for v in python_rules if v["kural"] == key)
        assert (a, ab) == (int(rule["oncul_musteri"]), int(rule["ayrilan_musteri"]))
        for name, value in values.items():
            assert math.isclose(float(rule[name]), value, abs_tol=1e-12)
        verified_profiles.append(dict(profil=label, kural=key, oncul=a, ayrilan=ab,
                                      lift_sira=float(rule["lift_sira"]),
                                      kulc_sira=float(rule["kulc_sira"]), **values))

    result = {
        "veri_sha256": digest, "sutunlar": fields,
        "kod_kaynagi": "BIL545_Proje1_Grup01.ipynb 3.1–3.4",
        "weka_kod_sha256": hashlib.sha256(weka_code.encode()).hexdigest(),
        "genel": total, "kup_30_hucre": cube,
        "ulke_yas": group(["ulke", "yas"]), "yas": group(["yas"]),
        "ulke": group(["ulke"]), "aktiflik": group(["aktiflik"]),
        "cinsiyet": group(["cinsiyet"]),
        "almanya_cinsiyet_yas": group(["cinsiyet", "yas"], [r for r in rows if r["Geography"] == "Germany"]),
        "simpson_taramasi": simpson, "uc_kural": verified_profiles,
        "weka": {"toplam_kural": all_weka_count, "hedef_kural": len(weka),
                 "python_hedef_kural": len(python_keys), "ortak": len(common),
                 "yalniz_python": len(python_keys - weka.keys()), "yalniz_weka": len(extras),
                 "ek_kurallarin_oncul_oge_sayisi": 4,
                 "maks_guven_farki": max(confidence_diff), "maks_lift_farki": max(lift_diff),
                 "kapsam": "Kayıtlı Weka 3.8.7 Apriori çıktısı ayrıştırıldı; masaüstü deneyi yeniden çalıştırılmadı."},
    }
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n")
    print(f"Doğrulandı: 30 küp hücresi, 3 ham veri profili ve 116 ortak Python/Weka kuralı. Çıktı: {args.output}")


if __name__ == "__main__":
    main()
