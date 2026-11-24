"""Deixa vídeos da página leves (categorias, demonstrações curtas) sem perda visível no celular.

Uso: python3 otimizar_video.py video1.mp4 [video2.mp4 ...] [--largura 540] [--segundos 10] [--som]
Saída: <nome>-web.mp4 (H.264, sem som por padrão, começa a tocar antes de baixar tudo) e <nome>-web.webp (capa)
na mesma pasta. Vídeo narrado (vídeo de tela do Como Funciona): use --som e --segundos 0 (inteiro).
"""
import argparse, os, shutil, subprocess, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("videos", nargs="+")
    ap.add_argument("--largura", type=int, default=540)
    ap.add_argument("--segundos", type=float, default=10, help="0 = vídeo inteiro")
    ap.add_argument("--som", action="store_true")
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg não encontrado")
    for v in a.videos:
        base = os.path.splitext(v)[0]
        out = base + "-web.mp4"
        cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", v]
        if a.segundos:
            cmd += ["-t", str(a.segundos)]
        cmd += ["-vf", "scale=%d:-2" % a.largura, "-c:v", "libx264", "-preset", "slow", "-crf", "27",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
        cmd += ["-c:a", "aac", "-b:a", "96k"] if a.som else ["-an"]
        subprocess.run(cmd + [out], check=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", out, "-vframes", "1", "-q:v", "80", base + "-web.webp"], check=True)
        antes, depois = os.path.getsize(v) / 1e6, os.path.getsize(out) / 1e6
        print("%s: %.1f MB -> %.1f MB  (%s)" % (os.path.basename(v), antes, depois, os.path.basename(out)))
        if depois > 1.6 and not a.som:
            print("  AVISO: acima de ~1,5 MB. Tente --segundos 8 ou --largura 480.")


if __name__ == "__main__":
    main()
