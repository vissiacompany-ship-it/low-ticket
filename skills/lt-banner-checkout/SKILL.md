---
name: lt-banner-checkout
description: Cria o banner do topo do checkout de ofertas low ticket (a imagem "ÚLTIMO PASSO, você está a um passo de..." que fica acima do formulário de pagamento, modelada no 50 Viral Fit). Entrega o texto exato da arte, a lista do que anexar e o prompt pronto para gerar no ChatGPT ou no Gemini, em versão clara e versão escura, com checklist de conferência e prompt de correção. Use quando pedirem "banner do checkout", "banner de checkout", "imagem do topo do checkout", "banner último passo", "banner da OnProfit/Kiwify/Hotmart", "prompt do banner do checkout", ou depois de criar a página com a skill lt-pagina.
---

# Banner do checkout

> **Playbook do checkout (04/11/2026):** leia `.claude/skills/low-ticket/playbook/playbook-checkout-lt.md` e use os prompts de `prompts-imagens-lt.md` (seção 10: variante "mundo do nicho", modelo Instravel; referência `referencias/ceu-mundo-do-nicho_instravel.png`).

A peça que fecha a esteira: o cliente clicou no botão da página, caiu no checkout e vê este banner antes do formulário. Ele não vende nada novo. Ele **lembra a promessa, tira o medo (selos) e empurra para preencher os dados**.

Esta skill **não monta o banner**. Ela entrega o prompt para o Paulo gerar no ChatGPT ou no Gemini (1 prompt por conversa, anexando os arquivos), no mesmo modelo da `lt-criativos-imagem`.

- Referências visuais em `referencias/` (abra antes de escrever o prompt):
  - `claro_50-viral-fit.png`: o modelo principal. Fundo cinza claro, cartão branco com a headline, dois celulares, selos pretos com verde neon, barra verde.
  - `escuro_anuncio-pronto.png`: versão escura (azul-marinho com brilho roxo, selos com contorno roxo, barra verde).
  - `claro-simples_molde-viral.png`: versão clara simples, só com cartões de produto no lugar dos celulares.
- Páginas e criativos do mesmo projeto: skills `lt-pagina` e `lt-criativos-imagem`.

## Antes de começar, tenha em mãos

1. **A headline da primeira dobra da página e o nome do produto.** O banner repete a promessa da página (congruência).
2. **O logo do produto** (PNG, de preferência com fundo transparente).
3. **A imagem do produto em uso:** os 2 criativos, reels, telas ou mockups que aparecem na página (hero ou "o que você recebe"). É isso que vai dentro dos celulares.
4. **As cores da marca** (primária e de destaque). Pergunte a identidade do cliente. Referência visual não é identidade.
5. **As garantias reais da oferta:** forma de pagamento (ex.: pagamento único), como entrega (ex.: acesso imediato) e dias de garantia. Só vale o que está na oferta aprovada (`oferta/oferta.md`).
6. Se tiver, uma frase de contexto real da oferta (ex.: "nessa Black Friday"), só quando a campanha e a página de fato dizem isso.

Se faltar item 1, 2 ou 5, pergunte antes. Os demais, assuma e declare a suposição.

## Passo a passo

1. **Monte o texto da arte** com a estrutura fixa abaixo e mostre para o Paulo aprovar ou trocar (headline, rótulos, chips, selos). Só depois escreva o prompt.
2. **Escolha o tema:** claro (padrão, modelo 50 Viral Fit) ou escuro (ofertas de tecnologia, IA, ou quando a página é escura). Se ele não disser, entregue o claro e ofereça o escuro.
3. **Escreva o prompt** usando o esqueleto abaixo, preenchendo todos os colchetes. Prompt em inglês, textos da arte em português entre aspas, exatamente como devem aparecer.
4. **Entregue no formato de entrega** (abaixo): texto da arte, anexos, prompt em bloco de código, como usar.
5. **Salve** em `<projeto>/criativo/banner-checkout/banner-checkout.md` (texto da arte, anexos, prompt aprovado e qual versão foi ao ar). O PNG final fica na mesma pasta.
6. **Depois da geração:** ele traz a imagem, você confere com o checklist e, se precisar, entrega o prompt de correção (um erro por vez).

## Estrutura fixa do banner (de cima para baixo)

Formato **4:3 horizontal** (1024x768, ou 1000x750). Na tela do checkout no computador ele aparece com cerca de 575 px de largura e no celular ocupa a largura toda, então **tudo precisa ler bem pequeno**.

| Bloco | Conteúdo | Regra |
|---|---|---|
| Logo | Logo do produto no canto superior esquerdo | O anexado, sem redesenhar |
| Selo de etapa | Pílula verde com "!" em círculo branco: **ÚLTIMO PASSO** | Fixo |
| Cartão da headline | Cartão branco arredondado colado na borda esquerda, 3 a 4 linhas | Estrutura: "Você está a **um passo** de [verbo + o que recebe] para [benefício]." Até 24 palavras, 3 ou 4 trechos destacados em degradê da cor da marca e negrito |
| Visual do produto | À direita: 2 celulares (ou reels) levemente inclinados em sentidos opostos, com a imagem do produto em uso dentro | Imagem anexada, nada inventado |
| Elementos flutuantes | 2 a 4 pequenos: ícones de seguidor/notificação, rótulos "+clientes", "+vendas" | Palavras de benefício, nunca número de resultado |
| Selos de confiança | 3 pílulas lado a lado com ícone: **PAGAMENTO ÚNICO**, **ACESSO IMEDIATO**, **7 DIAS DE GARANTIA** | Texto em caixa alta. Só as garantias reais da oferta |
| Barra final | Faixa verde na base, largura total: **FINALIZE SEUS DADOS E ACESSE AGORA** | Fixa em toda oferta |

## Esqueleto do prompt (versão clara, modelo 50 Viral Fit)

```
Horizontal checkout page header banner, 4:3 landscape (1024x768), Brazilian infoproduct style, clean and modern. I am attaching: (1) the product logo, (2) [N] images of the product in use, and (3) a reference banner. Use the reference banner only as a guide for layout, spacing and hierarchy. Do not copy its text, its logo or its images.

Background: very light grey (#F2F2F4) with a soft white glow behind the right side and a few very faint decorative swirl shapes.

Top left: the attached "[nome do produto]" logo, used exactly as provided, medium size, with a small green rounded pill below it containing a white circle with a green exclamation mark and the bold white text "ÚLTIMO PASSO".

Left, below the logo: a large white rounded card with a soft shadow, attached to the left edge of the banner (square on the left side, rounded on the right side). Inside it, in a clean geometric sans-serif, dark grey (#1F1F2B), left-aligned, 4 lines:
"Você está a [um passo] de" / "[verbo + o que recebe]" / "[para benefício 1] e" / "[benefício 2]."
The words in brackets are bold and filled with a smooth gradient from [cor primária] to [cor secundária]; the remaining words are regular weight dark grey. Write the text exactly like this, without the brackets, with exact Brazilian Portuguese accents.

Right side: two modern smartphones (or vertical video frames), slightly rotated in opposite directions (about -4 and +4 degrees), overlapping a little, with thin colored outlines in [cor primária] and [cor de apoio]. The screens show, sharp and legible, the attached product images, one per phone, filling the screen. Both phones are lit by the same soft light with a gentle shadow on the background. Around them, small floating elements: [2 to 4 itens: ex. small red rounded notification bubbles with a person icon, small green rounded label "+clientes", small blue rounded label "+vendas"]. No numbers presented as results.

Below, spanning the width in a single row, three rounded black pills with a thin neon green (#39FF6A) outline. Each has a neon green outline icon on the left and neon green bold uppercase text:
[icone de cartão] "PAGAMENTO ÚNICO" / [icone de envelope ou raio] "ACESSO IMEDIATO" / [icone de escudo com check] "7 DIAS DE GARANTIA".

Bottom: a full-width dark green banner strip (#14672B to #0F4F22 gradient, subtle top highlight) with bold white uppercase text centered: "FINALIZE SEUS DADOS E ACESSE AGORA".

Style: premium, high-contrast, generous spacing, very large legible text that stays readable when the image is shrunk to 575 px wide, sharp edges, exact Brazilian Portuguese with accents. No other text besides the texts quoted above, no real brand logos besides the attached one, no fake testimonials, no price.
```

## Esqueleto do prompt (versão escura, modelo Anúncio Pronto)

Mesmo prompt, trocando só estes blocos:

```
Background: deep navy (#070B1F) with a soft dark-blue gradient at the top left and a glowing [cor primária] light behind the phones on the right. The logo is white.

Headline card: a translucent dark card with a thin white 14% outline, rounded corners, bold white text, with the highlighted words in a gradient from turquoise (#5EEAD4) to blue (#60A5FA).

Trust pills: dark translucent pills with a 2px [cor primária em tom claro] outline, white bold uppercase text and turquoise outline icons.

Bottom strip: solid green (#16A34A) with a soft green glow upward.
```

## Formato de entrega (o que o Paulo recebe)

```
### Banner do checkout · [Produto] · versão [clara/escura]

Texto da arte:
- Selo: ÚLTIMO PASSO
- Headline: [headline com os destaques marcados]
- Rótulos dos celulares: [...]
- Elementos flutuantes: [...]
- Selos: [3 selos]
- Barra: FINALIZE SEUS DADOS E ACESSE AGORA

Anexar: [logo] + [imagens do produto em uso] + [referência: banner do 50 Viral Fit, arquivo referencias/claro_50-viral-fit.png]

(prompt em bloco de código)

Como usar: abra uma conversa nova no ChatGPT (ou Gemini), anexe os arquivos, cole o prompt. Se o texto sair errado, use o prompt de correção.
```

## Conferência depois da geração

Marque cada item com a imagem em tamanho de checkout (reduza para ~575 px):

- [ ] Todos os textos iguais ao aprovado, com acentos (VOCÊ, ÚLTIMO, ACESSO, GARANTIA).
- [ ] Headline legível em 575 px, destaques visíveis.
- [ ] Logo igual ao original (não redesenhado nem distorcido).
- [ ] Os 3 selos e a barra verde presentes, sem texto cortado.
- [ ] Imagens dentro dos celulares são as do produto, nítidas.
- [ ] Nenhum número de resultado, depoimento, preço ou logo de marca real que não foi pedido.
- [ ] Nada importante a menos de 4% das bordas.
- [ ] Mesma promessa da primeira dobra da página.

## Prompts de correção (um erro por vez, na mesma conversa)

- **Texto errado:** `Keep everything exactly as is, only fix the text in [bloco]. It must read exactly: "[texto correto]". Same font, size and position.`
- **Logo alterado:** `Keep everything as is. Replace the logo with the attached logo, reproduced exactly as provided, same position and size.`
- **Texto pequeno:** `Keep the layout and colors. Increase the headline font size by about 15% and the three trust pills' text by 10%, keeping everything inside the safe margins.`
- **Elemento a mais:** `Remove [elemento]. Keep everything else unchanged.`
- **Cores fora da marca:** `Keep the layout. Change the gradient on the highlighted words to [cor 1] to [cor 2] and the pill color to [cor].`

## Regras (valem para toda arte e todo texto)

- **Texto exato e curto:** headline até 24 palavras, 3 selos, 1 barra. Nada além do aprovado.
- **Selos só com garantia real.** Se a oferta não tem 7 dias de garantia, troque pelo que tem. Nunca prometer o que o checkout não entrega.
- **Sem prova inventada:** nada de "+10 mil alunos", "50K views" como resultado, depoimento, print de venda ou nota de avaliação. Elementos flutuantes são palavras de benefício ("+clientes").
- **Promessa sem renda garantida** (o Meta reprova): falar de seguidores, clientes, conversas e resultado tangível, nunca valor em reais.
- **Contexto sazonal só se for real** ("nessa Black Friday" só se a oferta e a página dizem isso). Cronômetro e escassez só com prazo real.
- **Sem logo real** de banco, Pix, WhatsApp, Instagram ou bandeira de cartão. Use ícone genérico. O checkout já mostra os meios de pagamento.
- **Sem travessão (—)** em nenhum texto.
- **Congruência:** a promessa do banner, a da página e a do criativo são a mesma.
- **Fidelidade do logo:** sempre "used exactly as provided". Se houver foto de especialista, usar a cláusula de fidelidade facial da `lt-criativos-imagem` uma única vez, no fim do prompt.
- **Elementos integrados:** celulares com a mesma luz e sombra do fundo, nada flutuando solto e sem sombra.
- **Formato:** 4:3 horizontal. No celular o banner é mostrado na largura da tela, então testar o PNG reduzido.
