#!/usr/bin/env python3
"""Gera a página de vendas low ticket (estrutura Anúncio Pronto / 50 Viral Fit / Mulher Exemplar) a partir de um pagina.json.

Uso: python3 gerar_pagina.py caminho/pagina.json [--saida pasta]
Saída: index.html único (CSS e JS embutidos). Imagens ficam como caminhos relativos ao index.html.

Marcação de texto aceita em qualquer campo de copy:
  [[texto]]  destaque na cor primária (negrito)
  {{texto}}  destaque na cor de sucesso (negrito)
  __texto__  sublinhado à mão
  **texto**  negrito
"""
import html, json, os, re, sys, urllib.parse

WA_IC = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'
CHECK = '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="10" fill="currentColor" opacity=".14"/><path d="M5.5 10.2l3 3 6-6.4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

AVISOS = []
PRELOAD = []
LARGURAS = (240, 360, 560, 720, 1080, 1600)
try:
    from PIL import Image
except Exception:
    Image = None


def variantes(base, src):
    """Cria versões WebP menores (qualidade 82, visualmente igual) em assets/_otm/ e devolve (srcset, w, h, src_final)."""
    caminho = os.path.join(base, src)
    if Image is None or not os.path.exists(caminho) or not src.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        return "", None, None, src
    try:
        im = Image.open(caminho)
        W, H = im.size
    except Exception:
        return "", None, None, src
    pasta = os.path.join(base, "assets", "_otm")
    os.makedirs(pasta, exist_ok=True)
    nome = re.sub(r"[^a-zA-Z0-9_-]", "-", os.path.splitext(src)[0])
    partes, final = [], src
    for lw in [x for x in LARGURAS if x < W * 0.9] + [W]:
        if lw == W and src.lower().endswith(".webp"):
            partes.append("%s %dw" % (src, W))  # tamanho original: usa o próprio arquivo, sem recomprimir
            final = src
            continue
        rel = "assets/_otm/%s-%d.webp" % (nome, lw)
        dest = os.path.join(base, rel)
        if not os.path.exists(dest) or os.path.getmtime(dest) < os.path.getmtime(caminho):
            v = im.convert("RGBA") if im.mode in ("P", "LA", "RGBA") else im.convert("RGB")
            if lw < W:
                v = v.resize((lw, round(H * lw / W)), Image.LANCZOS)
            v.save(dest, "WEBP", quality=82 if lw < W else 88, method=6)
        partes.append("%s %dw" % (rel, lw))
        final = rel
    return ", ".join(partes), W, H, final


def fmt(s):
    s = html.escape(str(s or ""), quote=False)
    s = re.sub(r"\[\[(.+?)\]\]", r'<em class="c1">\1</em>', s)
    s = re.sub(r"\{\{(.+?)\}\}", r'<em class="c2">\1</em>', s)
    s = re.sub(r"__(.+?)__", r'<span class="lt-sublinha">\1</span>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s


def attr(s):
    return html.escape(str(s or ""), quote=True)


def img(base, src, cls, alt="", w=800, h=800, eager=False, sizes=None, preload=False, depois=False):
    if not src:
        return ""
    externo = re.match(r"^(https?:)?//", src)
    if not externo and not os.path.exists(os.path.join(base, src)):
        AVISOS.append("imagem não encontrada: %s" % src)
    srcset, rw, rh, final = ("", None, None, src) if externo else variantes(base, src)
    if rw:
        w, h = rw, rh
    extra = ' srcset="%s" sizes="%s"' % (attr(srcset), attr(sizes or "(max-width:560px) 92vw, 600px")) if srcset else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    if preload or (eager and not PRELOAD):
        PRELOAD.append('<link rel="preload" as="image" href="%s"%s fetchpriority="high">' % (
            attr(final), ' imagesrcset="%s" imagesizes="%s"' % (attr(srcset), attr(sizes or "(max-width:560px) 92vw, 600px")) if srcset else ""))
    if depois:  # carrega só depois que a página aparece (itens que não são vistos de cara)
        extra = extra.replace(' srcset=', ' data-srcset=')
        return '<img class="%s" data-src="%s"%s alt="%s" width="%d" height="%d" decoding="async">' % (cls, attr(final), extra, attr(alt), w, h)
    return '<img class="%s" src="%s"%s alt="%s" width="%d" height="%d" %s decoding="async">' % (cls, attr(final), extra, attr(alt), w, h, load)


def num(v):
    return float(str(v).replace(".", "").replace(",", "."))


def brl(v):
    s = "%.2f" % v
    i, d = s.split(".")
    i = "{:,}".format(int(i)).replace(",", ".")
    return "%s,%s" % (i, d)


def selo_svg(dias, c_esc, c_pri):
    return ('<svg viewBox="0 0 220 220" role="img" aria-label="Garantia de %(d)s dias"><defs>'
            '<linearGradient id="ltAnel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E8ECF6"/><stop offset=".55" stop-color="#FFFFFF"/><stop offset="1" stop-color="%(p)s"/></linearGradient>'
            '<linearGradient id="ltNum" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%(e)s"/><stop offset="1" stop-color="%(p)s"/></linearGradient>'
            '<path id="ltCirc" d="M110,110 m-92,0 a92,92 0 1,1 184,0 a92,92 0 1,1 -184,0"/></defs>'
            '<circle cx="110" cy="110" r="106" fill="url(#ltAnel)" stroke="#D5DCEB" stroke-width="2"/><circle cx="110" cy="110" r="80" fill="#fff"/>'
            '<text font-family="sans-serif" font-size="11" font-weight="800" letter-spacing="1.5" fill="%(e)s"><textPath href="#ltCirc" textLength="570">RISCO ZERO • RISCO ZERO • RISCO ZERO • RISCO ZERO • RISCO ZERO • RISCO ZERO •</textPath></text>'
            '<text x="110" y="70" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="900" fill="%(e)s">GARANTIA DE</text>'
            '<text x="110" y="166" text-anchor="middle" font-family="sans-serif" font-size="%(fs)d" font-weight="900" fill="url(#ltNum)">%(d)s</text>'
            '<text x="110" y="182" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="900" letter-spacing="3" fill="%(p)s">DIAS</text></svg>'
            ) % {"d": dias, "e": c_esc, "p": c_pri, "fs": 112 if len(str(dias)) == 1 else 84}


def vitrine(base, imagens, cls, intervalo=2000, setas=False, alt="", eager_centro=True):
    """Carrossel 3D em leque, simétrico: o item do meio de frente e os outros iguais para a esquerda e para a direita."""
    if not imagens:
        return ""
    n = len(imagens)
    perto = lambda i: min(i, n - i) <= 1  # o do centro e um de cada lado carregam na hora
    itens = "".join('<figure class="lt-vit-i">%s</figure>' % img(base, x, "", alt, 1080, 1920, i == 0 and eager_centro, "(max-width:640px) 176px, (max-width:1024px) 224px, 256px", depois=not perto(i)) for i, x in enumerate(imagens))
    ctrl = ('<div class="lt-vit-ctrl"><button type="button" data-vit-ant aria-label="Anterior">‹</button><span class="lt-vit-dots">%s</span><button type="button" data-vit-prox aria-label="Próximo">›</button></div>'
            % "".join("<i></i>" for _ in imagens)) if setas else ""
    return '<div class="lt-vit %s" data-vit data-intervalo="%d"><div class="lt-vit-palco">%s</div>%s</div>' % (cls, int(intervalo), itens, ctrl)


def fonte_local(base, familia, pesos=(400, 500, 600, 700, 800)):
    """Baixa a fonte do Google uma vez para assets/fonts e devolve (@font-face, preloads). Sem internet: ("", "")."""
    import urllib.request
    pasta = os.path.join(base, "assets", "fonts")
    css_cache = os.path.join(pasta, "%s.css" % familia.replace(" ", "-"))
    try:
        if not os.path.exists(css_cache):
            os.makedirs(pasta, exist_ok=True)
            url = "https://fonts.googleapis.com/css2?family=%s:wght@%s&display=swap" % (familia.replace(" ", "+"), ";".join(map(str, pesos)))
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"})
            css = urllib.request.urlopen(req, timeout=20).read().decode()
            blocos = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*{[^}]*})", css)
            saida = []
            for sub, bloco in blocos:
                if sub not in ("latin", "latin-ext"):
                    continue
                furl = re.search(r"url\((https://[^)]+\.woff2)\)", bloco).group(1)
                peso = re.search(r"font-weight:\s*(\d+)", bloco).group(1)
                nome = "%s-%s-%s.woff2" % (familia.replace(" ", "-"), peso, sub)
                open(os.path.join(pasta, nome), "wb").write(urllib.request.urlopen(furl, timeout=20).read())
                saida.append(bloco.replace(furl, "assets/fonts/" + nome))
            open(css_cache, "w").write("\n".join(saida))
        css = open(css_cache).read()
        pre = "".join('<link rel="preload" as="font" type="font/woff2" href="assets/fonts/%s-%d-latin.woff2" crossorigin>' % (familia.replace(" ", "-"), p) for p in (600, 800))
        return css, pre
    except Exception as e:
        AVISOS.append("fonte não baixada (%s): usando o Google Fonts" % e)
        return "", ""


def gerar(cfg, base):
    if cfg.get("modelo") == "v2":  # réplica fiel do design do Instravel (scripts/modelo_v2.py)
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import modelo_v2
        return modelo_v2.render(cfg, base, sys.modules[__name__])
    C = {"primaria": "#0042FF", "escura": "#03163F", "fundo": "#F7F3EF", "sucesso": "#16A34A", "destaque": "#16A34A",
         "acento": "#7C3AED", "alerta": "#EF2B2D", "laranja": "#F97316", "texto": "#1B2238", "suave": "#55607A", "linha": "#E6E0D8",
         "destaque_foto": "#FFF3A6", "pausa": "#12294F"}
    C.update(cfg.get("cores", {}))
    fonte = cfg.get("fonte", "Inter")
    produto = cfg["produto"]
    of = cfg["oferta"]
    checkout = cfg.get("checkout", "")
    S = []
    B = {}
    AV = " lt-btn-av" if cfg.get("botao_avancar") == "primaria" else ""

    def botao(texto, cls="", final=False):
        if final and checkout:
            return '<a class="lt-btn%s" href="%s" data-lt-checkout>%s<span aria-hidden="true">→</span></a>' % (cls, attr(checkout), fmt(texto))
        if final:
            AVISOS.append("checkout vazio: botão da oferta ficou sem link")
        return '<a class="lt-btn%s%s" href="#oferta">%s<span aria-hidden="true">↓</span></a>' % (cls, AV, fmt(texto))

    # 1. faixa
    aba = ""
    if cfg.get("faixa"):
        if cfg.get("faixa_estilo") == "aba":
            aba = '<p class="lt-faixa-aba">%s</p>' % fmt(cfg["faixa"])
        else:
            S.append('<p class="lt-faixa">%s</p>' % fmt(cfg["faixa"]))

    # 2. hero
    h = cfg["hero"]
    v = h.get("visual", {})
    vis = ""
    if v.get("tipo") == "pessoa_telas":
        notifs = "".join('<span class="lt-notif lt-n%d">%s<b data-conta="%s">%s</b></span>' % (i + 1, WA_IC if v.get("icone_notif", "whatsapp") == "whatsapp" else "🔔", n, n) for i, n in enumerate(v.get("notificacoes", [])[:3]))
        selos = "".join('<span class="lt-badge lt-b%d">%s</span>' % (i + 1, fmt(t)) for i, t in enumerate(v.get("selos", [])[:3]))
        telas = "".join('<div class="lt-fone lt-f%d"><div class="lt-tela">%s</div></div>' % (i + 1, img(base, t, "lt-tela-img", "", 520, 650, True)) for i, t in enumerate(v.get("telas", [])[:2]))
        vis = '<div class="lt-palco" aria-hidden="true">%s%s%s<div class="lt-fones">%s</div></div>' % (notifs, selos, img(base, v.get("pessoa"), "lt-pessoa", "", 480, 480, True), telas)
    elif v.get("tipo") == "imagem":
        vis = '<div class="lt-hero-img">%s</div>' % img(base, v.get("imagem"), "", produto, 900, 700, True, "(max-width:560px) 92vw, 460px")
    depois = ""
    if v.get("tipo") == "vitrine":
        vis = vitrine(base, v.get("imagens", []), "lt-vit-topo", v.get("intervalo", 2000), False, produto)
        if v.get("faixa"):
            fx = "".join(img(base, x, "", "", 300, 533, sizes="(max-width:768px) 117px, 144px", depois=True) for x in v["faixa"])
            depois = '<div class="lt-marquee lt-marquee-v" aria-hidden="true"><div class="lt-marquee-in">%s%s</div></div>' % (fx, fx)
    logo = img(base, h.get("logo"), "lt-logo", produto, 480, 152, True) if h.get("logo") else ""
    sub2 = '<br><b>%s</b>' % fmt(h["sub_destaque"]) if h.get("sub_destaque") else ""
    abaixo = '<a class="lt-hero-link" href="#dobra2">%s</a>' % fmt(h["link_abaixo"]) if h.get("link_abaixo") else ""
    fundo = ""
    if h.get("fundo"):
        fundo = '<div class="lt-bg" aria-hidden="true">%s</div>' % img(base, h["fundo"], "", "", 1920, 1080, True, "100vw", preload=True)
    S.append('''<section class="lt-hero%s">%s%s<div class="lt-w lt-hero-c">%s
<h1>%s</h1>
<p class="lt-sub"><span>%s</span>%s</p>
%s
<a class="lt-btn lt-btn-topo%s" href="#dobra2">%s<span aria-hidden="true">↓</span></a>%s
</div>%s</section>''' % (" lt-hero-foto" if fundo else "", fundo, aba, logo, fmt(h["titulo"]), fmt(h.get("sub", "")), sub2, vis,
        AV, fmt(h.get("botao", "Quero o meu " + produto)), abaixo, depois))

    primeira = ""

    # 3. depoimentos (só prints e falas reais)
    d = cfg.get("depoimentos") or {}
    if d.get("prints") or d.get("cartoes"):
        prints = "".join('<div class="lt-dep-print">%s</div>' % img(base, p, "", "Depoimento de cliente", 400, 710, sizes="240px") for p in d.get("prints", []))
        cartoes = "".join('<div class="lt-dep-card"><div class="lt-dep-top">%s<span><b>%s</b><small>%s</small></span></div><p class="lt-dep-est">★★★★★</p><p>%s</p></div>' % (
            img(base, c.get("foto"), "lt-dep-foto", "", 80, 80) if c.get("foto") else '<i class="lt-dep-ini">%s</i>' % attr(c.get("nome", "?")[:1]),
            fmt(c.get("nome")), fmt(c.get("usuario", "")), fmt(c.get("texto"))) for c in d.get("cartoes", []))
        nt = d.get("nota") or {}
        nota = ('<div class="lt-nota"><b>%s</b><span>%s</span><span class="lt-nota-est" aria-label="5 estrelas">★★★★★</span><span>%s</span></div>' % (
            fmt(nt.get("valor", "5,0")), fmt(nt.get("linha1", "")), fmt(nt.get("linha2", "")))) if nt else ""
        if d.get("formato") == "carrossel3d" and d.get("prints"):
            bloco_prints = vitrine(base, d["prints"], "lt-vit-dep", d.get("intervalo", 3000), True, "Story de cliente", False)
        else:
            bloco_prints = '<div class="lt-trilho">%s</div>' % prints if prints else ""
        auto = " data-auto" if d.get("cartoes_auto") else ""
        B["depoimentos"] = '''<section class="lt-sec lt-dep"%s><div class="lt-w">
%s<p class="lt-tag">%s</p><h2 class="lt-h2">%s</h2>
%s%s%s</div></section>''' % (primeira, nota, fmt(d.get("tag", "Depoimentos")), fmt(d.get("titulo", "Veja o resultado de quem já usa")),
            bloco_prints, '<div class="lt-trilho lt-trilho-c"%s>%s</div>' % (auto, cartoes) if cartoes else "",
            "" if (d.get("formato") == "carrossel3d" and not cartoes) else '<p class="lt-arraste">Arraste para ver mais →</p>')
        primeira = ""

    # 3b. prova social em formato de demonstração do produto (sem depoimento real): páginas/telas do próprio produto
    dm = cfg.get("demonstracao") or {}
    if dm.get("itens") and not (d.get("prints") or d.get("cartoes")):
        figs = "".join('<figure class="lt-demo-f"><div class="lt-demo-img">%s</div><figcaption>%s</figcaption></figure>' % (
            img(base, x["imagem"], "", x.get("legenda", ""), 520, 650), fmt(x.get("legenda", ""))) for x in dm["itens"])
        B["demonstracao"] = ('''<section class="lt-sec lt-dep lt-demo"%s><div class="lt-w">
<p class="lt-tag">%s</p><h2 class="lt-h2">%s</h2>%s
<div class="lt-trilho">%s</div><p class="lt-arraste">Arraste para ver mais →</p></div></section>''' % (
            primeira, fmt(dm.get("tag", "Veja por dentro")), fmt(dm.get("titulo", "Veja o [[material por dentro]]")),
            '<p class="lt-demo-sub">%s</p>' % fmt(dm["sub"]) if dm.get("sub") else "", figs))
        primeira = ""

    # 4. dor + problema x virada
    dor = cfg.get("dor")
    if dor:
        cards = "".join('<div class="lt-dor-card">%s<p>"%s"</p></div>' % (
            img(base, c["foto"], "lt-dor-foto", "", 800, 600) if c.get("foto") else '<span class="lt-dor-ic" aria-hidden="true">%s</span>' % c.get("emoji", "😣"),
            fmt(c["texto"])) for c in dor.get("cartoes", []))
        vs = ""
        if dor.get("problema") and dor.get("virada"):
            p, vr = dor["problema"], dor["virada"]
            centro = '<div class="lt-vs-img">%s</div>' % img(base, dor["imagem_centro"], "", "", 800, 700) if dor.get("imagem_centro") else ""
            vs = '''<div class="lt-vs%s"><div class="lt-vs-card lt-vs-prob"><span class="lt-vs-tag">%s</span><h3>%s</h3><p>%s</p></div>%s
<div class="lt-vs-card lt-vs-sol"><span class="lt-vs-tag">%s</span><h3>%s</h3><p>%s</p></div></div>''' % (
                " lt-vs3" if centro else "", fmt(p.get("tag", "O problema")), fmt(p["titulo"]), fmt(p["texto"]), centro,
                fmt(vr.get("tag", "A virada")), fmt(vr["titulo"]), fmt(vr["texto"]))
        B["dor"] = ('''<section class="lt-sec lt-dor"%s><div class="lt-w">
<h2 class="lt-dor-t">%s<span>%s</span></h2>
<div class="lt-dores">%s</div>%s</div></section>''' % (primeira, fmt(dor["titulo"]), fmt(dor.get("titulo_destaque", "")), cards, vs))
        primeira = ""

    # 5. como funciona (3 passos)
    ps = cfg["passos"]
    itens = ps.get("itens", [])
    video = ps.get("video")
    corpo = ""
    vertical = bool(video and video.get("formato") == "vertical")
    if vertical:
        if video.get("embed"):
            vtag = '<div class="lt-vv" data-embed="%s"><button type="button" class="lt-vv-play" aria-label="Assistir ao vídeo">%s<span>▶</span></button></div>' % (
                attr(video["embed"]), img(base, video.get("poster"), "", "", 1080, 1920, sizes="300px") if video.get("poster") else "")
        else:
            vtag = '<div class="lt-vv"><video src="%s" poster="%s" controls playsinline preload="none" width="1080" height="1920"></video></div>' % (attr(video.get("mp4", "")), attr(video.get("poster", "")))
        ics = '<ol class="lt-passos-ic">%s</ol>' % "".join('<li><span class="lt-pic">%s<i>%02d</i></span><b>%s</b></li>' % (it.get("icone", "✨"), i + 1, fmt(it["titulo"])) for i, it in enumerate(itens)) if itens else ""
        pb = ps.get("botao") or {}
        btn = '<a class="lt-btn lt-btn-ac" href="#b-%s">%s<span aria-hidden="true">↓</span></a>' % (attr(pb.get("alvo", "oferta")), fmt(pb["texto"])) if pb.get("texto") else ""
        B["passos"] = '''<section class="lt-sec lt-claro"%s><div class="lt-w"><div class="lt-pv">%s<h2 class="lt-h2 lt-pv-t">%s</h2>
<div class="lt-pv-v">%s%s</div><div class="lt-pv-i">%s</div><div class="lt-pv-b">%s</div></div>%s</div></section>''' % (
            primeira, '<p class="lt-tag lt-pv-tag">%s</p>' % fmt(ps["tag"]) if ps.get("tag") else "", fmt(ps["titulo"]),
            '<p class="lt-pv-l">%s</p>' % fmt(ps["linha"]) if ps.get("linha") else "", vtag, ics, btn,
            '<p class="lt-frase">%s</p>' % fmt(ps["frase"]) if ps.get("frase") else "")
    elif video and video.get("mp4"):
        corpo += '<div class="lt-video"><video id="lt-video-passos" src="%s" poster="%s" muted playsinline loop preload="none" width="1280" height="720" aria-label="%s"></video></div>' % (
            attr(video["mp4"]), attr(video.get("poster", "")), attr("Os 3 passos do " + produto))
        if not os.path.exists(os.path.join(base, video["mp4"])):
            AVISOS.append("vídeo não encontrado: %s" % video["mp4"])
        if ps.get("icones", True) and itens:
            corpo += '<ol class="lt-passos-ic">%s</ol>' % "".join('<li><span class="lt-pic">%s<i>%02d</i></span><b>%s</b></li>' % (it.get("icone", "✨"), i + 1, fmt(it["titulo"])) for i, it in enumerate(itens))
    if not vertical and ps.get("cartoes", not (video and video.get("mp4"))) and itens:
        corpo += '<ol class="lt-passos">%s</ol>' % "".join('<li class="lt-passo"><span class="lt-pn">%d</span><span class="lt-pi">%s</span><p class="lt-pl">PASSO %d</p><h3>%s</h3><p>%s</p></li>' % (
            i + 1, it.get("icone", "✨"), i + 1, fmt(it["titulo"]), fmt(it.get("texto", ""))) for i, it in enumerate(itens))
    frase = '<p class="lt-frase">%s</p>' % fmt(ps["frase"]) if ps.get("frase") else ""
    if not vertical:
        B["passos"] = '<section class="lt-sec lt-claro"%s><div class="lt-w">%s<h2 class="lt-h2">%s</h2>%s%s</div></section>' % (
            primeira, '<p class="lt-tag">%s</p>' % fmt(ps["tag"]) if ps.get("tag") else "", fmt(ps["titulo"]), corpo, frase)
    primeira = ""

    # 5b. categorias em vídeo (momentos do avatar)
    ct = cfg.get("categorias") or {}
    if ct.get("itens"):
        cards = ""
        for x in ct["itens"]:
            if x.get("video"):
                midia = '<video data-src="%s" muted loop playsinline preload="none"%s width="540" height="960" aria-label="%s"></video>' % (
                    attr(x["video"]), ' poster="%s"' % attr(x["poster"]) if x.get("poster") else "", attr(x.get("rotulo", "")))
                if not re.match(r"^(https?:)?//", x["video"]) and not os.path.exists(os.path.join(base, x["video"])):
                    AVISOS.append("vídeo não encontrado: %s" % x["video"])
            else:
                midia = img(base, x.get("imagem"), "", x.get("rotulo", ""), 540, 960, sizes="(max-width:860px) 46vw, 260px")
            cards += '<figure class="lt-cat">%s<figcaption>%s %s</figcaption></figure>' % (midia, x.get("emoji", ""), fmt(x.get("rotulo", "")))
        B["categorias"] = '''<section class="lt-sec lt-cats"><div class="lt-w">%s<h2 class="lt-h2 lt-h2-g">%s</h2>%s
<div class="lt-cats-g">%s</div>%s</div></section>''' % (
            '<p class="lt-tag">%s</p>' % fmt(ct["tag"]) if ct.get("tag") else "", fmt(ct.get("titulo", "")),
            '<p class="lt-demo-sub">%s</p>' % fmt(ct["sub"]) if ct.get("sub") else "", cards,
            '<p class="lt-cats-f">%s</p>' % fmt(ct["fecho"]) if ct.get("fecho") else "")

    # 6. o que você recebe
    r = cfg.get("recebe") or {}
    prop = r.get("proporcao", "4/5")
    bloq = set(r.get("bloquear", [2, 4, 5, 7]))
    gal = ""
    for i, g in enumerate(r.get("galeria", []), 1):
        sobre = ""
        if g.get("faixa") or g.get("titulo"):
            sobre = '<div class="lt-g-arte">%s%s</div>' % ('<span class="lt-g-faixa">%s</span>' % fmt(g["faixa"]) if g.get("faixa") else "", '<b>%s</b>' % fmt(g["titulo"]) if g.get("titulo") else "")
        rot = '<span class="lt-g-rot">%s</span>' % fmt(g["rotulo"]) if g.get("rotulo") else ""
        gal += '<figure class="lt-g%s"><div class="lt-g-img" style="aspect-ratio:%s">%s%s%s</div></figure>' % (" lt-g-lock" if i in bloq else "", prop, img(base, g["imagem"], "", "", 520, 650, sizes="(max-width:860px) 46vw, 260px"), sobre, rot)
    chips = '<ul class="lt-chips">%s</ul>' % "".join("<li>%s</li>" % fmt(c) for c in r["chips"]) if r.get("chips") else ""
    mais = ""
    if r.get("numero"):
        mais = '<div class="lt-mais"><span class="lt-mais-n">%s</span><span class="lt-mais-t"><small>%s</small><b>%s</b></span></div>' % (fmt(r["numero"]), fmt(r.get("numero_linha1", "")), fmt(r.get("numero_linha2", "")))
    rol = ""
    if r.get("faixa_rolante"):
        fx = "".join(img(base, f, "", "", 300, 300, sizes="130px") for f in r["faixa_rolante"])
        rol = '<div class="lt-marquee" aria-hidden="true"><div class="lt-marquee-in">%s%s</div></div>' % (fx, fx)
    extras = ""
    if r.get("extras"):
        extras = '<h3 class="lt-rec-t2">%s</h3><div class="lt-extras">%s</div>' % (fmt(r.get("titulo2", "Tudo pronto para você usar agora e [[já ver resultado]]:")), "".join(
            '<div class="lt-extra">%s<b>%s</b><p>%s</p></div>' % (img(base, e["imagem"], "lt-extra-img", "", 800, 600) if e.get("imagem") else '<span aria-hidden="true">%s</span>' % e.get("emoji", "✅"), fmt(e["titulo"]), fmt(e["texto"])) for e in r["extras"]))
    r = r if r.get("titulo") or r.get("galeria") else None
    if r: B["recebe"] = ('''<section class="lt-sec lt-rec"><div class="lt-w">
<h2 class="lt-h2 lt-h2-g">%s</h2>%s%s%s
<div class="lt-gal">%s</div>%s%s%s%s</div></section>''' % (
        fmt(r["titulo"]), '<p class="lt-rec-l">%s</p>' % fmt(r["linha"]) if r.get("linha") else "", mais, chips, gal, rol,
        '<p class="lt-gal-nota">%s</p>' % fmt(r["nota"]) if r.get("nota") else "",
        '<p class="lt-frase">%s</p>' % fmt(r["frase"]) if r.get("frase") else "", extras))

    # 7. bônus
    b = cfg.get("bonus")
    if b and b.get("itens"):
        lista = b.get("estilo") == "lista"
        rot = b.get("rotulo", "BÔNUS %d" if lista else "🎁 BÔNUS %d")
        bh = "".join('<div class="lt-bonus"><div class="lt-bonus-txt"><span class="lt-bonus-tag">%s</span><h3>%s</h3><p>%s</p></div>%s</div>' % (
            attr(rot % (i + 1)), fmt(x["titulo"]), fmt(x["texto"]), img(base, x["imagem"], "lt-bonus-img", "", 800, 800, sizes="(max-width:860px) 112px, 340px") if x.get("imagem") else '<div class="lt-bonus-ph" aria-hidden="true">%s</div>' % x.get("emoji", "🎁")) for i, x in enumerate(b["itens"]))
        B["bonus"] = '<section class="lt-sec lt-bon%s"><div class="lt-w">%s<h2 class="lt-h2 lt-h2-g">%s</h2><div class="lt-bonus-g">%s</div></div></section>' % (
            " lt-bon-lista" if lista else "", '<p class="lt-tag">%s</p>' % fmt(b["tag"]) if b.get("tag") else "", fmt(b.get("titulo", "Além do " + produto + ", você ainda recebe [[bônus exclusivos]] 🎁")), bh)

    # 7b. transição (resultado imaginado em uma frase)
    if cfg.get("transicao"):
        B["transicao"] = '<section class="lt-transicao"><div class="lt-w lt-estreito"><p>%s</p></div></section>' % fmt(cfg["transicao"])

    # 8. ancoragem + oferta
    recap = of.get("recap") or []
    if not recap and not of.get("de"):
        AVISOS.append("oferta sem 'recap' e sem 'de': não há âncora de preço")
    total = num(of["de"]) if of.get("de") else sum(num(v) for _, v in recap) or num(of["preco"])
    preco = num(of["preco"])
    eco = total - preco
    desc = round((1 - preco / total) * 100)
    rh = "".join('<li>%s<span>%s</span><s>R$ %s</s></li>' % (CHECK, fmt(t), brl(num(v))) for t, v in recap)
    recap_html = '<div class="lt-recap"><h2><em>Recapitulando</em> tudo o que você vai receber</h2><ul>%s</ul><p class="lt-total">TOTAL <s>R$ %s</s></p></div>' % (rh, brl(total)) if recap else ""
    prazo = of.get("prazo", "")
    minutos = of.get("cronometro_minutos")
    cheio = ""
    if minutos and not prazo:
        topo = '<small class="lt-tempo-tag">%s</small><b class="lt-tempo">⏱ <span data-lt-visita="%d" data-chave="%s">00 : %02d : 00</span></b><span>%s</span>' % (
            fmt(of.get("frase_topo", "OFERTA POR TEMPO LIMITADO")), int(minutos), attr(re.sub(r"\W", "", produto.lower())), int(minutos) % 60, fmt(of.get("frase_topo2", "Válida somente até o tempo acabar.")))
        # ao zerar nada muda na oferta: o cronômetro só para em 00:00:00 (decisão do Paulo, 04/11/2026)
    elif prazo:
        topo = '<span class="lt-tempo-l">%s</span><b class="lt-tempo">⏱ <span data-lt-timer data-fim="%s">00 : 00 : 00</span></b>' % (fmt(of.get("frase_prazo", "Esse preço termina em:")), attr(prazo))
    else:
        topo = '<b class="lt-of-excl">%s</b><span>%s</span>' % (fmt(of.get("frase_topo", "🔥 Oferta Especial")), fmt(of.get("frase_topo2", "Preço exclusivo desta página.")))
    parc = '<p class="lt-of-por">por apenas %s de:</p><p class="lt-of-preco">R$ %s</p><p class="lt-of-unico">ou R$ %s à vista</p>' % (attr(of["parcelas"]), attr(of["parcela"]), brl(preco)) if of.get("parcelas") else '<p class="lt-of-por">por apenas:</p><p class="lt-of-preco">R$ %s</p>' % brl(preco)
    prod_img = img(base, of["imagem"], "lt-of-img", produto, 860, 634, sizes="(max-width:560px) 88vw, 420px") if of.get("imagem") else ""
    of_logo = img(base, of["logo"], "lt-of-logo", produto, 480, 152, sizes="250px") if of.get("logo") else '<p class="lt-of-nome">%s</p>' % fmt(of.get("nome_destacado", "[[" + produto + "]]"))
    nb = len((cfg.get("bonus") or {}).get("itens", []))
    # frases padrão da Kamilla: valem como ponto de partida, cada oferta pode trocar ("frase_transicao": "" tira)
    ft = of.get("frase_transicao", "Tudo isso custaria R$ %s. Mas somente nessa página você garante essa oferta exclusiva por tempo limitado." % brl(total) if recap else "")
    trans_html = '<p class="lt-trans">%s</p>' % fmt(ft) if ft else ""
    checks_html = "".join("<li>%s</li>" % fmt(c) for c in of.get("checks", ["Pagamento único", "Sem mensalidade", of.get("acesso", "Acesso imediato")]))
    of_bg = '<div class="lt-bg" aria-hidden="true">%s</div>' % img(base, of["fundo"], "", "", 1920, 1080, sizes="100vw") if of.get("fundo") else ""
    B["oferta"] = ('''<section class="lt-sec lt-noite%s" id="oferta">%s<div class="lt-w lt-estreito">
%s%s
%s
<p class="lt-parabens" id="lt-parabens">🎉 Parabéns! Você ganhou %d%% OFF</p>
<div class="lt-of"><div class="lt-of-topo">%s</div><div class="lt-of-corpo">%s<div class="lt-of-desc">
<p class="lt-of-acesso">Acesso imediato ao</p>%s%s%s
<p class="lt-of-de">De R$ %s</p>%s
<p class="lt-of-eco">Você economiza R$ %s levando agora</p>
%s
<div class="lt-pag" aria-label="Formas de pagamento: Visa, Mastercard, Pix. Compra 100%% segura"><span class="lt-visa">VISA</span><span class="lt-master"><i></i><i></i></span><span class="lt-pix">◆ pix</span><span class="lt-seg">🔒 COMPRA 100%%<br>SEGURA</span></div>
<ul class="lt-checks">%s</ul>
%s</div></div></div></div></section>''' % (
        " lt-of-foto" if of_bg else "", of_bg, '<p class="lt-imagine">%s</p>' % fmt(of["imagine"]) if of.get("imagine") else "", recap_html, trans_html, desc, topo, cheio, of_logo,
        '<p class="lt-of-mais">+ %d bônus exclusivos</p>' % nb if nb else "", prod_img, brl(total), parc, brl(eco),
        botao(of.get("botao", "Quero o " + produto + " agora 🔥"), " lt-btn-of", final=True), checks_html,
        '<p class="lt-alerta">%s</p>' % fmt(of["alerta"]) if of.get("alerta") else ""))

    # 9. garantia
    g = cfg.get("garantia", {})
    dias = g.get("dias", 7)
    gt = g.get("texto") or ["Você pode testar o %s por %s dias completos. Se dentro desse período você achar que o produto não é para você, basta solicitar o reembolso e devolvemos 100%% do seu dinheiro." % (produto, dias)]
    B["garantia"] = ('''<section class="lt-sec lt-gar-sec"><div class="lt-w"><div class="lt-gar"><div class="lt-selo" aria-hidden="true">%s</div>
<div class="lt-gar-txt"><h2>Compra 100%% Segura</h2><p class="lt-gar-sub">GARANTIA DE %s DIAS</p>%s%s</div></div></div></section>''' % (
        selo_svg(dias, C["escura"], C["primaria"]), dias, "".join("<p>%s</p>" % fmt(t) for t in gt), '<p class="lt-gar-forte">%s</p>' % fmt(g["forte"]) if g.get("forte") else ""))

    # 10. autoridade
    a = cfg.get("autor")
    if a:
        B["autor"] = ('''<section class="lt-sec lt-autor-sec"><div class="lt-w"><div class="lt-autor"><div class="lt-autor-txt">
<h2>%s</h2><p class="lt-autor-cargo">%s</p>%s%s</div>%s</div></div></section>''' % (
            fmt(a["nome"]), fmt(a.get("cargo", "Criador(a) do " + produto)), "".join("<p>%s</p>" % fmt(p) for p in a.get("paragrafos", [])),
            '<p class="lt-forte">%s</p>' % fmt(a["fecho"]) if a.get("fecho") else "", img(base, a.get("foto"), "lt-autor-foto", a["nome"], 480, 480, sizes="230px")))

    # 11. FAQ
    if cfg.get("faq"):
        fq = "".join('<details class="lt-faq-i"><summary>%s<span aria-hidden="true">+</span></summary><p>%s</p></details>' % (fmt(q), fmt(r_)) for q, r_ in cfg["faq"])
        B["faq"] = '<section class="lt-sec lt-claro"><div class="lt-w lt-estreito">%s<h2 class="lt-h2">%s</h2><div class="lt-faq">%s</div></div></section>' % (
            '<p class="lt-tag">%s</p>' % fmt(cfg["faq_tag"]) if cfg.get("faq_tag") else "", fmt(cfg.get("faq_titulo", "Perguntas Frequentes")), fq)

    # 12. WhatsApp
    w = cfg.get("whatsapp") or {}
    if w.get("numero"):
        link = "https://wa.me/%s?text=%s" % (re.sub(r"\D", "", w["numero"]), urllib.parse.quote(w.get("mensagem", "Olá! Vim pela página do %s e tenho uma dúvida." % produto)))
        B["whatsapp"] = ('<section class="lt-sec lt-duvida"><div class="lt-w lt-estreito lt-centro"><h2 class="lt-h2">%s</h2><a class="lt-wa" href="%s" target="_blank" rel="noopener">%s%s</a></div></section>' % (fmt(w.get("titulo", "Ficou com alguma dúvida?")), attr(link), WA_IC, fmt(w.get("botao", "Clique aqui para falar no WhatsApp."))))

    # 13. rodapé
    rd = cfg.get("rodape", {})
    leg = []
    if rd.get("politica"):
        leg.append('<a href="%s">Política de Privacidade</a>' % attr(rd["politica"]))
    if rd.get("termos"):
        leg.append('<a href="%s">Termos de Uso</a>' % attr(rd["termos"]))
    emp = fmt(rd.get("empresa", "")) + (" | CNPJ: %s" % attr(rd["cnpj"]) if rd.get("cnpj") else "")
    B["rodape"] = ('''<footer class="lt-rod"><p>© %s %s. Todos os Direitos Reservados</p>%s%s
<p class="lt-legal">Este site não possui qualquer vínculo ou afiliação com o Facebook ou suas empresas associadas. Após sair do Facebook, toda responsabilidade passa a ser exclusivamente do nosso site. A aquisição deste material não assegura resultados específicos.</p></footer>''' % (
        attr(rd.get("ano", "2026")), fmt(produto), "<p>%s</p>" % emp if emp.strip() else "", "<p>%s</p>" % " | ".join(leg) if leg else ""))

    # montagem: ordem padrão ou a da oferta ("ordem" no pagina.json)
    padrao = ["depoimentos", "demonstracao", "dor", "categorias", "passos", "recebe", "bonus", "transicao", "oferta", "garantia", "autor", "faq", "whatsapp", "rodape"]
    ordem = cfg.get("ordem") or padrao
    for k in B:
        if k not in ordem:
            AVISOS.append("bloco '%s' existe mas não está em 'ordem': ficou fora da página" % k)
    ancora = False
    for k in ordem:
        if k in B:
            if not ancora:
                S.append('<div id="dobra2"></div>')
                ancora = True
            S.append('<div id="b-%s">%s</div>' % (k, B[k]))
    flut = cfg.get("flutuante") or []
    if flut:
        S.append('<a class="lt-flut" href="#oferta" data-flut="%s" aria-label="Continuar" hidden>⌄</a>' % attr(",".join(flut)))

    # rastreio
    rt = cfg.get("rastreio", {})
    head_extra = ""
    if rt.get("meta_pixel_id"):
        # PageView entra na fila na hora; o arquivo do Facebook só carrega depois que a página aparece (não pesa na nota)
        head_extra += ("<script>!function(f,b){if(f.fbq)return;var n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];"
                       "function go(){if(go.d)return;go.d=1;var t=b.createElement('script');t.async=!0;t.src='https://connect.facebook.net/en_US/fbevents.js';b.head.appendChild(t)}"
                       "addEventListener('load',function(){setTimeout(go,300)});['scroll','pointerdown','touchstart','keydown'].forEach(function(e){addEventListener(e,go,{once:true,passive:true})})}(window,document);"
                       "fbq('init','%s');fbq('track','PageView');</script>" % attr(rt["meta_pixel_id"]))
    tail_extra = ""
    if rt.get("clarity_id"):
        tail_extra = "<script>(function(){var f=0;function go(){if(f)return;f=1;(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src='https://www.clarity.ms/tag/'+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)})(window,document,'clarity','script','%s')}['scroll','pointerdown','keydown','touchstart'].forEach(function(e){addEventListener(e,go,{once:true,passive:true})});setTimeout(go,7000)})();</script>" % attr(rt["clarity_id"])

    css = CSS
    for k in sorted(C, key=len, reverse=True):  # nomes maiores primeiro (destaque_foto antes de destaque)
        css = css.replace("$" + k, C[k])
    css = css.replace("$fonte", fonte).replace("SUBLINHA_COR", C["primaria"].replace("#", "%23"))
    fonte_url = "https://fonts.googleapis.com/css2?family=%s:wght@400;500;600;700;800&display=swap" % fonte.replace(" ", "+")
    ff_css, ff_pre = fonte_local(base, fonte) if cfg.get("fonte_local", True) else ("", "")
    if ff_css:
        css = ff_css + css
        fonte_tags = ff_pre
    else:
        fonte_tags = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preload" as="style" href="%s"><link href="%s" rel="stylesheet" media="print" onload="this.media=\'all\'"><noscript><link href="%s" rel="stylesheet"></noscript>' % (fonte_url, fonte_url, fonte_url)
    return '''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title><meta name="description" content="%s">%s
%s
%s<style>%s</style>%s</head><body><div class="lt">
%s
</div>
<script>%s</script>%s</body></html>''' % (
        attr(cfg.get("titulo_aba", produto)), attr(cfg.get("descricao", "")), '<meta name="robots" content="noindex">' if cfg.get("noindex", True) else "",
        fonte_tags, "".join(dict.fromkeys(PRELOAD)), css, head_extra, "\n".join(S), JS, tail_extra)


CSS = r"""
:root{--dsf:$destaque_foto;--pau:$pausa;--pri:$primaria;--esc:$escura;--fun:$fundo;--ok:$sucesso;--dst:$destaque;--ace:$acento;--ale:$alerta;--lar:$laranja;--txt:$texto;--sub:$suave;--lin:$linha}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--fun)}
.lt{color:var(--txt);background:var(--fun);font-family:"$fonte",system-ui,sans-serif;font-size:16px;line-height:1.55;overflow-x:hidden;overflow-x:clip}
.lt h1,.lt h2,.lt h3{margin:0;letter-spacing:-.02em;color:inherit}
.lt p{margin:0}
.lt img{max-width:100%}
.lt em{font-style:normal;color:var(--pri)}
.lt em.c1{color:var(--pri);font-weight:800}.lt em.c2{color:var(--dst);font-weight:800}
.lt-sublinha{white-space:nowrap;padding-bottom:6px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 12' preserveAspectRatio='none'%3E%3Cpath d='M2 8 C 40 3, 80 3, 110 6 S 170 10, 198 4' fill='none' stroke='SUBLINHA_COR' stroke-width='3' stroke-linecap='round'/%3E%3C/svg%3E") left bottom/100% 10px no-repeat}
.lt-w{max-width:1080px;margin:0 auto;padding:0 20px}
.lt-estreito{max-width:760px}
.lt-centro{text-align:center}
.lt-sec{padding:64px 0}
.lt-claro{background:#fff}
.lt .lt-h2{font-size:clamp(1.5rem,3vw,2.1rem);line-height:1.2;font-weight:800;text-align:center;max-width:860px;margin:0 auto 34px}
.lt .lt-h2-g{font-size:clamp(1.7rem,3.6vw,2.6rem);margin-bottom:16px}
.lt .lt-tag{display:table;margin:0 auto 12px;background:color-mix(in srgb,var(--pri) 12%,#fff);color:var(--pri);font-size:13px;font-weight:700;padding:5px 14px;border-radius:999px}
.lt-frase{margin:28px 0 0;text-align:center;color:var(--pri);font-weight:800;font-size:19px}

/* faixa + topo */
.lt-faixa{background:linear-gradient(90deg,var(--pri),var(--esc));color:#fff;text-align:center;font-size:13.5px;font-weight:700;letter-spacing:.04em;padding:10px 16px}
.lt-hero{padding:22px 0 46px;background:#F4F6FB radial-gradient(70% 60% at 50% 30%,#fff 0%,rgba(255,255,255,0) 70%)}
.lt-hero-c{text-align:center;max-width:900px}
.lt-logo{display:block;height:60px;width:auto;margin:0 auto 12px}
.lt-hero h1{font-weight:500;font-size:clamp(1.42rem,3.2vw,1.95rem);line-height:1.22;letter-spacing:-.015em;margin:0 auto 10px;max-width:820px}
.lt-hero h1 em,.lt-hero h1 b{font-weight:800}
.lt-sub{font-style:italic;color:var(--sub);font-size:.98rem;margin:0 auto 6px;max-width:640px}
.lt-sub .lt-sublinha{background:none;text-decoration:underline;text-underline-offset:3px;padding:0}
.lt-sub b{display:inline-block;margin-top:4px;color:var(--pri);font-weight:800}
.lt-hero-img{margin:14px auto 22px;max-width:460px}
.lt-hero-img img{display:block;width:100%;height:auto}
.lt-hero-link{display:block;margin:14px 0 0;color:var(--sub);font-size:14px;text-decoration:none}
.lt-palco{position:relative;width:min(460px,100%);margin:6px auto 22px;padding-top:6px}
.lt-pessoa{display:block;width:195px;max-width:44%;height:auto;margin:0 auto -13%;position:relative;z-index:1;-webkit-mask-image:linear-gradient(180deg,#000 70%,transparent 100%);mask-image:linear-gradient(180deg,#000 70%,transparent 100%)}
.lt-fones{position:relative;z-index:2;display:flex;justify-content:center;gap:18px}
.lt-fone{width:162px;max-width:37%;background:#0D1220;border-radius:24px;padding:7px;box-shadow:0 26px 50px -24px rgba(3,22,63,.6)}
.lt-f1{transform:rotate(-4deg);border:2px solid #FF4D8D}.lt-f2{transform:rotate(4deg);margin-top:14px;border:2px solid #FFB020}
.lt-tela{border-radius:17px;overflow:hidden;background:#fff;aspect-ratio:4/5}
.lt-tela-img{display:block;width:100%;height:100%;object-fit:cover}
.lt-badge{position:absolute;z-index:3;font-size:13px;font-weight:700;color:#fff;padding:7px 13px;border-radius:999px;box-shadow:0 10px 20px -10px rgba(0,0,0,.5);white-space:nowrap}
.lt-b1{top:4%;right:4%;background:linear-gradient(90deg,var(--pri),#6A5BFF)}.lt-b2{top:11%;right:0;background:linear-gradient(90deg,#7C3AED,#DB2777)}.lt-b3{top:18%;right:5%;background:linear-gradient(90deg,#16A34A,#22C55E)}
.lt-notif{position:absolute;z-index:3;display:inline-flex;align-items:center;gap:4px;background:#EF2B2D;color:#fff;font-weight:800;font-size:14px;padding:7px 10px;border-radius:12px 12px 12px 3px;box-shadow:0 10px 18px -8px rgba(239,43,45,.7)}
.lt-notif svg{width:15px;height:15px}
.lt-n1{top:5%;left:8%;transform:rotate(-10deg)}.lt-n2{top:12%;left:18%;font-size:18px}.lt-n3{top:20%;left:5%;transform:rotate(-6deg)}

/* botões: pulso + cor correndo + brilho */
.lt-btn,.lt-wa{position:relative;overflow:hidden;isolation:isolate;display:inline-flex;align-items:center;justify-content:center;gap:12px;color:#fff!important;text-decoration:none;font-weight:800;border-radius:999px;white-space:nowrap;
  background-color:var(--ok);box-shadow:0 14px 30px -12px color-mix(in srgb,var(--ok) 75%,transparent),0 0 22px -4px color-mix(in srgb,var(--ok) 55%,transparent);animation:lt-pulso 1.6s ease-in-out infinite;will-change:transform}
.lt-btn{font-size:17px;text-transform:uppercase;letter-spacing:.01em;padding:19px 30px;min-width:min(420px,100%)}
.lt-btn span{font-size:20px}
.lt-btn::before,.lt-wa::before{content:"";position:absolute;top:0;left:0;bottom:0;width:200%;z-index:-1;background:linear-gradient(90deg,color-mix(in srgb,var(--ok) 80%,#000),var(--ok),color-mix(in srgb,var(--ok) 70%,#fff),color-mix(in srgb,var(--ok) 80%,#000),var(--ok),color-mix(in srgb,var(--ok) 70%,#fff),color-mix(in srgb,var(--ok) 80%,#000));animation:lt-cor 3s linear infinite;will-change:transform}
.lt-btn::after,.lt-wa::after{content:"";position:absolute;top:0;left:0;width:40%;height:100%;background:linear-gradient(100deg,rgba(255,255,255,0),rgba(255,255,255,.55),rgba(255,255,255,0));animation:lt-brilho 3s ease-in-out 5;will-change:transform}
.lt-btn:hover,.lt-wa:hover{filter:brightness(1.08)}
.lt-btn-topo span{display:inline-block;animation:lt-desce 1.2s ease-in-out infinite}
@keyframes lt-pulso{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
@keyframes lt-cor{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@keyframes lt-brilho{0%,55%{transform:translateX(-150%) skewX(-20deg)}100%{transform:translateX(350%) skewX(-20deg)}}
@keyframes lt-desce{0%,100%{transform:translateY(-2px)}50%{transform:translateY(4px)}}

/* depoimentos */
.lt-dep{background:var(--fun)}
.lt-trilho{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding:6px 4px 14px;-webkit-overflow-scrolling:touch}
.lt-dep-print{flex:0 0 240px;scroll-snap-align:start;border-radius:18px;overflow:hidden;box-shadow:0 18px 40px -24px rgba(3,22,63,.5);background:#111}
.lt-dep-print img{display:block;width:100%;height:auto}
.lt-trilho-c{margin-top:10px}
.lt-dep-card{flex:0 0 300px;scroll-snap-align:start;background:#fff;border:1px solid var(--lin);border-radius:18px;padding:18px}
.lt-dep-top{display:flex;gap:10px;align-items:center;margin-bottom:6px}
.lt-dep-top b{display:block;font-size:15px}.lt-dep-top small{color:var(--sub);font-size:12.5px}
.lt-dep-foto{width:40px;height:40px;border-radius:50%;object-fit:cover}
.lt-dep-ini{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;background:var(--pri);color:#fff;font-style:normal;font-weight:800}
.lt-dep-est{color:#F5B300;font-size:14px;margin-bottom:6px!important}
.lt-dep-card p{font-size:14.5px;color:var(--sub)}
.lt-demo .lt-tag{display:table;margin:0 auto 12px}
.lt-demo-sub{text-align:center;color:var(--sub);max-width:620px;margin:-6px auto 18px!important}
.lt-demo-f{flex:0 0 260px;scroll-snap-align:start;margin:0}
.lt-demo-img{border-radius:18px;overflow:hidden;box-shadow:0 18px 40px -24px rgba(3,22,63,.5);background:#fff;border:1px solid var(--lin)}
.lt-demo-img img{display:block;width:100%;height:auto}
.lt-demo-f figcaption{margin-top:10px;font-size:14px;font-weight:700;text-align:center;color:var(--txt)}
.lt-arraste{text-align:center;color:var(--sub);font-size:14px;margin-top:8px!important}

/* dor + problema x virada */
.lt-dor{background:#fff}
.lt-dor-t{font-size:clamp(1.5rem,3vw,2.15rem);line-height:1.2;font-weight:800;text-align:center;max-width:920px;margin:0 auto 34px!important}
.lt-dor-t span{display:block;color:var(--pri)}
.lt-dores{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.lt-dor-card{background:var(--fun);border:1px solid var(--lin);border-radius:18px;padding:20px 18px;display:flex;flex-direction:column;gap:10px}
.lt-dor-foto{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:12px}
.lt-dor-ic{display:grid;place-items:center;width:42px;height:42px;border-radius:12px;background:#FFE4E4;font-size:21px}
.lt-dor-card p{font-weight:600;font-size:15px;line-height:1.45}
.lt-vs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;align-items:center;margin-top:44px}
.lt-vs3{grid-template-columns:minmax(0,1fr) minmax(0,1.25fr) minmax(0,1fr)}
.lt-vs-card{border-radius:20px;padding:24px 22px}
.lt-vs-card h3{font-size:1.3rem;font-weight:800;margin:10px 0 8px}
.lt-vs-card p{font-size:15px}
.lt-vs-tag{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;padding:5px 11px;border-radius:999px;color:#fff}
.lt-vs-prob{background:#FFF1F1;border:1px solid #FFD0D0}.lt-vs-prob .lt-vs-tag{background:#DC2626}.lt-vs-prob h3{color:#B91C1C}.lt-vs-prob p{color:#5B2B2B}
.lt-vs-sol{background:#EEFBF2;border:1px solid #BBF0CC}.lt-vs-sol .lt-vs-tag{background:#16A34A}.lt-vs-sol h3{color:#15803D}.lt-vs-sol p{color:#1F4D30}
.lt-vs-img img{display:block;width:100%;height:auto;border-radius:22px;box-shadow:0 24px 50px -30px rgba(3,22,63,.45)}

/* passos */
.lt-video{max-width:780px;margin:0 auto;aspect-ratio:16/9;border-radius:22px;overflow:hidden;background:var(--esc);border:4px solid #fff;box-shadow:0 0 0 1px rgba(30,20,120,.06),0 0 44px 4px color-mix(in srgb,var(--ace) 45%,transparent)}
.lt-video video{display:block;width:100%;height:100%;object-fit:cover}
.lt-passos-ic{list-style:none;padding:0;margin:26px auto 0;display:flex;justify-content:center;align-items:flex-start;gap:12px}
.lt-passos-ic li{display:flex;flex-direction:column;align-items:center;gap:8px;width:120px;text-align:center;font-size:13.5px;position:relative}
.lt-passos-ic li+li::before{content:"→";position:absolute;left:-18px;top:16px;color:var(--sub);font-size:20px}
.lt-pic{position:relative;width:54px;height:54px;border-radius:14px;display:grid;place-items:center;font-size:24px;background:linear-gradient(135deg,var(--pri),var(--ace));box-shadow:0 10px 20px -10px var(--pri)}
.lt-pic i{position:absolute;top:-8px;right:-8px;background:#fff;color:var(--txt);font-style:normal;font-size:10.5px;font-weight:800;border-radius:999px;padding:2px 6px;box-shadow:0 2px 6px rgba(0,0,0,.2)}
.lt-passos{list-style:none;padding:0;margin:24px 0 0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.lt-passo{position:relative;background:#fff;border:1px solid var(--lin);border-radius:20px;padding:22px;box-shadow:0 14px 34px -26px rgba(3,22,63,.35)}
.lt-pn{position:absolute;top:14px;right:18px;font-size:34px;font-weight:800;color:color-mix(in srgb,var(--pri) 14%,#fff)}
.lt-pi{display:grid;place-items:center;width:40px;height:40px;border-radius:50%;background:color-mix(in srgb,var(--pri) 12%,#fff);font-size:18px}
.lt-pl{color:var(--pri);font-size:12px;font-weight:800;letter-spacing:.06em;margin:12px 0 4px!important}
.lt-passo h3{font-size:1.08rem;font-weight:800;margin-bottom:6px}
.lt-passo p{color:var(--sub);font-size:15px}

/* o que recebe */
.lt-rec{background:var(--fun)}
.lt-rec-l{text-align:center;color:var(--sub);font-weight:700;margin:0 0 18px!important}
.lt-mais{display:flex;align-items:center;justify-content:center;gap:16px;margin:0 auto 26px}
.lt-mais-n{font-size:clamp(3.4rem,8vw,5rem);font-weight:800;line-height:1;letter-spacing:-.04em;background:linear-gradient(180deg,color-mix(in srgb,var(--pri) 70%,#fff),var(--pri));-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 6px 14px color-mix(in srgb,var(--pri) 35%,transparent))}
.lt-mais-t{display:flex;flex-direction:column;line-height:1.1;text-align:left}
.lt-mais-t small{font-size:clamp(.85rem,1.8vw,1.05rem);font-weight:800}
.lt-mais-t b{font-size:clamp(1.3rem,3vw,1.9rem);font-weight:800;color:var(--pri);padding-bottom:6px;background:linear-gradient(90deg,var(--pri),var(--dst)) left bottom/100% 3px no-repeat}
.lt-chips{list-style:none;padding:0;margin:0 auto 38px;display:flex;flex-wrap:wrap;justify-content:center;gap:8px;max-width:760px}
.lt-chips li{background:#fff;border:1px solid var(--lin);border-radius:999px;padding:8px 15px;font-size:14px;font-weight:600}
.lt-gal{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.lt-g{margin:0;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 20px 50px -24px rgba(3,22,63,.45);border:1px solid var(--lin)}
.lt-g-img{position:relative;overflow:hidden;background:#ddd}
.lt-g-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.lt-g-arte{position:absolute;left:0;right:0;bottom:0;padding:44px 14px 14px;background:linear-gradient(180deg,rgba(3,22,63,0),rgba(3,22,63,.88));color:#fff}
.lt-g-arte b{display:block;font-size:16px;line-height:1.15;font-weight:800}
.lt-g-faixa{display:inline-block;background:#FFD43B;color:#1B2238;font-size:11px;font-weight:800;padding:4px 9px;border-radius:6px;margin:0 0 7px}
.lt-g-rot{position:absolute;top:10px;left:10px;background:rgba(255,255,255,.92);color:var(--txt);font-size:11.5px;font-weight:700;padding:3px 9px;border-radius:999px}
.lt-g-lock .lt-g-img>*{filter:blur(9px);transform:scale(1.06)}
.lt-g-lock .lt-g-img::after{content:"🔒";position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:2;width:58px;height:58px;display:grid;place-items:center;font-size:24px;background:rgba(255,255,255,.85);border-radius:50%;box-shadow:0 10px 24px -8px rgba(3,22,63,.5)}
.lt-gal-nota{text-align:center;color:var(--sub);font-size:13px;margin:14px 0 0!important}
.lt-marquee{overflow:hidden;margin:22px -20px 0;-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.lt-marquee-in{display:flex;gap:12px;width:max-content;animation:lt-rola 40s linear infinite}
.lt-marquee img{width:130px;height:130px;object-fit:cover;border-radius:14px;flex:none}
@keyframes lt-rola{to{transform:translateX(-50%)}}
.lt-rec-t2{text-align:center;font-size:clamp(1.25rem,2.4vw,1.6rem);font-weight:800;margin:46px auto 20px!important}
.lt-extras{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.lt-extra{background:#fff;border:1px solid var(--lin);border-radius:18px;padding:22px;text-align:center}
.lt-extra span{display:block;font-size:30px;margin:0 0 8px}
.lt-extra-img{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:14px;margin:0 0 14px}
.lt-extra b{display:block;font-size:1.05rem;margin:0 0 6px}
.lt-extra p{color:var(--sub);font-size:14.5px}

/* bônus */
.lt-bon{background:linear-gradient(180deg,#FBF9F7,#F3F5FB)}
.lt-bonus-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.lt-bonus{background:#fff;border:1px solid #E6E3F5;border-radius:22px;padding:22px;display:flex;flex-direction:column;box-shadow:0 0 60px -10px color-mix(in srgb,var(--ace) 28%,transparent),0 0 40px -14px rgba(255,140,60,.35)}
.lt-bonus-tag{align-self:flex-start;background:#fff;font-size:13px;font-weight:700;padding:7px 14px;border-radius:999px;box-shadow:0 4px 14px -4px rgba(3,22,63,.25)}
.lt-bonus h3{font-size:1.08rem;font-weight:800;margin:12px 0 6px}
.lt-bonus p{flex:1;color:var(--sub);font-size:15px}
.lt-bonus-img{display:block;width:100%;height:auto;aspect-ratio:1/1;object-fit:cover;border-radius:16px;margin-top:16px}
.lt-bonus-ph{margin-top:16px;aspect-ratio:1/1;border-radius:16px;display:grid;place-items:center;font-size:64px;background:linear-gradient(135deg,var(--pri),var(--ace))}

/* ancoragem + oferta */
.lt-noite{background:#0E1530;color:#fff}
.lt-imagine{font-size:1.15rem;line-height:1.55;text-align:center;color:#DCE4FF;margin:0 0 30px!important}
.lt-recap{background:#fff;color:var(--txt);border-radius:20px;padding:26px}
.lt-recap h2{font-size:1.2rem;font-weight:800;text-align:center;margin:0 0 16px}
.lt-recap h2 em{font-style:italic}
.lt-recap ul{list-style:none;padding:0;margin:0}
.lt-recap li{display:flex;align-items:center;gap:10px;padding:11px 0;border-bottom:1px solid var(--lin);font-size:15px}
.lt-recap li span{flex:1}
.lt-recap svg{width:24px;height:24px;flex:none;color:var(--ok)}
.lt-recap s,.lt-total s{color:#DC2626;font-weight:700;white-space:nowrap}
.lt-total{display:flex;justify-content:space-between;margin:14px 0 0!important;font-weight:800}
.lt-trans{text-align:center;color:#DCE4FF;margin:24px 0!important}
.lt-parabens{display:table;margin:34px auto 16px!important;background:#16A34A;color:#fff;font-weight:800;font-size:16px;padding:10px 22px;border-radius:999px;box-shadow:0 10px 26px -10px rgba(22,163,74,.8);animation:lt-parab 1.4s ease-in-out 6}
@keyframes lt-parab{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
.lt-of{max-width:510px;margin:0 auto;background:#fff;border:3px solid var(--ale);border-radius:26px;overflow:hidden;box-shadow:0 40px 80px -40px rgba(0,0,0,.7);color:var(--txt)}
.lt-of-topo{background:var(--ale);color:#fff;text-align:center;padding:14px 16px;display:flex;flex-direction:column;align-items:center;gap:2px}
.lt-of-topo span{font-size:13px;font-weight:600}
.lt-of-excl{font-size:19px;font-weight:800}
.lt-tempo-l{font-weight:700!important}
.lt-tempo{font-size:30px;font-weight:800;letter-spacing:.04em;font-variant-numeric:tabular-nums;line-height:1.1}
.lt-tempo span{font-size:inherit!important;font-weight:800!important}
.lt-of-corpo{padding:22px 24px 26px;text-align:center}
.lt-of-acesso{color:var(--sub);font-size:1.15rem;font-weight:600}
.lt-of-logo{display:block;width:min(250px,75%);height:auto;margin:10px auto 8px}
.lt-of-nome{font-size:1.6rem;font-weight:800;margin:4px 0!important}
.lt-of-mais{color:var(--ace);font-weight:800;font-size:1.15rem}
.lt-of-img{display:block;width:100%;max-width:420px;height:auto;margin:18px auto 6px}
.lt-of-de{color:#9AA3B5;text-decoration:line-through;font-size:1.25rem;font-weight:600;margin-top:10px!important}
.lt-of-por{color:var(--sub);font-size:14px;margin-top:4px!important}
.lt-of-preco{color:var(--ok);font-size:clamp(3.4rem,11vw,4.8rem);font-weight:800;letter-spacing:-.04em;line-height:1.05}
.lt-of-unico{color:var(--sub);font-weight:700;font-size:14px}
.lt-of-eco{display:inline-block;margin:14px 0 6px!important;background:var(--ok);color:#fff;font-weight:800;font-size:14px;padding:7px 16px;border-radius:999px}
.lt-btn-of{width:100%;margin-top:14px;min-width:0}
.lt-pag{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:14px;margin:20px 0 14px}
.lt-visa{font-weight:900;font-style:italic;font-size:22px;color:#1A1F71;letter-spacing:-.02em}
.lt-master{display:inline-flex}.lt-master i{width:24px;height:24px;border-radius:50%;background:#EB001B;display:block}.lt-master i+i{background:#F79E1B;margin-left:-10px;mix-blend-mode:multiply}
.lt-pix{font-weight:800;font-size:19px;color:#32BCAD}
.lt-seg{font-size:10px;font-weight:900;line-height:1.1;color:#16A34A;text-align:left}
.lt-checks{list-style:none;padding:0;margin:0 0 18px;display:flex;flex-wrap:wrap;justify-content:center;gap:6px 16px;font-size:14px;color:var(--sub)}
.lt-checks li::before{content:"✓ ";color:var(--lar);font-weight:900}
.lt-alerta{background:var(--ale);color:#fff;font-weight:800;font-size:14.5px;padding:13px 14px;border-radius:14px;border:2px solid #FFD43B}

/* garantia */
.lt-gar-sec{background:#0E1530;padding-top:0}
.lt-gar{max-width:900px;margin:0 auto;background:#fff;border-radius:26px;padding:44px 48px;display:grid;grid-template-columns:240px minmax(0,1fr);gap:40px;align-items:center}
.lt-selo svg{display:block;width:100%;height:auto;filter:drop-shadow(0 14px 24px rgba(3,22,63,.25))}
.lt-gar-txt h2{font-size:clamp(1.6rem,3vw,2.1rem);font-weight:800;margin:0 0 6px}
.lt-gar-txt .lt-gar-sub{margin:0 0 18px!important;font-weight:800;color:var(--lar);letter-spacing:.02em}
.lt-gar-txt p{color:var(--sub);margin:0 0 12px}
.lt-gar-forte{color:var(--txt)!important;font-weight:700;margin-top:20px!important}
.lt-gar-forte em.c1,.lt-gar-forte em.c2{color:var(--lar)}

/* autor */
.lt-autor-sec{background:#fff}
.lt-autor{max-width:820px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr) 230px;gap:44px;align-items:center}
.lt-autor-txt h2{font-size:clamp(1.7rem,3vw,2.1rem);font-weight:800}
.lt-autor-txt .lt-autor-cargo{color:var(--ace);font-weight:800;margin:4px 0 22px!important}
.lt-autor-txt p{color:var(--sub);margin:0 0 14px;font-size:1.02rem}
.lt-autor-txt b{color:#4B5568}
.lt-forte{color:var(--txt)!important;font-weight:800}
.lt-autor-foto{width:230px;height:230px;border-radius:50%;object-fit:cover}

/* faq + dúvida + rodapé */
.lt-faq{display:grid;gap:10px}
.lt-faq-i{background:var(--fun);border:1px solid var(--lin);border-radius:14px;padding:0 18px}
.lt-faq-i summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:12px;padding:16px 0;font-weight:700}
.lt-faq-i summary::-webkit-details-marker{display:none}
.lt-faq-i summary span{color:var(--pri);font-size:20px;line-height:1;transition:transform .2s}
.lt-faq-i[open] summary span{transform:rotate(45deg)}
.lt-faq-i p{margin:0 0 16px;color:var(--sub)}
.lt-duvida{background:var(--fun)}
.lt-wa{gap:10px;padding:15px 24px;font-size:16px}
.lt-wa svg{width:22px;height:22px}
.lt-rod{background:#1B2238;color:#B7C0D6;text-align:center;font-size:13px;padding:34px 20px 40px}
.lt-rod p{margin:0 0 6px}
.lt-rod a{color:#fff}
.lt-legal{max-width:720px;margin:14px auto 0!important;font-size:11.5px;opacity:.8}


/* ---- desempenho: seções abaixo da primeira tela só são desenhadas quando chegam perto ---- */
.lt-sec,.lt-rod,.lt-transicao{content-visibility:auto;contain-intrinsic-size:auto 900px}

/* ---- cor por função do botão ---- */
.lt-btn.lt-btn-av{--ok:var(--pri)}.lt-btn.lt-btn-ac{--ok:var(--ace)}

/* ---- topo com fundo do mundo do nicho ---- */
.lt-hero{position:relative}
.lt-bg{position:absolute;inset:0;z-index:0;overflow:hidden}.lt-bg img{width:100%;height:100%;object-fit:cover;object-position:center bottom}
.lt-hero-foto{background:var(--pau);color:#fff;padding-top:0}
.lt-hero-foto .lt-hero-c,.lt-hero-foto .lt-vit-zona,.lt-hero-foto .lt-marquee{position:relative;z-index:1}
.lt-hero-foto h1{color:#fff;font-weight:600;text-shadow:0 2px 12px rgba(18,41,79,.35)}
.lt-hero-foto h1 em.c1,.lt-hero-foto h1 em.c2,.lt-hero-foto h1 b{color:var(--dsf);font-weight:800}
.lt-hero-foto .lt-sub{color:#fff;font-style:normal;font-weight:500;text-shadow:0 1px 4px rgba(18,41,79,.45)}
.lt-hero-foto .lt-sub em,.lt-hero-foto .lt-sub b{color:var(--dsf)}
.lt .lt-faixa-aba{position:relative;z-index:2;display:table;margin:0 auto 22px;background:color-mix(in srgb,var(--ace) 30%,#fff);color:var(--esc);font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;padding:13px 22px;border-radius:0 0 18px 18px;box-shadow:0 8px 22px -6px rgba(0,0,0,.2)}
.lt-hero-foto .lt-w{padding-top:0}

/* ---- carrossel 3D simétrico (vitrine e depoimentos) ---- */
.lt-vit{position:relative;width:100%;overflow:hidden;user-select:none;touch-action:pan-y}
.lt-vit-palco{position:relative;height:340px;display:flex;align-items:center;justify-content:center}
.lt-vit-i{position:absolute;margin:0;width:176px;aspect-ratio:9/16;border-radius:16px;overflow:hidden;box-shadow:0 18px 40px -18px rgba(0,0,0,.45);transition:transform .7s cubic-bezier(.2,.8,.2,1),opacity .5s;background:#ddd}
.lt-vit-i img{width:100%;height:100%;object-fit:cover;display:block;pointer-events:none}
.lt-vit-ctrl{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:8px}
.lt-vit-ctrl button{width:36px;height:36px;border-radius:50%;border:1px solid var(--lin);background:#fff;color:var(--sub);font-size:20px;cursor:pointer}
.lt-vit-dots{display:flex;gap:6px}.lt-vit-dots i{width:6px;height:6px;border-radius:50%;background:color-mix(in srgb,var(--sub) 30%,transparent)}.lt-vit-dots i.on{background:var(--pri)}
.lt-vit-zona{padding:8px 0 0}
.lt-vit-topo,.lt-vit-dep{width:100vw;margin-left:calc(50% - 50vw)}
.lt-hero-foto .lt-vit-zona+.lt-marquee,.lt-marquee-v{margin:18px 0 0}
.lt-marquee-v img{width:117px;height:208px;object-fit:cover}
@media (min-width:640px){.lt-vit-palco{height:430px}.lt-vit-i{width:224px}}
@media (min-width:1024px){.lt-vit-palco{height:500px}.lt-vit-i{width:256px}.lt-marquee-v img{width:144px;height:256px}}

/* ---- nota da prova social ---- */
.lt-nota{display:flex;flex-direction:column;align-items:center;gap:2px;margin:0 0 18px}
.lt-nota b{font-size:clamp(40px,12vw,66px);font-weight:800;line-height:1;color:var(--esc)}
.lt-nota-est{color:#F5B300;font-size:20px;letter-spacing:2px}
.lt-nota span{font-size:clamp(14px,4vw,18px)}

/* ---- categorias em vídeo ---- */
.lt-cats{background:linear-gradient(180deg,#fff,var(--fun))}
.lt-cats-g{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin-top:26px}
.lt-cat{position:relative;margin:0;border-radius:18px;overflow:hidden;background:#EAF0F8;border:1px solid color-mix(in srgb,var(--ace) 40%,#fff);box-shadow:0 0 26px color-mix(in srgb,var(--ace) 30%,transparent)}
.lt-cat video,.lt-cat img{display:block;width:100%;height:auto;aspect-ratio:9/16;object-fit:cover}
.lt-cat figcaption{position:absolute;left:10px;bottom:10px;background:rgba(255,255,255,.92);color:var(--esc);font-size:11px;font-weight:600;padding:4px 10px;border-radius:999px;border:1px solid color-mix(in srgb,var(--ace) 40%,#fff)}
.lt-cats-f{text-align:center;color:var(--sub);margin:28px auto 0!important;max-width:640px}
@media (max-width:860px){.lt-cats-g{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}}

/* ---- passos com vídeo vertical (tela) ---- */
.lt-pv{display:grid;grid-template-columns:minmax(0,1fr) 300px;grid-template-areas:"tag v" "t v" "i v" "b v";column-gap:56px;row-gap:22px;align-items:center;max-width:980px;margin:0 auto}
.lt-pv-tag{grid-area:tag;margin:0!important;justify-self:start}.lt-pv-t{grid-area:t;text-align:left;margin:0!important}
.lt-pv-v{grid-area:v;text-align:center}.lt-pv-i{grid-area:i}.lt-pv-b{grid-area:b}
.lt-pv-l{color:var(--sub);font-size:15px;margin:0 0 10px!important}
.lt-vv{position:relative;aspect-ratio:9/16;border-radius:22px;overflow:hidden;background:var(--esc);box-shadow:0 24px 50px -24px rgba(3,22,63,.5)}
.lt-vv video,.lt-vv iframe,.lt-vv img{position:absolute;inset:0;width:100%;height:100%;border:0;object-fit:cover}
.lt-vv-play{position:absolute;inset:0;border:0;padding:0;background:transparent;cursor:pointer}
.lt-vv-play span{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:64px;height:64px;border-radius:50%;background:var(--ace);color:#fff;font-size:24px;display:grid;place-items:center;box-shadow:0 10px 24px -8px rgba(0,0,0,.5)}
.lt-pv .lt-passos-ic{justify-content:flex-start;margin:0}
@media (max-width:860px){.lt-pv{grid-template-columns:minmax(0,1fr);grid-template-areas:"tag" "t" "v" "i" "b";text-align:center}
 .lt-pv-tag{justify-self:center}.lt-pv-t{text-align:center}.lt-pv-v{max-width:320px;margin:0 auto;width:100%}.lt-pv .lt-passos-ic{justify-content:center}}

/* ---- bônus em lista (imagem ao lado no celular) ---- */
.lt-bon-lista .lt-bonus-tag{background:var(--pri);color:#fff;font-size:11px;font-weight:600;letter-spacing:.16em;box-shadow:0 6px 16px -4px color-mix(in srgb,var(--pri) 60%,transparent)}
.lt-bonus-txt{display:flex;flex-direction:column;flex:1}
@media (max-width:860px){.lt-bon-lista .lt-bonus-g{gap:12px}.lt-bon-lista .lt-bonus{flex-direction:row-reverse;align-items:center;gap:12px;padding:12px;text-align:left}
 .lt-bon-lista .lt-bonus-img,.lt-bon-lista .lt-bonus-ph{width:112px;flex:none;margin:0;border-radius:12px}.lt-bon-lista .lt-bonus h3{font-size:16px;margin:8px 0 4px}.lt-bon-lista .lt-bonus p{font-size:12.5px}
 .lt-bon-lista .lt-bonus-tag{font-size:10px;padding:4px 11px}}

/* ---- faixa de transição ---- */
.lt-transicao{background:var(--pau);color:#fff;padding:44px 0;text-align:center}
.lt-transicao p{font-size:clamp(19px,3vw,32px);line-height:1.25;font-weight:400}
.lt-transicao em.c1,.lt-transicao em.c2{color:var(--pri);font-weight:800}

/* ---- oferta com fundo e cronômetro por visitante ---- */
.lt-noite{position:relative}.lt-noite>.lt-w{position:relative;z-index:1}
.lt-of-foto{background:var(--pau)}
.lt-tempo-tag{font-size:10px;font-weight:600;letter-spacing:.22em;opacity:.9}
.lt-of-fim{font-weight:700;color:var(--ale);margin-bottom:8px!important}

/* ---- botão flutuante ---- */
.lt-flut[hidden]{display:none!important}.lt-flut{position:fixed;right:16px;bottom:20px;z-index:60;width:56px;height:56px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:26px;text-decoration:none;background:var(--pri);box-shadow:0 0 22px color-mix(in srgb,var(--pri) 55%,transparent),0 10px 26px -10px rgba(0,0,0,.5);animation:lt-desce 1.6s ease-in-out infinite}

/* seções fora da tela: animações pausadas */
.lt-pausa,.lt-pausa *,.lt-pausa *::before,.lt-pausa *::after{animation-play-state:paused!important}

@media (max-width:860px){
  .lt-dores{grid-template-columns:repeat(2,minmax(0,1fr))}
  .lt-vs,.lt-vs3,.lt-bonus-g,.lt-extras,.lt-passos{grid-template-columns:minmax(0,1fr)}
  .lt-gal{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
}
@media (max-width:760px){
  .lt-gar{grid-template-columns:minmax(0,1fr);padding:30px 22px;text-align:center;gap:22px}
  .lt-selo{max-width:190px;margin:0 auto}
  .lt-autor{grid-template-columns:minmax(0,1fr);gap:24px}
  .lt-autor-foto{order:-1;margin:0 auto;width:180px;height:180px}
}
@media (max-width:560px){
  .lt-sec{padding:48px 0}
  .lt-w{padding:0 18px}
  .lt-faixa{font-size:10px;letter-spacing:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:8px 15px}
  .lt-hero{padding:14px 0 36px}
  .lt-logo{height:44px;margin-bottom:10px}
  .lt-hero h1{font-size:1.42rem}
  .lt-sub{font-size:.86rem;line-height:1.4}
  .lt-palco{width:100%;margin:16px auto 16px}
  .lt-fones{gap:12px}
  .lt-fone{border-radius:18px;padding:5px}.lt-tela{border-radius:13px}
  .lt-badge{font-size:10.5px;padding:5px 9px}
  .lt-b1{top:2%;right:2%}.lt-b2{top:11%;right:0}.lt-b3{top:20%;right:3%}
  .lt-notif{font-size:11px;padding:4px 7px}.lt-notif svg{width:12px;height:12px}.lt-n2{font-size:13px}
  .lt-btn{font-size:14.5px;padding:17px 12px;gap:8px;letter-spacing:0;width:100%;min-width:0}
  .lt-dores{display:block}
  .lt-dor-card{background:#fff;border-radius:22px;padding:14px 14px 18px;margin:0 0 18px;box-shadow:0 18px 34px -24px rgba(3,22,63,.35)}
  .lt-dor-foto{aspect-ratio:16/10;border-radius:14px}
  .lt-dor-card p{font-size:16px;line-height:1.4;padding:0 4px}
  .lt-passos-ic li{width:92px;font-size:12px}.lt-passos-ic li+li::before{left:-14px}
  .lt-chips li{font-size:12.5px;padding:6px 11px}
  .lt-g-arte{padding:30px 9px 9px}.lt-g-arte b{font-size:13px}.lt-g-faixa{font-size:10px}
  .lt-g-lock .lt-g-img::after{width:44px;height:44px;font-size:18px}
  .lt-of-corpo{padding:22px 16px 24px}
  .lt-btn-of{font-size:13px;padding:16px 10px;gap:6px}
  .lt-of-eco{font-size:12.5px;padding:7px 12px}
  .lt-alerta{font-size:12.5px}
  .lt-wa{font-size:14px;padding:14px 18px}
  .lt-dep-print{flex-basis:200px}
}
"""

JS = r"""
(function(){if(!("IntersectionObserver"in window))return;var io=new IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle("lt-pausa",!e.isIntersecting)})},{rootMargin:"120px 0px"});document.querySelectorAll(".lt-hero,.lt-sec").forEach(function(el){io.observe(el)})})();
(function(){document.querySelectorAll("[data-conta]").forEach(function(el,i){var fim=+el.dataset.conta,n=0;el.textContent="0";setTimeout(function(){var t=setInterval(function(){n++;el.textContent=n;if(n>=fim)clearInterval(t)},Math.max(40,600/fim))},900+i*350)})})();
(function(){var el=document.querySelector("[data-lt-timer]");if(!el)return;var fim=new Date(el.dataset.fim).getTime();function z(n){return(n<10?"0":"")+n}
function tic(){var r=Math.max(0,fim-Date.now()),h=Math.floor(r/36e5),m=Math.floor(r%36e5/6e4),s=Math.floor(r%6e4/1e3);el.textContent=(h>=24?Math.floor(h/24)+"d ":"")+z(h%24)+" : "+z(m)+" : "+z(s);if(r>0)setTimeout(tic,1000)}tic()})();
(function(){var alvo=document.getElementById("lt-parabens"),feito=false;if(!alvo||!("IntersectionObserver"in window))return;
function soltar(){if(feito)return;feito=true;var r=alvo.getBoundingClientRect(),x=(r.left+r.width/2)/innerWidth,y=(r.top+r.height/2)/innerHeight,c=window.confetti;if(!c)return;var cores=["#16A34A","#22C55E","#0042FF","#FFD43B","#EF2B2D","#7C3AED"];
c({particleCount:120,spread:80,startVelocity:45,origin:{x:x,y:y},colors:cores});setTimeout(function(){c({particleCount:70,angle:60,spread:65,origin:{x:0,y:.75},colors:cores});c({particleCount:70,angle:120,spread:65,origin:{x:1,y:.75},colors:cores})},350)}
function carregar(cb){if(window.confetti)return cb();var s=document.createElement("script");s.src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.9.3/dist/confetti.browser.min.js";s.onload=cb;document.head.appendChild(s)}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.disconnect();carregar(soltar)}})},{threshold:.9});io.observe(alvo)})();
(function(){var v=document.getElementById("lt-video-passos");if(!v||!("IntersectionObserver"in window))return;v.pause();function para(){v.pause();if(v.currentTime)v.currentTime=0}
new IntersectionObserver(function(es){es.forEach(function(e){if(e.intersectionRatio>=.6){if(v.paused){v.preload="auto";var p=v.play();if(p)p.catch(function(){})}}else if(e.intersectionRatio<.2)para()})},{threshold:[0,.2,.6]}).observe(v);
document.addEventListener("visibilitychange",function(){if(document.hidden)v.pause()})})();
(function(){document.querySelectorAll("[data-vit]").forEach(function(box){var its=[].slice.call(box.querySelectorAll(".lt-vit-i")),n=its.length,cur=0,dots=[].slice.call(box.querySelectorAll(".lt-vit-dots i")),vis=true,t;if(!n)return;
function cfg(){var w=innerWidth;return w<640?[90,20,8,.06]:w<1024?[130,30,10,.09]:[170,40,12,.12]}
function pos(){var c=cfg();its.forEach(function(el,i){var d=((i-cur)%n+n)%n;if(d>n/2)d-=n;var a=Math.abs(d);el.style.transform="translateX("+d*c[0]+"px) translateY("+a*c[1]+"px) rotate("+d*c[2]+"deg) scale("+Math.max(.5,1-a*c[3])+")";el.style.zIndex=100-a;el.style.opacity=a>n/2-.5&&n>4?0:1});dots.forEach(function(x,i){x.classList.toggle("on",i===((cur%n)+n)%n)})}
function ir(k){cur+=k;pos()}function auto(){clearInterval(t);t=setInterval(function(){if(vis&&!document.hidden)ir(1)},+box.dataset.intervalo||2000)}
var a=box.querySelector("[data-vit-ant]"),p=box.querySelector("[data-vit-prox]");if(a)a.onclick=function(){ir(-1);auto()};if(p)p.onclick=function(){ir(1);auto()};
var x0=null;box.addEventListener("pointerdown",function(e){x0=e.clientX});box.addEventListener("pointerup",function(e){if(x0===null)return;var dx=e.clientX-x0;x0=null;if(Math.abs(dx)>30){ir(dx<0?1:-1);auto()}});
if("IntersectionObserver"in window)new IntersectionObserver(function(es){vis=es[0].isIntersecting}).observe(box);addEventListener("resize",pos,{passive:true});pos();auto()})})();
(function(){function go(){document.querySelectorAll("img[data-src]").forEach(function(i){if(i.dataset.srcset){i.srcset=i.dataset.srcset}i.src=i.dataset.src;i.removeAttribute("data-src")})}if(document.readyState==="complete")setTimeout(go,200);else addEventListener("load",function(){setTimeout(go,200)})})();
(function(){if(!("IntersectionObserver"in window))return;var io=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;if(e.isIntersecting){if(!v.src&&v.dataset.src){v.src=v.dataset.src}var p=v.play();if(p)p.catch(function(){})}else v.pause()})},{rootMargin:"300px 0px"});document.querySelectorAll("video[data-src]").forEach(function(v){io.observe(v)})})();
(function(){document.querySelectorAll(".lt-vv[data-embed]").forEach(function(b){function go(){if(b.dataset.ok)return;b.dataset.ok=1;var f=document.createElement("iframe");f.src=b.dataset.embed;f.allow="autoplay;encrypted-media;picture-in-picture;fullscreen";f.allowFullscreen=true;b.innerHTML="";b.appendChild(f)}b.querySelector("button").onclick=go;if("IntersectionObserver"in window){var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){io.disconnect();setTimeout(go,600)}},{rootMargin:"300px 0px"});io.observe(b)}})})();
(function(){document.querySelectorAll(".lt-trilho[data-auto]").forEach(function(tr){var parado=false;["pointerdown","touchstart","mouseenter"].forEach(function(e){tr.addEventListener(e,function(){parado=true},{passive:true})});tr.addEventListener("mouseleave",function(){parado=false});
setInterval(function(){if(parado||document.hidden)return;var c=tr.firstElementChild;if(!c)return;var w=c.getBoundingClientRect().width+16;if(tr.scrollLeft+tr.clientWidth>=tr.scrollWidth-4)tr.scrollTo({left:0,behavior:"smooth"});else tr.scrollBy({left:w,behavior:"smooth"})},3500)})})();
(function(){var el=document.querySelector("[data-lt-visita]");if(!el)return;var k="lt-ini-"+el.dataset.chave,ms=+el.dataset.ltVisita*6e4,ini=Date.now();try{var s=+localStorage.getItem(k);if(s&&Date.now()-s<864e5)ini=s;else localStorage.setItem(k,ini)}catch(e){}
function z(n){return(n<10?"0":"")+n}function tic(){var r=Math.max(0,ini+ms-Date.now());var p=[z(Math.floor(r/36e5)),z(Math.floor(r%36e5/6e4)),z(Math.floor(r%6e4/1e3))];if(el.dataset.fmt==="v2")el.innerHTML=p.join("<i>:</i>");else el.textContent=p.join(" : ");if(r>0)setTimeout(tic,1000)}tic()})();
(function(){var b=document.querySelector("[data-flut]");if(!b||!("IntersectionObserver"in window))return;var ids=b.dataset.flut.split(","),on={};var blocos=[].slice.call(document.querySelectorAll('[id^="b-"]'));
ids.forEach(function(id){var s=document.getElementById("b-"+id);if(!s)return;new IntersectionObserver(function(es){on[id]=es[0].isIntersecting;var at=ids.filter(function(x){return on[x]})[0];b.hidden=!at;if(at){var i=blocos.indexOf(document.getElementById("b-"+at)),nx=blocos[i+1];if(nx)b.setAttribute("href","#"+nx.id)}}).observe(s)})})();
(function(){var q=location.search.replace(/^\?/,"");document.querySelectorAll("[data-lt-checkout]").forEach(function(a){if(window.fbq)a.addEventListener("click",function(){fbq("track","InitiateCheckout")});if(!q)return;var h=a.getAttribute("href");if(h&&h.indexOf("http")===0)a.setAttribute("href",h+(h.indexOf("?")<0?"?":"&")+q)})})();
"""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = os.path.abspath(sys.argv[1])
    out = os.path.dirname(src)
    if "--saida" in sys.argv:
        out = os.path.abspath(sys.argv[sys.argv.index("--saida") + 1])
    cfg = json.load(open(src, encoding="utf-8"))
    os.makedirs(out, exist_ok=True)
    pagina = gerar(cfg, out)
    if "—" in pagina:
        AVISOS.append("a copy tem travessão (—): trocar por vírgula, ponto ou dois-pontos")
    dest = os.path.join(out, "index.html")
    open(dest, "w", encoding="utf-8").write(pagina)
    print("página gerada:", dest)
    for a in AVISOS:
        print("AVISO:", a)


if __name__ == "__main__":
    main()
