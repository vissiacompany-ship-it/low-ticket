# Prompts das imagens da página e do checkout low ticket

**Versão 1 · 04/11/2026.** Todas as imagens do modelo Instravel, com o que é, onde entra, o tamanho, o que anexar e o prompt pronto. Serve para os dois playbooks (`playbook-pagina-lt.md` e `playbook-checkout-lt.md`).

## Como usar

- Ferramenta: ChatGPT (imagem) ou Gemini / Nano Banana. **Um prompt por conversa**, anexando os arquivos pedidos.
- Prompt em inglês; textos que aparecem na arte em português, entre aspas, exatamente como devem sair.
- Troque tudo que está entre `[colchetes]`. O exemplo do Instravel vem logo abaixo de cada prompt.
- **Regra de ouro:** a tela do produto dentro de mockups é sempre **print real do produto** anexado. A IA monta o cenário, nunca inventa o produto.
- **O que nunca gerar com IA:** depoimento, print de cliente, conversa, foto da especialista, número de resultado, avaliação.
- O "mundo do nicho" (fundo) é o mesmo em quase todas as peças. Gere ele primeiro e anexe nas outras como referência de fundo.

| # | Imagem | Onde entra | Tamanho | Gerar com IA? |
|---|---|---|---|---|
| 1 | Fundo do mundo do nicho | Topo, oferta, checkout | 1920x1080 e 828x1792 | Sim |
| 2 | Modelos da vitrine e capas | Carrossel 3D e faixa rolante | 1080x1920 | **Não**: exportar do produto |
| 3 | Vídeos das categorias | Tudo em um só app | 9:16 | **Não**: gravar a tela |
| 4 | Mockup da oferta | Cartão da oferta e banner do checkout | 1200x700, fundo transparente | Sim, com prints reais |
| 5 | Bônus 1 (coleção de exemplos) | Cartão do bônus | 600x600 | Sim |
| 6 | Bônus 2 (grade do feed) | Cartão do bônus | 600x600 | Sim, com prints reais |
| 7 | Bônus 3 (tutorial: notebook + celular) | Cartão do bônus | 600x600 | Sim, com prints reais |
| 8 | Selo de garantia | Garantia | 1024x1024, transparente | Sim |
| 9 | Ramos dourados da nota | Depoimentos | 2 PNG pequenos | Sim (só se houver nota real) |
| 10 | Banner do checkout | Checkout | 1024x736 | Sim |
| 11 | Imagem do bump 1, bump 2, combo | Checkout | 400x400 | Sim |
| 12 | Ícone do produto | Cartão do produto no checkout, favicon | 512x512 | Sim |
| 13 | Foto da especialista | Autoridade | 600x600 redonda | **Não**: foto real |
| 14 | Capa do vídeo | Como funciona (antes de tocar) | 1080x1920 | Print do próprio vídeo |

---

## 1. Fundo do mundo do nicho

O cenário que representa o assunto. No Instravel: céu azul com nuvens (viagem). Topo de página e oferta usam a mesma imagem.

```
Wide background photograph for a sales page, [16:9, 1920x1080 | 9:19.5 vertical, 828x1792 for mobile]. [Clear bright blue sky seen from above the clouds, soft white cumulus clouds along the bottom edge, a few thin wispy clouds at the top, natural daylight, airy and optimistic]. The upper two thirds must be calm and fairly uniform so white headline text stays readable on top of it. No people, no objects, no text, no logos. Photorealistic, high resolution, slightly saturated, clean.
```
Outros nichos: cozinha clara com bancada de mármore e luz da janela (confeitaria); academia limpa com luz lateral (fitness); céu ao amanhecer com raios de luz (cristão); mesa de escritório de madeira clara com plantas (negócios).

## 2. Modelos da vitrine e capas (não gerar)

São o próprio produto. Exportar do Canva (ou de onde o produto é feito) em 1080x1920, WebP. Escolher 10 para o carrossel 3D e 10 diferentes para a faixa rolante, misturando categorias e cores. Em produto de PDF ou prompt, usar teaser (título legível, resto borrado), nunca o conteúdo inteiro.

## 3. Vídeos das categorias (não gerar)

Gravação da tela do celular rolando os modelos de uma categoria, 6 a 10 s, sem som, 9:16, MP4 leve (até ~1,5 MB). Um vídeo por categoria. Rolagem lenta e contínua, começando já com modelos bonitos na tela.

## 4. Mockup da oferta

Notebook aberto com a tela do produto + 2 celulares (um atrás à esquerda, outro na frente à direita), fundo transparente. É usado no cartão da oferta e no banner do checkout.

Anexar: 1 print da tela do produto no computador (grade de modelos), 2 prints do celular (tela do app e um modelo aberto).

```
Product mockup on a transparent background (PNG), 1200x700. Composition: an open modern silver laptop in the center-right, seen slightly from the front and a bit from above; its screen shows the attached desktop screenshot, sharp and legible, filling the screen. Behind it on the left, a modern smartphone slightly rotated to the left (about -8 degrees) showing the attached phone screenshot 1. In front on the right, overlapping the laptop's corner, a second smartphone slightly rotated to the right (about +6 degrees) showing the attached phone screenshot 2. Thin black phone bezels, realistic glass reflections, soft natural shadows under the devices. Do not change, redraw or invent anything on the screens: use the attached screenshots exactly. No text, no logos besides what is on the screenshots, no background.
```

## 5. Bônus 1: coleção de exemplos (Instravel: Inspirações de Fotos)

Mosaico de fotos de referência (as "inspirações"), cantos arredondados, sobre o fundo do nicho.

```
Square image 600x600. Background: [the attached sky background, bright blue with soft clouds]. On top, a dense mosaic of [7] rounded-corner photo tiles of different sizes, arranged like a masonry collage that bleeds off the edges, with thin gaps showing the background. The photos show [aspirational travel moments: a hand holding a fresh coconut on a tropical beach, a woman in a white hat watching the sunset over the sea, two wine glasses toasting on a wooden pier at sunset, a woman with open arms on a turquoise beach, a couple on a boat near green cliffs, a man drinking a smoothie by palm trees, a suitcase on cobblestones]. Natural, warm, Instagram-style travel photography, diverse people, nobody looking at the camera. No text, no logos.
```

## 6. Bônus 2: grade do feed (Instravel: Posts para o Feed)

Grade 3x3 de posts prontos, como um perfil do Instagram.

Anexar: 9 posts reais do produto (ou 4 a 6 e pedir para repetir com variação).

```
Square image 600x600. Background: [the attached sky background]. In the center, a 3x3 grid of square social media posts with thin white gaps, like an Instagram profile grid, slightly larger than the frame on the sides, with a soft drop shadow under the grid. Use the attached post images exactly, one per cell, without redrawing their text or design. If fewer than 9 are attached, repeat them in a balanced order. No extra text, no logos, no phone frame.
```

## 7. Bônus 3: tutorial (notebook + celular flutuando)

Anexar: print do editor (Canva) com um modelo aberto no computador e print do app no celular.

```
Square image 600x600. Background: [the attached sky background, bright blue sky with fluffy white clouds at the bottom]. A modern silver laptop floats in the left half, tilted about 15 degrees, its screen showing the attached desktop screenshot (an editor with a template open), sharp and legible. In front of it on the right, a smartphone floats tilted the opposite way, showing the attached phone screenshot. Soft shadows, gentle depth of field on the clouds, clean and bright. Use the screenshots exactly, do not redraw them. No text, no logos.
```

## 8. Selo de garantia

```
Round guarantee badge on a transparent background (PNG), 1024x1024, flat vector style. Outer shape: a wavy scalloped circle in [vivid sky blue #12B5F5]. Inside: a white ring with a thin dashed [blue] line, then a dark charcoal (#2B2B2B) center circle. Curved text along the top of the white ring, bold black uppercase: "100% DINHEIRO DE VOLTA"; along the bottom: "GARANTIDO"; two small [blue] stars on the left and right of the ring. In the center circle, a huge bold [blue] number "7" and below it the bold [blue] word "DIAS". Exact Brazilian Portuguese spelling, clean and crisp, no other text.
```

## 9. Ramos dourados da nota (só com nota real)

```
Two separate golden laurel branches on a transparent background (PNG), each about 200x400, one curving to the left and one mirrored to the right, like the sides of an award wreath. Glossy 3D gold with soft highlights, a few round leaves, elegant and minimal. No text, no stars, nothing in the middle.
```

## 10. Banner do checkout (variante "mundo do nicho", modelo Instravel)

Referência visual: `skills/lt-banner-checkout/referencias/ceu-mundo-do-nicho_instravel.png`. A skill `lt-banner-checkout` tem o passo a passo e o modelo antigo (fundo cinza).

Anexar: o fundo do nicho (1), o mockup da oferta (4), o banner de referência.

```
Horizontal checkout page header banner, 1024x736, Brazilian infoproduct style, bright and modern. I am attaching: (1) a background photo, (2) a product mockup with transparent background, (3) a reference banner. Use the reference only for layout, spacing and hierarchy. Do not copy its text or images.

Background: the attached background photo filling the whole banner [bright blue sky with soft clouds].

Top left: a green rounded pill (#22C55E) with a white circle containing a green exclamation mark and the bold white uppercase text "ÚLTIMO PASSO".

Left, below it: a large white card with a soft shadow, attached to the left edge (square on the left, rounded on the right). Inside, in a bold modern geometric sans-serif (like Poppins), very dark grey, left-aligned, 3 lines:
"Você está a [um passo]" / "de [postar fotos lindas] e" / "[criativas] da sua viagem."
The words in brackets are in [vivid orange #F4511E]; the rest dark grey. Write exactly like this, without the brackets, with correct Brazilian Portuguese accents.
Two small 3D emoji-style objects overlap the card's corners: [a small white airplane at the top right corner and a vintage camera with a sparkle at the bottom right corner].

Right side: the attached product mockup, large, slightly overlapping the card, used exactly as provided.

Lower area: three rounded pills in a single row, [royal blue #1E63D6 to #2F80ED gradient] with a thin light outline, each with a white outline icon on the left and bold white text: [card icon] "Pagamento único" / [envelope icon with speed lines] "Acesso imediato" / [shield with check icon] "7 dias de garantia".

Bottom: a full-width bright green strip (#16A34A to #4ADE80 gradient) with bold white uppercase centered text: "PREENCHA SEUS DADOS E ACESSE [O APP] AGORA".

Style: high contrast, generous spacing, very large legible text that still reads when the banner is shrunk to 375 px wide. No price, no testimonials, no other text besides the quoted texts.
```

## 11. Imagens dos order bumps (quadradas, 400x400)

Pequenas no checkout (~100 px). Precisam ler em miniatura: um objeto grande, cor forte, quase nada de texto.

**Bump 1, mesmo uso (Instravel: figurinhas para Stories)**
Anexar: 1 Story real do produto com figurinhas aplicadas, se existir.
```
Square image 400x400. A vertical phone story (9:16) in the center, slightly rotated, showing [a golden sunset over a river with a small person silhouette], decorated with bold playful stickers: [a handwritten title sticker "Amazônia", a small airplane, a location pin, a sun]. Around the phone, 4 or 5 loose stickers floating with white die-cut borders and soft shadows. Bright, saturated, fun. No other text.
```

**Bump 2, outro uso (Instravel: quadro para imprimir)**
```
Square image 400x400. Several printed travel photo collages in thin black and white frames, overlapping at slight angles on a bright blue background: a world map collage, a "MÉXICO" photo collage, a beach collage. Realistic paper texture, soft shadows, cheerful travel colors. Only the word "MÉXICO" as text, nothing else.
```

**Combo**
Anexar: as imagens do bump 1 e do bump 2.
```
Square image 400x400. Bright blue background. In the back, the two attached product images side by side, slightly rotated. In front, centered, [a smiling young woman in a yellow jacket pulling a blue suitcase], cut out with a white outline like a sticker. At the bottom, a white rounded label with bold blue uppercase text "COMBO VIAGEM 2 EM 1". No other text.
```

## 12. Ícone do produto

```
App icon, 512x512, rounded square with white background and a subtle soft shadow. In the center, [a bold blue outline camera with a small airplane flying out of the lens, leaving a curved dotted trail], [gradient from #1E63D6 to #28C9E6]. Flat, modern, simple shapes that read at 48 px. No text.
```

## 13. Foto da especialista (não gerar)

Foto real, de preferência em situação do nicho (Kamila: sorrindo, em viagem, rua de pedra com flores). Recorte redondo, rosto no centro, fundo com cor e luz natural. Sem foto real, a seção vai só com texto.

## 14. Capa do vídeo

Print de um momento do próprio vídeo de tela (o app aberto com modelos bonitos), 1080x1920, com o botão de play da página por cima. Não criar capa com IA.
