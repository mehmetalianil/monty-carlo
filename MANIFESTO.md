Sevgili güruh,

Bu yazıyı yazmamın nedeni biraz da yazılım mimarisi kurma konusundaki tecrübesizliğim, hem size aklımdakileri anlatma ihtiyacım (çünkü sadece hayal etmiş olmaktansa birilerine anlatmanın ve onlardan yorum almanın ayaklarımı toprağa bastıracağını düşündüğümden) ve aynı zamanda sizin de bu erken kararları verme mekanizmasının içinde bulunmanızı istemem. 

Dolayısı ile az çok kenarda köşede konuşup durduğum şeyleri burada olabildiğince net bir şekilde anlatmaya çalışacağım. Bunu buradaki wiki'ye yazıyorum, sanırım çünkü emailden ziyade yorumlanabilir ve değiştirilebilir olmasını istiyorum.

###Felsefe###

Bu aralar Getting Real adlı bir kitabı okuyorum, kendisine buradan ulaşabilirsiniz: http://gettingreal.37signals.com/ Sizin de arada bakmanızı tavsiye ediyorum. Bu kitapta önemli bir kaç vurgu var ve bunları söylemek istiyorum.

**GR diyor ki:**

> *Build Less*

> *Underdo your competition*

> *Conventional wisdom says that to beat your competitors you need to one-up them. If they have four features, you need five (or 15, or 25). If they're spending x, you need to spend xx. If they have 20, you need 30.*

>  ...

>  *So what to do then? The answer is less. Do less than your competitors to beat them. Solve the simple problems and leave the hairy, difficult, nasty problems to everyone else. Instead of oneupping, try one-downing. Instead of outdoing, try underdoing.*


Bu benim oldukça zorlandığım bir şey, hepimizin aslında kod yazarken daha iyi nasıl yaparım sorusuna cevabı bulunuyor, ben bu cevabın kişisel olmaması gerektiğini, insanın kodunu yazarken bir an onu unutup düşünmesi, tartışması gerektiğini düşünüyorum, en nihayetinde en iyi eserler, en acımasızca budanmışlar oluyor genelde.

Bence dile hakim olduğumuzda oldukça iyi bir grup olacağız. Şu benim bu düşüncemi pekiştirdi:

**GR:**

> Build software for yourself

> A great way to build software is to start out by solving your own problems. You'll be the target audience and you'll know what's important and what's not. That gives you a great head start on delivering a breakout  product.

>  ...

>  When you solve your own problem, you create a tool that you're passionate about. And passion is key. passion means you'll truly use it and care about it. And that's the best way to get others to feel passionate about it too.

Bundan dolayı herkesin bu kod ile ilgili kafasında yapabileceği şeyler olmasını istiyorum. Çünkü eğer merak ettiğimiz, denemek istediğimiz sistemler olmazsa, modüler bir Monte Carlo kodu yazmamızın vereceği tek şey biliyor, öğreniyor olmanın hazzı olur, ki bu eminim uzun vadede tükenecektir. En nihayetinde ilerlememizi ve sürekliliğimizi sağlayan şey, yazarken bize nasıl vizyonlar açacağı olmalıdır, ama üzgünüm ki yazdığımız kod da buna hizmet etmemelidir. Çünkü : 

**GR:**

> The secret to building half a product instead of a half-ass product is saying no.*

Kendimize de  :)

Dolayısı ile, be kafamdaki yapıyı söyleyeceğim, siz de hayır! diyeceksiniz umarım.

### Yapı ###

Buradaki özellikleri gereklilik kipinde yazacağım, aslında gerekli olmayabiliriler.

Öncelikle büyük bir **durumlar kümesini** kapsayacak bir durum tanımı yapmalıyız. İki boyutlu Ising spinlerinin , üç boyutlu Ising spinlerinin, kutu içerisindeki bir gazın, bir Go oyunu tahtasının, bir ekonomik modele göre ekonominin durumlarının hepsi aynı derecese tanımlanabilir olmalı. Diğer türlü, zaten OOP kullanmamızı gerektirecek çok bir şey yok, herkes kendi kodunun daha düşük seviye bir dilde yazıp koşturabilir zaten. 

Yapılacak makine, minimum enerji ya da maksimum dirayet durumlarını Metropolis algoritmasına göre bahsedilen durum tanımına için bulacak. Burada durumun tanımı şöyle olabilir (parantez içinde Ising spinlerinde tekabül edenler): 

* Durumu oluşturan elemanlar (Spinler)
* Durum parametresi (Spin'in spini)
* Serbest parametreler (Sıcaklık, Dış Mag. Alan..)
* Enerji tanımı (Ising hamiltonyeni)
    * Elemanlararası etkileşim (Ising hamiltonyeni, tek spin için)
    * Elemanlararası etkileşim ağı (Komşuluk)
* Durum değiştirme operatörü (İlgili spini döndürme operatörü)

Bu parametreler dışarıdan ulaşabilir, ve birbirini görebili şekilde tasarlanmalılar. Zira, elemanlararası etkileşim, spinlerin her birine ulaşabilmeli, elemanlararası etkileşim ağı ise hem bir elemana, hem de tüm duruma ulaşabilmeli ki etkileşimin doğasını (çiftlerarası etkileşim) yapıya (kristale) uygulayabilmeli. 

Aynı sistem başka bir sisteme de uygulanabilmeli: (Go oyunu tahtası)

* Durumu oluşturan elemanlar (taşlar ya da boşluk)
* Durum parametresi (Bir yerin boş, siyah ya da beyaz taşla dolu olması)
* Serbest parametreler (Oyuncunun "Sıcaklığı" :) )
* Enerji tanımı (Tasarımcının ceza fonksiyonu)
    * Elemanlararası etkileşim (Taşın komşuları, ikincil komşuları ve tahtadaki konumu)
    * Elemanlararası etkileşim ağı (Komşuluk)
* Durum değiştirme operatörü (Belli bir yere taş koyma operatörü)

Monte Carlo motoru, bu tipte, modüler bir durum objesini alıp işleyecek durumda olmalı. Bunu yaparken ihtiyacı olacağı farklı şeyler olacak:

* Durum
* Bir rastgle sayı üreteci 
* Durumdan çıkarılacak fonksiyonlar (Magnetizasyon)
* Durum değiştirme operatörünün uygulanma kuralı (e^-bT ?< dE)
* Bir MC simülasyonunun bitme koşulları (dM < epsilon)
* Her Monte Carlo algoritmasi bittiğinde koşulacak bir impuls operatörü (Mesela Dış Magnetik Alan sinüsoidal ise ne olur?, Bir şizofren nasıl Go oynar :P)

Dolayısı ile yazılımın yapısı da bununla paralel olmak durumunda, yani MC çekirdeği ***herhangi bir*** durumu alabilmeli, biz de kendi konumuda çalışacağımız sistemi bu durum parametreleri cinsinden yazabilmeliyiz. Bunun haricinde yazılması gereken başka şeyler de var, sadece birkaçı:

* Hata ve sıradışı durumları yöneten bir modül (Exception Handling)
* Durumları, simülasyonları, sonuçları kaydedip açabilen bir modül 
* Parallel Mimariler için bir modül
* Grafik çizimleri için modül
* Programın yüklenebilir olması için modül
ve aklıma muhtemelen gelmeyeck olan bir sürü şey.

Tüm bunların en basitinin bile baştan yapılması ayları bulan geliştirme zamanı alacak iken, Pyton'da bunların hepsi için çok iyi modüller var şu an, adapte edilmeleri gerekiyor. 

Dolayısı ile yukarıdakileri yapabilen, aynı zamanda en az bir iki tane uygulama için class tanımları tamamen yapılmış bir program öneriyorum, 1.0 için. 

Ve 1.0 için bir code name bulalım diyorum! 1.0.0 beta build 322432 yerine. 
