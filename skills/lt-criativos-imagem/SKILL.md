---
name: lt-criativos-imagem
description: Cria lotes de criativos em imagem (estáticos 4:5 para Meta Ads) para ofertas low ticket ou qualquer produto, sempre variando narrativa e modelo visual. Entrega, para cada criativo, o texto exato da arte, o prompt pronto para o ChatGPT (com fidelidade de rosto do especialista), o texto principal, o título e a descrição do anúncio, e mantém um controle do que já foi feito e testado para o próximo lote nunca repetir combinação. Modelos: especialista em degradê (frase lateral, citação, palavra gigante, frase com barra, equação com celular, segredo do mecanismo), manchete com cena (mecanismo, inimigo, preço comparado, persona na dor, contraste, notícia real), alerta tech, cartão de texto sem foto, cena com palavra circulada à mão e checklist, e resultado projetado com funil para B2B serviço. Use quando pedirem "criativos em imagem", "estáticos", "artes para anúncio", "novos criativos", "mais variações de criativo", "prompts de criativo para o ChatGPT".
---

# Criativos em imagem (estáticos)

Gera lotes de criativos que variam **narrativa** (o que se diz) e **modelo visual** (como a arte é montada). O objetivo do framework da Kamilla é testar volume: 10 por semana, achar 2 ou 3 campeões e criar variações deles.

- Modelos visuais e esqueletos de prompt: `catalogo-modelos.md`
- Imagens de referência de cada modelo: `referencias/` (abra as do modelo escolhido antes de escrever o prompt)
- Lote real aprovado (exemplo completo, 10 criativos): `.claude/skills/low-ticket/fontes/1-clientes/primeiro-cnpj/5-produtos/anuncio-pronto/criativo/criativos-meta-ads.md` e `copy-meta-ads.md`
- Base da Kamilla: `.claude/skills/low-ticket/fontes/4-conhecimento/cursos-e-sistemas/Low Ticket Kamilla/Criativos/framework-criativos-lt.md`
- Prompt de pessoa: `.claude/skills/low-ticket/fontes/4-conhecimento/frameworks/framework-extrator-prompt-foto-ia.md`

## Antes de começar, tenha em mãos

1. A oferta (`oferta/oferta.md` da skill `lt-oferta`): Big Idea, real problema, mecanismo, promessa, 3 passos, dores, objeções, preço.
2. A headline da primeira dobra da página. **Congruência:** a promessa do criativo é a mesma da página.
3. Foto de referência do especialista (o caminho do arquivo) e a roupa que ele usa nela.
4. Logo do produto (PNG) e as cores da marca.
5. O controle de criativos do projeto (`criativo/controle-criativos.md`), se existir.

## Passo a passo

1. **Monte a árvore de narrativas** a partir da oferta: Big Idea → 3 a 5 teses → ângulos. Use os ângulos da tabela abaixo.
2. **Monte a matriz do lote** (padrão 10 criativos): cada criativo é uma combinação **ângulo × modelo visual** que ainda não foi usada no controle. Regras da matriz:
   - Pelo menos 4 ângulos diferentes e pelo menos 5 modelos diferentes no lote.
   - Metade com especialista (linha A) e metade sem (linhas B e C), salvo se o Paulo pedir outra proporção.
   - Pelo menos 1 de promessa direta igual à página (A3 palavra gigante) e 1 de mecanismo (A6 ou B1).
   - Se houver campeão no controle: 3 do lote são variações dele (mesmo ângulo com outro modelo, ou mesmo modelo com outra frase).
3. **Mostre a matriz antes dos prompts:** tabela com código, tese, ângulo, modelo e o texto da arte. O Paulo aprova ou troca. Depois escreva os prompts.
4. **Escreva cada criativo** no formato abaixo, seguindo o esqueleto do modelo no catálogo.
5. **Salve** em `<projeto>/criativo/lote-N.md` e atualize `<projeto>/criativo/controle-criativos.md` (modelo abaixo).
6. **Execução das imagens:** por padrão, entregue os prompts para o Paulo gerar no ChatGPT (1 prompt por conversa, anexando foto e logo). Só gere por API (skill `higgsfield-generate`) se ele pedir.
7. **Depois do teste:** quando ele trouxer os números, marque campeões e cortados no controle. Campeão ganha versão 9:16 (mesmo prompt, trocando o formato e subindo o texto para longe das bordas) e 3 variações no lote seguinte.

## Ângulos de narrativa

| Ângulo | O que faz | Modelos que combinam |
|---|---|---|
| Identificação | A persona se vê na dor ("Seu serviço é bom. Falta o bairro saber que você existe.") | A1, B4 |
| Revelação | Mostra o que ela não via (onde está o cliente, o real problema) | B1, A2 |
| Contra-crença / inimigo | Derruba o que ela acha que funciona ("Postar todo dia não traz cliente novo") | B2, C1 |
| Mecanismo / segredo | Nomeia a solução ("O segredo é o Raio de Clientes Ativos") | A6, B1 |
| Promessa direta | A headline da página, sem enfeite | A3 |
| Facilidade | Prova que é simples ("Anúncio pronto + R$ 10 por dia = cliente no WhatsApp") | A5, A3 |
| Preço / objeção de custo | Compara com algo do dia a dia | B3 |
| Contraste | Dois lados ("por que o do lado tem fila?") | B5 |
| Autoridade | Frase do especialista, aprovada por ele | A2, A4 |
| Notícia real | Fato verificado e recente ligado à dor | B6 |
| Tendência / previsão | Opinião do especialista sobre o mercado | C2 |
| Objeção ("sem X") | Tira o "será que eu consigo?" (sem aparecer, sem computador) | C1, A1 |
| Contra-crença B2B (sem imagem) | Derruba crença do nicho profissional em formato limpo, sem foto, estilo card/blog | D1 |
| Contra-crença com anotação | Vira a crença com um traço desenhado à mão sobre a palavra-chave, reforçada por checklist | E1 |
| Resultado projetado (serviço) | Cenário ilustrativo de contratos/clientes em X dias, para oferta de prestação de serviço B2B | F1 |

## Formato de cada criativo no lote

```
### [Código] · [Nome curto] ([tese], ângulo [ângulo], modelo [modelo])

Texto da arte: [linhas exatas, com o destaque marcado]

Anexar: [foto do especialista + logo] ou [só logo]

(prompt em bloco de código)

- Texto principal: [3 a 6 frases: gancho igual à arte, dor, mecanismo/solução, o que recebe, "Toque em Saiba mais."]
- Título: [até 40 caracteres]
- Descrição: [até 30 caracteres]
```

## Controle de criativos (`criativo/controle-criativos.md`)

```
| Código | Lote | Tese | Ângulo | Modelo | Texto da arte (resumo) | Status | CTR | CPC | Vendas | Observação |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | 1 | Vitrine invisível | Identificação | A1 frase lateral | Falta o bairro saber que você existe | testando | | | | |
```
Status: rascunho, aprovado, testando, campeão, cortado. Antes de cada lote novo, leia o controle e não repita combinação ângulo × modelo que já foi cortada.

## Regras (valem para toda arte e todo texto)

- **Política do Meta:** nada que afirme atributo pessoal ("Você está endividado?"), nada de promessa de renda ou faturamento, nada de antes e depois de corpo.
- **Nada de prova inventada.** Nunca criar print de conversa, depoimento, resultado de cliente, número de vendas ou de alunos. Celular com conversas só como ilustração do produto em uso: nomes genéricos, perguntas de interesse ("Quanto custa?", "Tem horário?") e nunca resultado ("vendi R$ X"), com "Imagem ilustrativa" escrito na arte.
- **Notícia só se for real:** fato verificado, com fonte e data anotadas no lote. Número exato da fonte.
- **Citação só se for aprovada** por quem assina.
- **Sem logo real** de WhatsApp, Instagram, Google ou banco: ícone genérico.
- **Texto da arte curto:** manchete com até 12 palavras, no máximo 3 blocos de texto além do logo.
- **Destaque obrigatório:** cada arte tem 1 ou 2 palavras em cor de destaque e negrito (amarelo na linha A, caixa vermelha na linha B).
- **Fidelidade facial uma vez só**, no fim do prompt. Âncora leve no meio. Repetir faz a IA ignorar o rosto.
- **Elementos integrados à cena:** objeto segurado pela pessoa ou apoiado na mesa, com a mesma luz e sombra. Não pedir nada que não esteja na arte aprovada.
- **Sem travessão (—)** em nenhum texto.
- **Congruência:** a promessa do criativo e a da primeira dobra da página são iguais.
- **Formato padrão:** 4:5 (1080x1350). Campeões ganham 9:16.
