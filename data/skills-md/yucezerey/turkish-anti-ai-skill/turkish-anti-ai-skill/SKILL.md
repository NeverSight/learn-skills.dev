---
name: turkish-anti-ai-skill
description: Türkçe metinlerdeki yapay zeka izlerini (AI slop, translationese, çeviri kokan cümle mimarisi, -mektedir/-dır şişmesi, yapay bağlaçlar ve TDK uyumsuzlukları) temizler; sıfırdan doğal, insani ve akıcı Türkçe metin üretir veya mevcut metinleri onarır. Kullanıcı Türkçe bir metni "insanlaştır", "humanize et", "AI kokusunu sil", "doğal Türkçeye çevir", "daha insani/akıcı yaz" dediğinde veya Türkçe blog, makale, kurumsal yazı, sosyal medya içeriği ve teknik doküman yazarken/düzenlerken bu yeteneği kullan.
license: MIT
metadata:
  author: yucezerey
  version: "1.0.0"
---

# Turkish Anti-AI Skill (Doğal Türkçe ve Anti-Slop Mimari Kılavuzu)

Bu yetenek, Büyük Dil Modellerinin (LLM) İngilizce ağırlıklı eğitim verisi ve RLHF süreçleri yüzünden ürettiği "Yapay Zeka Türkçesini" (kelimeleri Türkçe ama cümle iskeleti İngilizce olan, mekanik, şişirilmiş ve tekdüze metinleri) doğal, nefes alan ve TDK kurallarına tam uyumlu insan Türkçesine dönüştürür.

Detaylı dilbilimi kuralları ve sözlük tabloları için bu dizindeki referans dosyalarını oku:

- `references/sentaks-ve-morfoloji.md`: Sola dallanma, ulaç sistemi, vurgu yuvası, `-DIr/-mAktAdIr` dozajı, zamir düşürme ve kof yardımcı fiil dönüşümleri.
- `references/ai-turkcesi-sozlugu.md`: Tier-1 (kesin AI ifşaları), Tier-2 (bürokratik bağlaçlar) ve Tier-3 (SaaS/pazarlama çeviri kalıpları) sözlüğü.
- `references/tdk-ve-noktalama.md`: 5 mutlak noktalama yasağı, TDK birleşik/ayrı kelimeler ve yabancı teknik terimlerin Türkçe okunuşa göre ek uyumu.
- `references/register-ve-ornekler.md`: 5 register × 9 üslup boyutu matrisi ve uçtan uca Before/After dönüşüm çiftleri.

## Temel İlkeler

1. **Kelime Değiştirmek Yetmez, Cümle Mimarisini Yeniden Kur:** Türkçe sondan eklemeli (agglutinative) ve sola dallanan (left-branching) bir dildir. İngilizcenin sağa dallanan SVO iskeletini koruyarak yalnızca eşanlamlı kelime değiştirmek AI etkisini silmez. Önce cümle mimarisini onar.
2. **Olgusal Sadakat Kilidi (Anti-Fabrication Lock):** Onarım (`rewrite`) modunda kaynak metinde bulunmayan hiçbir sayı, tarih, özel isim, kişisel anekdot veya nedensellik bağı uydurma. "İnsan gibi görünmek" için yalan söyleme, yalnızca mevcut bilginin ifade edilişini doğallaştır.
3. **Register (Bağlam) Dozajı:** Her metin aynı tonda yazılmaz. Akademik makalede `-mAktAdIr` eki doğalken, blog veya kurumsal bültende yapay durur. İşleme başlamadan önce metnin register'ını belirle.
4. **Sınırları Olan Kurallar:** Sınırı olmayan her kural yeni bir yapay tike dönüşür. Devrik cümle, söylem parçacığı (`işte`, `zaten`, `hani`) veya kısa cümle kullanımını kotaya bağlama ve silme testinden geçmeyen hiçbir üslup aracını metinde tutma.

## Çalışma Modları

Kullanıcı isteğine göre aşağıdaki üç moddan birini seç:

- **Onarım Modu (`rewrite` - Varsayılan):** Mevcut bir Türkçe metni veya çeviriyi alır, olgusal sadakati %100 koruyarak AI kalıplarını temizler ve cümle mimarisini Türkçeleştirir.
- **Üretim Modu (`write`):** Verilen bir konu veya taslaktan sıfırdan Türkçe metin üretir. Kompozisyon ve cümle kararlarını ilk cümleden itibaren İngilizce düşünmeden, doğrudan Türkçe kurar.
- **Denetim Modu (`audit`):** Metni yeniden yazmaz; metindeki P0 (Kesin AI İfşası), P1 (Yapısal Çeviri Kokusu) ve P2 (Ritim/Noktalama Kusuru) sinyallerini alıntılayarak raporlar.

## Adım Adım İş Akışı (Mark -> Draft -> Audit -> Deletion Test)

### Adım 1: Register ve Üslup Kalibrasyonu

Kullanıcı kendi yazısından örnek verdiyse (few-shot referans), cümle uzunluğu, bağlaç tercihi ve ton açısından kullanıcının örneğini en üst kural kabul et. Örnek yoksa metni şu 5 register'dan birine ata (`references/register-ve-ornekler.md`):

| Register | Kompozisyon Müdahalesi | Cümle Mimarisi | `-DIr` / `-mAktAdIr` | Devrik Cümle ve Parçacık |
| :--- | :--- | :--- | :--- | :--- |
| **Blog / Deneme / Sosyal Medya** | Tam (Sahne ile başla, ilan etme) | Tam (Ulaç, özne düşürme, `-mIş`) | Tamamen sil | Serbest (400 kelimede maks. 2-3 devrik) |
| **Teknik Doküman / Mühendislik** | Orta (Doğrudan probleme gir) | Tam (Sola dallanma, ulaç, net yüklem) | Sil (Geniş zaman `-Ir/-Ar` kullan) | Devrik yok, parçacık çok az |
| **Kurumsal / İş İletişimi / SaaS** | Orta (Tezi ilk cümlede söyle) | Tam (Edilgeni etkene çevir, kof fiili at) | Yalnızca resmi tanımlarda | Devrik yok, doğal ve doğrudan |
| **Akademik / Resmi / Hukuki** | Kapalı (Belge iskeletini koru) | Sola dallanma, ulaç ve vurgu yuvası | Korunur (100 kelimede 1-3 arası) | Kesinlikle yasak |
| **Edebi / Anlatı** | Tam (Ritim ve imge odaklı) | Tam (Nefes uzunluğu varyasyonu yüksek) | Tamamen sil | Anlatı ritmine göre doğal |

### Adım 2: Üç Katmanlı Dönüşüm

#### Katman 1: Kompozisyon ve Retorik Kalıplar (P0 Sinyalleri)

- **Sahneleme Yerine Doğrudan Söyle:** "Bu yazıda X konusunu ele alacağız", "Günümüzün hızla değişen dünyasında" gibi sahneleme girişlerini silip konunun kendisine gir.
- **Negatif Paralellikleri Kaldır:** "Sadece X değil, aynı zamanda Y", "Bu bir A değil, bir B'dir" ve "X ile değil, Y ile" gibi tüm negatif paralellik kalıplarını olumlu ve net bir yargıya dönüştür (detaylar: `references/ai-turkcesi-sozlugu.md`).
- **Tek Satırlık Dramatik Kapanışları ve Özet Kuyruklarını Sil:** Paragraf sonlarındaki "İşte asıl fark burada ortaya çıkıyor.", "Sonuç olarak X'in önemi yadsınamaz." gibi ders veren kapanışları kes.
- **Üçlü Liste (Rule of Three) Otomatizmini Kır:** Fikirleri sürekli üçlü sıfat veya üçlü örnek grupları ("hızlı, güvenilir ve ölçeklenebilir") halinde dizme; gerçekten kaç öğe varsa o kadarını sırala.
- **Kalın Etiketli Madde İmlerini (`**Başlık:** Açıklama`) Çöz:** Gerekmedikçe her paragrafı madde imine çevirme. Liste şartsa kalın etiket + iki nokta şablonu yerine yalın cümle kur.

#### Katman 2: Türkçe Cümle Mimarisi ve Sentaks (P1 Sinyalleri)

Detaylı kurallar ve örnekler için `references/sentaks-ve-morfoloji.md` dosyasını oku:

- **Sola Dallanma (Left-Branching):** Niteleyicileri ve yan cümleleri baş ismin arkasına veya Hint-Avrupa tipi `ki` bağlacıyla cümle sonuna takma, sıfat-fiillerle (`-An`, `-DIk`, `-AcAk`) ismin önüne al (*"Bir sistem kurduk, bu sistem verileri tarıyor"* -> *"Verileri tarayan bir sistem kurduk"*).
- **Refleks `ve` Yerine Ulaç (Zarf-Fiil) Sistemi:** Sıralı eylemleri mekanik `ve` veya `ve sonra` ile bağlamak yerine Türkçenin ulaç eklerini (`-Ip`, `-IncA`, `-dIkçA`, `-ArAk`, `-mAdAn`) kullan (*"Veriyi çektik ve işledik"* -> *"Veriyi çekip işledik"*).
- **`-DIr` ve `-mAktAdIr` Salgınını Durdur:** İngilizcedeki `is/are` koşulacını her cümlede `-DIr` veya `-mektedir` olarak çevirme. Akademik/hukuki register dışında *"Bu yöntem etkilidir ve hız sağlamaktadır"* yerine *"Bu yöntem etkili, sistemi de hızlandırıyor"* de.
- **Vurgu Yuvasını (Yüklem Önü) Kullan:** Türkçede vurgu kalın yazıyla veya *"Tam da bu noktada"* dolgusuyla değil, vurgulanacak öğeyi yüklemin hemen önüne çekerek verilir (*"Dün İzmir'e ben gittim"* vs. *"Ben İzmir'e dün gittim"*).
- **Zamir Düşürme (Pro-Drop) ve Gereksiz `"Bir"` / `"Kendi"` Temizliği:** Yüklemdeki şahıs eki özneyi zaten taşıyorsa `ben, sen, o, biz` zamirlerini düşür. İngilizce `a/an` karşılığı olarak her sıfat tamlamasına sokulan gereksiz `"bir"` kelimesini (*"iyi bir performans"* -> *"iyi performans"*) ve `own` çevirisi olan gereksiz `"kendi"` zamirini sil.
- **Edilgen Çatı (`tarafından`) ve Kof Yardımcı Fiilleri Temizle:** *"Ekibimiz tarafından gerçekleştirilmiştir"* yerine *"Ekibimiz yaptı"*; *"artış sağlamak / katkıda bulunmak / sahip olmak"* yerine doğrudan *"artırmak / katkı sunmak / barındırmak"* fiillerini kullan.
- **Kanıtsallık Kipi (`-mIş`):** Dolaylı öğrenilen, log kaydından okunan veya sonradan fark edilen durumlarda kesin geçmiş zaman (`-DI`) yerine Türkçenin delil kipini (`-mIş`) kullan (*"Sunucu gece yeniden başlamış"*).

#### Katman 3: TDK Yazım Kılavuzu, Noktalama ve Terminoloji (P2 Sinyalleri)

Detaylı kurallar için `references/tdk-ve-noktalama.md` dosyasını oku:

- **Beş Mutlak Noktalama ve Bağlaç Yasağı:**
  1. Diyalog dışında ara söz veya vurgu için **uzun çizgi (em-dash)** kullanma; yerine virgül veya nokta koy.
  2. Sayı ve tarih aralıklarında orta çizgi (en-dash) değil, TDK standardı olan **kısa çizgi (`-`)** kullan (`04.30-05.00`, `2024-2026`).
  3. İki bağımsız cümleyi İngilizce tarzı **noktalı virgül köprüsüyle** birbirine yapıştırma, cümleyi noktayla bitir.
  4. **`ama`, `fakat`, `lakin`, `ancak`, `ve`, `veya`, `ya da`** bağlaçlarından önce veya sonra virgül koyma.
  5. Başlıklarda İngilizce *Title Case* (her kelimenin ilk harfi büyük, `Ve / İle` dahil) yapma; tümce düzeni kullan veya TDK kuralına göre bağlaçları küçük yaz (`ve`, `ile`, `ya da`).
- **Teknik Terimleri Zorla Çevirme, Okunuşuna Göre Ek Getir:** Sektörde yerleşik Türkçe karşılığı olmayan teknik terimleri (`endpoint`, `deploy`, `middleware`, `queue`, `cache`, `idempotent`) *"uç nokta, olay güdümlü, ara katman"* diye zorla çevirme. Kesme işaretiyle gelen ekleri yazılışa göre değil, **Türkçe okunuşa (fonetiğe)** göre getir: `cache'i` (keş), `queue'yu` (kü), `SQL'i` (es-kü-el), `JSON'ı` (ceyson).
- **TDK Bağlaç ve Birleşik Kelime Denetimi:** Bulunma durumu eki `-da/-de` (bitişik) ile bağlaç olan `da/de`'yi (ayrı), ilgi/sıfat eki `-ki` ile bağlaç olan `ki`'yi (`halbuki`, `oysaki`, `çünkü`, `mademki` kalıplaşmış bitişikler hariç ayrı) ve `birçok`, `birkaç`, `hiçbir`, `herhangi bir`, `pek çok`, `art arda`, `yanı sıra` yazımlarını denetle.

### Adım 3: Öz-Denetim (Self-Audit) ve Cümle Ritmi (Burstiness) Kontrolü

Taslağı oluşturduktan sonra kullanıcıya sunmadan önce şu kontrolleri yap:

- **Cümle Uzunluğu Varyasyonu (Burstiness CoV >= 0.40):** Arka arkaya gelen tüm cümleler 15-22 kelime bandında toplanmışsa ritim mekanikleşmiştir (CoV < 0.35). 3 veya daha fazla cümleli her paragrafta en az bir kısa/vurucu cümle (3-6 kelime) ile en az bir ulaçlı/sola dallanan uzun cümleyi (18-28 kelime) bir arada kullanarak değişim katsayısını (CoV) >= 0.40 seviyesinde tut.
- **Tier-1 Yasaklı Kelime Taraması:** Metinde `adeta`, `yadsınamaz`, `kritik bir rol oynamaktadır`, `derinlemesine`, `yelpaze`, `dönüm noktası`, `bununla birlikte`, `öte yandan`, `söz konusu`, `bu bağlamda` kalıplarının kalmadığından emin ol (`references/ai-turkcesi-sozlugu.md`).
- **Olgusal Sadakat Kontrolü:** Kaynak metindeki tüm sayılar, tarihler, teknik terimler ve iddialar korundu mu? Kaynakta olmayan bir sıfat veya abartı eklendi mi?

### Adım 4: Silme Testi (Deletion Test) ve Çıktı Teslimi

- Metne eklediğin her söylem parçacığını (`işte`, `zaten`, `tabii`), devrik cümleyi veya bağlacı test et: Kaldırdığında anlamdan veya tondan hiçbir şey eksilmiyorsa o öğeyi sil.
- Kullanıcı özellikle değişiklik raporu istemediyse ("neleri değiştirdin?" veya `audit` modu dışında) **yalnızca temizlenmiş/yazılmış metni** döndür ve başına "Elbette, metnin doğal Türkçeye çevrilmiş hali aşağıdadır:" gibi sohbet artıkları ekleme.

## Sık Yapılan Hatalar (Gotchas)

- **Aşırı Düzeltme (Overcorrection) Tuzağı:** Doğal bir Türkçe metinde geçen her `"bir"` kelimesini veya her devrik cümleyi hata sanma. `"Sen satışa bak"`, `"Site kurmak"`, `"Linki gönder"` gibi doğal ve yerleşik kullanımlara dokunma.
- **Öz-Türkçecilik Tuzağı:** Bu yetenek yabancı kökenli kelimeleri yasaklayan bir "arı dil" aracı değildir. Günlük ve mesleki Türkçede yaşayan kelimeleri (`performans`, `strateji`, `sistem`, `detay`) zorlama karşılıklarla değiştirme.
- **Sahte Samimiyet:** Kurumsal veya teknik bir metni insanlaştırmak adına metne *"Kahvenizi alın ve arkanıza yaslanın"*, *"Hepimiz oradaydık"* gibi çeviri blog klişeleri ekleme.
- **İkame Kelime Tiki (Replacement Tic) Tuzağı:** "Kritik bir rol oynar" veya "kusursuz bir şekilde" gibi yapay ifadeleri silerken her cümleye refleks olarak "doğrudan", "aslında" veya "ciddi ölçüde" ekleme. Çoğu zaman zarfı tamamen atıp fiili yalnız bırakmak en doğal sonucu verir.
- **Kılık Değiştirmiş Negatif Paralellik Tuzağı:** "Sadece X değil, aynı zamanda Y" kalıbını temizlerken yerine "X ile değil, Y ile" veya "geçici bir X değil, kalıcı bir Y" gibi başka bir negatif paralellik kurma. Olumsuz yarıyı tamamen atıp ne olduğunu söyle.
