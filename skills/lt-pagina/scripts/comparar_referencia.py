"""Compara, seção por seção, a página de referência e a nossa (lado a lado), no computador e no celular.

Uso: python3 comparar_referencia.py <url da referência> <url ou pasta da nossa> [--saida pasta] [--larguras 1440,390]
Saída: s00-1440.jpg, s01-1440.jpg... (referência à esquerda, nossa à direita) e a altura de cada seção das duas.
Regra: só mostrar ao Paulo depois de olhar todas as imagens e corrigir o que estiver diferente (playbook, seção 6C).
"""
import argparse, os, pathlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def capturar(b, url, W, destino):
    mob = W < 600
    c = b.new_context(viewport={"width": W, "height": 900}, is_mobile=mob, has_touch=mob)
    pg = c.new_page()
    pg.goto(url, wait_until="networkidle", timeout=90000)
    for _ in range(100):
        pg.evaluate("scrollBy(0,500)"); pg.wait_for_timeout(200)
        if pg.evaluate("scrollY+innerHeight>=document.documentElement.scrollHeight-5"):
            break
    pg.wait_for_timeout(6500)
    pg.add_style_tag(content="*,*::before,*::after{content-visibility:visible!important}")
    pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(800)
    caixas = pg.evaluate("""[...document.querySelectorAll('section,footer')].filter(e=>!e.parentElement.closest('section')).map(e=>{const r=e.getBoundingClientRect();return [r.top+scrollY,r.height]})""")
    pg.screenshot(path=destino, full_page=True)
    c.close()
    return caixas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("referencia"); ap.add_argument("nossa")
    ap.add_argument("--saida", default="comparacao"); ap.add_argument("--larguras", default="1440,390")
    a = ap.parse_args()
    out = pathlib.Path(a.saida); out.mkdir(parents=True, exist_ok=True)
    nossa = a.nossa
    if not nossa.startswith("http"):
        import medir_velocidade
        nossa = medir_velocidade.servir(pathlib.Path(nossa))
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        for W in [int(x) for x in a.larguras.split(",")]:
            rb = capturar(b, a.referencia, W, str(out / ("ref-%d.png" % W)))
            nb = capturar(b, nossa, W, str(out / ("nossa-%d.png" % W)))
            R = Image.open(out / ("ref-%d.png" % W)); N = Image.open(out / ("nossa-%d.png" % W))
            print("%d px: %d seções na referência, %d na nossa" % (W, len(rb), len(nb)))
            for i, (r, n) in enumerate(zip(rb, nb)):
                x = R.crop((0, int(r[0]), W, int(r[0] + min(r[1], 2600)))); y = N.crop((0, int(n[0]), W, int(n[0] + min(n[1], 2600))))
                s = Image.new("RGB", (W * 2 + 20, max(x.height, y.height)), "red"); s.paste(x, (0, 0)); s.paste(y, (W + 20, 0))
                s.save(out / ("s%02d-%d.jpg" % (i, W)), quality=72)
                aviso = "  <- diferente" if abs(r[1] - n[1]) > max(40, r[1] * .06) else ""
                print("  seção %02d: referência %4d px | nossa %4d px%s" % (i, r[1], n[1], aviso))
        b.close()


if __name__ == "__main__":
    main()
