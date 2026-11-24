---
name: lt-nova-oferta
description: Conduz uma oferta low ticket do zero até a página no ar, na metodologia da Kamila (playbook low ticket, modelo Instravel): briefing, oferta, copy, identidade, imagens e prompts, roteiro do vídeo de tela, página modelo v2, comparação com a referência, velocidade 95+, checkout (banner e order bumps) e criativos, parando nos checkpoints de aprovação do Paulo. Use quando o Paulo disser "/lt-nova-oferta", "quero criar uma oferta low ticket", "monta a página do meu produto", "faz uma página igual à do Instravel para o produto X", ou trouxer uma ideia de produto para vender barato no tráfego.
---

# Nova oferta low ticket (do zero à página no ar)

Esta skill não faz o trabalho de cada etapa: ela chama a skill certa na ordem certa e para nos checkpoints. Base de tudo: `.claude/skills/low-ticket/playbook/` (`playbook-pagina-lt.md`, `playbook-checkout-lt.md`, `playbook-funil-escala-lt.md` (funil completo, recuperação, ticket médio e escala), `prompts-imagens-lt.md`; caderno visual `PLAYBOOK-LOW-TICKET.html`). Processo: `.claude/skills/low-ticket/fontes/0-vissia/operacao/processos/pagina-de-vendas-low-ticket.md`.

## 0. Briefing (perguntar só o que faltar, em texto corrido)

1. **Produto:** o que a pessoa recebe (formato, quantidade), se já existe ou está "a produzir", onde roda (app, Canva, PDF, área de membros).
2. **Para quem:** avatar, identidade ou profissão, os momentos da vida dele em que usa o produto.
3. **Resultado prometido:** o que muda e em quanto tempo (tangível, sem promessa de renda).
4. **Especialista:** nome, história real, foto real.
5. **Prova real que já existe:** prints de uso, textos de retorno (Google, direct, WhatsApp), nota da marca.
6. **Identidade:** guia de marca do cliente (`/identidade` ou Playbook Visual). Sem guia: rodar `/identidade` ou usar a identidade da referência só como ponto de partida, avisando.
7. **Preço e checkout:** plataforma, link, preço pensado, se terá order bumps.
8. **Decisões por oferta** (playbook, seção 10): WhatsApp sim ou não, ancoragem (âncora única ou "Recapitulando"), urgência (cronômetro por visitante ou data), tipo de vídeo (tela ou animação).
9. **Referência:** se for seguir uma página específica, o link (para comparar lado a lado).

Crie a pasta `<cliente ou produto>/5-produtos/<nome>/` com `oferta/`, `pagina/assets/`, `video-demo/`, `criativo/` e um `ESTADO.md` (etapas: pronto, falta, depende de quem).

## Etapas e checkpoints

| # | Etapa | Skill | Saída | Checkpoint (o Paulo aprova) |
|---|---|---|---|---|
| 1 | Oferta | `lt-oferta` | `oferta/oferta.md`: promessa nos 4 pilares, produto por momentos do avatar, 3 bônus pela jornada, preço e âncora, bumps 2 + combo (ou 3 + combo), garantia | **nome, promessa, produto, bônus, preço** |
| 2 | Copy | `lt-copy-pagina` (modelo `copy-pagina-modelo-v2.md`) | `oferta/copy-pagina-vendas.md` nos campos do v2 | **esqueleto**, depois **texto** |
| 3 | Imagens | `prompts-imagens-lt.md` | lista do que o Paulo exporta do produto (vitrine, capas, vídeos de tela das categorias) + prompts das que a IA gera (fundo, mockup, bônus, selo, bumps, ícone) | **imagens** |
| 4 | Vídeo de tela | `lt-video-demo` | `video-demo/roteiro.md` | **roteiro**, depois o Paulo grava |
| 5 | Página | `lt-pagina`, modelo v2 | `pagina/pagina.json` + `index.html` | ver etapa 6 antes |
| 6 | Conferência | `comparar_referencia.py` (se houver referência), checklist 6C, `medir_velocidade.py` | imagens lado a lado e nota 95+ no celular e no computador | **página no celular e no computador**, antes de publicar |
| 7 | Publicar | Vercel (`vercel --prod --yes` em `pagina/`) | link no ar | **preço e link do checkout** |
| 8 | Checkout | `playbook-checkout-lt.md` + `lt-banner-checkout` | banner, textos e imagens dos bumps | **banner e bumps** |
| 9 | Criativos | `lt-criativos-imagem`, `lt-criativos-video` | anúncios | ver as skills |

Ao fim de cada etapa: atualizar o `ESTADO.md` e, ao fim do trabalho, perguntar em uma linha se vale virar conteúdo (`/conteudo`).

## Regras que não mudam

- **A referência é a regra do design** (modelo v2 = Instravel). Antes de mostrar a página, comparar lado a lado e passar no checklist 6C. Nunca "melhorar" por conta própria.
- Nada de depoimento escrito do zero: só prints e textos de retornos reais. A nota pode ser da marca como um todo.
- Cronômetro por visitante: ao zerar, nada muda.
- Promessa sem renda garantida. Sem travessão. Sem palavras proibidas (aprenda, descubra, método, estratégia, curso).
- Velocidade: só publicar com 95+ no celular e no computador.
- Correção nova do Paulo vira regra no processo e, se for de design, no checklist 6C do playbook.
