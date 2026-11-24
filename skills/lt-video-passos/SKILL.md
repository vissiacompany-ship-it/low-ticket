---
name: lt-video-passos
description: Cria o vídeo animado "Passo 1, Passo 2, Passo 3" (motion no estilo do 50 Viral Fit) para o bloco Como Funciona da página de vendas low ticket, em qualquer nicho. Fundo em degradê se movendo, pílula PASSO N + título surgindo com desfoque, uma demonstração por passo (galeria com cursor escolhendo, mapa com raio, anúncio virando conversa no WhatsApp, celular passando telas, post no Instagram recebendo curtidas), fechamento "Tudo pronto." + frases curtas com contador subindo e logo. Mostra prévia para aprovar e depois renderiza MP4 leve para a página. Use quando pedirem "vídeo dos 3 passos", "motion do passo a passo", "vídeo igual ao do 50 Viral Fit/Anúncio Pronto", ou ao montar a página com a skill lt-pagina.
---

# Vídeo dos 3 passos

> **Playbook (04/11/2026):** antes de começar, leia `.claude/skills/low-ticket/playbook/playbook-pagina-lt.md` (metodologia da Kamila com todas as páginas dela como referência, Instravel como exemplo principal; diferenças entre páginas são decisões por oferta, seção 10; oferta, copy, prova, design, animações, CTAs e vídeo, seção por seção). Versão visual: `PLAYBOOK-LOW-TICKET.html`. Onde o playbook e esta skill divergirem, vale esta skill até o Paulo aprovar a atualização (seção 12 do playbook).

Tudo sai de um arquivo `video.json`. O modelo, o renderizador e o exemplo já estão prontos:

- Modelo da animação: `scripts/template.html`
- Renderizador: `scripts/render.py` (prévia, folha de quadros e MP4)
- Exemplo completo (Anúncio Pronto): `modelos/video.exemplo.json`
- Vídeo de referência da Kamilla: `.claude/skills/low-ticket/fontes/1-clientes/primeiro-cnpj/5-produtos/anuncio-pronto/PASSO A PASSO 50 VIRAL FIT (atualizado).mp4`
- Resultado real no ar: bloco "3 passos simples" de https://primeirocnpj.com.br/anuncio-pronto/

## Passo a passo

1. **Textos dos passos:** use os 3 passos da oferta (`lt-oferta`, campo Método) sem mudar a copy. Título de cada passo curto, com até 6 palavras, para caber em uma linha.
2. **Crie `<projeto>/video-passos/video.json`** a partir do exemplo, com uma pasta `assets/` para as imagens.
3. **Escolha a demonstração de cada passo** (tabela abaixo) pelo que o passo mostra de verdade.
4. **Confira antes de mostrar:** `python3 <skill>/scripts/render.py video.json --quadros 1.6,5,9,13,17,21,25,28,31` e olhe `quadros.jpg`. Corrija texto cortado, imagem faltando ou cena vazia.
5. **Mande a prévia para aprovação** (o Paulo sempre quer aprovar antes do MP4): `python3 <skill>/scripts/render.py video.json --previa`. Isso gera `previa.html`, que toca em loop com pausa e barra. Passe o caminho, sem abrir o navegador sozinho.
6. **Depois de aprovado, renderize:** `python3 <skill>/scripts/render.py video.json` em segundo plano (leva uns 10 a 12 min para 33s). Saem `passos.mp4` (1280x720, uns 2 MB, para a página), `passos-1080p.mp4` (anúncio e Instagram) e `passos-poster.webp` (capa).
7. **Na página:** aponte `passos.video.mp4` e `passos.video.poster` do `pagina.json` (skill `lt-pagina`). O player já toca só com 60% do vídeo na tela, sempre do Passo 1, e volta ao início quando a pessoa sai.

## Demonstrações disponíveis (`demo.tipo`)

| Tipo | Mostra | Campos |
|---|---|---|
| `galeria` | 8 cartões entram, o cursor clica em um e ele vem para o centro | `itens` [{imagem, faixa, titulo}], `estilo` ("anuncio" põe topo Patrocinado + botão Enviar mensagem), `proporcao` ("4/5", "9/16", "1/1"), `escolhido` (índice) |
| `mapa` | Celular com mapa, raio abre em volta do "você", casas dentro ficam verdes com ícone | `etiqueta`, `icone` |
| `conversa` | Anúncio à esquerda, seta, WhatsApp à direita; cursor toca "Enviar mensagem" e as conversas chegam com contador | `esquerda` {imagem, faixa, titulo, estilo} |
| `celular` | Celular passando até 3 telas com toques do cursor, check verde no fim | `telas` [3 imagens], `etiqueta` |
| `instagram` | Post ou story no celular, corações subindo e contador de curtidas | `imagem`, `etiqueta`, `icone`, `ate` |

Exemplos por tipo de produto:
- Pack de modelos, templates, stories ou carrosséis: `galeria` (9/16 ou 4/5) → `celular` (baixar ou editar) → `instagram` (postar).
- Anúncio pronto ou negócio local: `galeria` → `mapa` → `conversa`.
- Scripts ou mensagens de WhatsApp: `galeria` → `celular` → `conversa`.
- App ou ferramenta: `celular` → `celular` → `instagram` ou `conversa`.

## Fechamento

- `fechamento.titulo`: "Tudo pronto." (padrão da referência).
- `fechamento.frases`: 3 pedaços curtos da frase do bloco, como "É só escolher," / "baixar" / "e postar!". Cada um aparece sozinho.
- `fechamento.contador`: `icone` (whatsapp, seguidores, coracao, vendas), `de` e `ate`. Use `false` para tirar.
- `logo` (imagem) ou `marca` (texto) no cartão branco do final.

## Cores e fonte

`cores.base` (fundo), `cores.blobs` (4 manchas que se movem), `cores.pill` (texto da pílula PASSO), `cores.pri` (botão e raio). Use a identidade do cliente. Fonte padrão: Plus Jakarta Sans (Google Fonts).

## Regras

- **Nada de fala ou resultado inventado de cliente.** As conversas aparecem como barras cinzas, sem texto, e os contadores são ilustração do produto em uso. Não escreva mensagem de cliente, valor de venda ou print fingindo ser real.
- **Copy só da oferta aprovada.** Sem travessão.
- Formato 16:9 (página). Para Reels ou Stories, adapte o palco para 1080x1920 antes de renderizar.
- Renderizar demora: rode em segundo plano e avise o tempo estimado.
