"""Gera o PDF de gravação (tamanho de celular) e o .md dos roteiros a partir de um roteiro.json.

Uso: python3 gerar_pdf.py <roteiro.json> <pasta-de-saida> [--conferencia <pasta>]
Saída: <pasta>/roteiro-gravacao-<slug>.pdf e <pasta>/videos-por-takes.md
Com --conferencia, salva um PNG por página para conferir antes de entregar.
Formato do JSON: ver ../modelos/roteiro.exemplo.json
"""
import html, json, os, subprocess, sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

ETAPAS = {
    "quebra": ("1. Quebra de padrão", "#6B4FBB", "1 a 2 s"),
    "gancho": ("2. Gancho", "#E0A800", "3 s"),
    "dor": ("3. Problema / Dor", "#E52521", ""),
    "solucao": ("4. Solução / Promessa", "#3FA31A", ""),
    "prova": ("5. Prova", "#F26B10", ""),
    "cta": ("6. CTA reforçada", "#0A8FE8", ""),
}
E = html.escape


def etq(et):
    nome, cor, tempo = ETAPAS[et]
    t = f' <span class="tempo">{tempo}</span>' if tempo else ""
    return f'<span class="etq" style="background:{cor}">{nome}{t}</span>'


def montar_html(r):
    p = []
    p.append(f"""
<section class="pg capa">
  <p class="marca">{E(r['marca'])}</p>
  <h1>Roteiro de gravação</h1>
  <p class="sub">{len(r['videos'])} vídeos de anúncio, gravados frase por frase.</p>
  <div class="barra">{''.join(f'<i style="background:{c}"></i>' for _, c, _ in ETAPAS.values())}</div>
  <p class="para">Para: {E(r['para'])}<br>Data: {E(r['data'])}</p>
</section>

<section class="pg">
  <h2>Como vai ser a gravação</h2>
  <p>A gente não grava o vídeo inteiro de uma vez. Cada frase é um <b>take</b>: você fala uma frase, a gente para e grava a próxima.</p>
  <div class="box"><b>Você não precisa decorar o vídeo.</b> Só a próxima frase. Lê, olha para a câmera e fala.</div>
  <p>Na edição a gente junta as frases, tira os silêncios, coloca legenda e as imagens da tela do produto.</p>
  <h3>Os 2 segredos</h3>
  <div class="seg"><span>1</span><p><b>Colocar vida.</b> Expressão no rosto, gesto e tom de voz que muda. Cada frase diz <i>como falar</i>.</p></div>
  <div class="seg"><span>2</span><p><b>Saber exatamente o que vai falar.</b> Frase por frase, sem pensar com a câmera ligada.</p></div>
</section>

<section class="pg">
  <h2>As 6 etapas de todo anúncio</h2>
  <p>Todo vídeo segue esta ordem. Cada frase do roteiro vem com a cor da etapa.</p>
  <div class="et" style="--c:#6B4FBB"><b>1. Quebra de padrão · 1 a 2 s</b><p>O que a pessoa <b>vê</b> logo no começo e faz ela parar de rolar: um gesto, um objeto, um texto na tela. Acontece <b>junto</b> com a primeira frase.</p></div>
  <div class="et" style="--c:#E0A800"><b>2. Gancho · 3 s</b><p>A primeira frase. Você já começa falando, sem "oi". Curta e direta.</p></div>
  <div class="et" style="--c:#E52521"><b>3. Problema / Dor</b><p>A pessoa pensa: "é exatamente isso que acontece comigo".</p></div>
  <div class="et" style="--c:#3FA31A"><b>4. Solução / Promessa</b><p>O que é o produto e como é simples usar.</p></div>
  <div class="et" style="--c:#F26B10"><b>5. Prova</b><p>Mostrar funcionando: "olha aqui", com a tela do produto.</p></div>
  <div class="et" style="--c:#0A8FE8"><b>6. CTA reforçada</b><p>O pedido para clicar, dito duas vezes, com um motivo para fazer hoje.</p></div>
  <div class="box">Tempo de cada vídeo: <b>mínimo 35 segundos, máximo 1 minuto.</b></div>
</section>

<section class="pg">
  <h2>Antes de apertar o REC</h2>
  <ul class="chk">
    <li><b>Microfone de lapela</b> na roupa. Barulho de carro e vento estragam o vídeo.</li>
    <li><b>Luz:</b> na sombra, com o céu claro na sua frente. Nunca sol no rosto nem atrás de você.</li>
    <li><b>Celular em pé</b> (vertical), na altura dos olhos, do peito para cima.</li>
    <li><b>Andando:</b> quem filma anda de costas na sua frente, devagar.</li>
    <li><b>Fundo:</b> loja e gente passando pode, sem focar rosto de ninguém nem nome de loja.</li>
  </ul>
  <h2>Como gravar cada take</h2>
  <ol class="passos">
    <li>Mostre com os dedos o <b>número do take</b> para a câmera.</li>
    <li>Fique <b>1 segundo parada</b>, olhando a câmera.</li>
    <li>Fale a frase. No take 1, já comece fazendo o gesto da quebra de padrão.</li>
    <li>Segure <b>1 segundo</b> depois de terminar.</li>
    <li>Grave <b>de novo</b>, agora com mais energia.</li>
  </ol>
  <div class="box">Errou? Não para. Respira e repete a frase inteira. Se uma palavra travar, troque por outra que diga a mesma coisa.</div>
  <div class="box">Troque de lugar a cada 2 ou 3 takes. O vídeo fica mais dinâmico.</div>
</section>
""")
    for v in r["videos"]:
        p.append(f"""
<section class="pg">
  <p class="cod">{E(v['cod'])} · {E(v['angulo'])}</p>
  <h2>{E(v['titulo'])}</h2>
  <p class="meta">Duração: {E(v['dur'])}</p>
  <div class="box">{E(v['ideia'])}</div>
""")
        for i, t in enumerate(v["takes"], 1):
            cor = ETAPAS[t["etapa"]][1]
            extra = ""
            if t.get("quebra"):
                extra += f'<div class="qb"><div class="th">{etq("quebra")}</div><p class="d">{E(t["quebra"])}</p></div>'
            p.append(f"""  <div class="take" style="--c:{cor}">
    {extra}<div class="th"><span class="n">{i}</span>{etq(t['etapa'])}</div>
    <p class="fala">{E(t['fala'])}</p>
    <p class="d"><b>O que fazer:</b> {E(t['fazer'])}</p>
    <p class="d"><b>Como falar:</b> {E(t['como'])}</p>
    {f'<p class="d ed"><b>Na edição:</b> {E(t["edicao"])}</p>' if t.get('edicao') else ''}
  </div>
""")
        p.append('  <div class="extras"><b>Ganchos extras</b><p>Grave só o take 1 de novo com estas frases. Cada uma vira um anúncio diferente.</p><ul>' +
                 "".join(f"<li>{E(x)}</li>" for x in v["extras"]) + "</ul></div>\n</section>\n")
    p.append(f"""
<section class="pg">
  <h2>Imagens para pegar na gravação</h2>
  <p>Sem fala, de 5 a 10 segundos cada. Entram por cima da sua voz na edição.</p>
  <ul class="chk">{''.join(f'<li>{E(x)}</li>' for x in r['broll'])}</ul>
  <h2>Depois, em casa</h2>
  <ul class="chk">{''.join(f'<li>{E(x)}</li>' for x in r['depois'])}</ul>
  <div class="box fim">Pronto. Uma frase de cada vez, com vida no rosto e na voz. 💛</div>
</section>
""")
    return "".join(p)


CSS = """
@page{size:120mm 213mm;margin:9mm 8mm}
*{box-sizing:border-box}
body{font-family:-apple-system,"Helvetica Neue",Arial,sans-serif;color:#1B2238;font-size:10.5pt;line-height:1.45;margin:0}
.pg{break-after:page}.pg:last-child{break-after:auto}
h1{font-size:28pt;line-height:1.05;color:#03163F;margin:0 0 10px}
h2{font-size:17pt;line-height:1.15;color:#03163F;margin:0 0 8px;break-after:avoid}
h3{font-size:12.5pt;color:#03163F;margin:14px 0 6px}
p{margin:0 0 8px}
.capa{display:flex;flex-direction:column;justify-content:center;min-height:190mm}
.marca{font-weight:700;color:#0042FF;letter-spacing:.04em;text-transform:uppercase;font-size:9pt}
.sub{font-size:13pt;color:#55607A}
.barra{display:flex;gap:3px;margin:18px 0}.barra i{flex:1;height:10px;border-radius:3px}
.para{color:#55607A;font-size:10pt;margin-top:20px}
.box{background:#F7F3EF;border-radius:10px;padding:9px 11px;margin:10px 0;break-inside:avoid}
.fim{font-weight:700;text-align:center;font-size:12pt}
.seg{display:flex;gap:10px;align-items:flex-start;margin:8px 0;break-inside:avoid}
.seg span{flex:none;width:26px;height:26px;border-radius:50%;background:#0042FF;color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center}
.et{border-left:6px solid var(--c);padding:4px 0 4px 10px;margin:7px 0;break-inside:avoid}
.et b{color:var(--c)}.et p{margin:2px 0 0}
.chk,.passos{padding-left:18px;margin:6px 0 12px}.chk li,.passos li{margin:0 0 6px}
.cod{font-weight:800;color:#0042FF;font-size:9.5pt;margin:0 0 2px;text-transform:uppercase;letter-spacing:.04em}
.meta{color:#55607A;font-size:9.5pt}
.take{border:1.5px solid #E6E0D8;border-left:6px solid var(--c);border-radius:10px;padding:8px 10px;margin:8px 0;break-inside:avoid}
.qb{background:#F1EDFA;border-radius:8px;padding:6px 8px;margin-bottom:7px}.qb .d{margin:4px 0 0}
.th{display:flex;align-items:center;gap:7px;margin-bottom:5px}
.n{width:24px;height:24px;border-radius:50%;background:#03163F;color:#fff;font-weight:800;font-size:10pt;display:flex;align-items:center;justify-content:center;flex:none}
.etq{color:#fff;font-weight:700;font-size:8pt;border-radius:999px;padding:2px 8px}.tempo{opacity:.85;font-weight:600}
.fala{font-size:13pt;font-weight:800;line-height:1.25;color:#03163F;margin:0 0 6px}
.d{font-size:9.5pt;margin:0 0 2px;color:#33405C}.ed{color:#8A5A00}
.extras{background:#FFF7DB;border-radius:10px;padding:9px 11px;margin-top:12px;break-inside:avoid}
.extras p{font-size:9.5pt;margin:3px 0 4px}.extras ul{margin:0;padding-left:18px}.extras li{font-weight:700;margin-bottom:4px}
"""


def montar_md(r, pdf_nome):
    md = [f"# Vídeos por takes: {r['produto']}\n",
          "Estrutura (Kamilla): 1. Quebra de padrão (1 a 2 s, visual, junto com o gancho) · 2. Gancho (3 s) · 3. Problema/Dor · 4. Solução/Promessa · 5. Prova · 6. CTA reforçada. Tempo: 35 s a 1 min.\n",
          f"Fonte: `roteiro.json` (editar lá e rodar `.claude/skills/low-ticket/skills/lt-criativos-video/scripts/gerar_pdf.py`). PDF de gravação: `{pdf_nome}`.\n",
          f"Congruência: {r['congruencia']}\n"]
    for v in r["videos"]:
        palavras = sum(len(t["fala"].split()) for t in v["takes"])
        md.append(f"\n## {v['cod']} · {v['titulo']} ({v['angulo']}, {v['dur']}, {palavras} palavras)\n\n{v['ideia']}\n\n| # | Etapa | Fala | O que fazer | Como falar | Na edição |\n|---|---|---|---|---|---|")
        for i, t in enumerate(v["takes"], 1):
            nome = ETAPAS[t["etapa"]][0] + (" + Quebra: " + t["quebra"] if t.get("quebra") else "")
            md.append(f"| {i} | {nome} | {t['fala']} | {t['fazer']} | {t['como']} | {t.get('edicao', '')} |")
        md.append("\n**Ganchos extras (regravar o take 1):**\n" + "\n".join(f"- {x}" for x in v["extras"]))
    md.append(f"\n## Legenda do anúncio (trocar a 1ª linha pelo gancho)\n\n{r['legenda']}\n\n**Título:** {r['titulo_anuncio']}\n")
    return "\n".join(md)


def main():
    rj, saida = sys.argv[1], sys.argv[2]
    conf = sys.argv[sys.argv.index("--conferencia") + 1] if "--conferencia" in sys.argv else None
    r = json.load(open(rj))
    pdf = os.path.join(saida, f"roteiro-gravacao-{r['slug']}.pdf")
    tmp_html = os.path.join(conf or saida, "_roteiro-gravacao.html")
    open(tmp_html, "w").write(f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8"><title>Roteiro de gravação · {E(r["produto"])}</title><style>{CSS}</style></head><body>{montar_html(r)}</body></html>')
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", "file://" + tmp_html], check=True, capture_output=True)
    if not conf:
        os.remove(tmp_html)
    open(os.path.join(saida, "videos-por-takes.md"), "w").write(montar_md(r, os.path.basename(pdf)))
    for v in r["videos"]:
        n = sum(len(t["fala"].split()) for t in v["takes"])
        print(f"{v['cod']}: {n} palavras, cerca de {round(n / 2.5)} s")
    if conf:
        import fitz
        d = fitz.open(pdf)
        for i in range(d.page_count):
            d[i].get_pixmap(dpi=100).save(os.path.join(conf, f"p{i + 1:02d}.png"))
        print("páginas:", d.page_count)
    print(pdf)


if __name__ == "__main__":
    main()
