"""Translated pages (Hindi, Brazilian Portuguese, Indonesian) for the most-searched tools.

Each page mirrors an English page (``base``) so build.py can emit hreflang alternates and a
language switcher. Slugs are "<lang>/<english-slug>" so tool URLs stay recognisable."""
from content import PAGE_COST, _fit_range, kb_label, kb_slug
from i18n import tr_for

# ---------------------------------------------------------------- shared phrases per language
P = {
    "hi": dict(
        crumb_home="होम",
        faq_privacy=("क्या मेरी फ़ाइल कहीं अपलोड होती है?",
                     "नहीं। सारा काम आपके ब्राउज़र में होता है — फ़ाइल आपके डिवाइस से बाहर नहीं जाती। पेज खुलने के बाद इंटरनेट बंद करके भी यह चलता है।"),
        faq_free=("क्या यह सच में मुफ़्त है? कोई लिमिट?",
                  "हाँ, पूरी तरह मुफ़्त — कोई डेली लिमिट नहीं, कोई साइन-अप नहीं, कोई वॉटरमार्क नहीं।"),
        faq_kb=("मेरी फ़ाइल 1000 या 1024 वाले KB में से किससे गिनी जाती है?",
                "कुछ साइट 1 KB = 1000 बाइट मानती हैं, कुछ 1024। हम 1000 बाइट मानकर छोटा रखते हैं, ताकि फ़ाइल दोनों तरह से पास हो जाए।"),
        faq_rules=("मुझे कौन-सा साइज़ चुनना चाहिए?",
                   "हमेशा अपने फ़ॉर्म या आधिकारिक नोटिफ़िकेशन में दिए गए नियम मानें — KB, पिक्सेल या cm, DPI और फ़ॉर्मेट। यहाँ दिए प्रीसेट सिर्फ़ उदाहरण हैं।"),
        fit_head=["आपकी PDF में क्या है", "हर पेज का साइज़", "{L} में कितने पेज", "क्या संभव है?"],
        fit_rows=["सिर्फ़ टेक्स्ट वाला पेज (Word, Google Docs से बना)", "ग्रेस्केल में स्कैन पेज (पत्र, फ़ॉर्म, प्रमाण पत्र)",
                  "रंगीन स्कैन पेज (मोहर, फ़ोटो, रंगीन बैकग्राउंड)", "पूरे पेज की रंगीन फ़ोटो या ब्रोशर"],
        fit_title="क्या मेरी PDF {L} में आ सकती है?",
        fit_intro="यह लगभग पूरी तरह इस पर निर्भर है कि पेज पर क्या है और कितने पेज हैं। टेक्स्ट बहुत छोटा होता है; स्कैन और फ़ोटो असल में इमेज होते हैं, और सभी पेज मिलकर {L} में आने चाहिए। अच्छे कंप्रेशन के बाद हर पेज का आम साइज़:",
        fit_note="ये A4 पेज के अनुमान हैं; आपकी फ़ाइल अलग हो सकती है। टूल हमेशा बताता है कि {L} तक पहुँचा या नहीं।",
        wont_fit="अगर फ़िट न हो तो",
        wont_fit_items=["“और विकल्प” में <strong>ग्रेस्केल</strong> चुनें — स्कैन के लिए साइज़ अक्सर आधा हो जाता है।",
                        "सिर्फ़ ज़रूरी पेज रखें — PDF को बाँटें या फ़ालतू पेज हटाएँ।",
                        "300 DPI रंगीन की जगह 150 DPI ग्रेस्केल में दोबारा स्कैन करें और काग़ज़ के किनारों तक क्रॉप करें।"],
    ),
    "pt": dict(
        crumb_home="Início",
        faq_privacy=("Meu arquivo é enviado para algum servidor?",
                     "Não. Tudo acontece no seu navegador — o arquivo nunca sai do seu dispositivo. Depois que a página abre, funciona até sem internet."),
        faq_free=("É grátis mesmo? Tem limite?", "Sim, totalmente grátis — sem limite diário, sem cadastro e sem marca d'água."),
        faq_kb=("O site considera 1 KB como 1000 ou 1024 bytes?",
                "Alguns sites usam 1000, outros 1024. Nós usamos 1000 bytes por KB, deixando o arquivo um pouco menor, para ele passar nos dois casos."),
        faq_rules=("Qual tamanho devo escolher?",
                   "Siga sempre as regras do edital ou das instruções do formulário — KB, pixels ou cm, DPI e formato. Os modelos aqui são apenas exemplos."),
        fit_head=["O que o seu PDF tem", "Tamanho por página", "Páginas que cabem em {L}", "Dá para fazer?"],
        fit_rows=["Página só com texto (exportada do Word, Google Docs)", "Página escaneada em tons de cinza (cartas, formulários, certificados)",
                  "Página escaneada colorida (carimbos, fotos, fundo colorido)", "Foto colorida de página inteira ou folheto"],
        fit_title="{L} é realista para o meu PDF?",
        fit_intro="Depende quase só do conteúdo e do número de páginas. Texto ocupa muito pouco; páginas escaneadas e fotos são imagens, e todas as páginas dividem os mesmos {L}. Tamanho típico por página depois de uma boa compressão:",
        fit_note="Estimativas para páginas A4 com boa leitura; o seu arquivo pode variar. A ferramenta sempre mostra se chegou a {L}.",
        wont_fit="Se não couber",
        wont_fit_items=["Marque <strong>tons de cinza</strong> em “Mais opções” — em documentos escaneados o tamanho costuma cair pela metade.",
                        "Envie só as páginas pedidas — divida o PDF ou exclua páginas desnecessárias.",
                        "Escaneie de novo a 150 DPI em tons de cinza em vez de 300 DPI colorido, e recorte nas bordas do papel."],
    ),
    "id": dict(
        crumb_home="Beranda",
        faq_privacy=("Apakah file saya diupload?",
                     "Tidak. Semua proses berjalan di browser Anda — file tidak pernah keluar dari perangkat. Setelah halaman terbuka, alat ini tetap jalan walau internet mati."),
        faq_free=("Benar-benar gratis? Ada batasnya?", "Ya, gratis sepenuhnya — tanpa batas harian, tanpa daftar akun, tanpa watermark."),
        faq_kb=("1 KB dihitung 1000 atau 1024 byte?",
                "Ada situs yang memakai 1000, ada yang 1024. Kami memakai 1000 byte per KB supaya file sedikit lebih kecil dan lolos di kedua cara hitung."),
        faq_rules=("Ukuran mana yang harus saya pilih?",
                   "Selalu ikuti aturan di pengumuman resmi atau petunjuk formulir — KB, piksel atau cm, DPI, dan format. Preset di sini hanya contoh."),
        fit_head=["Isi PDF Anda", "Ukuran per halaman", "Halaman yang muat di {L}", "Bisa?"],
        fit_rows=["Halaman teks saja (dari Word, Google Docs)", "Halaman scan hitam-putih (surat, formulir, sertifikat)",
                  "Halaman scan berwarna (stempel, foto, latar berwarna)", "Foto berwarna satu halaman penuh atau brosur"],
        fit_title="Apakah {L} realistis untuk PDF saya?",
        fit_intro="Hampir sepenuhnya tergantung isi dan jumlah halaman. Teks sangat kecil; hasil scan dan foto adalah gambar, dan semua halaman berbagi {L} yang sama. Ukuran umum per halaman setelah dikompres dengan baik:",
        fit_note="Perkiraan untuk halaman A4 yang tetap terbaca; file Anda bisa berbeda. Alat ini selalu memberi tahu apakah {L} tercapai.",
        wont_fit="Jika tidak muat",
        wont_fit_items=["Centang <strong>hitam-putih</strong> di “Opsi lainnya” — untuk hasil scan ukurannya sering turun setengah.",
                        "Upload hanya halaman yang diminta — pisahkan PDF atau hapus halaman yang tidak perlu.",
                        "Scan ulang di 150 DPI hitam-putih, bukan 300 DPI berwarna, dan potong sampai tepi kertas."],
    ),
}


def fit_table(lang, kb, L):
    p, tr = P[lang], tr_for(lang)
    eff = kb // 1024 * 1000 if kb >= 1024 and kb % 1024 == 0 else kb
    rows = ""
    for (label, lo, _typ, hi), name in zip(PAGE_COST, p["fit_rows"]):
        rng, verdict = _fit_range(eff, lo, hi, text=label.startswith("Text"))
        rows += f"<tr><td>{name}</td><td>{lo}–{hi} KB</td><td>{tr(rng) if rng == 'under 1' else rng}</td><td>{tr(verdict)}</td></tr>"
    head = "".join(f"<th>{h.format(L=L)}</th>" for h in p["fit_head"])
    items = "".join(f"<li>{x}</li>" for x in p["wont_fit_items"])
    return f"""<h2>{p['fit_title'].format(L=L)}</h2>
<p>{p['fit_intro'].format(L=L)}</p>
<div class="tablewrap"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="muted small">{p['fit_note'].format(L=L)}</p>
<h3>{p['wont_fit']}</h3><ul>{items}</ul>"""


def page(lang, base, tool, **kw):
    d = dict(lang=lang, base=base, slug=f"{lang}/{base}" if base else lang, tool=tool, group="tr", faqs=[], steps=None)
    d.update(kw)
    d.setdefault("mode", "target" if d.get("target_kb") else "recommended")
    return d


# ---------------------------------------------------------------- home pages
def homes():
    out = []
    hi, pt, id_ = P["hi"], P["pt"], P["id"]
    out.append(page("hi", "", "compress", crumb="PDF कंप्रेस करें",
        title="PDF का साइज़ कम करें — मुफ़्त, बिना अपलोड, 100 KB तक",
        desc="PDF का साइज़ मुफ़्त में कम करें — 100 KB, 200 KB या कोई भी सटीक साइज़। फ़ाइल आपके डिवाइस पर ही प्रोसेस होती है: कोई अपलोड नहीं, कोई लिमिट नहीं।",
        h1="PDF का साइज़ कम करें — मुफ़्त और सुरक्षित",
        lead="PDF को 90% तक छोटा करें या 100 KB जैसा सटीक साइज़ पाएँ। सब कुछ आपके डिवाइस पर होता है — फ़ाइल कहीं अपलोड नहीं होती।",
        facts=["100% ब्राउज़र में: आपकी PDF किसी सर्वर पर अपलोड नहीं होती।", "कोई डेली लिमिट नहीं, कोई साइन-अप नहीं, कोई वॉटरमार्क नहीं।",
               "सटीक साइज़ मोड (जैसे 100 KB, 200 KB, 1 MB) — ऑनलाइन फ़ॉर्म के लिए।",
               "टेक्स्ट और लिंक सुरक्षित रहते हैं; सिर्फ़ PDF के अंदर की इमेज कंप्रेस होती हैं।",
               "एक साथ कई PDF कंप्रेस करें और ZIP में डाउनलोड करें।"],
        steps_title="PDF का साइज़ कैसे कम करें",
        steps=["अपनी PDF ऊपर वाले बॉक्स में डालें या “फ़ाइलें चुनें” पर टैप करें।",
               "लेवल चुनें — अनुशंसित, ज़्यादा या हल्का — या “सटीक साइज़” में अपने फ़ॉर्म की सीमा डालें।",
               "“डाउनलोड” पर क्लिक करें, या कई फ़ाइलें हों तो ZIP डाउनलोड करें।"],
        body="""<h2>यह PDF कंप्रेसर अलग क्यों है</h2>
<div class="grid">
<div class="card"><h3>कभी अपलोड नहीं</h3><p>कंप्रेशन आपके ब्राउज़र में होता है। बैंक स्टेटमेंट, आधार या मार्कशीट किसी सर्वर तक नहीं पहुँचते।</p></div>
<div class="card"><h3>सटीक साइज़</h3><p>फ़ॉर्म को 100 KB से कम चाहिए? वही डालें — टूल उस साइज़ में सबसे अच्छी क्वालिटी खोजता है।</p></div>
<div class="card"><h3>टेक्स्ट साफ़ रहता है</h3><p>सिर्फ़ इमेज कंप्रेस होती हैं, इसलिए PDF का टेक्स्ट पढ़ने और कॉपी करने लायक रहता है।</p></div>
<div class="card"><h3>कोई लिमिट नहीं</h3><p>“दिन में 2 फ़ाइल” जैसी कोई पाबंदी नहीं, कोई अकाउंट नहीं।</p></div>
</div>
<h2>PDF इतनी बड़ी क्यों होती है?</h2>
<p>ज़्यादातर बड़ी PDF में असली वजह इमेज होती हैं — 300–600 DPI पर स्कैन किए पेज या मोबाइल कैमरे की फ़ोटो। टेक्स्ट बहुत कम जगह लेता है।
इसलिए हम इमेज को सही रेज़ोल्यूशन पर दोबारा सेव करते हैं और छिपा हुआ फ़ालतू डेटा (मेटाडेटा, थंबनेल, पुराने एडिट) हटाते हैं।</p>
<h2>लोकप्रिय साइज़</h2>
<p><a href="/hi/compress-pdf-to-50kb/">PDF 50 KB में</a> · <a href="/hi/compress-pdf-to-100kb/">PDF 100 KB में</a> ·
<a href="/hi/compress-pdf-to-200kb/">PDF 200 KB में</a> · <a href="/hi/resize-image-to-20kb/">फ़ोटो 20 KB में</a> ·
<a href="/hi/photo-signature-resizer/">फ़ोटो और हस्ताक्षर रिसाइज़र</a></p>""",
        faqs=[hi["faq_privacy"], hi["faq_free"],
              ("PDF कितनी छोटी हो जाएगी?", "स्कैन और फ़ोटो वाली PDF आमतौर पर 60–95% छोटी होती हैं। सिर्फ़ टेक्स्ट वाली PDF पहले से छोटी होती हैं; उनमें 5–40% बचत होती है। अगर छोटी न हो सके, तो हम मूल फ़ाइल ही देते हैं।"),
              ("क्या यह मोबाइल पर चलता है?", "हाँ — Android और iPhone के किसी भी ब्राउज़र में, कोई ऐप इंस्टॉल किए बिना।")]))
    out.append(page("pt", "", "compress", crumb="Comprimir PDF",
        title="Comprimir PDF Grátis — Sem Upload, Tamanho Exato de 100 KB",
        desc="Diminua o tamanho do PDF grátis, até um tamanho exato como 100 KB ou 200 KB. Tudo no seu dispositivo: sem upload, sem limites e sem cadastro.",
        h1="Comprimir PDF — grátis e com privacidade",
        lead="Reduza PDFs em até 90% ou para um tamanho exato como 100 KB. Tudo acontece no seu dispositivo: nada é enviado e não há limites.",
        facts=["100% no navegador: seu PDF nunca é enviado para um servidor.", "Sem limite diário, sem cadastro e sem marca d'água.",
               "Modo de tamanho exato (100 KB, 200 KB, 1 MB…) para formulários online.",
               "Texto e links continuam selecionáveis; só as imagens dentro do PDF são recomprimidas.",
               "Comprima vários PDFs de uma vez e baixe tudo em ZIP."],
        steps_title="Como comprimir um PDF",
        steps=["Solte o PDF na caixa acima ou toque em “escolha os arquivos”.",
               "Escolha o nível — Recomendado, Forte ou Leve — ou use “Tamanho exato” com o limite do seu formulário.",
               "Clique em “Baixar” (ou baixe tudo em ZIP)."],
        body="""<h2>Por que este compressor é diferente</h2>
<div class="grid">
<div class="card"><h3>Nunca enviado</h3><p>A compressão roda no navegador. Extratos, RG e diplomas não passam por nenhum servidor.</p></div>
<div class="card"><h3>Tamanho exato</h3><p>O edital pede menos de 100 KB? Digite o limite — a ferramenta busca a melhor qualidade que cabe.</p></div>
<div class="card"><h3>Texto continua texto</h3><p>Só as imagens são recomprimidas: o PDF continua pesquisável e copiável.</p></div>
<div class="card"><h3>Sem limites</h3><p>Nada de “2 arquivos por dia” ou conta obrigatória.</p></div>
</div>
<h2>Por que o PDF fica tão grande?</h2>
<p>Quase sempre por causa das imagens: páginas escaneadas a 300–600 DPI ou fotos tiradas com o celular. O texto ocupa muito pouco.
Por isso recomprimimos as imagens numa resolução adequada e removemos dados ocultos (metadados, miniaturas, edições antigas).</p>
<h2>Tamanhos mais procurados</h2>
<p><a href="/pt/compress-pdf-to-100kb/">PDF para 100 KB</a> · <a href="/pt/compress-pdf-to-200kb/">200 KB</a> ·
<a href="/pt/compress-pdf-to-500kb/">500 KB</a> · <a href="/pt/compress-pdf-to-1mb/">1 MB</a> ·
<a href="/pt/resize-image-to-100kb/">Imagem para 100 KB</a> · <a href="/pt/jpg-to-pdf/">JPG para PDF</a> · <a href="/pt/merge-pdf/">Juntar PDF</a></p>""",
        faqs=[pt["faq_privacy"], pt["faq_free"],
              ("Quanto o PDF vai diminuir?", "PDFs escaneados ou com fotos costumam cair 60–95%. PDFs só com texto já são pequenos; neles a economia é de 5–40%. Se não der para diminuir, devolvemos o original."),
              ("Funciona no celular?", "Sim — em qualquer navegador de Android ou iPhone, sem instalar aplicativo.")]))
    out.append(page("id", "", "compress", crumb="Kompres PDF",
        title="Kompres PDF Gratis — Tanpa Upload, Ukuran Pas 100 KB",
        desc="Perkecil ukuran PDF gratis hingga ukuran pas seperti 100 KB atau 200 KB. Diproses di perangkat Anda — tanpa upload, tanpa batas, tanpa daftar.",
        h1="Kompres PDF — gratis dan aman",
        lead="Perkecil PDF hingga 90% atau ke ukuran pas seperti 100 KB. Semua terjadi di perangkat Anda — tidak ada yang diupload, tanpa batas.",
        facts=["100% di browser: PDF Anda tidak pernah diupload ke server.", "Tanpa batas harian, tanpa daftar akun, tanpa watermark.",
               "Mode ukuran pas (100 KB, 200 KB, 1 MB…) untuk formulir online.",
               "Teks dan tautan tetap bisa dipilih; hanya gambar di dalam PDF yang dikompres ulang.",
               "Kompres banyak PDF sekaligus dan unduh dalam ZIP."],
        steps_title="Cara kompres PDF",
        steps=["Taruh PDF di kotak di atas atau ketuk “pilih file”.",
               "Pilih tingkat — Disarankan, Kuat, atau Ringan — atau isi “Ukuran pas” sesuai batas formulir.",
               "Klik “Unduh” (atau unduh semua dalam ZIP)."],
        body="""<h2>Kenapa kompres PDF ini berbeda</h2>
<div class="grid">
<div class="card"><h3>Tidak pernah diupload</h3><p>Kompresi berjalan di browser. KTP, ijazah, dan rekening koran tidak pernah sampai ke server.</p></div>
<div class="card"><h3>Ukuran pas</h3><p>Formulir minta di bawah 100 KB? Isi batasnya — alat ini mencari kualitas terbaik yang masih muat.</p></div>
<div class="card"><h3>Teks tetap teks</h3><p>Hanya gambar yang dikompres, jadi PDF tetap bisa dicari dan disalin.</p></div>
<div class="card"><h3>Tanpa batas</h3><p>Tidak ada “2 file per hari” dan tidak perlu akun.</p></div>
</div>
<h2>Kenapa PDF bisa sebesar itu?</h2>
<p>Hampir selalu karena gambar: halaman hasil scan 300–600 DPI atau foto dari kamera ponsel. Teks hanya butuh sedikit ruang.
Karena itu kami mengompres ulang gambar ke resolusi yang wajar dan membuang data tersembunyi (metadata, thumbnail, sisa edit).</p>
<h2>Ukuran paling dicari</h2>
<p><a href="/id/compress-pdf-to-100kb/">Kompres PDF 100 KB</a> · <a href="/id/compress-pdf-to-200kb/">200 KB</a> ·
<a href="/id/compress-pdf-to-1mb/">1 MB</a> · <a href="/id/resize-image-to-100kb/">Kompres foto 100 KB</a> ·
<a href="/id/resize-image-to-200kb/">Kompres foto 200 KB</a> · <a href="/id/photo-signature-resizer/">Pas foto &amp; tanda tangan</a></p>""",
        faqs=[id_["faq_privacy"], id_["faq_free"],
              ("Seberapa kecil PDF saya nanti?", "PDF hasil scan atau berisi foto biasanya turun 60–95%. PDF berisi teks saja sudah kecil; hematnya 5–40%. Jika tidak bisa lebih kecil, kami kembalikan file aslinya."),
              ("Bisa dipakai di HP?", "Bisa — di browser Android atau iPhone mana pun, tanpa instal aplikasi.")]))
    return out


# ---------------------------------------------------------------- PDF to X KB
PDF_WHO = {
    "hi": {50: "भर्ती और स्कॉलरशिप पोर्टल पर जाति/आय प्रमाण पत्र, ID प्रूफ़ और मार्कशीट जैसे दस्तावेज़।",
           100: "सरकारी नौकरी और परीक्षा फ़ॉर्म, एडमिशन, स्कॉलरशिप और KYC — ऑनलाइन सबसे आम PDF साइज़ सीमा।",
           200: "पासपोर्ट और वीज़ा के सहायक दस्तावेज़, यूनिवर्सिटी एडमिशन, बैंक और बीमा फ़ॉर्म।"},
    "pt": {100: "Muitos formulários de concursos, vestibulares e programas de bolsa limitam cada documento a poucos KB — 100 KB é um dos limites mais comuns.",
           200: "Documentos de matrícula, RG ou CNH escaneados, comprovantes de residência e anexos de processos seletivos.",
           500: "Currículos com foto, laudos e documentos para portais de RH ou envio por e-mail.",
           1024: "Portais de vagas, sistemas de RH, serviços públicos online e anexos de e-mail."},
    "id": {100: "Pendaftaran CPNS, PPDB, beasiswa, dan lamaran kerja online sering membatasi dokumen hingga 100 KB.",
           200: "Ijazah, transkrip nilai, KTP/KK hasil scan, dan dokumen pendukung pendaftaran kuliah atau visa.",
           1024: "Portal lowongan kerja, sistem HR, formulir online, dan lampiran email."},
}


def pdf_size(lang, kb):
    L, s, p = kb_label(kb), kb_slug(kb), P[lang]
    who = PDF_WHO[lang][kb]
    if lang == "hi":
        t = dict(crumb=f"PDF {L} में", title=f"PDF को {L} में कंप्रेस करें — मुफ़्त, सटीक साइज़, बिना अपलोड",
                 desc=f"PDF का साइज़ {L} से कम करें, कुछ ही सेकंड में। सटीक साइज़, टेक्स्ट साफ़ रहता है, फ़ाइल अपलोड नहीं होती — मुफ़्त और बिना लिमिट।",
                 h1=f"PDF को {L} में कंप्रेस करें",
                 lead=f"ऑनलाइन फ़ॉर्म के लिए किसी भी PDF को {L} से कम करें। साइज़ पहले से सेट है — बस फ़ाइल डालें।",
                 facts=[f"जहाँ संभव हो, नतीजा {L} या उससे कम होने की गारंटी — और अगर न हो सके तो साफ़ बताता है।",
                        "टेक्स्ट और लिंक सुरक्षित रहते हैं; ज़रूरत पड़ने पर ही पेज इमेज में बदलते हैं।",
                        "1 KB = 1000 बाइट मानकर गिनती, ताकि फ़ाइल हर पोर्टल पर पास हो।",
                        "आपके ब्राउज़र में चलता है: फ़ाइल कभी अपलोड नहीं होती। मुफ़्त, कोई वॉटरमार्क नहीं।"],
                 steps_title=f"PDF को {L} में कैसे करें",
                 steps=["ऊपर बॉक्स में PDF डालें या “फ़ाइलें चुनें” पर टैप करें।", f"साइज़ पहले से {L} पर सेट है — अगर फ़ॉर्म में अलग सीमा है तो बदल दें।",
                        "कुछ सेकंड रुकें, फिर “डाउनलोड” करें और फ़ॉर्म में अपलोड करें।"],
                 who_h=f"{L} वाली PDF किसे चाहिए?",
                 faq=(f"क्या स्कैन किया गया पेज {L} में आ सकता है?", f"हाँ, अगर पेज कम हों। ग्रेस्केल में स्कैन किया एक पेज आमतौर पर 30–90 KB का होता है। ऊपर की तालिका से अंदाज़ा लगाएँ कि आपके कितने पेज {L} में आएँगे।"))
    elif lang == "pt":
        t = dict(crumb=f"PDF para {L}", title=f"Comprimir PDF para {L} Online Grátis — Tamanho Exato",
                 desc=f"Reduza um PDF para menos de {L} em segundos. Tamanho exato, texto nítido, funciona no navegador — sem upload, sem cadastro, sem limites.",
                 h1=f"Comprimir PDF para {L}",
                 lead=f"Deixe qualquer PDF abaixo de {L} para formulários e uploads. O tamanho já vem configurado — é só soltar o arquivo.",
                 facts=[f"Garante o resultado em {L} ou menos quando possível — e avisa quando não dá.",
                        "Texto e links continuam selecionáveis; as páginas só viram imagem se for necessário.",
                        "Conta 1 KB como 1000 bytes, para o arquivo passar em qualquer site.",
                        "Roda no seu navegador: o arquivo nunca é enviado. Grátis e sem marca d'água."],
                 steps_title=f"Como deixar um PDF com {L}",
                 steps=["Solte o PDF na caixa acima ou toque em “escolha os arquivos”.", f"O limite já está em {L} — mude se o seu formulário pedir outro.",
                        "Espere alguns segundos e clique em “Baixar”."],
                 who_h=f"Quem precisa de um PDF com menos de {L}?",
                 faq=(f"Uma página escaneada cabe em {L}?", f"Depende do número de páginas. Uma página escaneada em tons de cinza costuma ter 30–90 KB depois de comprimida. Use a tabela acima para ver quantas páginas cabem em {L}."))
    else:
        t = dict(crumb=f"PDF {L}", title=f"Kompres PDF {L} Online Gratis — Ukuran Pas, Tanpa Upload",
                 desc=f"Perkecil PDF di bawah {L} dalam hitungan detik. Ukuran pas, teks tetap tajam, berjalan di browser — tanpa upload, tanpa daftar, tanpa batas.",
                 h1=f"Kompres PDF ke {L}",
                 lead=f"Buat PDF apa pun di bawah {L} untuk formulir dan upload online. Ukurannya sudah diatur — tinggal masukkan file.",
                 facts=[f"Menjamin hasil {L} atau lebih kecil jika memungkinkan — dan memberi tahu jika tidak bisa.",
                        "Teks dan tautan tetap bisa dipilih; halaman hanya diubah jadi gambar bila perlu.",
                        "Menghitung 1 KB = 1000 byte agar file lolos di semua situs.",
                        "Berjalan di browser Anda: file tidak pernah diupload. Gratis, tanpa watermark."],
                 steps_title=f"Cara kompres PDF ke {L}",
                 steps=["Taruh PDF di kotak di atas atau ketuk “pilih file”.", f"Batasnya sudah {L} — ubah jika formulir Anda meminta ukuran lain.",
                        "Tunggu beberapa detik, lalu klik “Unduh”."],
                 who_h=f"Siapa yang butuh PDF di bawah {L}?",
                 faq=(f"Apakah halaman hasil scan muat di {L}?", f"Tergantung jumlah halaman. Satu halaman scan hitam-putih biasanya 30–90 KB setelah dikompres. Lihat tabel di atas untuk tahu berapa halaman yang muat di {L}."))
    body = f"<h2>{t['who_h']}</h2><p>{who}</p>\n{fit_table(lang, kb, L)}"
    return page(lang, f"compress-pdf-to-{s}", "compress", target_kb=kb, crumb=t["crumb"], title=t["title"], desc=t["desc"],
                h1=t["h1"], lead=t["lead"], facts=t["facts"], steps_title=t["steps_title"], steps=t["steps"], body=body,
                faqs=[t["faq"], p["faq_kb"], p["faq_privacy"]])


# ---------------------------------------------------------------- Image to X KB
IMG_WHO = {
    "hi": {20: "परीक्षा और भर्ती फ़ॉर्म में हस्ताक्षर और पासपोर्ट-साइज़ फ़ोटो — ऑनलाइन फ़ॉर्म की सबसे आम सीमाओं में से एक।",
           50: "जॉब पोर्टल, एडमिशन फ़ॉर्म और KYC के लिए फ़ोटो और ID स्कैन।"},
    "pt": {100: "Foto 3x4 para inscrições, foto de perfil e documentos fotografados com o celular."},
    "id": {100: "Pas foto untuk pendaftaran online (CPNS, sekolah, beasiswa) dan foto profil.",
           200: "Foto KTP atau ijazah dari ponsel, foto dokumen, dan gambar untuk situs web."},
}


def img_size(lang, kb):
    L, p = f"{kb} KB", P[lang]
    who = IMG_WHO[lang][kb]
    if lang == "hi":
        t = dict(crumb=f"फ़ोटो {L} में", title=f"फ़ोटो का साइज़ {L} करें — मुफ़्त, JPG, बिना अपलोड",
                 desc=f"फ़ोटो या हस्ताक्षर को एक क्लिक में {L} से कम करें। सटीक पिक्सेल या cm साइज़, DPI, बेहतरीन क्वालिटी — मुफ़्त और सुरक्षित।",
                 h1=f"फ़ोटो का साइज़ {L} करें",
                 lead=f"ऑनलाइन फ़ॉर्म के लिए किसी भी फ़ोटो, हस्ताक्षर या स्कैन को {L} से कम करें — ज़रूरत हो तो सटीक साइज़ के साथ।",
                 facts=[f"{L} या उससे कम की JPG बनाता है, सबसे अच्छी क्वालिटी के साथ।",
                        "ज़रूरत हो तो सटीक पिक्सेल या cm साइज़ (जैसे 3.5×4.5 cm, 200 DPI) और न्यूनतम साइज़ भी।",
                        "JPG, PNG, WebP और iPhone की HEIC फ़ोटो चलती हैं। कई फ़ोटो एक साथ, ZIP में।",
                        "फ़ोटो आपके डिवाइस पर ही प्रोसेस होती है — कभी अपलोड नहीं। लोकेशन (EXIF) डेटा हट जाता है।"],
                 steps_title=f"फ़ोटो को {L} में कैसे करें",
                 steps=["अपनी फ़ोटो, हस्ताक्षर या स्कैन चुनें।", f"{L} पहले से सेट है — फ़ॉर्म के अनुसार साइज़ और डाइमेंशन बदलें।", "JPG डाउनलोड करें और फ़ॉर्म में अपलोड करें।"],
                 who_h=f"{L} वाली फ़ोटो किसे चाहिए?",
                 tips_h="बेहतरीन नतीजे के लिए सुझाव",
                 tips=["पहले फ़ॉर्म में दिया पिक्सेल या cm साइज़ डालें, फिर KB सीमा।", "सादा, हल्के रंग का बैकग्राउंड रखें — भरा हुआ बैकग्राउंड ज़्यादा जगह लेता है।",
                       "हस्ताक्षर सफ़ेद काग़ज़ पर काले पेन से करें और पास से क्रॉप करें।"],
                 faq=(f"क्या {L} में फ़ोटो साफ़ दिखेगी?", f"हाँ, आम पासपोर्ट-साइज़ फ़ोटो (लगभग 200×230 से 400×500 पिक्सेल) {L} में अच्छी दिखती है। बड़ी फ़ोटो को टूल अपने आप थोड़ा छोटा कर देता है ताकि क्वालिटी बनी रहे।"))
    elif lang == "pt":
        t = dict(crumb=f"Imagem para {L}", title=f"Reduzir Imagem para {L} Online Grátis — JPG",
                 desc=f"Reduza uma foto ou assinatura para menos de {L} em um clique. Tamanho exato em pixels ou cm, DPI e boa qualidade. Grátis e sem upload.",
                 h1=f"Reduzir imagem para {L}",
                 lead=f"Deixe qualquer foto, assinatura ou documento abaixo de {L} para formulários — com tamanho exato, se precisar.",
                 facts=[f"Gera um JPG com {L} ou menos, na melhor qualidade possível.",
                        "Tamanho exato opcional em pixels ou cm (como 3x4 cm a 300 DPI) e tamanho mínimo.",
                        "Aceita JPG, PNG, WebP e fotos HEIC do iPhone. Várias imagens de uma vez, em ZIP.",
                        "A foto é processada no seu dispositivo — nunca enviada. Dados de localização (EXIF) são removidos."],
                 steps_title=f"Como reduzir uma imagem para {L}",
                 steps=["Escolha a foto, assinatura ou documento.", f"{L} já está configurado — ajuste tamanho e dimensões conforme o formulário.", "Baixe o JPG e envie no formulário."],
                 who_h=f"Quem precisa de uma imagem com menos de {L}?",
                 tips_h="Dicas para a melhor qualidade",
                 tips=["Primeiro coloque as dimensões pedidas (pixels ou cm), depois o limite em KB.", "Use fundo liso e claro — fundos cheios de detalhes ocupam mais espaço.",
                       "Para 3x4: escolha cm, digite 3 × 4 e o DPI pedido (por exemplo 300)."],
                 faq=(f"A foto fica nítida com {L}?", f"Sim. Uma foto de documento ou 3x4 fica muito boa com {L}. Fotos grandes de celular são reduzidas automaticamente para manter a qualidade."))
    else:
        t = dict(crumb=f"Foto {L}", title=f"Kompres Foto {L} Online Gratis — JPG, Ukuran Pas",
                 desc=f"Perkecil foto atau tanda tangan di bawah {L} dalam satu klik. Ukuran piksel atau cm yang pas, DPI, kualitas terbaik. Gratis, tanpa upload.",
                 h1=f"Kompres foto ke {L}",
                 lead=f"Buat foto, tanda tangan, atau hasil scan di bawah {L} untuk formulir online — dengan ukuran pas jika diperlukan.",
                 facts=[f"Menghasilkan JPG {L} atau lebih kecil dengan kualitas terbaik.",
                        "Opsional: ukuran pas dalam piksel atau cm (mis. 3x4 cm, 300 DPI) dan ukuran minimal.",
                        "Mendukung JPG, PNG, WebP, dan foto HEIC dari iPhone. Banyak foto sekaligus, unduh ZIP.",
                        "Foto diproses di perangkat Anda — tidak pernah diupload. Data lokasi (EXIF) dihapus."],
                 steps_title=f"Cara kompres foto ke {L}",
                 steps=["Pilih foto, tanda tangan, atau hasil scan.", f"{L} sudah diatur — sesuaikan ukuran dan dimensi dengan formulir.", "Unduh JPG dan upload ke formulir."],
                 who_h=f"Siapa yang butuh foto di bawah {L}?",
                 tips_h="Tips agar hasilnya bagus",
                 tips=["Isi dulu dimensi yang diminta (piksel atau cm), baru batas KB.", "Gunakan latar polos berwarna terang (atau merah/biru sesuai ketentuan).",
                       "Untuk pas foto 3x4 atau 4x6: pilih cm, isi ukurannya, dan DPI yang diminta."],
                 faq=(f"Apakah foto tetap jelas di {L}?", f"Ya. Pas foto dan foto dokumen tetap jelas di {L}. Foto besar dari ponsel otomatis diperkecil agar kualitasnya terjaga."))
    tips = "".join(f"<li>{x}</li>" for x in t["tips"])
    body = f"<h2>{t['who_h']}</h2><p>{who}</p><h2>{t['tips_h']}</h2><ul>{tips}</ul>"
    return page(lang, f"resize-image-to-{kb}kb", "image", target_kb=kb, crumb=t["crumb"], title=t["title"], desc=t["desc"],
                h1=t["h1"], lead=t["lead"], facts=t["facts"], steps_title=t["steps_title"], steps=t["steps"], body=body,
                faqs=[t["faq"], p["faq_rules"], p["faq_privacy"]])


# ---------------------------------------------------------------- other tools
def extras():
    hi, pt, id_ = P["hi"], P["pt"], P["id"]
    out = []
    out.append(page("hi", "photo-signature-resizer", "image", target_kb=50, img=dict(presets="exam", open=True),
        crumb="फ़ोटो और हस्ताक्षर रिसाइज़र", title="परीक्षा फ़ॉर्म के लिए फ़ोटो और हस्ताक्षर रिसाइज़र — KB, cm, DPI",
        desc="ऑनलाइन परीक्षा और नौकरी फ़ॉर्म के लिए फ़ोटो और हस्ताक्षर का साइज़ ठीक करें: सटीक KB, पिक्सेल या cm, DPI और फ़ोटो पर नाम-तारीख़। मुफ़्त, बिना अपलोड।",
        h1="ऑनलाइन फ़ॉर्म के लिए फ़ोटो और हस्ताक्षर रिसाइज़र",
        lead="परीक्षा, नौकरी और स्कॉलरशिप फ़ॉर्म के लिए फ़ोटो और हस्ताक्षर एक ही बार में सही करें — KB, साइज़, DPI और फ़ॉर्मेट।",
        facts=["अधिकतम और न्यूनतम KB, px/cm/mm/inch में सटीक साइज़ और DPI — सब एक साथ।", "ज़रूरत हो तो फ़ोटो पर नाम और तारीख़ भी लिखता है।",
               "डिफ़ॉल्ट रूप से JPG — जो लगभग हर पोर्टल पर मान्य है।", "आपके ब्राउज़र में चलता है: फ़ोटो और हस्ताक्षर कभी अपलोड नहीं होते।"],
        steps_title="फ़ोटो और हस्ताक्षर कैसे रिसाइज़ करें",
        steps=["अपने फ़ॉर्म के निर्देशों में फ़ोटो और हस्ताक्षर के नियम पढ़ें।", "फ़ोटो डालें, उसकी KB सीमा और साइज़ सेट करें (प्रीसेट से शुरुआत करें), डाउनलोड करें।",
               "हस्ताक्षर के लिए उसकी अपनी सीमा के साथ यही दोहराएँ।"],
        body="""<h2>अपलोड रिजेक्ट क्यों होता है</h2>
<ul><li><strong>फ़ाइल साइज़</strong> सीमा से बाहर — बहुत बड़ी <em>या</em> बहुत छोटी (कई फ़ॉर्म में न्यूनतम सीमा होती है)।</li>
<li><strong>ग़लत डाइमेंशन</strong> — फ़ॉर्म पिक्सेल या cm और DPI जाँचता है।</li>
<li><strong>ग़लत फ़ॉर्मेट</strong> — JPG की जगह PNG या iPhone की HEIC फ़ोटो।</li>
<li><strong>नाम/तारीख़ नहीं</strong> — कुछ भर्ती फ़ॉर्म में फ़ोटो पर ये ज़रूरी होते हैं (<a href="/hi/add-name-and-date-on-photo/">फ़ोटो पर नाम और तारीख़</a>)।</li></ul>
<p>यह टूल चारों बातें एक साथ संभालता है। हस्ताक्षर सफ़ेद काग़ज़ पर काले पेन से करें और पास से क्रॉप करें।</p>""",
        faqs=[hi["faq_rules"], ("क्या iPhone की HEIC फ़ोटो चलेगी?", "हाँ — HEIC फ़ोटो अपने आप JPG में बदल जाती है।"), hi["faq_privacy"]]))
    out.append(page("hi", "add-name-and-date-on-photo", "image", target_kb=50, img=dict(presets="exam", text=True),
        crumb="फ़ोटो पर नाम और तारीख़", title="फ़ोटो पर नाम और तारीख़ लिखें — परीक्षा फ़ॉर्म के लिए मुफ़्त",
        desc="कुछ परीक्षा और भर्ती फ़ॉर्म के लिए फ़ोटो के नीचे अपना नाम और फ़ोटो की तारीख़ लिखें। सटीक KB और साइज़ के साथ। मुफ़्त, बिना अपलोड।",
        h1="फ़ोटो पर नाम और तारीख़ लिखें",
        lead="कुछ भर्ती और परीक्षा फ़ॉर्म में उम्मीदवार का नाम और फ़ोटो खिंचवाने की तारीख़ फ़ोटो पर होना ज़रूरी है। यहाँ कुछ सेकंड में करें।",
        facts=["फ़ोटो के नीचे सफ़ेद पट्टी में आपका नाम और तारीख़ साफ़ काले अक्षरों में।", "फ़ॉर्म के अनुसार तारीख़ का फ़ॉर्मेट चुनें (DD-MM-YYYY, DD/MM/YYYY आदि)।",
               "फ़ाइल आपकी KB सीमा और सटीक साइज़ में रहती है।", "फ़ोटो आपके डिवाइस पर ही प्रोसेस होती है — कभी अपलोड नहीं।"],
        steps_title="फ़ोटो पर नाम और तारीख़ कैसे लिखें",
        steps=["अपनी फ़ोटो चुनें।", "अपना नाम लिखें और फ़ोटो की तारीख़ व फ़ॉर्मेट चुनें।", "फ़ॉर्म के अनुसार KB सीमा और साइज़ सेट करें, फिर डाउनलोड करें।"],
        body="""<h2>सुझाव</h2>
<ul><li>वही तारीख़ डालें जब फ़ोटो खींची गई थी, और देखें कि फ़ोटो फ़ॉर्म के नियमों के हिसाब से नई है।</li>
<li>नाम की स्पेलिंग वही रखें जो आवेदन में है।</li>
<li>प्रीव्यू देखें: टेक्स्ट पढ़ने लायक हो और चेहरा फ़ोटो का ज़्यादातर हिस्सा भरे।</li></ul>""",
        faqs=[hi["faq_rules"], ("क्या टेक्स्ट से मेरा चेहरा छोटा हो जाएगा?", "पट्टी के ऊपर का हिस्सा भरने के लिए फ़ोटो क्रॉप होती है, इसलिए चेहरा बड़ा रहता है। सटीक साइज़ के लिए “सटीक साइज़ में क्रॉप करें” चुनें।"), hi["faq_privacy"]]))
    out.append(page("id", "photo-signature-resizer", "image", target_kb=100, img=dict(presets="exam", open=True),
        crumb="Pas foto & tanda tangan", title="Ubah Ukuran Pas Foto & Tanda Tangan — KB, cm, DPI Gratis",
        desc="Atur pas foto dan tanda tangan untuk pendaftaran CPNS, sekolah, dan lamaran kerja: ukuran KB, piksel atau cm, dan DPI yang pas. Gratis, tanpa upload.",
        h1="Ubah ukuran pas foto dan tanda tangan",
        lead="Siapkan pas foto dan tanda tangan sesuai aturan formulir online — ukuran file, dimensi, DPI, dan format sekaligus.",
        facts=["Batas KB maksimal dan minimal, ukuran pas dalam px/cm/mm/inci, dan DPI sekaligus.", "Preset 3x4 dan 4x6 cm tinggal diisi lewat ukuran cm.",
               "Hasil JPG — format yang diterima hampir semua portal pendaftaran.", "Berjalan di browser: foto dan tanda tangan tidak pernah diupload."],
        steps_title="Cara mengubah ukuran pas foto",
        steps=["Baca aturan foto dan tanda tangan di pengumuman resmi.", "Masukkan foto, atur batas KB dan ukurannya (misalnya 3 × 4 cm), lalu unduh.", "Ulangi untuk tanda tangan dengan batasnya sendiri."],
        body="""<h2>Kenapa upload sering ditolak</h2>
<ul><li><strong>Ukuran file</strong> di luar batas — terlalu besar <em>atau</em> terlalu kecil.</li>
<li><strong>Dimensi salah</strong> — formulir memeriksa piksel atau cm pada DPI tertentu.</li>
<li><strong>Format salah</strong> — PNG atau HEIC (iPhone) padahal diminta JPG.</li>
<li><strong>Warna latar</strong> — beberapa pendaftaran meminta latar merah atau biru; pakai foto dengan latar yang sesuai.</li></ul>
<h2>Ukuran pas foto umum</h2>
<div class="tablewrap"><table><thead><tr><th>Ukuran</th><th>Piksel di 300 DPI</th></tr></thead><tbody>
<tr><td>2 × 3 cm</td><td>236 × 354</td></tr><tr><td>3 × 4 cm</td><td>354 × 472</td></tr><tr><td>4 × 6 cm</td><td>472 × 709</td></tr>
</tbody></table></div>""",
        faqs=[id_["faq_rules"], ("Bisa pakai foto HEIC dari iPhone?", "Bisa — foto HEIC otomatis diubah menjadi JPG."), id_["faq_privacy"]]))
    for lang, p in (("hi", hi), ("id", id_)):
        if lang == "hi":
            t = dict(crumb="JPG से PDF 100 KB में", title="JPG से PDF 100 KB में — कई फ़ोटो एक PDF में, सटीक साइज़",
                     desc="एक या कई फ़ोटो या स्कैन को 100 KB से कम की एक PDF में बदलें — ऑनलाइन फ़ॉर्म के लिए। पेज क्रम, A4 साइज़। मुफ़्त, बिना अपलोड।",
                     h1="JPG से PDF — 100 KB से कम", lead="कई फ़ॉर्म दस्तावेज़ 100 KB से कम की एक PDF में माँगते हैं। अपनी फ़ोटो या स्कैन डालें और एक ही बार में सही साइज़ की PDF पाएँ।",
                     facts=["फ़ोटो से PDF बनाकर उसे अपने आप 100 KB से कम करता है।", "1 KB = 1000 बाइट मानकर गिनती, ताकि हर पोर्टल पर पास हो।",
                            "A4, Letter या इमेज जितना पेज; मोबाइल फ़ोटो का रोटेशन अपने आप ठीक।", "आपके डिवाइस पर ही — दस्तावेज़ कभी अपलोड नहीं होते।"],
                     steps_title="JPG से 100 KB की PDF कैसे बनाएँ",
                     steps=["अपनी फ़ोटो डालें (प्रमाण पत्र के पेज, ID का आगे-पीछे…)।", "क्रम सही करें; 100 KB पहले से सेट है।", "“PDF बनाएँ” पर क्लिक करें और डाउनलोड करें।"],
                     body="""<h2>100 KB में फ़िट करने के सुझाव</h2><ul><li>फ़ोटो को काग़ज़ के किनारों तक क्रॉप करें।</li><li>1–2 पेज रखें; हर पेज इसी 100 KB में से हिस्सा लेता है।</li><li>टेक्स्ट दस्तावेज़ के लिए “छोटी फ़ाइल” क्वालिटी चुनें।</li></ul>""",
                     faq=("अगर 100 KB तक न पहुँचे तो?", "आपको संदेश दिखेगा। कम पेज रखें, फ़ोटो क्रॉप करें या “छोटी फ़ाइल” क्वालिटी चुनकर फिर कोशिश करें।"))
        else:
            t = dict(crumb="JPG ke PDF 100 KB", title="JPG ke PDF 100 KB — Gabung Foto Jadi PDF, Ukuran Pas",
                     desc="Ubah satu atau banyak foto atau hasil scan menjadi satu PDF di bawah 100 KB untuk formulir online. Atur urutan, ukuran A4. Gratis, tanpa upload.",
                     h1="JPG ke PDF di bawah 100 KB", lead="Banyak formulir meminta dokumen dalam satu PDF di bawah 100 KB. Masukkan foto atau hasil scan Anda dan dapatkan PDF yang muat sekaligus.",
                     facts=["Menggabungkan foto menjadi satu PDF lalu otomatis mengompresnya di bawah 100 KB.", "Menghitung 1 KB = 1000 byte agar lolos di semua portal.",
                            "Halaman A4, Letter, atau seukuran gambar; rotasi foto ponsel otomatis diperbaiki.", "Berjalan di perangkat Anda — dokumen tidak pernah diupload."],
                     steps_title="Cara membuat PDF 100 KB dari JPG",
                     steps=["Masukkan foto (halaman ijazah, KTP depan-belakang…).", "Atur urutannya; 100 KB sudah diatur.", "Klik “Buat PDF” lalu unduh."],
                     body="""<h2>Tips agar muat 100 KB</h2><ul><li>Potong foto sampai tepi kertas sebelum ditambahkan.</li><li>Pakai 1–2 halaman; setiap halaman berbagi 100 KB yang sama.</li><li>Pilih kualitas “File kecil” untuk dokumen berisi teks.</li></ul>""",
                     faq=("Bagaimana jika tidak bisa mencapai 100 KB?", "Akan muncul pesan. Kurangi halaman, potong fotonya, atau pilih kualitas “File kecil” lalu coba lagi."))
        out.append(page(lang, "jpg-to-pdf-under-100kb", "img2pdf", pdf_max_kb=100, crumb=t["crumb"], title=t["title"], desc=t["desc"],
                        h1=t["h1"], lead=t["lead"], facts=t["facts"], steps_title=t["steps_title"], steps=t["steps"], body=t["body"],
                        faqs=[t["faq"], p["faq_privacy"]]))
    out.append(page("pt", "jpg-to-pdf", "img2pdf", crumb="JPG para PDF",
        title="Converter JPG para PDF Grátis — Páginas Ilimitadas, Sem Upload",
        desc="Transforme fotos JPG, PNG e do celular em um único PDF — 40, 100 ou mais páginas, sem limite. A4, Carta ou tamanho da imagem. Grátis e privado.",
        h1="Converter JPG e imagens para PDF",
        lead="Junte fotos, documentos escaneados e prints em um PDF organizado — na ordem e no tamanho de página que você quiser.",
        facts=["Sem limite de páginas: junte 40, 100 ou mais imagens em um PDF, grátis.", "Aceita JPG, PNG, WebP, GIF e fotos HEIC do iPhone.",
               "Páginas A4, Carta ou do tamanho da imagem; fotos deitadas viram páginas deitadas.", "Roda no seu dispositivo — as imagens nunca são enviadas."],
        steps_title="Como converter JPG para PDF",
        steps=["Solte as imagens na caixa acima.", "Organize a ordem e escolha tamanho de página, margem e qualidade.", "Clique em “Criar PDF” e baixe."],
        body="""<h2>Fotos de documentos → um PDF</h2>
<p>Fotografou os documentos com o celular? Junte tudo em um PDF aqui. Precisa de um limite? Preencha “Tamanho máximo do PDF”
ou depois use <a href="/pt/compress-pdf-to-100kb/">Comprimir PDF para 100 KB</a>.</p>""",
        faqs=[("Quantas imagens posso converter de uma vez?", "Não há limite fixo — 40, 100 ou mais imagens funcionam. Lotes muito grandes só demoram mais e dependem da memória do aparelho."),
              ("Por que minha foto fica de lado em outros conversores?", "O celular guarda a rotação como informação extra. Nós aplicamos essa rotação antes de criar o PDF, então as páginas saem na posição certa."),
              pt["faq_privacy"]]))
    out.append(page("pt", "merge-pdf", "merge", crumb="Juntar PDF",
        title="Juntar PDF Online Grátis — Sem Limite de Tamanho, Sem Upload",
        desc="Junte vários PDFs em um só, sem limite de tamanho ou de arquivos. Reordene, mantenha texto e links. Grátis e no seu navegador — nada é enviado.",
        h1="Juntar arquivos PDF",
        lead="Combine PDFs em um único documento na ordem que você escolher — com privacidade, no seu dispositivo.",
        facts=["Junte quantos PDFs quiser; reordene com ↑ ↓ ou em ordem alfabética.", "As páginas são copiadas como estão: texto, fontes e qualidade não mudam.",
               "Sem limite de tamanho além da memória do seu aparelho.", "Roda no navegador — os arquivos nunca são enviados."],
        steps_title="Como juntar PDFs",
        steps=["Solte os PDFs que quer juntar.", "Coloque na ordem com ↑ ↓ (ou Ordenar A→Z).", "Clique em “Juntar PDFs” e baixe."],
        body="""<h2>Junte e depois comprima</h2>
<p>Muitos formulários querem todos os documentos em um só arquivo com limite de tamanho. Junte aqui e depois use
<a href="/pt/compress-pdf-to-200kb/">Comprimir PDF para 200 KB</a> no arquivo unido.</p>""",
        faqs=[("Tem limite de tamanho para juntar?", "Não há limite fixo. Os arquivos são unidos no seu próprio aparelho, então o limite é só a memória dele — centenas de MB funcionam na maioria dos computadores."),
              ("Juntar reduz a qualidade?", "Não. As páginas são copiadas sem recompressão."), pt["faq_privacy"]]))
    return out


SETS = {"hi": {"pdf": [50, 100, 200], "img": [20, 50]},
        "pt": {"pdf": [100, 200, 500, 1024], "img": [100]},
        "id": {"pdf": [100, 200, 1024], "img": [100, 200]}}


def i18n_pages():
    pages = homes()
    for lang, s in SETS.items():
        pages += [pdf_size(lang, kb) for kb in s["pdf"]]
        pages += [img_size(lang, kb) for kb in s["img"]]
    pages += extras()
    return pages
