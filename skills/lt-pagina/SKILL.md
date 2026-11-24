---
name: lt-pagina
description: Cria a página de vendas low ticket completa (metodologia 13S da Kamilla e do Carlos, modelada no 50 Viral Fit, Carrosséis Personal, App Stories Bíblicos e Ativa FIT; o Anúncio Pronto é o exemplo nosso), para qualquer nicho. Gera um index.html único com todos os blocos, elementos e efeitos (botão pulsando com brilho, galeria com cadeado, +N com chips, vídeo dos 3 passos que toca ao rolar, oferta com faixa vermelha e confete, selo de garantia, FAQ, WhatsApp, pixel). Use quando pedirem "página de vendas low ticket", "página do produto X", "replicar a estrutura do Anúncio Pronto", "página igual à da Kamilla/50 Viral Fit", ou depois de criar uma oferta com a skill lt-oferta.
---

# Página de vendas low ticket

> **Playbook (04/11/2026):** antes de começar, leia `.claude/skills/low-ticket/playbook/playbook-pagina-lt.md` (metodologia da Kamila com todas as páginas dela como referência, Instravel como exemplo principal; diferenças entre páginas são decisões por oferta, seção 10; oferta, copy, prova, design, animações, CTAs e vídeo, seção por seção). Versão visual: `PLAYBOOK-LOW-TICKET.html`. Onde o playbook e esta skill divergirem, vale esta skill até o Paulo aprovar a atualização (seção 12 do playbook).

Papel de **design e montagem**. O design já está validado (modelo da Kamilla e da Carlos & Kamila + Anúncio Pronto) e vive no gerador: só as cores, a fonte e as imagens mudam por produto. Não escreve copy (`lt-copy-pagina`) nem cria a oferta (`lt-oferta`).

Gera a página inteira a partir de um arquivo `pagina.json`. Nada de montar HTML na mão: a estrutura, os efeitos e o responsivo já estão no gerador.

- Gerador: `scripts/gerar_pagina.py`
- Modelo completo preenchido (Anúncio Pronto): `modelos/pagina.exemplo.json`
- Página real de referência: https://primeirocnpj.com.br/anuncio-pronto/
- **A metodologia é a 13S** (slide "Estrutura 13S" da Kamilla): 1 Impacto visual + promessa, 2 Prova social, 3 Passo a passo, 4 Entregáveis, 5 Bônus, 6 Resultado imaginado, 7 Ancoragem, 8 Oferta, 9 Garantia, 10 Autoridade, 11 FAQ, 12 Suporte, 13 Rodapé. Nenhum bloco fora dela (o antigo bloco `dor` foi inventado, não é da referência, e saiu em 02/11/2026).
- Referências reais (prints completos das páginas da Carlos & Kamila, no banco de ofertas, ofertas 11 a 14, arquivos "pv ..." copiados em `.claude/skills/low-ticket/fontes/2-aplicativos/banco-de-ofertas/storage/`, lista em `.claude/skills/low-ticket/fontes/2-aplicativos/banco-de-ofertas/offer_files-11-14.md`): 50 Viral Fit, 50 Viral Fit Personal (carrosséis), App Stories Bíblicos, Ativa FIT. Texto das duas primeiras em `.claude/skills/low-ticket/fontes/2-aplicativos/banco-de-ofertas/page_archive-21-22.md`.
- Texto dos 12 blocos: `.claude/skills/low-ticket/fontes/4-conhecimento/cursos-e-sistemas/Low Ticket Kamilla/Página de Vendas/framework-pagina-vendas-lt.md`. Prints antigos em `.claude/skills/low-ticket/fontes/4-conhecimento/cursos-e-sistemas/Low Ticket Kamilla/Swipe Files/50 viral fit/` e `.../Swipe Files/mulher exemplar/`.
- Processo documentado: `.claude/skills/low-ticket/fontes/0-vissia/operacao/processos/pagina-de-vendas-low-ticket.md`

## Dois modelos de página (escolha no `pagina.json`)

| Modelo | Quando | Como | Exemplo |
|---|---|---|---|
| **v2 (réplica fiel do Instravel)** | Padrão para oferta nova: visual mais atual, mais rápido | `"modelo": "v2"` (código em `scripts/modelo_v2.py`) | `modelos/pagina.v2.exemplo.json` |
| Clássico (Anúncio Pronto / 50 Viral Fit) | Páginas que já existem e variantes antigas | sem `"modelo"` | `modelos/pagina.exemplo.json` |

No v2 a estrutura, os tamanhos, os pesos, as sombras e os efeitos são os da referência e **não se mudam**. A marca entra por `cores` (primaria, destaque_foto, acento, texto, titulo_escuro, clara, clara_fundo, mundo, pausa), fonte, imagens e textos. Quebras de linha: `|` no texto, e campos `*_pc` para o computador. Ícones dos passos: `smartphone`, `grid`, `camera`, `download`, `mensagem`, `editar`, `enviar`, `play`, `estrela`, `check`, `arquivo`, `coracao` (ou um emoji).

### Ferramentas da skill
- `scripts/gerar_pagina.py <pagina.json>`: gera a página (cria versões de imagem em tamanhos de celular em `assets/_otm/` e baixa a fonte para `assets/fonts/`).
- `scripts/otimizar_video.py <videos>`: vídeos de categoria de 10 a 18 MB viram cerca de 1 MB, mais a capa.
- `scripts/medir_velocidade.py <pasta ou url>`: nota do Google (meta 95 no celular e no computador).
- `scripts/comparar_referencia.py <url referência> <pasta>`: lado a lado, seção por seção, celular e computador.

### Regra de réplica (Paulo, 04/11/2026)
Quando a página segue uma referência, **o design da referência é a regra**: mesma tipografia, tamanhos, pesos, quebras de linha, cores, sombras, espaçamentos, efeitos e posições. Antes de mostrar ao Paulo: rodar `comparar_referencia.py`, olhar todas as seções no celular e no computador e corrigir. Checklist do que ele já apontou: playbook, seção 6C.

## Passo a passo

1. **Pegue a copy aprovada.** `oferta/copy-pagina-vendas.md` é a saída da skill `lt-copy-pagina`. Se não existir, rode `lt-oferta` e depois `lt-copy-pagina` antes. Esta skill não escreve copy: só monta. Não invente texto que não esteja na copy aprovada.
2. **Crie a pasta da página** dentro do projeto: `<projeto>/pagina/` com uma subpasta `assets/`.
3. **Copie `modelos/pagina.exemplo.json` para `<projeto>/pagina/pagina.json`** e troque todo o conteúdo pelo da oferta nova. Mantenha a ordem dos blocos.
4. **Imagens:** liste para o Paulo as imagens que faltam (nomes em `assets/`). Enquanto não existirem, use `emoji` nos cartões que aceitam (extras, bônus). O gerador avisa cada imagem que não encontrar.
5. **Vídeo dos 3 passos:** rode a skill `lt-video-passos` e aponte `passos.video.mp4` e `passos.video.poster` para os arquivos gerados. Sem vídeo, deixe `"video": null` e os passos aparecem em cartões (modelo Mulher Exemplar).
6. **Gere:** `python3 <skill>/scripts/gerar_pagina.py <projeto>/pagina/pagina.json`
6b. **Compare com a referência** (se houver): `python3 <skill>/scripts/comparar_referencia.py <url> <projeto>/pagina --saida <projeto>/pagina/comparacao`. Corrija tudo que estiver diferente antes de mostrar.
7. **Confira no navegador** em 1280px e 390px (playwright ou Chrome) antes de dizer que está pronta: topo inteiro na primeira tela, nada vazando para o lado, imagens carregando, botão da oferta com o link do checkout.
7b. **Velocidade (obrigatório, regra do Paulo de 04/11/2026):** nota 95 ou mais no PageSpeed no celular e no computador, abrindo em até 2 s, sem perder qualidade de imagem. Meça com `python3 <skill>/scripts/medir_velocidade.py <pasta ou url>` e só publique se passar. Como chegar lá: playbook, seção 6B. Medição de 04/11: o gerador atual dá ~78 no celular e ~92 no computador (Lighthouse local), então ainda falta ajustar o gerador.
8. **Publicar:** a pasta `pagina/` é estática. Vercel: `vercel --prod --yes` dentro dela.

## Os blocos (ordem fixa)

| # | Bloco (chave no JSON) | O que é | Modelo |
|---|---|---|---|
| 1 | `faixa` | Faixa no topo: "🔥 EXCLUSIVO PARA ..." | 50 Viral Fit |
| 2 | `hero` | Logo, headline com destaques, sub (parte sublinhada + linha em negrito), visual e botão que desce para a 2ª dobra | Anúncio Pronto / Mulher Exemplar |
| 3 | `depoimentos` | Prints e cartões de quem usou, em trilho que arrasta para o lado | Mulher Exemplar / 50 Viral Fit |
| 4 | `passos` | Título com "3 passos simples" sublinhado, vídeo dos passos, ícones 01 02 03, frase final | 50 Viral Fit |
| 5 | `recebe` | Título, "Veja alguns modelos 👇", +N grande com chips, galeria com cadeado nos alternados, faixa rolante, nota, "Tudo pronto..." + 3 cartões extras | 50 Viral Fit / Mulher Exemplar |
| 6 | `bonus` | 3 cartões com etiqueta 🎁 BÔNUS N e imagem, com brilho em volta | 50 Viral Fit |
| 7 | `oferta` | "Imagine...", Recapitulando com preços riscados, total, frase de transição fixa, "🎉 Parabéns! Você ganhou X% OFF" com confete, cartão com faixa vermelha, logo, + N bônus, imagem do produto, De/por/parcelas/à vista, economia, botão do checkout, bandeiras, checks e alerta | Kamilla blocos 6 e 7 / 50 Viral Fit |
| 8 | `garantia` | Selo SVG "Garantia de N dias / Risco zero", texto e frase forte | 50 Viral Fit |
| 9 | `autor` | Nome, cargo, 3 a 6 parágrafos em 1ª pessoa, frase final, foto redonda | 50 Viral Fit |
| 10 | `faq` | 4 a 8 perguntas, abre e fecha | Kamilla bloco 11 |
| 11 | `whatsapp` | "Ficou com alguma dúvida?" + botão verde | Kamilla bloco 10 |
| 12 | `rodape` | ©, empresa, CNPJ, links e aviso legal fixo do Facebook | Kamilla bloco 12 |

Blocos opcionais: `faixa`, `depoimentos`, `bonus`, `autor`, `faq`, `whatsapp`. Se a chave não existir ou estiver vazia, o bloco some.

## Campos importantes

- **Marcação de texto** (vale em qualquer copy): `[[texto]]` cor primária em negrito, `{{texto}}` cor de destaque em negrito, `__texto__` sublinhado à mão, `**texto**` negrito.
- **`cores`**: primaria, escura, fundo, sucesso (botões e preço), destaque (2ª cor da headline), acento (roxo dos bônus e cargo), alerta (vermelho da oferta), laranja. Pergunte a identidade do cliente. Referência visual não é identidade.
- **`hero.visual.tipo`**: `pessoa_telas` (pessoa recortada + 2 celulares + notificações que contam + selos coloridos) ou `imagem` (um mockup só, como no Mulher Exemplar).
- **`recebe.bloquear`**: posições da galeria que ficam borradas com cadeado (padrão 2, 4, 5, 7). `[]` mostra todas.
- **`recebe.proporcao`**: `4/5` para anúncio ou post, `9/16` para stories, `1/1` para quadrado.
- **`oferta.de`**: total da ancoragem. O desconto e a economia são calculados sozinhos.
- **`oferta.prazo`**: data real de fim da oferta (ex.: `2026-11-30T23:59:00-03:00`). Com prazo, a faixa vermelha mostra o cronômetro até essa data. Sem prazo, mostra "Oferta Especial / Preço exclusivo desta página".
- **`checkout`**: só o botão da oferta vai ao checkout (com as UTMs da página repassadas). Os outros botões descem até a oferta.
- **`rastreio`**: `meta_pixel_id` (PageView + InitiateCheckout no clique) e `clarity_id` (carrega na primeira interação para não pesar).

## Efeitos que já vêm prontos

- Botões: pulso, cor verde correndo por dentro e brilho passando. Seta do botão do topo descendo.
- Animações pausam quando a seção sai da tela (desempenho no celular).
- Notificações do topo contam de 0 até o número.
- Galeria com cadeado e desfoque nos itens alternados (curiosidade: o resto está lá dentro).
- Faixa rolante de miniaturas (`recebe.faixa_rolante`).
- Vídeo dos passos só toca com 60% dele na tela, sempre do Passo 1, e volta ao início quando a pessoa sai.
- Confete quando "Parabéns! Você ganhou X% OFF" aparece.
- Rolagem suave, FAQ que abre e fecha, layout de celular em uma coluna sem empilhar.

## Prova social (ponto 2 da 13S) quando não há depoimento

O ponto 2 nunca some na referência, ele muda de formato (visto nas 4 páginas da Carlos & Kamila):
1. **Depoimentos reais** em trilho que arrasta (App Stories: prints de stories de clientes marcando a criadora). Nota "5,0 ★" só com avaliações reais.
2. **Prints de uso real** do produto (50 Viral Fit: perfis que usaram os modelos).
3. **Demonstração do produto** com exemplos passáveis e vídeo "Veja como funciona na prática" (Carrosséis Personal).
4. **Passo a passo mais cedo + autoridade** (Ativa FIT, sem depoimento nenhum).
Sem prova real, escolher 2, 3 ou 4. Nunca inventar nota, avaliação ou depoimento. O gerador monta o formato 1 (`depoimentos`) e o 3 (`demonstracao`: `titulo`, `sub`, `itens` com `imagem` e `legenda`). **Em produto digital, a demonstração é teaser: só o título da página legível, o resto borrado. A página nunca entrega o conteúdo do produto.** O mockup do topo é celular (`hero.visual.tipo: imagem`, com celulares mostrando a capa e páginas em teaser).

## Regras que não mudam

- **Depoimento de retorno real.** Prints (Stories, carrossel, Instagram, WhatsApp) e textos copiados de retornos reais (Google, direct, WhatsApp, comentário) podem ir em cartão sem foto ou @. A nota "5,0 · +X avaliações" pode usar avaliações da marca ou da especialista como um todo. Não escrever depoimento do zero nem gerar print com IA. Sem retorno nenhum, o bloco some.
- **Cronômetro:** por data real (`oferta.prazo`) ou por visitante (`oferta.cronometro_minutos`, 15 min no padrão Instravel). Ao zerar, **nada muda**: o cronômetro para em 00:00:00 e o resto fica igual (decisão do Paulo, 04/11/2026). Não reinicia ao recarregar.
- **Frases da Kamilla são padrão validado, não obrigação.** O gerador traz como ponto de partida: a transição da ancoragem (`oferta.frase_transicao`, `""` tira), os checks "Pagamento único / Sem mensalidade" (`oferta.checks`), o título e o botão do WhatsApp (`whatsapp.titulo`, `whatsapp.botao`). Cada oferta decide se faz sentido; a copy vem da skill `lt-copy-pagina`. Só o aviso legal do rodapé é fixo.
- **Sem travessão (—) na copy.** O gerador avisa se encontrar.
- **Mesmo texto no celular e no computador.** Só muda tamanho e espaço.
- **Promessa sem renda garantida** (o Meta reprova): falar de conversas, clientes, resultado tangível.
- Se a página ficar dentro de um site existente (como o PrimeiroCNPJ), gere aqui e adapte para o build do site. Não reescreva os blocos do zero.
