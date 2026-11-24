"""Mede a velocidade de uma página no celular e no computador e diz se passou na meta (nota >= 95).

Uso:
  python3 medir_velocidade.py https://site.com/pagina/        (página no ar)
  python3 medir_velocidade.py caminho/para/pagina/            (pasta local com index.html)
  opções: --rodadas 3   --meta 95

Com PAGESPEED_API_KEY no ambiente ou no .env da Vissia, usa o PageSpeed Insights oficial do Google
(a medida que vale). Sem chave, usa o Lighthouse local (mesmo motor, mas num Mac lento a nota de celular
sai mais baixa e oscila: serve para comparar antes e depois, não como nota final).
"""
import argparse, json, os, pathlib, shutil, socket, statistics, subprocess, sys, tempfile, threading, urllib.parse, urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial

VISSIA_ENV = pathlib.Path(__file__).resolve().parents[6] / ".env"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
METRICAS = [("first-contentful-paint", "FCP"), ("largest-contentful-paint", "LCP"),
            ("total-blocking-time", "TBT"), ("cumulative-layout-shift", "CLS"), ("speed-index", "SI")]


def chave():
    if os.environ.get("PAGESPEED_API_KEY"):
        return os.environ["PAGESPEED_API_KEY"]
    if VISSIA_ENV.exists():
        for linha in VISSIA_ENV.read_text().splitlines():
            if linha.startswith("PAGESPEED_API_KEY="):
                return linha.split("=", 1)[1].strip().strip('"')
    return None


def psi(url, estrategia, k):
    q = urllib.parse.urlencode({"url": url, "strategy": estrategia, "category": "performance", "key": k})
    with urllib.request.urlopen("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?" + q, timeout=180) as r:
        return json.load(r)["lighthouseResult"]


def lighthouse(url, estrategia):
    saida = tempfile.mktemp(suffix=".json")
    cmd = ["npx", "-y", "lighthouse@12.2.1", url, "--only-categories=performance", "--output=json",
           f"--output-path={saida}", "--quiet", "--chrome-flags=--headless=new"]
    if estrategia == "desktop":
        cmd.insert(4, "--preset=desktop")
    env = dict(os.environ, CHROME_PATH=CHROME)
    subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    return json.load(open(saida))


def servir(pasta):
    s = socket.socket(); s.bind(("127.0.0.1", 0)); porta = s.getsockname()[1]; s.close()
    import gzip, io, mimetypes

    class Quieto(SimpleHTTPRequestHandler):
        """Serve a pasta comprimindo HTML/CSS/JS como a Vercel faz (senão o teste local fica mais lento que o real)."""
        def log_message(self, *a):
            pass

        def send_head(self):
            caminho = self.translate_path(self.path.split("?")[0])
            if os.path.isdir(caminho):
                caminho = os.path.join(caminho, "index.html")
            tipo = mimetypes.guess_type(caminho)[0] or ""
            if os.path.isfile(caminho) and (tipo.startswith("text/") or tipo in ("application/javascript", "application/json", "image/svg+xml")) and "gzip" in self.headers.get("Accept-Encoding", ""):
                dados = gzip.compress(open(caminho, "rb").read())
                self.send_response(200)
                self.send_header("Content-Type", tipo + ("; charset=utf-8" if tipo.startswith("text/") else ""))
                self.send_header("Content-Encoding", "gzip")
                self.send_header("Content-Length", str(len(dados)))
                self.end_headers()
                return io.BytesIO(dados)
            return super().send_head()

    class Servidor(ThreadingHTTPServer):
        def handle_error(self, *a):
            pass
    srv = Servidor(("127.0.0.1", porta), partial(Quieto, directory=str(pasta)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{porta}/"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("alvo"); ap.add_argument("--rodadas", type=int, default=3); ap.add_argument("--meta", type=int, default=95)
    a = ap.parse_args()
    url = a.alvo
    if not url.startswith("http"):
        pasta = pathlib.Path(url)
        pasta = pasta.parent if pasta.is_file() else pasta
        url = servir(pasta)
        print("Servindo a pasta local em", url, "(sem CDN: no ar, com Vercel, tende a ser mais rápido)")
    k = chave()
    if not k and not shutil.which("npx"):
        sys.exit("Sem PAGESPEED_API_KEY e sem npx: não dá para medir.")
    if k and url.startswith("http://127.0.0.1"):
        print("Página local: o PageSpeed oficial não alcança. Usando Lighthouse local.")
        k = None
    print("Ferramenta:", "PageSpeed Insights (Google)" if k else "Lighthouse local", "·", a.rodadas, "rodadas, vale a mediana\n")
    passou = True
    for est, nome in [("mobile", "Celular"), ("desktop", "Computador")]:
        notas, res = [], []
        for _ in range(a.rodadas + 2):
            if len(notas) >= a.rodadas:
                break
            try:
                l = psi(url, est, k) if k else lighthouse(url, est)
                sc = l["categories"]["performance"]["score"]
            except Exception:
                sc = None
            if sc is None:  # rodada falhou (Chrome travou): tenta de novo
                continue
            notas.append(round(sc * 100)); res.append(l)
        if not notas:
            print(f"{nome}: não deu para medir"); passou = False; continue
        med = statistics.median(notas)
        l = res[notas.index(sorted(notas)[len(notas) // 2])]
        au = l["audits"]
        ok = med >= a.meta
        passou &= ok
        print(f"{nome}: nota {med:.0f} {'OK' if ok else 'ABAIXO DA META'} (rodadas: {notas})")
        print("   " + " · ".join(f"{n} {au[c]['displayValue']}" for c, n in METRICAS))
        if not ok:
            print("   O que mais pesa:")
            for i in au.get("bootup-time", {}).get("details", {}).get("items", [])[:4]:
                print(f"     script {round(i['total'])} ms  {i['url'][:80]}")
            for c in ["uses-responsive-images", "unused-javascript", "render-blocking-resources", "modern-image-formats", "offscreen-images"]:
                if au.get(c, {}).get("score", 1) is not None and au.get(c, {}).get("score", 1) < 0.9:
                    print(f"     {au[c]['title']}: {au[c].get('displayValue', '')}")
        print()
    print("RESULTADO:", "PASSOU (pode publicar)" if passou else f"NÃO PASSOU: meta {a.meta} no celular e no computador")
    sys.exit(0 if passou else 1)


if __name__ == "__main__":
    main()
