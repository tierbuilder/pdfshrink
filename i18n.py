"""Interface translations. Keys are the English strings used in templates and scripts;
anything missing falls back to English. JS keys are also embedded in each translated page
(<script type="application/json" id="i18n">) and read by window.__t in engine.js."""

LANGS = {
    # code: (native name, English name, hreflang, og:locale)
    "hi": ("हिन्दी", "Hindi", "hi", "hi_IN"),
    "pt": ("Português", "Portuguese", "pt-BR", "pt_BR"),
    "id": ("Bahasa Indonesia", "Indonesian", "id", "id_ID"),
}

# Strings the scripts look up at runtime (window.__t). Placeholders: {x}, {n}, {i}, {f}, {p}.
JS_KEYS = [
    "Please choose PDF files.", "Waiting…", "🔒 Password-protected", "Kept original", "Done (pages flattened)",
    "Done — text & links kept", "✓ Under {x}", "✗ Above {x}", "Download", "Open Unlock PDF →",
    "Could not read this PDF. It may be damaged or password-protected (open password).", "Zipping…",
    "Download all (ZIP)", "Free PDF compressor that never uploads your files", "Link copied — thanks for sharing!",
    "This PDF is already well optimized — we kept the original.",
    "This PDF needs a password to open. Unlock it first (Unlock PDF tool), then compress the unlocked copy.",
    "Flattening pages…", "Optimizing…", "Protected PDF — flattening…", "Flattening…",
    "This PDF has security restrictions, so pages were flattened.",
    "Your file was already under the target size — we still removed hidden waste.",
    "Your file was already under the target size.", "Trying lossless cleanup…",
    "Re-encoding images (level {i}/{n})…", "Flattening pages (level {i}/{n})…",
    "Pages were flattened to images to reach the target — text is no longer selectable.",
    "Could not reach the target without flattening. Enable “Allow flattening” or split the PDF.",
    "Could not reach the target — this is the smallest readable version. Try splitting the PDF into fewer pages.",
    "This image format is not supported by your browser.",
    "Could not read this HEIC photo. Try exporting it as JPG from your Photos app.",
    "Below the {x} minimum — use larger dimensions or a bigger photo.",
    "Could not fit these dimensions under {x} — try smaller dimensions.", "Could not reach {x}.",
    "Please choose image files (JPG, PNG, WebP…).", "Processing…", "Preview of {x}", "Could not read this image.",
    "Move {x} up", "Move {x} down", "Remove {x}", "Please choose {x}.", "PDF files", "image files (JPG, PNG, WebP…)",
    "“{x}” is password-protected or encrypted. Remove the protection first.", "Merging…",
    "✓ Merged {f} files · {p} pages", "Download merged PDF", "Compress it →", "Could not merge these files.",
    "Creating PDF…", "Fitting under {x} KB…", "✓ under {x} KB",
    "✗ could not reach {x} KB — try fewer images or “Small file” quality", "{n} page", "{n} pages", "Download PDF",
    "Need it smaller? →", "Could not create the PDF.", "/", "/compress-pdf-to-100kb/",
]

UI = {
    # ------------------------------------------------------------------ Hindi
    "hi": {
        # page chrome
        "Skip to content": "मुख्य सामग्री पर जाएँ", "Home": "होम", "Key facts": "मुख्य बातें",
        "Frequently asked questions": "अक्सर पूछे जाने वाले सवाल", "More free tools": "और मुफ़्त टूल",
        "Last updated": "आख़िरी अपडेट", "All tools (English)": "सभी टूल (English)", "Language": "भाषा",
        "🔒 No upload": "🔒 कोई अपलोड नहीं", "∞ No limits": "∞ कोई लिमिट नहीं", "✓ No sign-up": "✓ साइन-अप नहीं",
        "🎯 Exact size": "🎯 सटीक साइज़", "🎯 Exact KB": "🎯 सटीक KB", "↕ Reorder": "↕ क्रम बदलें",
        "📄 A4 / Letter": "📄 A4 / Letter",
        "Tools in this language": "हिन्दी में टूल", "Help &amp; legal": "मदद और नियम",
        "About": "हमारे बारे में (English)", "Contact": "संपर्क (English)", "Privacy": "प्राइवेसी (English)",
        "Terms": "शर्तें (English)",
        "Free PDF and image tools that run in your browser. Your files never leave your device.":
            "मुफ़्त PDF और इमेज टूल जो आपके ब्राउज़र में चलते हैं। आपकी फ़ाइलें आपके डिवाइस से बाहर नहीं जातीं।",
        "Not affiliated with any government body, exam authority or brand mentioned on this site.":
            "यह साइट किसी सरकारी विभाग, परीक्षा संस्था या यहाँ बताए गए किसी ब्रांड से जुड़ी नहीं है।",
        "Disclaimer:": "अस्वीकरण:",
        "{name} is a personal hobby project, provided free and “as is”, without warranty of any kind. Always check the result and keep your original files.":
            "{name} एक निजी हॉबी प्रोजेक्ट है, जो मुफ़्त और “जैसा है” के आधार पर दिया जाता है — किसी भी तरह की वारंटी के बिना। हमेशा नतीजा जाँचें और अपनी मूल फ़ाइल संभालकर रखें।",
        "Full terms": "पूरी शर्तें",
        # compress tool
        "PDF compressor": "PDF कंप्रेसर", "Choose PDF files to compress": "कंप्रेस करने के लिए PDF फ़ाइलें चुनें",
        'Drop PDFs here or <span class="link">choose files</span>': 'PDF यहाँ छोड़ें या <span class="link">फ़ाइलें चुनें</span>',
        "Tap to choose PDFs": "PDF चुनने के लिए टैप करें",
        "🔒 Compressed on your device — never uploaded · No limits · No sign-up":
            "🔒 आपके डिवाइस पर ही कंप्रेस — कभी अपलोड नहीं · कोई लिमिट नहीं · साइन-अप नहीं",
        "Compression level": "कंप्रेशन लेवल", "Recommended": "अनुशंसित", "Best balance": "सबसे संतुलित",
        "Strong": "ज़्यादा", "Smallest file": "सबसे छोटी फ़ाइल", "Light": "हल्का", "Best quality": "सबसे अच्छी क्वालिटी",
        "Exact size": "सटीक साइज़", "e.g. 100 KB": "जैसे 100 KB", "Max size": "अधिकतम साइज़",
        "Target size": "लक्ष्य साइज़", "Unit": "इकाई", "More options": "और विकल्प",
        "Grayscale images (much smaller for scanned text)": "इमेज ग्रेस्केल करें (स्कैन किए टेक्स्ट के लिए बहुत छोटी फ़ाइल)",
        "Remove metadata, thumbnails &amp; editing data": "मेटाडेटा, थंबनेल और एडिटिंग डेटा हटाएँ",
        "Allow flattening pages to reach an exact size (text becomes an image)":
            "सटीक साइज़ के लिए पेज को इमेज में बदलने दें (टेक्स्ट इमेज बन जाएगा)",
        "Lossless only — don't touch images": "सिर्फ़ लॉसलेस — इमेज को न छुएँ",
        "Re-compress with new settings": "नई सेटिंग से फिर कंप्रेस करें", "Share this free tool": "यह मुफ़्त टूल शेयर करें",
        "Download all (ZIP)": "सब डाउनलोड करें (ZIP)", "Clear": "साफ़ करें",
        # shared dropzone + image tool
        "🔒 Processed on your device — never uploaded · Free · No sign-up":
            "🔒 आपके डिवाइस पर ही प्रोसेस — कभी अपलोड नहीं · मुफ़्त · साइन-अप नहीं",
        'Drop images here or <span class="link">choose files</span>': 'इमेज यहाँ छोड़ें या <span class="link">फ़ाइलें चुनें</span>',
        "Tap to choose images": "इमेज चुनने के लिए टैप करें", "Image resizer": "इमेज रिसाइज़र", "Photo resizer": "फ़ोटो रिसाइज़र",
        "optional": "वैकल्पिक", "Quality": "क्वालिटी", "High / lossless PNG": "हाई / लॉसलेस PNG", "Balanced": "संतुलित",
        "Small file": "छोटी फ़ाइल", "Smallest": "सबसे छोटी", "Format": "फ़ॉर्मेट",
        "JPG (accepted everywhere)": "JPG (हर जगह मान्य)", "PNG (keeps transparency)": "PNG (पारदर्शिता बनी रहती है)",
        "WebP (smallest, for websites)": "WebP (सबसे छोटी, वेबसाइट के लिए)",
        "Size, DPI, name &amp; date on photo": "साइज़, DPI, फ़ोटो पर नाम और तारीख़",
        "Width": "चौड़ाई", "Height": "ऊँचाई", "auto": "अपने आप", "Size unit": "साइज़ की इकाई",
        "Keep proportions": "अनुपात बनाए रखें", "Crop to exact size": "सटीक साइज़ में क्रॉप करें", "Resize mode": "रिसाइज़ मोड",
        "keep": "जैसा है", "Needed for cm/mm/inch sizes (default 200) and written into the file.":
            "cm/mm/inch साइज़ के लिए ज़रूरी (डिफ़ॉल्ट 200) — फ़ाइल में सेव होता है।",
        "Examples:": "उदाहरण:", "— always use the exact numbers in your form's instructions.":
            "— हमेशा अपने फ़ॉर्म के निर्देशों में दिए सटीक नंबर ही इस्तेमाल करें।",
        "Min size": "न्यूनतम साइज़", "none": "कोई नहीं", "KB (if your form has a minimum)": "KB (अगर फ़ॉर्म में न्यूनतम सीमा है)",
        "Print name and date at the bottom of the photo": "फ़ोटो के नीचे नाम और तारीख़ लिखें",
        "Name": "नाम", "Date": "तारीख़", "Date format": "तारीख़ का फ़ॉर्मेट", "Apply new settings": "नई सेटिंग लागू करें",
        "Photo 3.5×4.5 cm · 200 DPI": "फ़ोटो 3.5×4.5 cm · 200 DPI", "Photo 200×230 px": "फ़ोटो 200×230 px",
        "Signature 140×60 px": "हस्ताक्षर 140×60 px", "Signature 3.5×1.5 cm · 200 DPI": "हस्ताक्षर 3.5×1.5 cm · 200 DPI",
        # images → PDF and merge
        "Images to PDF": "इमेज से PDF", "Page size": "पेज साइज़", "Same as image": "इमेज जैसा", "Margin": "मार्जिन",
        "None": "कोई नहीं", "Small": "छोटा", "Large": "बड़ा", "High": "हाई", "Medium": "मीडियम",
        "Max PDF size": "अधिकतम PDF साइज़", "Create PDF": "PDF बनाएँ", "Sort A→Z": "A→Z क्रम", "Merge PDF": "PDF मर्ज करें",
        'Drop PDFs to merge or <span class="link">choose files</span>': 'मर्ज करने के लिए PDF छोड़ें या <span class="link">फ़ाइलें चुनें</span>',
        "Merge PDFs": "PDF मर्ज करें",
        # fit-table verdicts
        "✅ Yes, comfortably": "✅ हाँ, आराम से", "✅ Yes, if the file has only a few pages": "✅ हाँ, अगर पेज कम हैं",
        "⚠️ One page at most, at reduced quality": "⚠️ ज़्यादा से ज़्यादा एक पेज, कम क्वालिटी में",
        "⚠️ Only a page or two, at reduced quality": "⚠️ सिर्फ़ एक-दो पेज, कम क्वालिटी में",
        "❌ Unlikely — even one page needs heavy quality loss": "❌ मुश्किल — एक पेज के लिए भी क्वालिटी बहुत घटानी पड़ेगी",
        "✅ Short documents usually fit, text stays sharp": "✅ छोटे दस्तावेज़ आमतौर पर फ़िट हो जाते हैं, टेक्स्ट साफ़ रहता है",
        "under 1": "1 से कम",
        # JS
        "Please choose PDF files.": "कृपया PDF फ़ाइलें चुनें।", "Waiting…": "इंतज़ार…",
        "🔒 Password-protected": "🔒 पासवर्ड से सुरक्षित", "Kept original": "मूल फ़ाइल रखी गई",
        "Done (pages flattened)": "हो गया (पेज इमेज में बदले)", "Done — text & links kept": "हो गया — टेक्स्ट और लिंक सुरक्षित",
        "✓ Under {x}": "✓ {x} से कम", "✗ Above {x}": "✗ {x} से ज़्यादा", "Download": "डाउनलोड",
        "Open Unlock PDF →": "Unlock PDF खोलें →",
        "Could not read this PDF. It may be damaged or password-protected (open password).":
            "यह PDF पढ़ी नहीं जा सकी। यह ख़राब हो सकती है या पासवर्ड से सुरक्षित है।",
        "Zipping…": "ZIP बन रहा है…", "Free PDF compressor that never uploads your files": "मुफ़्त PDF कंप्रेसर जो आपकी फ़ाइल कभी अपलोड नहीं करता",
        "Link copied — thanks for sharing!": "लिंक कॉपी हो गया — शेयर करने के लिए धन्यवाद!",
        "This PDF is already well optimized — we kept the original.": "यह PDF पहले से ही ऑप्टिमाइज़ है — हमने मूल फ़ाइल रखी है।",
        "This PDF needs a password to open. Unlock it first (Unlock PDF tool), then compress the unlocked copy.":
            "इस PDF को खोलने के लिए पासवर्ड चाहिए। पहले इसे अनलॉक करें (Unlock PDF टूल), फिर अनलॉक की गई कॉपी कंप्रेस करें।",
        "Flattening pages…": "पेज इमेज में बदले जा रहे हैं…", "Optimizing…": "ऑप्टिमाइज़ हो रहा है…",
        "Protected PDF — flattening…": "सुरक्षित PDF — पेज इमेज में बदले जा रहे हैं…", "Flattening…": "इमेज में बदल रहा है…",
        "This PDF has security restrictions, so pages were flattened.": "इस PDF पर सुरक्षा पाबंदियाँ हैं, इसलिए पेज इमेज में बदले गए।",
        "Your file was already under the target size — we still removed hidden waste.":
            "आपकी फ़ाइल पहले से लक्ष्य साइज़ से कम थी — फिर भी हमने छिपा हुआ फ़ालतू डेटा हटा दिया।",
        "Your file was already under the target size.": "आपकी फ़ाइल पहले से लक्ष्य साइज़ से कम थी।",
        "Trying lossless cleanup…": "लॉसलेस सफ़ाई हो रही है…",
        "Re-encoding images (level {i}/{n})…": "इमेज दोबारा एनकोड हो रही हैं (लेवल {i}/{n})…",
        "Flattening pages (level {i}/{n})…": "पेज इमेज में बदले जा रहे हैं (लेवल {i}/{n})…",
        "Pages were flattened to images to reach the target — text is no longer selectable.":
            "लक्ष्य तक पहुँचने के लिए पेज इमेज में बदले गए — अब टेक्स्ट सिलेक्ट नहीं होगा।",
        "Could not reach the target without flattening. Enable “Allow flattening” or split the PDF.":
            "पेज को इमेज में बदले बिना लक्ष्य तक नहीं पहुँच सके। “पेज को इमेज में बदलने दें” चालू करें या PDF को बाँट दें।",
        "Could not reach the target — this is the smallest readable version. Try splitting the PDF into fewer pages.":
            "लक्ष्य तक नहीं पहुँच सके — यह सबसे छोटा पढ़ने लायक वर्शन है। PDF को कम पेजों में बाँटकर देखें।",
        "This image format is not supported by your browser.": "यह इमेज फ़ॉर्मेट आपका ब्राउज़र सपोर्ट नहीं करता।",
        "Could not read this HEIC photo. Try exporting it as JPG from your Photos app.":
            "यह HEIC फ़ोटो पढ़ी नहीं जा सकी। फ़ोटो ऐप से इसे JPG में एक्सपोर्ट करके देखें।",
        "Below the {x} minimum — use larger dimensions or a bigger photo.": "{x} की न्यूनतम सीमा से कम — बड़ा साइज़ या बड़ी फ़ोटो इस्तेमाल करें।",
        "Could not fit these dimensions under {x} — try smaller dimensions.": "इस साइज़ में {x} से कम नहीं हो सका — छोटा साइज़ आज़माएँ।",
        "Could not reach {x}.": "{x} तक नहीं पहुँच सके।",
        "Please choose image files (JPG, PNG, WebP…).": "कृपया इमेज फ़ाइलें चुनें (JPG, PNG, WebP…)।", "Processing…": "प्रोसेस हो रहा है…",
        "Preview of {x}": "{x} का प्रीव्यू", "Could not read this image.": "यह इमेज पढ़ी नहीं जा सकी।",
        "Move {x} up": "{x} को ऊपर करें", "Move {x} down": "{x} को नीचे करें", "Remove {x}": "{x} हटाएँ",
        "Please choose {x}.": "कृपया {x} चुनें।", "PDF files": "PDF फ़ाइलें", "image files (JPG, PNG, WebP…)": "इमेज फ़ाइलें (JPG, PNG, WebP…)",
        "“{x}” is password-protected or encrypted. Remove the protection first.": "“{x}” पासवर्ड से सुरक्षित है। पहले सुरक्षा हटाएँ।",
        "Merging…": "मर्ज हो रहा है…", "✓ Merged {f} files · {p} pages": "✓ {f} फ़ाइलें मर्ज हुईं · {p} पेज",
        "Download merged PDF": "मर्ज की गई PDF डाउनलोड करें", "Compress it →": "इसे कंप्रेस करें →",
        "Could not merge these files.": "ये फ़ाइलें मर्ज नहीं हो सकीं।", "Creating PDF…": "PDF बन रही है…",
        "Fitting under {x} KB…": "{x} KB से कम किया जा रहा है…", "✓ under {x} KB": "✓ {x} KB से कम",
        "✗ could not reach {x} KB — try fewer images or “Small file” quality": "✗ {x} KB तक नहीं पहुँच सके — कम इमेज या “छोटी फ़ाइल” क्वालिटी आज़माएँ",
        "{n} page": "{n} पेज", "{n} pages": "{n} पेज", "Download PDF": "PDF डाउनलोड करें", "Need it smaller? →": "और छोटी चाहिए? →",
        "Could not create the PDF.": "PDF नहीं बन सकी।", "/": "/hi/", "/compress-pdf-to-100kb/": "/hi/compress-pdf-to-100kb/",
    },
    # ------------------------------------------------------------------ Brazilian Portuguese
    "pt": {
        "Skip to content": "Pular para o conteúdo", "Home": "Início", "Key facts": "Principais pontos",
        "Frequently asked questions": "Perguntas frequentes", "More free tools": "Mais ferramentas grátis",
        "Last updated": "Atualizado em", "All tools (English)": "Todas as ferramentas (inglês)", "Language": "Idioma",
        "🔒 No upload": "🔒 Sem upload", "∞ No limits": "∞ Sem limites", "✓ No sign-up": "✓ Sem cadastro",
        "🎯 Exact size": "🎯 Tamanho exato", "🎯 Exact KB": "🎯 KB exato", "↕ Reorder": "↕ Reordenar",
        "📄 A4 / Letter": "📄 A4 / Carta",
        "Tools in this language": "Ferramentas em português", "Help &amp; legal": "Ajuda e termos",
        "About": "Sobre (inglês)", "Contact": "Contato (inglês)", "Privacy": "Privacidade (inglês)", "Terms": "Termos (inglês)",
        "Free PDF and image tools that run in your browser. Your files never leave your device.":
            "Ferramentas grátis de PDF e imagem que funcionam no seu navegador. Seus arquivos nunca saem do seu dispositivo.",
        "Not affiliated with any government body, exam authority or brand mentioned on this site.":
            "Sem vínculo com órgãos do governo, bancas de concurso ou marcas citadas neste site.",
        "Disclaimer:": "Aviso:",
        "{name} is a personal hobby project, provided free and “as is”, without warranty of any kind. Always check the result and keep your original files.":
            "{name} é um projeto pessoal (hobby), oferecido de graça e “no estado em que se encontra”, sem garantia de nenhum tipo. Sempre confira o resultado e guarde seus arquivos originais.",
        "Full terms": "Termos completos",
        "PDF compressor": "Compressor de PDF", "Choose PDF files to compress": "Escolha arquivos PDF para comprimir",
        'Drop PDFs here or <span class="link">choose files</span>': 'Solte os PDFs aqui ou <span class="link">escolha os arquivos</span>',
        "Tap to choose PDFs": "Toque para escolher PDFs",
        "🔒 Compressed on your device — never uploaded · No limits · No sign-up":
            "🔒 Comprimido no seu dispositivo — nunca enviado · Sem limites · Sem cadastro",
        "Compression level": "Nível de compressão", "Recommended": "Recomendado", "Best balance": "Melhor equilíbrio",
        "Strong": "Forte", "Smallest file": "Menor arquivo", "Light": "Leve", "Best quality": "Melhor qualidade",
        "Exact size": "Tamanho exato", "e.g. 100 KB": "ex.: 100 KB", "Max size": "Tamanho máximo", "Target size": "Tamanho alvo",
        "Unit": "Unidade", "More options": "Mais opções",
        "Grayscale images (much smaller for scanned text)": "Imagens em tons de cinza (bem menor para textos escaneados)",
        "Remove metadata, thumbnails &amp; editing data": "Remover metadados, miniaturas e dados de edição",
        "Allow flattening pages to reach an exact size (text becomes an image)":
            "Permitir converter páginas em imagem para atingir o tamanho exato (o texto vira imagem)",
        "Lossless only — don't touch images": "Somente sem perdas — não mexer nas imagens",
        "Re-compress with new settings": "Comprimir de novo com as novas opções", "Share this free tool": "Compartilhar esta ferramenta grátis",
        "Download all (ZIP)": "Baixar tudo (ZIP)", "Clear": "Limpar",
        "🔒 Processed on your device — never uploaded · Free · No sign-up": "🔒 Processado no seu dispositivo — nunca enviado · Grátis · Sem cadastro",
        'Drop images here or <span class="link">choose files</span>': 'Solte as imagens aqui ou <span class="link">escolha os arquivos</span>',
        "Tap to choose images": "Toque para escolher imagens", "Image resizer": "Redimensionador de imagem", "Photo resizer": "Redimensionador de foto",
        "optional": "opcional", "Quality": "Qualidade", "High / lossless PNG": "Alta / PNG sem perdas", "Balanced": "Equilibrada",
        "Small file": "Arquivo pequeno", "Smallest": "Menor possível", "Format": "Formato",
        "JPG (accepted everywhere)": "JPG (aceito em todo lugar)", "PNG (keeps transparency)": "PNG (mantém transparência)",
        "WebP (smallest, for websites)": "WebP (menor, para sites)", "Size, DPI, name &amp; date on photo": "Tamanho, DPI, nome e data na foto",
        "Width": "Largura", "Height": "Altura", "auto": "auto", "Size unit": "Unidade de tamanho", "Keep proportions": "Manter proporções",
        "Crop to exact size": "Recortar no tamanho exato", "Resize mode": "Modo de redimensionamento", "keep": "manter",
        "Needed for cm/mm/inch sizes (default 200) and written into the file.": "Necessário para tamanhos em cm/mm/polegadas (padrão 200) e gravado no arquivo.",
        "Examples:": "Exemplos:", "— always use the exact numbers in your form's instructions.": "— use sempre os números exatos das instruções do seu formulário.",
        "Min size": "Tamanho mínimo", "none": "nenhum", "KB (if your form has a minimum)": "KB (se o formulário tiver um mínimo)",
        "Print name and date at the bottom of the photo": "Escrever nome e data na parte de baixo da foto",
        "Name": "Nome", "Date": "Data", "Date format": "Formato da data", "Apply new settings": "Aplicar novas opções",
        "Photo 3.5×4.5 cm · 200 DPI": "Foto 3,5×4,5 cm · 200 DPI", "Photo 200×230 px": "Foto 200×230 px",
        "Signature 140×60 px": "Assinatura 140×60 px", "Signature 3.5×1.5 cm · 200 DPI": "Assinatura 3,5×1,5 cm · 200 DPI",
        "Images to PDF": "Imagens para PDF", "Page size": "Tamanho da página", "Same as image": "Igual à imagem", "Margin": "Margem",
        "None": "Nenhuma", "Small": "Pequena", "Large": "Grande", "High": "Alta", "Medium": "Média", "Max PDF size": "Tamanho máximo do PDF",
        "Create PDF": "Criar PDF", "Sort A→Z": "Ordenar A→Z", "Merge PDF": "Juntar PDF",
        'Drop PDFs to merge or <span class="link">choose files</span>': 'Solte os PDFs para juntar ou <span class="link">escolha os arquivos</span>',
        "Merge PDFs": "Juntar PDFs",
        "✅ Yes, comfortably": "✅ Sim, com folga", "✅ Yes, if the file has only a few pages": "✅ Sim, se o arquivo tiver poucas páginas",
        "⚠️ One page at most, at reduced quality": "⚠️ No máximo uma página, com qualidade reduzida",
        "⚠️ Only a page or two, at reduced quality": "⚠️ Só uma ou duas páginas, com qualidade reduzida",
        "❌ Unlikely — even one page needs heavy quality loss": "❌ Improvável — até uma página perde muita qualidade",
        "✅ Short documents usually fit, text stays sharp": "✅ Documentos curtos costumam caber, o texto fica nítido",
        "under 1": "menos de 1",
        "Please choose PDF files.": "Escolha arquivos PDF.", "Waiting…": "Aguardando…", "🔒 Password-protected": "🔒 Protegido por senha",
        "Kept original": "Original mantido", "Done (pages flattened)": "Pronto (páginas viraram imagem)",
        "Done — text & links kept": "Pronto — texto e links mantidos", "✓ Under {x}": "✓ Abaixo de {x}", "✗ Above {x}": "✗ Acima de {x}",
        "Download": "Baixar", "Open Unlock PDF →": "Abrir Desbloquear PDF →",
        "Could not read this PDF. It may be damaged or password-protected (open password).": "Não foi possível ler este PDF. Ele pode estar corrompido ou protegido por senha.",
        "Zipping…": "Criando ZIP…", "Free PDF compressor that never uploads your files": "Compressor de PDF grátis que nunca envia seus arquivos",
        "Link copied — thanks for sharing!": "Link copiado — obrigado por compartilhar!",
        "This PDF is already well optimized — we kept the original.": "Este PDF já está bem otimizado — mantivemos o original.",
        "This PDF needs a password to open. Unlock it first (Unlock PDF tool), then compress the unlocked copy.":
            "Este PDF precisa de senha para abrir. Desbloqueie primeiro (ferramenta Unlock PDF) e depois comprima a cópia desbloqueada.",
        "Flattening pages…": "Convertendo páginas em imagem…", "Optimizing…": "Otimizando…",
        "Protected PDF — flattening…": "PDF protegido — convertendo em imagem…", "Flattening…": "Convertendo em imagem…",
        "This PDF has security restrictions, so pages were flattened.": "Este PDF tem restrições de segurança, então as páginas viraram imagem.",
        "Your file was already under the target size — we still removed hidden waste.": "Seu arquivo já estava abaixo do tamanho alvo — mesmo assim removemos dados desnecessários.",
        "Your file was already under the target size.": "Seu arquivo já estava abaixo do tamanho alvo.",
        "Trying lossless cleanup…": "Fazendo limpeza sem perdas…", "Re-encoding images (level {i}/{n})…": "Recomprimindo imagens (nível {i}/{n})…",
        "Flattening pages (level {i}/{n})…": "Convertendo páginas em imagem (nível {i}/{n})…",
        "Pages were flattened to images to reach the target — text is no longer selectable.": "As páginas viraram imagem para atingir o tamanho — o texto não pode mais ser selecionado.",
        "Could not reach the target without flattening. Enable “Allow flattening” or split the PDF.":
            "Não foi possível atingir o tamanho sem converter em imagem. Ative “Permitir converter páginas em imagem” ou divida o PDF.",
        "Could not reach the target — this is the smallest readable version. Try splitting the PDF into fewer pages.":
            "Não foi possível atingir o tamanho — esta é a menor versão legível. Tente dividir o PDF em menos páginas.",
        "This image format is not supported by your browser.": "Seu navegador não suporta este formato de imagem.",
        "Could not read this HEIC photo. Try exporting it as JPG from your Photos app.": "Não foi possível ler esta foto HEIC. Exporte como JPG pelo app Fotos.",
        "Below the {x} minimum — use larger dimensions or a bigger photo.": "Abaixo do mínimo de {x} — use dimensões maiores ou uma foto maior.",
        "Could not fit these dimensions under {x} — try smaller dimensions.": "Não coube abaixo de {x} nessas dimensões — tente dimensões menores.",
        "Could not reach {x}.": "Não foi possível atingir {x}.", "Please choose image files (JPG, PNG, WebP…).": "Escolha arquivos de imagem (JPG, PNG, WebP…).",
        "Processing…": "Processando…", "Preview of {x}": "Prévia de {x}", "Could not read this image.": "Não foi possível ler esta imagem.",
        "Move {x} up": "Mover {x} para cima", "Move {x} down": "Mover {x} para baixo", "Remove {x}": "Remover {x}",
        "Please choose {x}.": "Escolha {x}.", "PDF files": "arquivos PDF", "image files (JPG, PNG, WebP…)": "arquivos de imagem (JPG, PNG, WebP…)",
        "“{x}” is password-protected or encrypted. Remove the protection first.": "“{x}” está protegido por senha. Remova a proteção primeiro.",
        "Merging…": "Juntando…", "✓ Merged {f} files · {p} pages": "✓ {f} arquivos juntados · {p} páginas",
        "Download merged PDF": "Baixar PDF unido", "Compress it →": "Comprimir →", "Could not merge these files.": "Não foi possível juntar estes arquivos.",
        "Creating PDF…": "Criando PDF…", "Fitting under {x} KB…": "Reduzindo para menos de {x} KB…", "✓ under {x} KB": "✓ abaixo de {x} KB",
        "✗ could not reach {x} KB — try fewer images or “Small file” quality": "✗ não chegou a {x} KB — use menos imagens ou a qualidade “Arquivo pequeno”",
        "{n} page": "{n} página", "{n} pages": "{n} páginas", "Download PDF": "Baixar PDF", "Need it smaller? →": "Precisa menor? →",
        "Could not create the PDF.": "Não foi possível criar o PDF.", "/": "/pt/", "/compress-pdf-to-100kb/": "/pt/compress-pdf-to-100kb/",
    },
    # ------------------------------------------------------------------ Indonesian
    "id": {
        "Skip to content": "Langsung ke konten", "Home": "Beranda", "Key facts": "Poin penting",
        "Frequently asked questions": "Pertanyaan umum", "More free tools": "Alat gratis lainnya", "Last updated": "Terakhir diperbarui",
        "All tools (English)": "Semua alat (bahasa Inggris)", "Language": "Bahasa",
        "🔒 No upload": "🔒 Tanpa upload", "∞ No limits": "∞ Tanpa batas", "✓ No sign-up": "✓ Tanpa daftar",
        "🎯 Exact size": "🎯 Ukuran pas", "🎯 Exact KB": "🎯 KB pas", "↕ Reorder": "↕ Atur urutan", "📄 A4 / Letter": "📄 A4 / Letter",
        "Tools in this language": "Alat dalam bahasa Indonesia", "Help &amp; legal": "Bantuan dan ketentuan",
        "About": "Tentang (Inggris)", "Contact": "Kontak (Inggris)", "Privacy": "Privasi (Inggris)", "Terms": "Ketentuan (Inggris)",
        "Free PDF and image tools that run in your browser. Your files never leave your device.":
            "Alat PDF dan gambar gratis yang berjalan di browser Anda. File Anda tidak pernah keluar dari perangkat.",
        "Not affiliated with any government body, exam authority or brand mentioned on this site.":
            "Tidak berafiliasi dengan instansi pemerintah, panitia seleksi, atau merek apa pun yang disebut di situs ini.",
        "Disclaimer:": "Penafian:",
        "{name} is a personal hobby project, provided free and “as is”, without warranty of any kind. Always check the result and keep your original files.":
            "{name} adalah proyek hobi pribadi, disediakan gratis dan “apa adanya”, tanpa jaminan apa pun. Selalu periksa hasilnya dan simpan file asli Anda.",
        "Full terms": "Ketentuan lengkap",
        "PDF compressor": "Kompres PDF", "Choose PDF files to compress": "Pilih file PDF untuk dikompres",
        'Drop PDFs here or <span class="link">choose files</span>': 'Taruh PDF di sini atau <span class="link">pilih file</span>',
        "Tap to choose PDFs": "Ketuk untuk memilih PDF",
        "🔒 Compressed on your device — never uploaded · No limits · No sign-up": "🔒 Dikompres di perangkat Anda — tidak pernah diupload · Tanpa batas · Tanpa daftar",
        "Compression level": "Tingkat kompresi", "Recommended": "Disarankan", "Best balance": "Paling seimbang", "Strong": "Kuat",
        "Smallest file": "File terkecil", "Light": "Ringan", "Best quality": "Kualitas terbaik", "Exact size": "Ukuran pas",
        "e.g. 100 KB": "mis. 100 KB", "Max size": "Ukuran maksimal", "Target size": "Ukuran target", "Unit": "Satuan", "More options": "Opsi lainnya",
        "Grayscale images (much smaller for scanned text)": "Gambar hitam-putih (jauh lebih kecil untuk hasil scan teks)",
        "Remove metadata, thumbnails &amp; editing data": "Hapus metadata, thumbnail, dan data edit",
        "Allow flattening pages to reach an exact size (text becomes an image)": "Izinkan halaman diubah jadi gambar agar ukuran pas (teks menjadi gambar)",
        "Lossless only — don't touch images": "Hanya lossless — jangan ubah gambar",
        "Re-compress with new settings": "Kompres ulang dengan pengaturan baru", "Share this free tool": "Bagikan alat gratis ini",
        "Download all (ZIP)": "Unduh semua (ZIP)", "Clear": "Hapus",
        "🔒 Processed on your device — never uploaded · Free · No sign-up": "🔒 Diproses di perangkat Anda — tidak pernah diupload · Gratis · Tanpa daftar",
        'Drop images here or <span class="link">choose files</span>': 'Taruh gambar di sini atau <span class="link">pilih file</span>',
        "Tap to choose images": "Ketuk untuk memilih gambar", "Image resizer": "Ubah ukuran gambar", "Photo resizer": "Ubah ukuran foto",
        "optional": "opsional", "Quality": "Kualitas", "High / lossless PNG": "Tinggi / PNG lossless", "Balanced": "Seimbang",
        "Small file": "File kecil", "Smallest": "Terkecil", "Format": "Format", "JPG (accepted everywhere)": "JPG (diterima di mana saja)",
        "PNG (keeps transparency)": "PNG (transparansi tetap)", "WebP (smallest, for websites)": "WebP (terkecil, untuk situs web)",
        "Size, DPI, name &amp; date on photo": "Ukuran, DPI, nama dan tanggal di foto", "Width": "Lebar", "Height": "Tinggi", "auto": "otomatis",
        "Size unit": "Satuan ukuran", "Keep proportions": "Pertahankan proporsi", "Crop to exact size": "Potong ke ukuran pas", "Resize mode": "Mode ubah ukuran",
        "keep": "tetap", "Needed for cm/mm/inch sizes (default 200) and written into the file.": "Diperlukan untuk ukuran cm/mm/inci (bawaan 200) dan disimpan di file.",
        "Examples:": "Contoh:", "— always use the exact numbers in your form's instructions.": "— selalu gunakan angka persis dari petunjuk formulir Anda.",
        "Min size": "Ukuran minimal", "none": "tidak ada", "KB (if your form has a minimum)": "KB (jika formulir punya batas minimal)",
        "Print name and date at the bottom of the photo": "Tulis nama dan tanggal di bagian bawah foto",
        "Name": "Nama", "Date": "Tanggal", "Date format": "Format tanggal", "Apply new settings": "Terapkan pengaturan baru",
        "Photo 3.5×4.5 cm · 200 DPI": "Foto 3,5×4,5 cm · 200 DPI", "Photo 200×230 px": "Foto 200×230 px",
        "Signature 140×60 px": "Tanda tangan 140×60 px", "Signature 3.5×1.5 cm · 200 DPI": "Tanda tangan 3,5×1,5 cm · 200 DPI",
        "Images to PDF": "Gambar ke PDF", "Page size": "Ukuran halaman", "Same as image": "Sama dengan gambar", "Margin": "Margin",
        "None": "Tanpa", "Small": "Kecil", "Large": "Besar", "High": "Tinggi", "Medium": "Sedang", "Max PDF size": "Ukuran PDF maksimal",
        "Create PDF": "Buat PDF", "Sort A→Z": "Urutkan A→Z", "Merge PDF": "Gabung PDF",
        'Drop PDFs to merge or <span class="link">choose files</span>': 'Taruh PDF untuk digabung atau <span class="link">pilih file</span>',
        "Merge PDFs": "Gabungkan PDF",
        "✅ Yes, comfortably": "✅ Ya, dengan mudah", "✅ Yes, if the file has only a few pages": "✅ Ya, jika halamannya sedikit",
        "⚠️ One page at most, at reduced quality": "⚠️ Paling banyak satu halaman, kualitas berkurang",
        "⚠️ Only a page or two, at reduced quality": "⚠️ Hanya satu-dua halaman, kualitas berkurang",
        "❌ Unlikely — even one page needs heavy quality loss": "❌ Sulit — satu halaman pun kualitasnya turun banyak",
        "✅ Short documents usually fit, text stays sharp": "✅ Dokumen pendek biasanya muat, teks tetap tajam",
        "under 1": "kurang dari 1",
        "Please choose PDF files.": "Silakan pilih file PDF.", "Waiting…": "Menunggu…", "🔒 Password-protected": "🔒 Dilindungi kata sandi",
        "Kept original": "File asli dipertahankan", "Done (pages flattened)": "Selesai (halaman jadi gambar)",
        "Done — text & links kept": "Selesai — teks dan tautan tetap", "✓ Under {x}": "✓ Di bawah {x}", "✗ Above {x}": "✗ Di atas {x}",
        "Download": "Unduh", "Open Unlock PDF →": "Buka Unlock PDF →",
        "Could not read this PDF. It may be damaged or password-protected (open password).": "PDF ini tidak bisa dibaca. Mungkin rusak atau dilindungi kata sandi.",
        "Zipping…": "Membuat ZIP…", "Free PDF compressor that never uploads your files": "Kompres PDF gratis yang tidak pernah mengupload file Anda",
        "Link copied — thanks for sharing!": "Tautan disalin — terima kasih sudah membagikan!",
        "This PDF is already well optimized — we kept the original.": "PDF ini sudah optimal — kami mempertahankan file aslinya.",
        "This PDF needs a password to open. Unlock it first (Unlock PDF tool), then compress the unlocked copy.":
            "PDF ini perlu kata sandi untuk dibuka. Buka kuncinya dulu (alat Unlock PDF), lalu kompres salinan yang sudah terbuka.",
        "Flattening pages…": "Mengubah halaman jadi gambar…", "Optimizing…": "Mengoptimalkan…",
        "Protected PDF — flattening…": "PDF terlindungi — mengubah jadi gambar…", "Flattening…": "Mengubah jadi gambar…",
        "This PDF has security restrictions, so pages were flattened.": "PDF ini punya batasan keamanan, jadi halamannya diubah menjadi gambar.",
        "Your file was already under the target size — we still removed hidden waste.": "File Anda sudah di bawah ukuran target — kami tetap membuang data yang tidak perlu.",
        "Your file was already under the target size.": "File Anda sudah di bawah ukuran target.", "Trying lossless cleanup…": "Membersihkan tanpa mengurangi kualitas…",
        "Re-encoding images (level {i}/{n})…": "Mengompres ulang gambar (level {i}/{n})…", "Flattening pages (level {i}/{n})…": "Mengubah halaman jadi gambar (level {i}/{n})…",
        "Pages were flattened to images to reach the target — text is no longer selectable.": "Halaman diubah jadi gambar agar ukurannya tercapai — teks tidak bisa dipilih lagi.",
        "Could not reach the target without flattening. Enable “Allow flattening” or split the PDF.":
            "Ukuran target tidak tercapai tanpa mengubah halaman jadi gambar. Aktifkan “Izinkan halaman diubah jadi gambar” atau pisahkan PDF.",
        "Could not reach the target — this is the smallest readable version. Try splitting the PDF into fewer pages.":
            "Ukuran target tidak tercapai — ini versi terkecil yang masih terbaca. Coba pisahkan PDF menjadi lebih sedikit halaman.",
        "This image format is not supported by your browser.": "Format gambar ini tidak didukung browser Anda.",
        "Could not read this HEIC photo. Try exporting it as JPG from your Photos app.": "Foto HEIC ini tidak bisa dibaca. Coba ekspor sebagai JPG dari aplikasi Foto.",
        "Below the {x} minimum — use larger dimensions or a bigger photo.": "Di bawah batas minimal {x} — gunakan dimensi lebih besar atau foto yang lebih besar.",
        "Could not fit these dimensions under {x} — try smaller dimensions.": "Dengan dimensi ini tidak bisa di bawah {x} — coba dimensi lebih kecil.",
        "Could not reach {x}.": "Tidak bisa mencapai {x}.", "Please choose image files (JPG, PNG, WebP…).": "Silakan pilih file gambar (JPG, PNG, WebP…).",
        "Processing…": "Memproses…", "Preview of {x}": "Pratinjau {x}", "Could not read this image.": "Gambar ini tidak bisa dibaca.",
        "Move {x} up": "Pindahkan {x} ke atas", "Move {x} down": "Pindahkan {x} ke bawah", "Remove {x}": "Hapus {x}",
        "Please choose {x}.": "Silakan pilih {x}.", "PDF files": "file PDF", "image files (JPG, PNG, WebP…)": "file gambar (JPG, PNG, WebP…)",
        "“{x}” is password-protected or encrypted. Remove the protection first.": "“{x}” dilindungi kata sandi. Hapus perlindungannya dulu.",
        "Merging…": "Menggabungkan…", "✓ Merged {f} files · {p} pages": "✓ {f} file digabung · {p} halaman",
        "Download merged PDF": "Unduh PDF gabungan", "Compress it →": "Kompres →", "Could not merge these files.": "File ini tidak bisa digabung.",
        "Creating PDF…": "Membuat PDF…", "Fitting under {x} KB…": "Memperkecil di bawah {x} KB…", "✓ under {x} KB": "✓ di bawah {x} KB",
        "✗ could not reach {x} KB — try fewer images or “Small file” quality": "✗ tidak mencapai {x} KB — kurangi gambar atau pilih kualitas “File kecil”",
        "{n} page": "{n} halaman", "{n} pages": "{n} halaman", "Download PDF": "Unduh PDF", "Need it smaller? →": "Perlu lebih kecil? →",
        "Could not create the PDF.": "PDF tidak bisa dibuat.", "/": "/id/", "/compress-pdf-to-100kb/": "/id/compress-pdf-to-100kb/",
    },
}


def tr_for(lang):
    """Return a translate function for the given language (identity for English)."""
    d = UI.get(lang)
    if not d:
        return lambda s: s
    return lambda s: d.get(s, s)


def js_dict(lang):
    d = UI.get(lang, {})
    return {k: d[k] for k in JS_KEYS if k in d}


def check():
    """Fail loudly if a language is missing any runtime (JS) string."""
    missing = {lang: [k for k in JS_KEYS if k not in UI[lang]] for lang in UI}
    return {k: v for k, v in missing.items() if v}
