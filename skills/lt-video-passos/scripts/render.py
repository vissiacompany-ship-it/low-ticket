#!/usr/bin/env python3
"""Vídeo dos 3 passos (motion estilo 50 Viral Fit) a partir de um video.json.

Uso:
  python3 render.py caminho/video.json --previa        gera previa.html (abre no Chrome, tem play/pausa e barra)
  python3 render.py caminho/video.json --quadros 1.6,8,19,30   tira prints desses segundos para conferir (quadros.jpg)
  python3 render.py caminho/video.json                 renderiza: passos.mp4 (web, 1280x720), passos-1080p.mp4 e passos-poster.webp

Os caminhos de imagem no video.json são relativos ao próprio video.json.
Precisa: playwright (python), Google Chrome, ffmpeg.
"""
import asyncio, json, os, shutil, subprocess, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FPS = 30

PLAYER = '''
<div id="ctl" style="position:fixed;left:0;right:0;bottom:0;background:#111;padding:10px 16px;display:flex;gap:12px;align-items:center;font:14px system-ui;color:#fff;z-index:99">
<button id="pp" style="font:700 14px system-ui;padding:6px 14px;border-radius:8px;border:0;cursor:pointer">Pausar</button>
<input id="sk" type="range" min="0" step="0.01" value="0" style="flex:1"><span id="tt" style="width:90px;text-align:right">0.0s</span></div>
<style>html,body{width:100%!important;height:100%!important;background:#000!important;overflow:hidden}#stage{position:absolute!important;left:50%;top:calc(50% - 26px);transform-origin:center}</style>
<script>(function(){const st=document.getElementById('stage');function fit(){const s=Math.min(innerWidth/1280,(innerHeight-60)/720);st.style.transform='translate(-50%,-50%) scale('+s+')'}fit();addEventListener('resize',fit);
let t=0,play=true,last=null;const sk=document.getElementById('sk'),tt=document.getElementById('tt'),pp=document.getElementById('pp');sk.max=DUR;
pp.onclick=()=>{play=!play;pp.textContent=play?'Pausar':'Play';last=null};sk.oninput=()=>{t=+sk.value;render(t);tt.textContent=t.toFixed(1)+'s'};
function loop(ts){if(play){if(last!=null)t+=(ts-last)/1000;if(t>DUR)t=0;render(t);sk.value=t;tt.textContent=t.toFixed(1)+'s'}last=ts;requestAnimationFrame(loop)}
document.fonts.ready.then(()=>requestAnimationFrame(loop));})();</script>'''


def resolver(v, base):
    if isinstance(v, dict):
        return {k: resolver(x, base) for k, x in v.items()}
    if isinstance(v, list):
        return [resolver(x, base) for x in v]
    if isinstance(v, str) and v.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")) and not v.startswith(("http", "file:")):
        p = os.path.abspath(os.path.join(base, v))
        if not os.path.exists(p):
            print("AVISO: imagem não encontrada:", v)
        return "file://" + p
    return v


def montar(cfg_path, previa=False):
    base = os.path.dirname(os.path.abspath(cfg_path))
    cfg = resolver(json.load(open(cfg_path, encoding="utf-8")), base)
    h = open(os.path.join(AQUI, "template.html"), encoding="utf-8").read()
    h = h.replace("/*CFG*/{}", json.dumps(cfg, ensure_ascii=False))
    if previa:
        h = h.replace("</body></html>", PLAYER + "</body></html>")
    return h, base


async def abrir(p, html_path, escala=1):
    b = await p.chromium.launch(executable_path=CHROME, args=["--allow-file-access-from-files"])
    pg = await b.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=escala)
    erros = []
    pg.on("pageerror", lambda e: erros.append(str(e)))
    await pg.goto("file://" + html_path)
    await pg.evaluate("document.fonts.ready")
    await pg.wait_for_timeout(1200)
    if erros:
        print("ERROS NA PÁGINA:", erros)
    return b, pg


async def quadros(html_path, base, ts):
    from playwright.async_api import async_playwright
    tmp = tempfile.mkdtemp()
    async with async_playwright() as p:
        b, pg = await abrir(p, html_path)
        print("duração:", await pg.evaluate("DUR"), "s")
        for i, t in enumerate(ts):
            await pg.evaluate("render(%s)" % t)
            await pg.screenshot(path=os.path.join(tmp, "%02d.jpg" % i), type="jpeg", quality=80)
        await b.close()
    lado = 4 if len(ts) > 4 else len(ts)
    linhas = (len(ts) + lado - 1) // lado
    out = os.path.join(base, "quadros.jpg")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-pattern_type", "glob", "-i", os.path.join(tmp, "*.jpg"),
                    "-vf", "scale=640:360,tile=%dx%d" % (lado, linhas), "-frames:v", "1", out], check=True)
    shutil.rmtree(tmp)
    print("folha de quadros:", out)


async def renderizar(html_path, base, nome):
    from playwright.async_api import async_playwright
    tmp = tempfile.mkdtemp()
    async with async_playwright() as p:
        b, pg = await abrir(p, html_path, 1.5)
        dur = await pg.evaluate("DUR")
        n = int(dur * FPS)
        print("renderizando %d quadros (%.1fs). Leva uns 10 a 12 min para 33s de vídeo..." % (n, dur), flush=True)
        for i in range(n):
            await pg.evaluate("render(%f)" % (i / FPS))
            await pg.screenshot(path=os.path.join(tmp, "%05d.png" % i))
            if i % 150 == 0:
                print("  %d/%d" % (i, n), flush=True)
        await b.close()
    web = os.path.join(base, nome + ".mp4")
    alta = os.path.join(base, nome + "-1080p.mp4")
    poster = os.path.join(base, nome + "-poster.webp")
    src = os.path.join(tmp, "%05d.png")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", src, "-vf", "scale=1280:720:flags=lanczos,format=yuv420p",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "25", "-profile:v", "high", "-movflags", "+faststart", "-an", web], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", src, "-vf", "format=yuv420p",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-movflags", "+faststart", "-an", alta], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(tmp, "%05d.png" % int(1.6 * FPS)), "-vf", "scale=1280:720",
                    "-c:v", "libwebp", "-quality", "80", poster], check=True)
    shutil.rmtree(tmp)
    for f in (web, alta, poster):
        print("%s (%.1f MB)" % (f, os.path.getsize(f) / 1e6))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cfg = sys.argv[1]
    if "--previa" in sys.argv:
        h, base = montar(cfg, previa=True)
        out = os.path.join(base, "previa.html")
        open(out, "w", encoding="utf-8").write(h)
        print("prévia:", out)
        return
    h, base = montar(cfg)
    tmp_html = os.path.join(base, ".render.html")
    open(tmp_html, "w", encoding="utf-8").write(h)
    try:
        if "--quadros" in sys.argv:
            ts = [float(x) for x in sys.argv[sys.argv.index("--quadros") + 1].split(",")]
            asyncio.run(quadros(tmp_html, base, ts))
        else:
            nome = "passos"
            if "--nome" in sys.argv:
                nome = sys.argv[sys.argv.index("--nome") + 1]
            asyncio.run(renderizar(tmp_html, base, nome))
    finally:
        os.remove(tmp_html)


if __name__ == "__main__":
    main()
