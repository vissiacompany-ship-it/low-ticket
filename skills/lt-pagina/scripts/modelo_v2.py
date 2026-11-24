"""Modelo v2 da página low ticket: réplica fiel do design do Instravel (Kamila Fontana).

Usado pelo gerar_pagina.py quando o pagina.json tem "modelo": "v2". Medidas, cores, sombras e efeitos
tirados do código da página de referência (playbook-pagina-lt.md, seções 6 e 6A). A estrutura é fixa;
a marca entra pelas cores ("cores"), fonte, imagens e textos.

Marcação de texto:
  [[texto]]  destaque (limão sobre a foto do topo; degradê quente com brilho nos títulos; secundária no Como funciona)
  {{texto}}  destaque simples na cor quente (sem brilho)
  **texto**  negrito
  linha 1|linha 2   quebra de linha escolhida (campos *_pc valem para o computador)
"""
import html, os, re

ICONES = {
    "smartphone": '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
    "grid": '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
    "camera": '<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>',
    "mensagem": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "editar": '<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>',
    "enviar": '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    "play": '<polygon points="6 3 20 12 6 21 6 3"/>',
    "estrela": '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arquivo": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/>',
    "coracao": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
}
SETA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>'
SETA_BAIXO = '<svg class="v-bounce" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M5 12l7 7 7-7"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
ALERTA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>'
RELOGIO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
CHEVRON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'

PADRAO_CORES = {
    "texto": "hsl(213 56% 40%)",          # azul do texto
    "titulo_escuro": "hsl(217 62% 19%)",  # títulos das seções claras de leitura
    "suave": "hsl(213 45% 45%)",
    "suave_escuro": "hsl(213 40% 32%)",
    "primaria": "#FF7043",                # quente: destaques, botões de avançar, etiqueta de bônus
    "quente_claro": "#FF8A65", "quente_escuro": "#F4511E", "texto_grad_claro": "#FFB199",
    "destaque_foto": "#FFF3A6",           # destaque sobre a foto do topo
    "acento": "#28C9E6",                  # secundária: Como funciona
    "clara": "#A8E6FF",                   # faixa do topo, bordas
    "clara_fundo": "#DCF1FB",             # etiquetas
    "etiqueta_texto": "#2D609F",
    "mundo": "#2C5F9E",                   # cor por baixo da foto do mundo do nicho
    "pausa": "#12294F",                   # transição e rodapé
    "fundo_fim": "#EAF6FD", "fundo_meio": "#F4FBFF",
    "sucesso": "#10B981", "sucesso_escuro": "#059669", "alerta": "#DC2626",
}


def render(cfg, base, G):
    img, attr = G.img, G.attr
    C = dict(PADRAO_CORES)
    dados = cfg.get("cores", {})
    if "primaria" in dados:  # marca nova: degradês derivados da cor quente, se não vierem prontos
        for k, pct in (("quente_claro", "75%, #fff"), ("texto_grad_claro", "55%, #fff"), ("quente_escuro", "85%, #000")):
            if k not in dados:
                C[k] = "color-mix(in srgb, %s %s)" % (dados["primaria"], pct)
    C.update(dados)
    produto = cfg["produto"]
    checkout = cfg.get("checkout", "")
    if not checkout:
        G.AVISOS.append("checkout vazio: botão da oferta ficou sem link")

    def tx(s):
        s = html.escape(str(s or ""), quote=False)
        s = re.sub(r"\[\[(.+?)\]\]", r'<em class="hl">\1</em>', s)
        s = re.sub(r"\{\{(.+?)\}\}", r'<em class="pk">\1</em>', s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        return s

    def linhas(cel, pc=None):
        """Texto com quebras escolhidas: uma versão para celular e outra para computador."""
        def ls(t):
            return "".join('<span class="ln">%s</span>' % tx(x.strip()) for x in str(t).split("|"))
        if pc is None and "|" not in str(cel):
            return tx(cel)
        return '<span class="so-cel">%s</span><span class="so-pc">%s</span>' % (ls(cel), ls(pc if pc is not None else cel))

    def etiqueta(t, cls="v-eb"):
        return '<span class="%s">%s</span>' % (cls, tx(t)) if t else ""

    def icone(nome, cls=""):
        if nome in ICONES:
            return '<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (cls, ICONES[nome])
        return '<span class="%s v-emo" aria-hidden="true">%s</span>' % (cls, html.escape(nome or "✨"))

    def carrossel(imagens, setas, alt, eager_centro):
        n = len(imagens)
        perto = lambda i: min(i, n - i) <= 1
        itens = "".join('<figure class="lt-vit-i">%s</figure>' % img(base, x, "", alt, 1080, 1920, i == 0 and eager_centro,
                        "(min-width:1024px) 256px, (min-width:640px) 224px, 176px", depois=not perto(i)) for i, x in enumerate(imagens))
        ctrl = ('<div class="lt-vit-ctrl"><button type="button" data-vit-ant aria-label="Anterior">%s</button><span class="lt-vit-dots">%s</span><button type="button" data-vit-prox aria-label="Próximo">%s</button></div>'
                % ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m15 18-6-6 6-6"/></svg>', "".join("<i></i>" for _ in imagens),
                   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>')) if setas else ""
        return '<div class="lt-vit v-vit" data-vit2 data-intervalo="%d"><div class="lt-vit-palco">%s</div>%s</div>' % (1000 if not setas else 3000, itens, ctrl)

    def pilha(imagens, alt):
        """Depoimentos: cartões retos em fila empurrados para trás em profundidade (pilha infinita dos dois lados)."""
        n = len(imagens)
        L = n * -(-25 // n)  # cópias suficientes para a pilha nunca acabar nas pontas
        itens = "".join('<div class="v-pi" data-k="%d">%s</div>' % (k, img(base, imagens[k % n], "", alt, 883, 1500, False,
                        "(min-width:1024px) 215px, (min-width:768px) 200px, (min-width:640px) 180px, 52vw", depois=k >= 3 and k < L - 2)) for k in range(L))
        sv = lambda d: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="%s"/></svg>' % d
        return ('<div class="v-pilha" data-pilha data-n="%d"><div class="v-pilha-palco">%s</div><div class="v-pilha-ctrl"><button type="button" data-ant aria-label="Depoimento anterior">%s</button>'
                '<span class="v-pilha-dots">%s</span><button type="button" data-prox aria-label="Próximo depoimento">%s</button></div></div>') % (
            n, itens, sv("M15 18l-6-6 6-6"), "".join('<button type="button" aria-label="Ir para o depoimento %d" data-ir="%d"></button>' % (i + 1, i) for i in range(n)), sv("M9 18l6-6-6-6"))

    B = {}
    h = cfg["hero"]

    # 1 + 2. topo e vitrine (mesmo fundo do mundo do nicho)
    fundo = img(base, h.get("fundo"), "v-mundo-img", "", 1920, 1080, True, "100vw", preload=True) if h.get("fundo") else ""
    espera = int(h.get("botao_espera", 0))  # contagem antes de liberar: desligada (decisão do Paulo, 04/11/2026)
    btn_topo = ('<div class="v-btn-wrap"><button type="button" class="v-btn v-btn-q v-btn-topo" data-alvo="b-%s" data-espera="%d"%s>'
                '<span class="v-barra" aria-hidden="true"></span><span class="v-btn-tx" data-tx="%s">%s</span></button></div>') % (
        attr(h.get("botao_alvo", "depoimentos")), espera, " disabled" if espera else "", attr(h.get("botao", "QUERO ↓")), ("%ds" % espera) if espera else tx(h.get("botao", "QUERO ↓")))
    faixa_rol = ""
    if h.get("faixa_rolante"):
        fx = "".join('<div class="v-mq-i">%s</div>' % img(base, x, "", "", 1080, 1920, sizes="(min-width:768px) 144px, 117px", depois=True) for x in h["faixa_rolante"])
        faixa_rol = '<div class="v-mq" aria-hidden="true"><div class="v-mq-in">%s%s</div></div>' % (fx, fx)
    B["topo"] = '''<div class="v-topo">%s
<section class="v-hero"><div class="v-faixa">%s<span>%s</span></div>
<div class="v-hero-c"><h1>%s</h1><p class="v-sub">%s</p></div></section>
<section class="v-vitrine">%s%s%s<div class="v-fade" aria-hidden="true"></div></section></div>''' % (
        '<div class="v-mundo" aria-hidden="true">%s</div>' % fundo if fundo else "",
        '<span aria-hidden="true">%s</span>' % html.escape(cfg.get("faixa_emoji", "")) if cfg.get("faixa_emoji") else "", tx(cfg.get("faixa", "")),
        linhas(h["titulo"], h.get("titulo_pc")), linhas(h.get("sub", ""), h.get("sub_pc")),
        carrossel(h.get("vitrine", []), False, "Modelo do " + produto, True), btn_topo, faixa_rol)

    # 3. depoimentos
    d = cfg.get("depoimentos") or {}
    if d.get("prints") or d.get("comentarios"):
        nt = d.get("nota") or {}
        nota = ""
        if nt:
            ramo = lambda k: img(base, nt[k], "v-ramo", "", 64, 128, sizes="64px") if nt.get(k) else ""
            nota = '''<div class="v-nota"><div class="v-nota-l">%s<span class="v-nota-n">%s</span>%s</div><p class="v-nota-a">%s</p>
<p class="v-nota-e" aria-label="5 estrelas">⭐⭐⭐⭐⭐</p><p class="v-nota-q">%s</p></div>''' % (
                ramo("ramo_esq"), tx(nt.get("valor", "5,0")), ramo("ramo_dir"), tx(nt.get("linha1", "")), tx(nt.get("linha2", "")))
        cores_ini = ["#2C5F9E", "#FF7043", "#43A047", "#7EC8E3", "#8E6BB5", "#E4A33B"]
        coms = "".join('''<div class="v-com"><div class="v-com-t"><span class="v-com-i" style="background:%s">%s</span><div><p class="v-com-n">%s</p>
<div class="v-com-d"><span>⭐⭐⭐⭐⭐</span><span>%s</span></div></div></div><p class="v-com-x">%s</p></div>''' % (
            cores_ini[i % 6], html.escape(c.get("nome", "?")[:1]), tx(c.get("nome")), tx(c.get("quando", "")), tx(c.get("texto"))) for i, c in enumerate(d.get("comentarios", [])))
        B["depoimentos"] = '''<section class="v-sec v-band-blue v-cloud v-dep"><div class="v-c">%s<h2 class="v-h2">%s</h2></div>
%s%s</section>''' % (nota, linhas(d.get("titulo", ""), d.get("titulo_pc")),
            '<div class="v-full">%s</div>' % pilha(d["prints"], "Story de cliente") if d.get("prints") else "",
            '<div class="v-coms-wrap"><div class="lt-trilho v-coms" data-auto>%s</div></div>' % coms if coms else "")

    # 4. categorias em vídeo
    ct = cfg.get("categorias") or {}
    if ct.get("itens"):
        cards = ""
        for x in ct["itens"]:
            if x.get("video"):
                midia = '<video data-src="%s" muted loop playsinline preload="none" width="540" height="960"%s aria-label="%s"></video>' % (
                    attr(x["video"]), ' data-poster="%s"' % attr(x["poster"]) if x.get("poster") else "", attr(x.get("rotulo", "")))
            else:
                midia = img(base, x.get("imagem"), "", x.get("rotulo", ""), 540, 960, sizes="(min-width:768px) 260px, 46vw")
            cards += '<div class="v-cat">%s<span class="v-cat-r"><span aria-hidden="true">%s</span><span>%s</span></span></div>' % (midia, html.escape(x.get("emoji", "")), tx(x.get("rotulo", "")))
        B["categorias"] = '''<section class="v-sec v-band-blue v-cats"><div class="v-c">%s<h2 class="v-h2 v-h2-cat">%s</h2>%s
<div class="v-cats-g">%s</div>%s</div></section>''' % (
            etiqueta(ct.get("etiqueta")), linhas(ct.get("titulo", ""), ct.get("titulo_pc")),
            '<p class="v-p-sub">%s</p>' % tx(ct["sub"]) if ct.get("sub") else "", cards,
            '<p class="v-p-fecho">%s</p>' % tx(ct["fecho"]) if ct.get("fecho") else "")

    # 5. como funciona
    ps = cfg.get("passos") or {}
    if ps:
        itens = ps.get("itens", [])
        passos = ""
        for i, it in enumerate(itens):
            passos += '<div class="v-ps"><div class="v-ps-ic"><span class="v-ps-glow" aria-hidden="true"></span><span class="v-ps-box">%s</span><span class="v-ps-n">%02d</span></div><p>%s</p></div>' % (
                icone(it.get("icone", "smartphone"), "v-ps-svg"), i + 1, tx(it["titulo"]))
            if i < len(itens) - 1:
                passos += '<div class="v-ps-seta">%s</div>' % SETA
        cols = " ".join(["1fr"] + ["auto 1fr"] * (len(itens) - 1)) if itens else "1fr"
        vd = ps.get("video") or {}
        if vd.get("embed"):
            vtag = '<div class="lt-vv v-vv" data-embed="%s"><button type="button" class="v-vv-play" aria-label="Carregar vídeo">%s<span>%s</span></button></div>' % (
                attr(vd["embed"]), img(base, vd.get("poster"), "", "", 1080, 1920, sizes="300px") if vd.get("poster") else "", '<svg viewBox="0 0 24 24" fill="currentColor"><polygon points="6 3 20 12 6 21 6 3"/></svg>')
        elif vd.get("mp4"):
            vtag = '<div class="v-vv"><video src="%s"%s controls playsinline preload="none" width="1080" height="1920"></video></div>' % (attr(vd["mp4"]), ' poster="%s"' % attr(vd["poster"]) if vd.get("poster") else "")
        else:
            vtag = ""
        pb = ps.get("botao") or {}
        btn = '<div class="v-ps-btn"><a class="v-btn v-btn-a" href="#b-%s">%s%s</a></div>' % (attr(pb.get("alvo", "bonus")), tx(pb["texto"]), SETA_BAIXO) if pb.get("texto") else ""
        titulo = tx(ps.get("titulo", ""))
        B["passos"] = '''<section class="v-sec v-band-light v-cloud v-pv" id="como-funciona"><div class="v-c">%s
<div class="v-pv-g"><div class="v-pv-esq"><h2 class="v-h2 v-pv-t so-pc">%s</h2><div class="v-ps-g" style="grid-template-columns:%s">%s</div>%s</div>
<div class="v-pv-dir"><h2 class="v-h2 v-pv-t so-cel">%s</h2>%s<div class="v-vv-box">%s</div></div></div></div></section>''' % (
            etiqueta(ps.get("etiqueta")), titulo, cols, passos, btn, titulo,
            '<p class="v-pv-l">%s</p>' % tx(ps["linha"]) if ps.get("linha") else "", vtag)

    # 6. bônus
    b = cfg.get("bonus") or {}
    if b.get("itens"):
        cards = "".join('''<div class="v-card v-bn"><div class="v-bn-im-cel">%s</div><div class="v-bn-tx"><span class="v-eb-q">%s</span><h3>%s</h3><p>%s</p></div>
<div class="v-bn-im-pc">%s</div></div>''' % (
            img(base, x.get("imagem"), "", x.get("titulo", ""), 400, 400, sizes="112px"), tx(x.get("rotulo", "Bônus %d" % (i + 1))), tx(x["titulo"]), tx(x["texto"]),
            img(base, x.get("imagem"), "", x.get("titulo", ""), 400, 400, sizes="320px")) for i, x in enumerate(b["itens"]))
        B["bonus"] = '''<section class="v-sec v-band-blue v-cloud v-bns"><div class="v-c">%s<h2 class="v-h2 v-h2-bn">%s</h2><div class="v-bns-g">%s</div></div></section>''' % (
            etiqueta(b.get("etiqueta")), linhas(b.get("titulo", ""), b.get("titulo_pc")), cards)

    # 7. transição
    if cfg.get("transicao"):
        B["transicao"] = '<section class="v-trans"><p>%s</p></section>' % tx(cfg["transicao"])

    # 8. oferta
    of = cfg["oferta"]
    num = G.num
    de = num(of["de"]) if of.get("de") else None
    avista = num(of["avista"])
    eco = of.get("economia") or ("R$%d" % round(de - avista) if de else "")
    pct = round((1 - avista / de) * 100) if de else 0
    minutos = int(of.get("cronometro_minutos", 15))
    cheio = ""  # ao zerar o cronômetro nada muda na oferta (decisão do Paulo, 04/11/2026)
    parc = of.get("parcela", "")
    p_int, p_dec = (parc.split(",") + [""])[:2]
    checks = of.get("checks", ["Pagamento único", "Sem mensalidade", "Acesso imediato"])
    ck = lambda t: '<span class="v-ck">%s %s</span>' % (CHECK, tx(t))
    checks_html = '<li>%s<span class="v-ck-sep">|</span>%s</li>' % (ck(checks[0]), ck(checks[1])) if len(checks) >= 2 else ""
    checks_html += "".join("<li>%s</li>" % ck(c) for c in checks[2:])
    confete = "".join('<span style="left:%.1f%%;background:%s;animation-delay:%.2fs;animation-duration:%.2fs"></span>' % (
        (t * 3.9 + 2) % 98, ["#FF7043", "#34D399", "#A8E6FF", "#FFD166"][t % 4], (t % 8) * .12, 2 + (t % 5) * .25) for t in range(26))
    B["oferta"] = '''<section class="v-of" id="oferta">%s<div class="v-of-c"><div class="v-confete" aria-hidden="true">%s</div>
<div class="v-pill-w"><span class="v-pill">%s</span></div>
<div class="v-of-card lt-of-desc-wrap"><div class="v-of-top"><span class="v-of-tag">%s</span><div class="v-tempo">%s<span data-lt-visita="%d" data-fmt="v2" data-chave="%s">00<i>:</i>%02d<i>:</i>00</span></div><p>%s</p></div>
<div class="v-of-body">%s<div class="lt-of-desc"><div class="v-of-row">%s<div class="v-of-info">%s<p class="v-of-bn">%s</p>%s</div></div>
<p class="v-of-por">%s</p><p class="v-preco">R$ %s<span>%s</span></p><p class="v-of-av">%s</p>
<div class="v-eco-w"><span class="v-eco">%s</span></div>
<a class="v-btn-c" href="%s" data-lt-checkout>%s</a>%s
<ul class="v-cks">%s</ul>%s</div></div></div></div></section>''' % (
        '<div class="v-mundo v-of-mundo" aria-hidden="true">%s</div>' % img(base, of["fundo"], "v-mundo-img", "", 1920, 1080, sizes="100vw") if of.get("fundo") else "",
        confete, tx(of.get("parabens", "🎉 Parabéns!!! Você ganhou %d%% OFF" % pct)),
        tx(of.get("etiqueta_tempo", "Oferta por tempo limitado")), RELOGIO, minutos, attr(re.sub(r"\W", "", produto.lower())), minutos % 60,
        tx(of.get("frase_tempo", "Válida somente até o tempo acabar.")), cheio,
        img(base, of.get("mockup"), "v-of-mock", "Entregáveis do " + produto, 600, 400, sizes="190px") if of.get("mockup") else "",
        img(base, of.get("logo"), "v-of-logo", produto, 300, 100, sizes="200px") if of.get("logo") else '<p class="v-of-nome">%s</p>' % tx(produto),
        tx(of.get("bonus_linha", "")), '<p class="v-of-de">De R$ %s</p>' % G.brl(de) if de else "",
        tx(of.get("por", "por apenas %s de" % of.get("parcelas", "12x"))), html.escape(p_int + ("," if p_dec else "")), html.escape(p_dec),
        tx(of.get("avista_linha", "ou R$ %s à vista" % G.brl(avista))), tx(of.get("economia_linha", "Você economiza %s levando agora" % eco)),
        attr(checkout), tx(of.get("botao", "QUERO")),
        img(base, of.get("pagamentos_img"), "v-pay", "Formas de pagamento aceitas", 440, 80, sizes="220px") if of.get("pagamentos_img") else "",
        checks_html, '<div class="v-alerta">%s<span>%s</span></div>' % (ALERTA, tx(of["alerta"]).replace("|", "<br>")) if of.get("alerta") else "")

    # 9. garantia
    g = cfg.get("garantia") or {}
    if g:
        selo = img(base, g.get("selo"), "v-selo", "Selo de garantia de %s dias" % g.get("dias", 7), 1024, 1024, sizes="224px") if g.get("selo") else '<div class="v-selo">%s</div>' % G.selo_svg(g.get("dias", 7), C["pausa"], C["primaria"])
        B["garantia"] = '''<section class="v-sec v-band-blue v-cloud v-gar"><div class="v-c"><div class="v-card v-gar-card">%s<div class="v-gar-t"><h2>%s <em>%s</em></h2><p>%s</p></div></div></div></section>''' % (
            selo, tx(g.get("titulo", "GARANTIA DE")), tx(g.get("titulo_destaque", "%s DIAS" % g.get("dias", 7))), tx(g.get("texto", "")))

    # 10. autoridade
    a = cfg.get("autor") or {}
    if a:
        pars = "".join('<p%s>%s</p>' % (' class="v-au-1"' if i == 0 else "", tx(p)) for i, p in enumerate(a.get("paragrafos", [])))
        B["autor"] = '''<section class="v-sec v-band-light v-cloud v-au"><div class="v-c"><div class="v-au-g"><div class="v-au-tx"><h2>%s</h2><p class="v-au-cargo">%s</p><div class="v-au-ps">%s</div></div>
<div class="v-au-foto">%s</div></div></div></section>''' % (tx(a.get("titulo", "")), tx(a.get("cargo", "")), pars, img(base, a.get("foto"), "", a.get("titulo", ""), 600, 600, sizes="(min-width:768px) 288px, 224px"))

    # 11. FAQ
    fq = cfg.get("faq") or {}
    if fq.get("itens"):
        its = "".join('<details class="v-card v-fq" name="faq"><summary>%s%s</summary><p>%s</p></details>' % (tx(q), CHEVRON, tx(r)) for q, r in fq["itens"])
        B["faq"] = '''<section class="v-sec v-band-light v-faq"><div class="v-c"><div class="v-faq-h">%s<h2 class="v-h2-faq">%s</h2></div><div class="v-fqs">%s</div></div></section>''' % (
            etiqueta(fq.get("etiqueta")), tx(fq.get("titulo", "Perguntas frequentes")), its)

    # 12. WhatsApp (opcional, decisão por oferta)
    w = cfg.get("whatsapp") or {}
    if w.get("numero"):
        import urllib.parse
        link = "https://wa.me/%s?text=%s" % (re.sub(r"\D", "", w["numero"]), urllib.parse.quote(w.get("mensagem", "Olá! Vim pela página do %s e tenho uma dúvida." % produto)))
        B["whatsapp"] = '<section class="v-sec v-band-light v-wa"><div class="v-c"><h2 class="v-h2">%s</h2><a class="v-btn-c v-wa-b" href="%s" target="_blank" rel="noopener">%s</a></div></section>' % (
            tx(w.get("titulo", "Ficou com alguma dúvida?")), attr(link), tx(w.get("botao", "Falar no WhatsApp")))

    # 13. rodapé
    rd = cfg.get("rodape") or {}
    leg = []
    if rd.get("politica") is not None:
        leg.append('<a href="%s">Política de Privacidade</a>' % attr(rd.get("politica") or "#"))
    if rd.get("termos") is not None:
        leg.append('<a href="%s">Termos de Uso</a>' % attr(rd.get("termos") or "#"))
    B["rodape"] = '''<footer class="v-rod"><div class="v-rod-c">%s<p class="v-rod-m">© %s %s<br>Todos os Direitos Reservados</p>%s%s
<p class="v-rod-av">Este site não possui qualquer vínculo ou afiliação com o Facebook ou suas empresas associadas. Após sair do Facebook, toda responsabilidade passa a ser exclusivamente do nosso site. A aquisição deste material não assegura resultados específicos.</p></div></footer>''' % (
        img(base, rd.get("logo"), "v-rod-logo", produto, 300, 100, sizes="150px") if rd.get("logo") else "", html.escape(str(rd.get("ano", "2026"))), html.escape(rd.get("marca", produto.upper())),
        '<p>%s</p>' % html.escape(rd["empresa"] + (" | CNPJ: %s" % rd["cnpj"] if rd.get("cnpj") else "")) if rd.get("empresa") else "",
        '<p>%s</p>' % " · ".join(leg) if leg else "")

    # montagem
    padrao = ["topo", "depoimentos", "categorias", "passos", "bonus", "transicao", "oferta", "garantia", "autor", "faq", "whatsapp", "rodape"]
    ordem = cfg.get("ordem") or padrao
    if "topo" not in ordem:
        ordem = ["topo"] + list(ordem)
    S = ['<div id="b-%s">%s</div>' % (k, B[k]) for k in ordem if k in B]
    for k in B:
        if k not in ordem:
            G.AVISOS.append("bloco '%s' existe mas não está em 'ordem': ficou fora da página" % k)
    flut = cfg.get("flutuante", ["depoimentos", "bonus"])
    if flut:
        S.append('<button type="button" class="v-flut" data-v-flut="%s" data-espera="%d" hidden aria-label="Continuar navegando"></button>' % (attr(",".join(flut)), int(cfg.get("flutuante_espera", 0))))

    css = CSS
    for k in sorted(C, key=len, reverse=True):
        css = css.replace("$" + k, C[k])
    fonte = cfg.get("fonte", "Poppins")
    ff_css, ff_pre = G.fonte_local(base, fonte)
    fonte_tags = ff_pre if ff_css else '<link href="https://fonts.googleapis.com/css2?family=%s:wght@400;500;600;700;800&display=swap" rel="stylesheet">' % fonte.replace(" ", "+")
    css = ff_css + css.replace("$fonte", fonte)

    rt = cfg.get("rastreio", {})
    head_extra = ""
    if rt.get("meta_pixel_id"):
        head_extra = ("<script>!function(f,b){if(f.fbq)return;var n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];"
                      "function go(){if(go.d)return;go.d=1;var t=b.createElement('script');t.async=!0;t.src='https://connect.facebook.net/en_US/fbevents.js';b.head.appendChild(t)}"
                      "addEventListener('load',function(){setTimeout(go,2500)});['scroll','pointerdown','touchstart','keydown'].forEach(function(e){addEventListener(e,go,{once:true,passive:true})})}(window,document);"
                      "fbq('init','%s');fbq('track','PageView');</script>" % attr(rt["meta_pixel_id"]))
    tail = ""
    if rt.get("clarity_id"):
        tail = "<script>addEventListener('load',function(){setTimeout(function(){(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src='https://www.clarity.ms/tag/'+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)})(window,document,'clarity','script','%s')},2500)});</script>" % attr(rt["clarity_id"])

    return '''<!doctype html>
<html lang="pt-BR" translate="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title><meta name="description" content="%s">%s<meta name="theme-color" content="%s">
%s%s<style>%s</style>%s</head><body><div class="lt v2">
%s
</div><script>%s%s</script>%s</body></html>''' % (
        attr(cfg.get("titulo_aba", produto)), attr(cfg.get("descricao", "")), '<meta name="robots" content="noindex">' if cfg.get("noindex", True) else "", attr(C["acento"]),
        fonte_tags, "".join(dict.fromkeys(G.PRELOAD)), css, head_extra, "\n".join(S), G.JS, JS, tail)


CSS = r"""
:root{--tx:$texto;--te:$titulo_escuro;--su:$suave;--se:$suave_escuro;--q:$primaria;--q1:$quente_claro;--q2:$quente_escuro;--qt:$texto_grad_claro;--lm:$destaque_foto;--ac:$acento;--cl:$clara;--clf:$clara_fundo;--ebt:$etiqueta_texto;--mu:$mundo;--pa:$pausa;--f1:$fundo_meio;--f2:$fundo_fim;--ok:$sucesso;--ok2:$sucesso_escuro;--al:$alerta;
 --sh-card:0 16px 40px -22px color-mix(in srgb,var(--tx) 25%,transparent),0 0 0 1px color-mix(in srgb,var(--cl) 55%,transparent),0 0 26px color-mix(in srgb,var(--cl) 35%,transparent);
 --sh-lift:0 24px 55px -22px color-mix(in srgb,var(--tx) 30%,transparent),0 0 0 1px color-mix(in srgb,var(--cl) 75%,transparent),0 0 38px color-mix(in srgb,var(--cl) 50%,transparent);
 --sh-soft:0 14px 40px -16px hsl(217 62% 15% / .4),0 4px 12px -6px hsl(217 62% 15% / .22);--sh-hover:0 28px 70px -18px hsl(217 62% 12% / .5),0 8px 20px -8px hsl(14 100% 55% / .3)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#fff}
.v2{font-family:"$fonte",system-ui,sans-serif;color:var(--tx);-webkit-font-smoothing:antialiased;overflow-x:clip;line-height:1.5}
:where(.v2) :where(h1,h2,h3,p){margin:0}:where(.v2) :where(h1,h2,h3){letter-spacing:-.02em;font-weight:800}
:where(.v2) em{font-style:normal}:where(.v2) img{max-width:100%;height:auto;display:block}:where(.v2) strong{font-weight:700}
.v2 .ln{display:block}.so-pc{display:none}@media(min-width:768px){.so-cel{display:none!important}.so-pc{display:block}.v2 h2.so-pc{display:block}}
.v-c{max-width:80rem;margin:0 auto;text-align:center}
.v-sec{padding:3rem 1.5rem;position:relative}@media(min-width:768px){.v-sec{padding:4rem 1.5rem}}
.v-band-blue{background:linear-gradient(180deg,#fff,var(--f1) 55%,var(--f2))}
.v-band-light{background:linear-gradient(180deg,#fff,var(--f1) 60%,var(--f2));--tx:var(--te);--su:var(--se)}
.v-cloud::before{content:"";position:absolute;top:-26px;left:0;right:0;height:64px;pointer-events:none;z-index:1;background:radial-gradient(28% 60% at 12% 70%,rgba(255,255,255,.95),transparent 72%),radial-gradient(22% 52% at 34% 55%,rgba(255,255,255,.85),transparent 72%),radial-gradient(26% 58% at 58% 72%,rgba(255,255,255,.9),transparent 72%),radial-gradient(20% 48% at 82% 58%,rgba(255,255,255,.8),transparent 72%);filter:blur(10px)}
.v-sec,.v-trans,.v-of,.v-rod{content-visibility:auto;contain-intrinsic-size:auto 800px}

/* etiquetas */
.v-eb,.v-eb-q{display:inline-flex;align-items:center;border-radius:9999px;padding:.375rem 1rem;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.18em}
.v-eb{background:var(--clf);border:1px solid var(--cl);color:var(--ebt);margin-bottom:1.25rem}
.v-eb-q{background:var(--q);color:#fff;border:1px solid color-mix(in srgb,var(--q) 55%,transparent);box-shadow:0 6px 18px color-mix(in srgb,var(--q) 45%,transparent),inset 0 1px #fff6}

/* destaques */
.v2 em.hl{display:inline-block;font-weight:800;background:linear-gradient(180deg,var(--qt) 0%,var(--q1) 45%,var(--q) 100%);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent;filter:drop-shadow(0 1px 0 hsl(217 62% 15% / .25)) drop-shadow(0 3px 12px color-mix(in srgb,var(--q) 45%,transparent))}
.v2 em.pk{color:var(--q);font-weight:inherit}

/* títulos */
.v-h2{font-weight:700;font-size:clamp(20px,5.6vw,28px);line-height:1.22;margin:0 auto 2rem;color:var(--tx)}
@media(min-width:768px){.v-h2{font-size:clamp(28px,3.4vw,40px);margin-bottom:2.5rem}}
.v-p-sub{color:var(--su);font-size:14px;line-height:1.625;max-width:42rem;margin:0 auto 2rem}
@media(min-width:768px){.v-p-sub{font-size:16px;margin-bottom:2.5rem}}

/* botões */
.v-btn{position:relative;display:inline-flex;align-items:center;justify-content:center;gap:.5rem;border:0;border-radius:9999px;padding:1rem 2rem;font:700 1rem/1.5rem "$fonte",system-ui,sans-serif;text-transform:uppercase;letter-spacing:.025em;color:#fff;text-decoration:none;cursor:pointer;transition:all .3s cubic-bezier(.4,0,.2,1);overflow:hidden;white-space:nowrap}
.v-btn::before{content:"";position:absolute;inset:1px 1px auto;height:45%;border-radius:9999px 9999px 50% 50%/9999px 9999px 100% 100%;background:linear-gradient(180deg,#ffffff8c,#fff0);pointer-events:none;z-index:1}
.v-btn::after{content:"";position:absolute;left:-30%;top:0;bottom:0;width:30%;background:linear-gradient(100deg,transparent,hsl(0 0% 100% / .45),transparent);transform:skew(-18deg);transition:left .7s ease;pointer-events:none;z-index:2}
.v-btn:hover::after{left:130%}.v-btn>*{position:relative;z-index:3}
.v-btn-q{background:linear-gradient(180deg,var(--q1) 0%,var(--q) 55%,var(--q2) 100%);text-shadow:0 1px 2px hsl(0 60% 25% / .35);box-shadow:inset 0 2px #ffffff8c,inset 0 -3px color-mix(in srgb,var(--q2) 50%,#000 20%),inset 0 0 18px #fff3,0 10px 24px -8px color-mix(in srgb,var(--q2) 55%,transparent),0 18px 40px -12px color-mix(in srgb,var(--q2) 45%,transparent)}
.v-btn-a{background:var(--ac);text-shadow:0 1px 2px hsl(195 80% 25% / .35);box-shadow:inset 0 2px #ffffff8c,inset 0 -3px color-mix(in srgb,var(--ac) 50%,#000 25%),inset 0 0 18px #fff3,0 10px 24px -8px color-mix(in srgb,var(--ac) 55%,transparent),0 18px 40px -12px color-mix(in srgb,var(--ac) 50%,transparent);animation:v-pulse-a 2.2s ease-in-out infinite;font-size:13px;padding:1rem 1.25rem}
@media(min-width:768px){.v-btn-a{font-size:1rem;padding:1rem 2rem}}
.v-btn-a:hover{animation-play-state:paused;transform:translateY(-2px)}
.v-pulse{animation:v-pulse 2.2s ease-in-out infinite}.v-pulse:hover{animation-play-state:paused}
@keyframes v-pulse{0%,to{transform:translateY(0);box-shadow:0 0 color-mix(in srgb,var(--q) 60%,transparent),var(--sh-soft)}50%{transform:translateY(-10px);box-shadow:0 14px 24px -10px color-mix(in srgb,var(--q) 70%,transparent),var(--sh-hover)}}
@keyframes v-pulse-a{0%,to{transform:translateY(0);box-shadow:0 0 color-mix(in srgb,var(--ac) 60%,transparent),var(--sh-soft)}50%{transform:translateY(-10px);box-shadow:0 14px 24px -10px color-mix(in srgb,var(--ac) 70%,transparent),var(--sh-hover)}}
.v-btn svg.v-bounce{width:16px;height:16px;animation:v-bounce 1.2s ease-in-out infinite}
@keyframes v-bounce{0%,to{transform:translateY(0)}50%{transform:translateY(4px)}}

/* topo + vitrine */
.v-topo{position:relative;isolation:isolate}
.v-mundo{position:absolute;inset:0;z-index:-1;background:var(--mu);overflow:hidden}
.v-mundo-img{width:100%;height:100%;object-fit:cover;object-position:center bottom}
@media(min-width:768px){.v-mundo-img{object-position:center}}
.v-hero{position:relative;display:flex;flex-direction:column;overflow:hidden}
.v-faixa{display:inline-flex;align-self:center;align-items:center;justify-content:center;gap:.5rem;padding:0 1.25rem;height:44px;border-radius:0 0 18px 18px;font-size:10px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;white-space:nowrap;border:1px solid var(--cl);border-top:0;background:var(--cl);color:var(--mu);box-shadow:0 8px 22px -6px color-mix(in srgb,var(--cl) 55%,transparent),inset 0 1px 0 hsl(0 0% 100% / .35)}
.v-faixa>span[aria-hidden]{font-size:1rem;line-height:1}
@media(min-width:640px){.v-faixa{font-size:12px}}
.v-hero-c{max-width:80rem;width:100%;margin:0 auto;padding:1.5rem .5rem .75rem;display:flex;flex-direction:column;align-items:center;text-align:center;gap:.5rem}
@media(min-width:768px){.v-hero-c{padding:2rem 1.25rem 1.25rem;gap:1rem}}
.v-hero h1{font-weight:600;line-height:1.18;font-size:clamp(17px,5.5vw,26px);letter-spacing:-.035em;color:#fff;filter:drop-shadow(0 2px 12px rgba(18,41,79,.35))}
@media(min-width:768px){.v-hero h1{line-height:1.15;font-size:clamp(30px,3.9vw,40px);letter-spacing:-.02em}}
.v-hero .ln{white-space:nowrap}
.v-hero h1 em.hl,.v-hero h1 em.pk{display:inline-block;font-weight:800;color:var(--lm);background:none;-webkit-text-fill-color:currentColor;filter:drop-shadow(0 2px 10px hsl(217 62% 15% / .35))}
.v-sub{margin-top:.25rem;font-weight:500;color:#fff;filter:drop-shadow(0 1px 4px rgba(18,41,79,.45));line-height:1.4;font-size:clamp(10.5px,3.3vw,15px);letter-spacing:-.01em}
@media(min-width:768px){.v-sub{margin-top:.375rem;font-size:clamp(15px,1.6vw,19px)}}
.v-sub em.hl,.v-sub em.pk{color:var(--lm);font-weight:500;background:none;-webkit-text-fill-color:currentColor;filter:none}
.v-vitrine{position:relative;padding:.5rem 0 2.5rem}
@media(min-width:768px){.v-vitrine{padding-bottom:3.5rem}}
.v-vitrine>*{position:relative;z-index:1}
.v-fade{position:absolute!important;left:0;right:0;bottom:0;height:5rem;z-index:0!important;pointer-events:none;background:linear-gradient(to top,#fff 0%,rgba(255,255,255,.9) 12%,rgba(255,255,255,.35) 32%,transparent 58%)}
@media(min-width:768px){.v-fade{height:7rem}}
.v-btn-wrap{position:relative;z-index:150;display:flex;justify-content:center;padding:0 1.25rem;margin-top:.75rem}
.v-vitrine .v-mq{z-index:150}
.v-btn-topo{width:fit-content;min-width:190px;max-width:100%;padding:1rem 2rem;font-size:14px;line-height:1.375rem}
@media(min-width:768px){.v-btn-topo{padding:1rem 2.5rem;font-size:16px;line-height:1.5rem}}
.v-btn-topo:disabled{cursor:not-allowed;opacity:.7;filter:saturate(.85)}
.v-barra{position:absolute!important;inset:0 auto 0 0;width:0;z-index:1!important;border-radius:9999px;background:rgba(255,255,255,.25);transition:width 1s linear}
.v-mq{position:relative;overflow:hidden;margin-top:1.25rem}
.v-mq::before,.v-mq::after{content:"";position:absolute;top:0;bottom:0;width:3rem;z-index:2;pointer-events:none}
.v-mq::before{left:0;background:linear-gradient(to right,var(--mu),transparent)}.v-mq::after{right:0;background:linear-gradient(to left,var(--mu),transparent)}
@media(min-width:768px){.v-mq::before,.v-mq::after{width:6rem}}
.v-mq-in{display:flex;width:max-content;gap:.75rem;animation:v-mq 40s linear infinite}
@media(min-width:768px){.v-mq-in{gap:1rem}}
@keyframes v-mq{to{transform:translateX(-50%)}}
.v-mq-i{flex:none;height:13rem;aspect-ratio:1080/1920;border-radius:.75rem;overflow:hidden;background:#fff;border:1px solid color-mix(in srgb,var(--cl) 50%,transparent);box-shadow:0 1px 2px rgba(0,0,0,.05)}
@media(min-width:768px){.v-mq-i{height:16rem}}
.v-mq-i img{height:100%;width:auto;object-fit:contain}

/* carrossel 3D (vitrine e depoimentos): sem sombra nem borda, cantos limpos */
.v-vit{position:relative;width:100vw;max-width:100vw;margin-left:calc(50% - 50vw);overflow:hidden;user-select:none;touch-action:pan-y}
.v-vitrine .v-vit{overflow-x:clip;overflow-y:visible}
@media(max-width:767px){.v-vitrine .v-btn-wrap{margin-top:36px}}
.v-vit .lt-vit-palco{position:relative;height:20rem;display:flex;align-items:center;justify-content:center}
@media(min-width:640px){.v-vit .lt-vit-palco{height:28rem}}@media(min-width:1024px){.v-vit .lt-vit-palco{height:32rem}}
.v-vit .lt-vit-i{position:absolute;margin:0;width:11rem;aspect-ratio:9/16;border-radius:1rem;overflow:hidden;will-change:transform,opacity;cursor:grab}
@media(min-width:640px){.v-vit .lt-vit-i{width:14rem}}@media(min-width:1024px){.v-vit .lt-vit-i{width:16rem}}
.v-vit .lt-vit-i img{width:100%;height:100%;max-width:none;object-fit:contain;pointer-events:none}
.v-vit .lt-vit-ctrl{display:flex;align-items:center;justify-content:center;gap:1rem;margin-top:.5rem}
.v-vit .lt-vit-ctrl button{display:flex;align-items:center;justify-content:center;width:2.25rem;height:2.25rem;border-radius:50%;border:1px solid var(--cl);background:transparent;color:var(--su);cursor:pointer}
.v-vit .lt-vit-ctrl svg{width:1rem;height:1rem}
.v-vit .lt-vit-dots{display:flex;gap:.375rem}.v-vit .lt-vit-dots i{width:6px;height:6px;border-radius:50%;background:color-mix(in srgb,var(--su) 30%,transparent)}.v-vit .lt-vit-dots i.on{background:var(--q)}

/* depoimentos: pilha em profundidade (perspectiva), infinita dos dois lados */
.v-pilha{position:relative;width:100%;overflow-x:clip;padding:16px 0 8px}
.v-pilha-palco{position:relative;height:calc(min(52vw,210px)*1500/883);perspective:1200px;transform-style:preserve-3d;cursor:grab;touch-action:pan-y;user-select:none}
@media(min-width:640px){.v-pilha-palco{height:calc(180px*1500/883)}}@media(min-width:768px){.v-pilha-palco{height:calc(200px*1500/883)}}@media(min-width:1024px){.v-pilha-palco{height:calc(215px*1500/883)}}
.v-pilha-palco:active{cursor:grabbing}
.v-pi{position:absolute;top:0;left:50%;width:min(52vw,210px);margin-left:calc(min(52vw,210px)/-2);aspect-ratio:883/1500;border-radius:1rem;overflow:hidden;will-change:transform;backface-visibility:hidden}
@media(min-width:640px){.v-pi{width:180px;margin-left:-90px}}@media(min-width:768px){.v-pi{width:200px;margin-left:-100px}}@media(min-width:1024px){.v-pi{width:215px;margin-left:-107.5px}}
.v-pi img{display:block;width:100%;height:100%;object-fit:cover;object-position:top;pointer-events:none}
.v-pilha-ctrl{margin-top:1rem;display:flex;align-items:center;justify-content:center;gap:.75rem}
.v-pilha-ctrl>button{display:flex;align-items:center;justify-content:center;width:2rem;height:2rem;border-radius:50%;border:1px solid color-mix(in srgb,var(--cl) 60%,transparent);background:transparent;color:var(--su);cursor:pointer;transition:color .2s}
.v-pilha-ctrl>button:hover{color:var(--q)}
.v-pilha-dots{display:flex;gap:.375rem}.v-pilha-dots button{width:7px;height:7px;padding:0;border:0;border-radius:50%;background:color-mix(in srgb,var(--su) 30%,transparent);cursor:pointer;transition:all .3s}
.v-pilha-dots button.on{transform:scale(1.25);background:var(--q)}
/* depoimentos */
.v-dep{padding-top:3rem}
.v-nota{display:flex;flex-direction:column;align-items:center;gap:.25rem;margin-bottom:1.25rem}
@media(min-width:768px){.v-nota{margin-bottom:1.5rem}}
.v-nota-l{display:flex;align-items:center;justify-content:center;gap:.5rem}
@media(min-width:768px){.v-nota-l{gap:.75rem}}
.v-ramo{height:clamp(44px,13vw,64px);width:auto}
.v-nota-n{font-weight:800;line-height:1;font-size:clamp(40px,12vw,66px);letter-spacing:-.02em;color:var(--tx)}
.v-nota-a{font-size:clamp(14px,4vw,18px);color:#171717;line-height:1.375}
.v-nota-e{font-size:clamp(16px,4.5vw,20px);line-height:1}
.v-nota-q{font-size:clamp(14px,4vw,18px);line-height:1.375;margin-top:.25rem!important}
.v-full{width:100vw;margin-left:calc(50% - 50vw)}
.v-coms-wrap{position:relative;margin:2rem -1.5rem 0;padding:0 1rem}
@media(min-width:768px){.v-coms-wrap{margin:2.5rem auto 0;padding:0;max-width:80rem}
 .v-coms-wrap::before,.v-coms-wrap::after{content:"";position:absolute;top:0;bottom:0;width:12%;z-index:2;pointer-events:none}
 .v-coms-wrap::before{left:0;background:linear-gradient(to right,var(--f1),transparent)}.v-coms-wrap::after{right:0;background:linear-gradient(to left,var(--f1),transparent)}}
.v-coms{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;padding:6px 0 4px;scrollbar-width:none}.v-coms::-webkit-scrollbar{display:none}
.v-com{flex:0 0 82vw;max-width:340px;scroll-snap-align:start;border-radius:1rem;background:#fff;padding:1rem;text-align:left;box-shadow:0 6px 20px rgba(44,95,158,.1),0 0 0 1px color-mix(in srgb,var(--cl) 70%,transparent)}
@media(min-width:640px){.v-com{flex-basis:320px}}@media(min-width:768px){.v-com{flex-basis:340px}}
.v-com-t{display:flex;align-items:center;gap:.75rem;margin-bottom:.5rem}
.v-com-i{display:flex;flex:none;align-items:center;justify-content:center;width:2.25rem;height:2.25rem;border-radius:50%;color:#fff;font-size:14px;font-weight:700}
.v-com-n{font-size:14px;font-weight:700;color:#000;line-height:1.25;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.v-com-d{display:flex;align-items:center;gap:.5rem}.v-com-d span:first-child{font-size:11px;line-height:1}.v-com-d span+span{font-size:11px;color:var(--su)}
.v-com-x{font-size:13.5px;line-height:1.375;color:#262626}

/* categorias */
.v-cats .v-h2-cat{font-size:clamp(21px,5.8vw,29px);margin-bottom:1rem}
@media(min-width:768px){.v-cats .v-h2-cat{font-size:clamp(28px,3.4vw,40px)}}
.v-cats-g{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;max-width:48rem;margin:0 auto}
@media(min-width:768px){.v-cats-g{grid-template-columns:repeat(4,minmax(0,1fr));gap:1rem;max-width:72rem}}
.v-cat{position:relative;overflow:hidden;border-radius:1rem;background:#fff;border:1px solid var(--cl);box-shadow:0 0 0 1px color-mix(in srgb,var(--cl) 55%,transparent),0 0 26px color-mix(in srgb,var(--cl) 35%,transparent)}
.v-cat video,.v-cat img{display:block;width:100%;height:auto;aspect-ratio:9/16;object-fit:cover;background:#EAF6FF}
.v-cat-r{position:absolute;left:.75rem;bottom:.75rem;z-index:2;display:inline-flex;align-items:center;gap:.25rem;border-radius:9999px;padding:.25rem .625rem;font-size:10px;font-weight:600;letter-spacing:-.025em;background:rgba(255,255,255,.9);color:var(--mu);border:1px solid var(--cl);box-shadow:0 2px 10px color-mix(in srgb,var(--cl) 45%,transparent)}
@media(min-width:768px){.v-cat-r{font-size:11px}}
.v-p-fecho{margin:2rem auto 0;color:var(--su);font-size:14px;line-height:1.625;max-width:42rem}
@media(min-width:768px){.v-p-fecho{margin-top:2.5rem;font-size:16px}}

/* como funciona */
.v-pv .v-eb{margin-bottom:1.5rem}
.v-pv-g{display:grid;grid-template-columns:1fr;gap:2rem;align-items:center;max-width:72rem;margin:0 auto}
@media(min-width:768px){.v-pv-g{grid-template-columns:1fr 1fr;gap:2.5rem}}@media(min-width:1024px){.v-pv-g{gap:3rem}}
.v-pv-esq{order:2}.v-pv-dir{order:1}@media(min-width:768px){.v-pv-esq{order:1}.v-pv-dir{order:2}}
.v-pv-t{font-weight:700;line-height:1.15;letter-spacing:-.02em;max-width:56rem;margin:0 auto 1.5rem;font-size:clamp(18px,6.6vw,26px)}
@media(min-width:640px){.v-pv-t{font-size:clamp(26px,5vw,36px)}}
@media(min-width:768px){.v-pv-t{font-size:clamp(28px,3.6vw,36px);margin-bottom:2rem}}@media(min-width:1024px){.v-pv-t{font-size:clamp(30px,3.2vw,40px)}}
.v-pv-t em.hl,.v-pv-t em.pk{color:var(--ac);font-weight:800;background:none;-webkit-text-fill-color:currentColor;filter:none}
.v-ps-g{display:grid;align-items:start;gap:.5rem}@media(min-width:768px){.v-ps-g{gap:1rem}}
.v-ps{display:flex;flex-direction:column;align-items:center;text-align:center}
.v-ps-ic{position:relative}
.v-ps-glow{position:absolute;inset:0;border-radius:1rem;filter:blur(40px);opacity:.6;background:color-mix(in srgb,var(--ac) 30%,transparent);transition:opacity .5s}
.v-ps:hover .v-ps-glow{opacity:1}
.v-ps-box{position:relative;display:flex;align-items:center;justify-content:center;width:3.5rem;height:3.5rem;border-radius:1rem;background:#fff;border:1px solid color-mix(in srgb,var(--cl) 60%,transparent);box-shadow:0 1px 2px rgba(0,0,0,.05);transition:transform .3s}
.v-ps:hover .v-ps-box{transform:translateY(-4px) scale(1.05)}
@media(min-width:768px){.v-ps-box{width:5rem;height:5rem}}
.v-ps-svg{width:1.5rem;height:1.5rem;color:var(--ac)}@media(min-width:768px){.v-ps-svg{width:2.25rem;height:2.25rem}}
.v-emo{font-size:1.5rem}@media(min-width:768px){.v-emo{font-size:2.1rem}}
.v-ps-n{position:absolute;top:-.5rem;right:-.5rem;display:flex;align-items:center;justify-content:center;width:1.5rem;height:1.5rem;border-radius:50%;background:#fff;border:1px solid var(--cl);font-size:10px;font-weight:700;color:color-mix(in srgb,var(--tx) 80%,transparent);box-shadow:0 1px 2px rgba(0,0,0,.05)}
@media(min-width:768px){.v-ps-n{width:1.75rem;height:1.75rem;font-size:12px}}
.v-ps p{margin-top:.75rem;font-weight:600;font-size:12px;line-height:1.25;max-width:110px}
@media(min-width:768px){.v-ps p{margin-top:1rem;font-size:16px;max-width:none}}
.v-ps-seta{display:flex;align-self:center;margin-top:1.25rem;color:color-mix(in srgb,var(--su) 50%,transparent)}
.v-ps-seta svg{width:1rem;height:1rem}@media(min-width:768px){.v-ps-seta{margin-top:2rem}.v-ps-seta svg{width:1.5rem;height:1.5rem}}
.v-ps-btn{margin-top:2rem;display:flex;justify-content:center}@media(min-width:768px){.v-ps-btn{margin-top:2.5rem}}
.v-pv-l{font-size:14px;color:var(--su);margin-bottom:.75rem!important}@media(min-width:768px){.v-pv-l{font-size:16px}}
.v-vv-box{width:100%;max-width:320px;margin:0 auto;border-radius:1.5rem;overflow:hidden;background:#fff;box-shadow:var(--sh-card)}
@media(min-width:640px){.v-vv-box{max-width:340px}}@media(min-width:768px){.v-vv-box{max-width:260px}}@media(min-width:1024px){.v-vv-box{max-width:300px}}
.v-vv{position:relative;aspect-ratio:9/16;overflow:hidden;background:color-mix(in srgb,var(--cl) 50%,#fff)}
.v-vv iframe,.v-vv video,.v-vv img{position:absolute;inset:0;width:100%;height:100%;border:0;object-fit:cover}
.v-vv-play{position:absolute;inset:0;border:0;padding:0;background:transparent;cursor:pointer}
.v-vv-play>span{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);display:flex;align-items:center;justify-content:center;width:4rem;height:4rem;border-radius:50%;background:var(--ac);color:#fff;box-shadow:0 10px 15px -3px rgba(0,0,0,.2)}
.v-vv-play svg{width:1.5rem;height:1.5rem}

/* bônus */
.v-h2-bn{font-size:clamp(21px,5.8vw,29px)}@media(min-width:768px){.v-h2-bn{font-size:clamp(28px,3.4vw,40px)}.v-h2-bn .ln{white-space:nowrap}}
.v-card{border-radius:1.5rem;border:1px solid color-mix(in srgb,var(--cl) 60%,transparent);background:#fff;box-shadow:var(--sh-card);transition:all .5s cubic-bezier(.4,0,.2,1)}
.v-card:hover{box-shadow:var(--sh-lift);transform:translateY(-3px)}
.v-bns-g{display:grid;grid-template-columns:1fr;gap:.75rem;align-items:stretch;max-width:64rem;margin:0 auto}
@media(min-width:768px){.v-bns-g{grid-template-columns:repeat(3,minmax(0,1fr));gap:1.5rem}}
.v-bn{display:flex;flex-direction:row;align-items:center;gap:.75rem;padding:.75rem;text-align:left;height:100%}
@media(min-width:768px){.v-bn{flex-direction:column;align-items:stretch;gap:0;padding:2rem}}
.v-bn-im-cel{width:112px;flex:none;overflow:hidden;border-radius:.75rem}@media(min-width:768px){.v-bn-im-cel{display:none}}
.v-bn-im-pc{display:none}@media(min-width:768px){.v-bn-im-pc{display:block;border-radius:1rem;overflow:hidden;margin:auto -.5rem 0}}
.v-bn img{width:100%;transition:transform 1.2s ease}.v-bn:hover img{transform:scale(1.04)}
.v-bn-tx{min-width:0;flex:1}
.v-bn .v-eb-q{font-size:10px;padding:.25rem .75rem;margin-bottom:.5rem}
@media(min-width:768px){.v-bn .v-eb-q{font-size:11px;padding:.375rem 1rem;margin-bottom:1rem}}
.v-bn h3{font-size:1rem;line-height:1.375;margin:.375rem 0 .25rem;color:var(--tx)}
@media(min-width:768px){.v-bn h3{font-size:1.5rem;margin:1rem 0 .75rem}}
.v-bn p{color:var(--su);font-size:12px;line-height:1.625}@media(min-width:768px){.v-bn p{font-size:14px;margin-bottom:1.5rem}}

/* transição */
.v-trans{background:var(--pa);color:#fff;padding:2.5rem 1.5rem;text-align:center}
@media(min-width:768px){.v-trans{padding:3.5rem 1.5rem}}
.v-trans p{font-weight:400;font-size:clamp(19px,5.2vw,26px);line-height:1.25;max-width:48rem;margin:0 auto}
@media(min-width:768px){.v-trans p{font-size:clamp(26px,3vw,34px)}}

/* oferta */
.v-of{position:relative;isolation:isolate;padding:4rem 1rem}@media(min-width:768px){.v-of{padding:5rem 1rem}}
.v-of-mundo{z-index:-1}
.v-of-c{position:relative;max-width:28rem;margin:0 auto;text-align:center}
.v-confete{position:absolute;inset:0;overflow:hidden;z-index:20;pointer-events:none;display:none}
.v-of.v-on .v-confete{display:block}
.v-confete span{position:absolute;top:-6%;width:.5rem;height:.5rem;border-radius:2px;animation:v-confete 1.8s ease-in forwards}
@keyframes v-confete{0%{transform:translateY(0) rotate(0);opacity:1}to{transform:translateY(420px) rotate(540deg);opacity:0}}
.v-pill-w{display:flex;justify-content:center;margin-bottom:1.5rem}
.v-pill{display:inline-flex;align-items:center;gap:.5rem;border-radius:9999px;background:linear-gradient(to right,#10b981,#34d399);color:#fff;font-size:14px;font-weight:600;padding:.5rem 1.25rem;box-shadow:0 8px 24px -8px rgba(16,185,129,.6)}
.v-of.v-on .v-pill{animation:v-pop .65s cubic-bezier(.34,1.56,.64,1) both,v-glow 2.4s ease-in-out .65s infinite}
@keyframes v-pop{0%{transform:scale(.9);opacity:0}55%{transform:scale(1.08);opacity:1}to{transform:scale(1);opacity:1}}
@keyframes v-glow{0%,to{box-shadow:0 8px 24px -8px #10b98199}50%{box-shadow:0 0 0 6px #10b98129,0 10px 30px -6px #10b981b3}}
.v-of-card{border-radius:1.5rem;background:#fff;overflow:hidden;box-shadow:0 25px 50px -12px rgba(0,0,0,.25)}
.v-of-top{position:relative;padding:1.25rem 1.5rem;display:flex;flex-direction:column;align-items:center;gap:.5rem;background:var(--al);color:#fff;border-bottom:1px solid rgba(255,255,255,.15)}
.v-of-tag{font-size:10px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:rgba(255,255,255,.9)}
.v-tempo{display:flex;align-items:center;justify-content:center;gap:.75rem}
.v-tempo svg{width:1.25rem;height:1.25rem}
.v-tempo span{font-variant-numeric:tabular-nums;font-size:1.5rem;font-weight:600;letter-spacing:.05em}@media(min-width:768px){.v-tempo span{font-size:1.875rem}}
.v-tempo i{font-style:normal;color:rgba(255,255,255,.5);margin:0 .25rem}
.v-of-top p{font-size:11px;font-weight:500;color:rgba(255,255,255,.85)}
.v-of-body{padding:1.5rem 1.5rem 2rem;color:#1a1a1a}
.v-of-row{display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;text-align:left}
.v-of-mock{width:46%;flex:none;border-radius:1rem}
.v-of-info{min-width:0}.v-of-logo{height:2.5rem;width:auto;object-fit:contain}@media(min-width:768px){.v-of-logo{height:3.5rem}}
.v-of-nome{font-size:1.5rem;font-weight:800;color:var(--q)}
.v-of-bn{font-size:14px;font-weight:600;color:var(--ok2);margin-top:.25rem!important}@media(min-width:768px){.v-of-bn{font-size:16px}}
.v-of-de{font-size:14px;color:#ef4444;text-decoration:line-through;margin-top:.5rem!important}
.v-of-por{font-size:12px;color:#737373;margin-top:.5rem!important}
.v-preco{display:inline-block;font-weight:700;font-size:3rem;line-height:1;margin:.25rem 0;color:var(--ok);animation:v-zoom 1.6s ease-in-out infinite;transform-origin:center}
@media(min-width:768px){.v-preco{font-size:3.75rem}}
@keyframes v-zoom{0%,to{transform:scale(1) rotate(0)}20%{transform:scale(1.12) rotate(-2deg)}40%{transform:scale(.96) rotate(2deg)}60%{transform:scale(1.1) rotate(-1deg)}80%{transform:scale(1) rotate(1deg)}}
.v-of-av{font-size:14px;color:#737373;margin-bottom:1.25rem!important}
.v-eco-w{display:flex;justify-content:center;margin-bottom:1.5rem}
.v-eco{display:inline-flex;align-items:center;border-radius:9999px;border:2px dashed var(--ok);color:var(--ok2);font-size:12px;font-weight:600;padding:.5rem 1rem}
.v-btn-c{position:relative;display:block;width:100%;border-radius:9999px;background:linear-gradient(to right,#66BB6A,#4CAF50,#43A047);color:#fff;font-weight:700;font-size:1rem;padding:1rem;text-decoration:none;animation:v-cta 1.8s ease-in-out infinite;box-shadow:0 0 30px 4px #1fe08680,0 10px 30px -8px #18b46b99}
.v-btn-c:hover{filter:brightness(1.1)}@media(min-width:768px){.v-btn-c{font-size:1.125rem}}
@keyframes v-cta{0%,to{transform:scale(1);box-shadow:0 0 #18b46b99,0 0 30px 4px #1cca798c,0 10px 30px -8px #159d5e99}50%{transform:scale(1.03);box-shadow:0 0 0 12px #18b46b00,0 0 50px 10px #1fe086cc,0 14px 40px -8px #159d5ecc}}
.v-pay{margin:1.25rem auto 0;max-width:220px;width:100%;height:auto;opacity:.9}
.v-cks{list-style:none;padding:0;margin:1.25rem 0 0;display:grid;gap:.5rem;font-size:13px;color:#404040}
.v-cks li{display:flex;align-items:center;justify-content:center;gap:.5rem;white-space:nowrap}
.v-ck{display:inline-flex;align-items:center;gap:.5rem}.v-ck svg{width:1rem;height:1rem;color:#f97316}
.v-ck-sep{margin:0 .25rem;color:#d4d4d4}
.v-alerta{margin-top:1.5rem;display:flex;align-items:center;justify-content:center;gap:.5rem;border-radius:1rem;background:#fef2f2;border:1px solid #f87171;color:#dc2626;font-size:13px;font-weight:600;padding:1rem .75rem;line-height:1.25;text-align:center}
.v-alerta svg{width:1.25rem;height:1.25rem;flex:none}

/* garantia */
.v-gar-card{padding:2.5rem;max-width:56rem;margin:0 auto;display:flex;flex-direction:column;align-items:center;gap:2.5rem}
@media(min-width:768px){.v-gar-card{padding:3.5rem;flex-direction:row}}
.v-selo{width:11rem;height:11rem;flex:none;object-fit:contain;filter:drop-shadow(0 10px 30px rgba(201,168,76,.35))}
@media(min-width:768px){.v-selo{width:14rem;height:14rem}}
.v-gar-t{text-align:center}@media(min-width:768px){.v-gar-t{text-align:left}}
.v-gar-t h2{font-weight:400;font-size:1.875rem;line-height:2.25rem;margin:1rem 0!important;color:var(--tx)}
@media(min-width:768px){.v-gar-t h2{font-size:2.25rem;line-height:2.5rem}}
.v-gar-t h2 em{color:var(--mu)}
.v-gar-t p{color:var(--su);line-height:1.625}

/* autoridade */
.v-au-g{max-width:64rem;margin:0 auto;display:flex;flex-direction:column-reverse;align-items:center;gap:3rem}
@media(min-width:768px){.v-au-g{display:grid;grid-template-columns:1fr auto}}
.v-au-tx{text-align:left}
.v-au-tx h2{font-weight:400;font-size:1.875rem;line-height:2.25rem;margin:1rem 0 .5rem!important;color:var(--tx)}
@media(min-width:768px){.v-au-tx h2{font-size:3rem;line-height:1}}
.v-au-cargo{color:var(--su);font-size:15px;margin-bottom:2rem!important}
.v-au-ps{color:var(--su);font-size:15px;line-height:1.625;display:grid;gap:1rem}
.v-au-ps .v-au-1,.v-au-ps strong{color:var(--tx)}
.v-au-foto{border-radius:50%;overflow:hidden;flex:none;margin:0 auto}
.v-au-foto img{width:14rem;height:14rem;object-fit:cover;border-radius:50%;transition:transform 1.2s ease}.v-au-foto:hover img{transform:scale(1.04)}
@media(min-width:768px){.v-au-foto img{width:18rem;height:18rem}}

/* FAQ */
.v-faq-h{margin-bottom:3rem}.v-faq .v-eb{margin-bottom:1.5rem}
.v-h2-faq{font-weight:700;font-size:1.875rem;line-height:2.25rem;margin-top:1rem!important;color:var(--tx)}
@media(min-width:768px){.v-h2-faq{font-size:3rem;line-height:1}}
.v-fqs{max-width:42rem;margin:0 auto;display:grid;gap:.75rem;text-align:left}
.v-fq{padding:0 1.5rem;border-color:color-mix(in srgb,var(--cl) 60%,transparent)}
.v-fq:hover{transform:none}
.v-fq summary{display:flex;align-items:center;justify-content:space-between;gap:0;padding:1rem 0;font-size:1.125rem;line-height:1.75rem;font-weight:500;cursor:pointer;list-style:none;color:var(--tx)}
.v-fq summary::-webkit-details-marker{display:none}.v-fq summary:hover{text-decoration:underline}
.v-fq summary svg{width:1rem;height:1rem;flex:none;transition:transform .2s}.v-fq[open] summary svg{transform:rotate(180deg)}
.v-fq p{padding-bottom:1rem;font-size:14px;color:var(--su);line-height:1.625}
.v-wa .v-btn-c{max-width:24rem;margin:0 auto}

/* rodapé */
.v-rod{padding:4rem 1.5rem;background:var(--pa);text-align:center;border-top:1px solid rgba(255,255,255,.1)}
.v-rod-c{max-width:48rem;margin:0 auto;display:grid;gap:1rem;font-size:14px;color:rgba(255,255,255,.8)}
.v-rod-logo{height:3rem;width:auto;margin:0 auto}
.v-rod-m{color:#fff;font-weight:600}.v-rod a{color:inherit;text-decoration:underline}
.v-rod-av{font-size:12px;color:rgba(255,255,255,.7);max-width:36rem;margin:0 auto}

/* botão flutuante */
.v-flut{position:fixed;bottom:1.25rem;right:1rem;z-index:60;display:flex;align-items:center;justify-content:center;width:3.5rem;height:3.5rem;border-radius:50%;border:1px solid color-mix(in srgb,var(--q) 40%,#fff);color:#fff;font:600 14px "$fonte",sans-serif;background:linear-gradient(180deg,var(--q1),var(--q) 55%,var(--q2));box-shadow:0 0 22px color-mix(in srgb,var(--q) 55%,transparent),0 10px 26px -10px color-mix(in srgb,var(--q2) 60%,transparent);cursor:pointer}
.v-flut[hidden]{display:none}.v-flut:disabled{opacity:.75;cursor:not-allowed}.v-flut.v-ok{animation:v-float 2.2s ease-in-out infinite}
.v-flut svg{width:1.5rem;height:1.5rem}
@keyframes v-float{0%,to{transform:translateY(0) scale(1)}30%{transform:translateY(6px) scale(1.04)}60%{transform:translateY(0) scale(1)}80%{transform:translateY(4px) scale(1.02)}}
.lt-pausa,.lt-pausa *,.lt-pausa *::before,.lt-pausa *::after{animation-play-state:paused!important}
"""

JS = r"""
(function(){document.querySelectorAll("[data-pilha]").forEach(function(box){
var palco=box.querySelector(".v-pilha-palco"),its=[].slice.call(box.querySelectorAll(".v-pi")),L=its.length,n=+box.dataset.n||1,dots=[].slice.call(box.querySelectorAll("[data-ir]"));if(!L)return;
var pos=0,vel=0,alvo=0,arr=false,ult=0,raf=0,vis=true,sobre=false,t,larg=0;
function w(){larg=its[0].offsetWidth+12}
function desenha(){its.forEach(function(el,k){var d=((k-pos)%L+L)%L;if(d>L/2)d-=L;var a=Math.abs(d);
el.style.transform="translate3d("+(d*larg).toFixed(2)+"px,0,"+(-240*a).toFixed(2)+"px)";el.style.zIndex=String(100-Math.round(a));el.style.visibility=a>L/2-1?"hidden":"visible"});
var i=((Math.round(pos)%n)+n)%n;dots.forEach(function(b,j){b.classList.toggle("on",j===i)})}
function passo(ts){var dt=Math.min(.032,(ts-(ult||ts))/1000||.016);ult=ts;
if(!arr){var f=-200*(pos-alvo)-30*vel;vel+=f*dt;pos+=vel*dt;if(Math.abs(pos-alvo)<.0005&&Math.abs(vel)<.001){pos=alvo;vel=0;desenha();raf=0;ult=0;return}}
desenha();raf=requestAnimationFrame(passo)}
function mexe(){if(!raf){ult=0;raf=requestAnimationFrame(passo)}}
function ir(k){alvo=Math.round(alvo)+k;mexe()}
function auto(){clearInterval(t);t=setInterval(function(){if(vis&&!sobre&&!arr&&!document.hidden)ir(1)},2000)}
box.querySelector("[data-ant]").onclick=function(){ir(-1);auto()};box.querySelector("[data-prox]").onclick=function(){ir(1);auto()};
dots.forEach(function(b){b.onclick=function(){var atual=((Math.round(alvo)%n)+n)%n,j=+b.dataset.ir,dlt=j-atual;if(dlt>n/2)dlt-=n;if(dlt<-n/2)dlt+=n;ir(dlt);auto()}});
palco.addEventListener("mouseenter",function(){sobre=true});palco.addEventListener("mouseleave",function(){sobre=false});
var x0=0,p0=0,hs=[];palco.addEventListener("pointerdown",function(e){arr=true;x0=e.clientX;p0=pos;hs=[[e.clientX,performance.now()]];vel=0;try{palco.setPointerCapture(e.pointerId)}catch(_){}mexe()});
palco.addEventListener("pointermove",function(e){if(!arr)return;pos=p0-(e.clientX-x0)/larg;hs.push([e.clientX,performance.now()]);if(hs.length>5)hs.shift()});
function solta(e){if(!arr)return;arr=false;var v=0;if(hs.length>1){var q=hs[0],z=hs[hs.length-1];v=(z[0]-q[0])/Math.max(1,z[1]-q[1])*1000}alvo=Math.round(pos-v/larg*.25);auto();mexe()}
palco.addEventListener("pointerup",solta);palco.addEventListener("pointercancel",solta);
if("IntersectionObserver"in window)new IntersectionObserver(function(es){vis=es[0].isIntersecting}).observe(box);
addEventListener("resize",function(){w();desenha()},{passive:true});w();desenha();auto()})})();
(function(){document.querySelectorAll("[data-vit2]").forEach(function(box){
var its=[].slice.call(box.querySelectorAll(".lt-vit-i")),n=its.length;if(!n)return;
var dots=[].slice.call(box.querySelectorAll(".lt-vit-dots i")),pos=0,vel=0,alvo=0,arrastando=false,ultimo=0,raf=0,vis=true,t;
function cfg(){var w=innerWidth;return w<640?{x:90,y:20,r:8,s:.06,div:120,sens:180}:w<1024?{x:130,y:30,r:10,s:.09,div:160,sens:220}:{x:170,y:40,r:12,s:.12,div:200,sens:250}}
var c=cfg();
function op(d){var h=n/2,a=Math.abs(d);return a>=h?0:a>h-.5?(h-a)/.5:1}
function desenha(){its.forEach(function(el,i){var d=((i-pos)%n+n)%n;if(d>n/2)d-=n;var a=Math.abs(d);
el.style.transform="translateX("+(d*c.x).toFixed(2)+"px) translateY("+(a<.05?0:a*c.y).toFixed(2)+"px) rotate("+(a<.05?0:d*c.r).toFixed(2)+"deg) scale("+(1-a*c.s).toFixed(4)+")";
el.style.opacity=op(d);el.style.zIndex=Math.round(100-a*10)});
var k=((Math.round(pos)%n)+n)%n;dots.forEach(function(x,i){x.classList.toggle("on",i===k)})}
function sobra(){var m=0;its.forEach(function(el,i){var d=((i-pos)%n+n)%n;if(d>n/2)d-=n;if(op(d)>0)m=Math.max(m,Math.abs(d)*c.y+el.offsetWidth*Math.sin(Math.abs(d*c.r)*Math.PI/180)*.5)});box.style.setProperty("--vit-sobra",Math.ceil(m)+"px");box.parentNode&&box.parentNode.style.setProperty("--vit-sobra",Math.ceil(m)+"px")}
function passo(ts){var dt=Math.min(.032,(ts-(ultimo||ts))/1000||.016);ultimo=ts;
if(!arrastando){var f=-200*(pos-alvo)-30*vel;vel+=f*dt;pos+=vel*dt;if(Math.abs(pos-alvo)<.0005&&Math.abs(vel)<.001){pos=alvo;vel=0;desenha();raf=0;ultimo=0;return}}
desenha();raf=requestAnimationFrame(passo)}
function mexe(){if(!raf){ultimo=0;raf=requestAnimationFrame(passo)}}
function ir(k){alvo=Math.round(alvo)+k;mexe()}
function auto(){clearInterval(t);t=setInterval(function(){if(vis&&!arrastando&&!document.hidden)ir(1)},+box.dataset.intervalo||1000)}
var a=box.querySelector("[data-vit-ant]"),p=box.querySelector("[data-vit-prox]");if(a)a.onclick=function(){ir(-1);auto()};if(p)p.onclick=function(){ir(1);auto()};
var x0=0,p0=0,xs=[];box.addEventListener("pointerdown",function(e){if(e.target.closest("button"))return;arrastando=true;x0=e.clientX;p0=pos;xs=[[e.clientX,performance.now()]];vel=0;try{box.setPointerCapture(e.pointerId)}catch(_){}mexe()});
box.addEventListener("pointermove",function(e){if(!arrastando)return;pos=p0-(e.clientX-x0)/c.sens;xs.push([e.clientX,performance.now()]);if(xs.length>5)xs.shift()});
function solta(e){if(!arrastando)return;arrastando=false;var v=0;if(xs.length>1){var q=xs[0],w=xs[xs.length-1];v=(w[0]-q[0])/Math.max(1,(w[1]-q[1]))*1000}
var off=-(e.clientX-x0)/c.div-v/(c.div*4),k=Math.max(-3,Math.min(3,Math.round(off)));alvo=Math.round(p0)+k;auto();mexe()}
box.addEventListener("pointerup",solta);box.addEventListener("pointercancel",solta);
if("IntersectionObserver"in window)new IntersectionObserver(function(es){vis=es[0].isIntersecting}).observe(box);
addEventListener("resize",function(){c=cfg();desenha();sobra()},{passive:true});desenha();sobra();auto()})})();
(function(){if(!("IntersectionObserver"in window))return;var io=new IntersectionObserver(function(es){es.forEach(function(e){e.target.classList.toggle("lt-pausa",!e.isIntersecting)})},{rootMargin:"150px 0px"});document.querySelectorAll(".v-topo,.v-sec,.v-of,.v-trans").forEach(function(el){io.observe(el)})})();
(function(){if(!("IntersectionObserver"in window))return;var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var v=e.target;if(v.dataset.poster){v.poster=v.dataset.poster;v.removeAttribute("data-poster")}io.unobserve(v)}})},{rootMargin:"600px 0px"});document.querySelectorAll("video[data-poster]").forEach(function(v){io.observe(v)})})();
(function(){var b=document.querySelector(".v-btn-topo");if(!b)return;var s=+b.dataset.espera||0,tx=b.querySelector(".v-btn-tx"),barra=b.querySelector(".v-barra"),n=0;
function ok(){b.disabled=false;tx.textContent=tx.dataset.tx;barra.style.display="none";b.classList.add("v-pulse")}
if(!s)ok();else{var t=setInterval(function(){n++;barra.style.width=(n/s*100)+"%";tx.textContent=(s-n)+"s";if(n>=s){clearInterval(t);ok()}},1000)}
b.addEventListener("click",function(){var a=document.getElementById(b.dataset.alvo);if(a)a.scrollIntoView({behavior:"smooth",block:"start"})})})();
(function(){var o=document.getElementById("oferta");if(!o||!("IntersectionObserver"in window))return;var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){io.disconnect();o.classList.add("v-on");setTimeout(function(){var c=o.querySelector(".v-confete");if(c)c.style.display="none"},3600)}},{threshold:.25});io.observe(o)})();
(function(){var b=document.querySelector("[data-v-flut]");if(!b||!("IntersectionObserver"in window))return;var ids=b.dataset.flut.split(","),esp=+b.dataset.espera||0,ativo=null,vistos={},cont={};
var seta='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>';
function pintar(){if(!ativo){b.hidden=true;return}b.hidden=false;var r=cont[ativo];if(r>0){b.disabled=true;b.classList.remove("v-ok");b.textContent=r+"s"}else{b.disabled=false;b.classList.add("v-ok");b.innerHTML=seta}}
ids.forEach(function(id){var s=document.getElementById("b-"+id);if(!s)return;cont[id]=esp;new IntersectionObserver(function(es){var e=es[0];if(e.isIntersecting){ativo=id;if(!vistos[id]){vistos[id]=1;var t=setInterval(function(){cont[id]--;if(cont[id]<=0)clearInterval(t);pintar()},1000)}}else if(ativo===id)ativo=null;pintar()},{threshold:[0,.05,.15]}).observe(s)});
b.addEventListener("click",function(){var bl=[].slice.call(document.querySelectorAll('[id^="b-"]')),i=bl.indexOf(document.getElementById("b-"+ativo)),nx=bl[i+1];if(nx)nx.scrollIntoView({behavior:"smooth",block:"start"})})})();
"""
