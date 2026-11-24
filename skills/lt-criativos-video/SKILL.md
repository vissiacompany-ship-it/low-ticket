---
name: lt-criativos-video
description: Cria roteiros de criativos em VÍDEO para anúncio low ticket (Meta Ads), gravados por takes (uma frase por take), na estrutura de 6 etapas da Kamilla (quebra de padrão, gancho, problema/dor, solução/promessa, prova, CTA reforçada; 35 s a 1 min), com base nos padrões extraídos dos vídeos reais dela. Entrega o roteiro.json, o .md e o PDF de gravação em tamanho de celular para quem vai gravar (frase em destaque, o que fazer, como falar, o que entra na edição), mais ganchos extras e lista de imagens. Use quando pedirem "roteiro de vídeo", "criativo em vídeo", "anúncio em vídeo", "vamos gravar os criativos", "roteiro por takes", "PDF de gravação". Não é para criativo em imagem (isso é lt-criativos-imagem).
user-invocable: true
---

# Criativos em vídeo (gravação por takes)

Processo: `.claude/skills/low-ticket/fontes/0-vissia/operacao/processos/criativos-video-low-ticket.md`.

- **Padrões reais da Kamilla (ler sempre antes de escrever):** `padroes-kamilla.md`
- **Lado visual (formatos de tela, aberturas, legendas, cartão final, os 11 vídeos desmontados com quadros):** `.claude/skills/low-ticket/playbook/playbook-criativos-video.md` (aba "Criativos em vídeo" do caderno `PLAYBOOK-LOW-TICKET.html`). Usar para o campo `quebra` do take 1 e a coluna "Na edição".
- Transcrições com tempo e quadros dos 11 vídeos: `referencias/transcricoes-kamilla.md` e `referencias/quadros-kamilla.png`. Vídeos: `.claude/skills/low-ticket/fontes/4-conhecimento/cursos-e-sistemas/Low Ticket Kamilla/Criativos/`
- Slide da estrutura e framework: `.claude/skills/low-ticket/fontes/4-conhecimento/cursos-e-sistemas/Low Ticket Kamilla/Criativos/framework-criativos-lt.md`
- Gerador do PDF: `scripts/gerar_pdf.py` · Formato do JSON: `modelos/roteiro.exemplo.json`
- **Padrão ouro, formato APROVADO pelo Paulo em 01/11/2026 (Anúncio Pronto):** `.claude/skills/low-ticket/fontes/1-clientes/primeiro-cnpj/5-produtos/anuncio-pronto/criativo/roteiro.json` e `roteiro-gravacao-anuncio-pronto.pdf`

## Antes de começar, tenha em mãos
1. A oferta do produto (`oferta/oferta.md`): dores, objeções, mecanismo, 3 passos, garantia. **E o que o produto é de verdade e o caminho do cliente** (o que ele faz, em que ordem), na memória do cliente ou perguntando ao Paulo.
2. **A primeira dobra da página que está no ar** (ler o código ou a página, não só o oferta.md: a promessa pode ter mudado). Congruência total: o vídeo só fala o que a página fala.
3. Quem grava (nome) e onde (rua, casa, escritório).
4. O controle de criativos do projeto (`criativo/controle-criativos.md`).

## Estrutura obrigatória (as 6 etapas, nesta ordem)
1. **Quebra de padrão (1 a 2 s):** é **visual** e acontece **junto** com o gancho. A fala começa no segundo 0, nunca com um take mudo. Gesto, objeto, celular colado na câmera, faixa de texto no topo com o público, elemento sobreposto.
2. **Gancho (3 s):** 1 frase, sem "oi". Tipos em `padroes-kamilla.md`.
3. **Problema / Dor:** 2 a 4 frases curtas, na linguagem do avatar.
4. **Solução / Promessa:** nome do produto + "é muito simples: [3 ou 4 ações]" + "e o melhor: [benefício]".
5. **Prova:** demonstração. "Olha aqui ó", com a tela do produto e a pessoa pequena no canto. Nunca depoimento inventado.
6. **CTA reforçada:** 3 frases. "Pra liberar o seu acesso, é só clicar no botão aqui embaixo" + motivo verdadeiro para agir hoje (data real, preço por dia, garantia) + "Então clica aqui e libera o seu acesso agora."

**Tempo:** 35 s a 1 min. Alvo de 120 a 145 palavras (ritmo de cerca de 2,5 palavras por segundo). O gerador imprime a contagem; se passar de 150, corte.

## Passo a passo
1. Ler `padroes-kamilla.md`, a oferta e a página no ar.
2. **Mostrar ao Paulo a matriz** (checkpoint 1): para cada vídeo, o código, o ângulo, o gancho e a quebra de padrão. Padrão: 4 vídeos, cobrindo dor, demonstração, contra-crença (inimigo) e uma data real ou novidade. Pelo menos 1 de demonstração (é o formato que a Kamilla mais usa).
3. Escrever o `criativo/roteiro.json` (formato em `modelos/roteiro.exemplo.json`). Um take = uma frase de até ~15 palavras. Em cada take: `fala`, `fazer` (onde e ação), `como` (a vida: expressão, gesto, tom), `edicao` (quando entra tela ou B-roll). No take 1, o campo `quebra`. Cada vídeo leva 2 ou 3 ganchos extras (o take 1 regravado vira outro anúncio).
4. Gerar o PDF e o .md:
   `python3 .claude/skills/low-ticket/skills/lt-criativos-video/scripts/gerar_pdf.py <projeto>/criativo/roteiro.json <projeto>/criativo --conferencia <pasta-temporária>`
5. **Conferir** as páginas PNG (quebra de página, nenhum cartão cortado) e a contagem de palavras.
6. Entregar o PDF (checkpoint 2: o Paulo aprova antes de gravar) e registrar os vídeos (V1, V2...) no `controle-criativos.md`.
7. Depois de gravar: `/editar-criativo` junta os takes, corta silêncios, coloca legenda palavra por palavra e a tela do produto com a pessoa pequena no canto.

## Regras (das correções do Paulo)
- **Seguir exatamente as 6 etapas do slide da Kamilla**, sem etapas inventadas (a "virada" vai dentro de Problema/Dor).
- **Nunca abaixo de 35 s.** A 1ª versão saiu com 30 s e foi refeita.
- Quebra de padrão não é take mudo: é o visual do começo, com o gancho já sendo falado.
- O documento para quem grava é **simples, sem jargão**, uma frase em destaque por cartão, em tamanho de celular.
- **Decisões do Paulo (04/11/2026):** promessa de renda pode entrar como a Kamila usa, com número real, e sempre com uma versão sem renda de reserva (o Meta costuma reprovar); "antes que este vídeo saia do ar" pode (o anúncio pode ser pausado); resultados, relatos, prints e notificações: usar os reais do cliente, pedindo antes de escrever. Sem atributo pessoal ("você é MEI endividado?"), sem "curso", sem travessão. Detalhes: playbook de criativos, seção 7.
- Dados do produto (números, tempo, garantia) só se estiverem na página.

## Erros já cometidos
- (01/11) Frases que confundiram o Paulo: "esse anúncio foi feito com IA" num vídeo (parece que o próprio vídeo é de IA) e "clica e aparece no bairro" (pulou a ativação na ferramenta de anúncios). Depois, ao corrigir, tirei a IA e as 4 perguntas sem ele pedir, e errei de novo. **Corrigir só o que o Paulo apontou**; o resto fica. Antes de escrever a solução, ter claro o que o produto é e o caminho do cliente (Anúncio Pronto: `.claude/skills/low-ticket/fontes/1-clientes/primeiro-cnpj/_memoria/project_primeiro_cnpj_anuncio_pronto.md`).
- Escrever pela oferta antiga: a página tinha mudado de "copie o anúncio pronto" para "gere com IA". Sempre ler a página no ar.
- Roteiro longo demais (186 palavras ≈ 74 s). Contar as palavras antes de gerar.
