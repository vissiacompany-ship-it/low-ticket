# Catálogo de modelos visuais

Cada modelo tem: quando usar, como a arte é montada, a referência em `referencias/` e o esqueleto do prompt. Os textos entre colchetes saem da oferta. Os prompts são em inglês e os textos da arte em português, entre aspas, exatamente como devem aparecer.

## Peças fixas de todo prompt

**Abertura (sempre):**
```
Vertical social media ad creative, 4:5 (1080x1350), Brazilian infoproduct style.
```

**Âncora leve de rosto (só quando tem o especialista, dentro do bloco Subject):**
```
Facial features accurately matched from the provided reference image. Hairstyle, hair texture, hair length, and hair color accurately matched from the provided reference image. [He/She] wears [roupa da foto de referência], exactly like the reference photo.
```

**Fechamento de estilo (sempre):**
```
Style: [clean/dramatic/editorial], high-contrast, premium Brazilian infoproduct ad, generous spacing, sharp legible text, exact Brazilian Portuguese with accents. No other text, no real brand logos besides the attached one.
```

**Cláusula forte de fidelidade (só com especialista, UMA vez, sempre a última coisa do prompt):**
```
Use exclusively and strictly the attached reference image as the single source of truth for the subject's face. Reproduce the face exactly as provided, preserving all facial proportions, bone structure, facial geometry, nose, lips, eyes, jawline, skin texture and asymmetries. Do not beautify, do not modify, do not stylize, do not replace facial features. The output must depict the same real human face, photorealistic, with identity fidelity at maximum level.
```

**Logo:** `the attached "[nome]" logo in white, used exactly as provided` (posição: rodapé central pequeno, canto superior ou grande no meio, conforme o modelo).

**Caixas de chamada:**
- Linha A: caixa branca arredondada com texto azul-marinho (nome do produto ou detalhe) + caixa só com contorno branco fino e texto branco "CLIQUE EM SAIBA MAIS".
- Linha B: caixa arredondada amarela (#FFD43B) com texto preto, ou vermelha (#E11D2E) com texto branco: "Clique em SAIBA MAIS e [benefício em até 12 palavras]."

---

## LINHA A: Especialista em degradê

Base: fundo em degradê da cor da marca com granulado leve e brilho atrás da pessoa, especialista recortado, tipografia branca grande, destaque em amarelo (ou cor de destaque da marca), caixa branca e logo.

### A1 · Frase lateral
- **Quando:** identificação, tese principal, dor dita com elegância.
- **Montagem:** pessoa do peito para cima de um lado; do outro, frase de 3 ou 4 linhas, condensada, com 1 palavra destacada; embaixo, caixa branca com o nome do produto + "CLIQUE EM SAIBA MAIS"; logo no rodapé.
- **Ref:** `A-frase-lateral_cura-da-alma.jpg`, `A-frase-lateral_anuncio-pronto.jpg`
```
Background: smooth vibrant gradient from [cor 1] at the top to [cor 2] at the bottom, very subtle film grain, soft light glow behind the subject.
Subject: [descrição], shown from the chest up on the [left] half of the frame, slightly turned toward the text, [expressão], looking at the camera. [âncora leve]. Soft studio light, gentle rim light.
Text ([right] side, top, white, bold condensed sans-serif, [left]-aligned):
"[linha 1]" / "[linha 2 com a palavra X em amarelo (#FFD43B)]" / "[linha 3]".
Lower half, centered: a rounded white box with dark navy bold text "[NOME DO PRODUTO OU PROMESSA CURTA]" and right below it a rounded box with only a thin white outline and white text "CLIQUE EM SAIBA MAIS".
Bottom center, small: [logo].
[estilo] [fidelidade]
```

### A2 · Citação assinada
- **Quando:** autoridade, revelação, frase de efeito do especialista. A frase precisa ser aprovada por quem assina.
- **Montagem:** pessoa no alto, aspas grandes, frase em itálico, assinatura com o nome (sem traço antes), logo grande, botão contornado.
- **Ref:** `A-citacao_cura-da-alma.jpg`, `A-citacao_anuncio-pronto.jpg`
```
Background: gradient from a light lavender-grey at the very top fading into [cor 1] and [cor 2] at the bottom, subtle grain.
Subject: [descrição], cut out from the chest up in the upper-left area, calm and confident. [âncora leve].
Middle: a quote block in white italic medium-weight text with a large opening quotation mark: "[citação]" and below, smaller, the signature "[Nome]" (no dash before the name).
Optional headline above the quote, bold, with one word in yellow: "[headline curta]".
Lower area: [logo] large and centered, and below it a rounded box with a thin white outline and white text "CLIQUE EM SAIBA MAIS".
[estilo editorial] [fidelidade]
```

### A3 · Palavra gigante
- **Quando:** promessa direta, igual à headline da página. A palavra é o verbo da promessa (COPIE, BAIXE, ENTENDA, ACESSE).
- **Montagem:** pessoa no alto ao centro; 1 palavra enorme amarela condensada sobrepondo a roupa; frase que completa a promessa em branco com o fim em amarelo; caixa branca com o detalhe de facilidade.
- **Ref:** `A-palavra-gigante_cura-da-alma.jpg`, `A-palavra-gigante_anuncio-pronto.jpg`
```
Subject: [descrição], cut out from the chest up, centered in the upper half. [âncora leve].
Text over the lower half, centered:
- One giant word in bright yellow (#FFD43B), extra bold condensed font, very large, slightly overlapping the bottom of [his/her] clothes: "[VERBO]"
- Below it, white bold text: "[resto da promessa]" with "[final]" in yellow.
- Below, a rounded white box with navy text "[FACILIDADE + PRAZO]".
Top left corner, small: [logo].
[estilo bold] [fidelidade]
```

### A4 · Frase com barra
- **Quando:** crença, frase de virada, provocação curta. Bom para marca pessoal.
- **Montagem:** pessoa no centro; frase curta à direita em condensada branca com 2 palavras amarelas e uma barra vertical fina ao lado; assinatura; nome do produto grande sobre o peito; caixa com data ou detalhe.
- **Ref:** `A-frase-barra_cura-da-alma.jpg`
```
Text (top right, white, heavy condensed sans-serif, right-aligned, with a thin vertical white bar on its right side): "[linha 1]" / "[linha 2 com X em amarelo]" / "[linha 3]", and below, small yellow "[Nome]".
Center, over the subject's chest: [logo] large in white.
Bottom: rounded white box with navy text "[detalhe]" + outline box "CLIQUE EM SAIBA MAIS".
```

### A5 · Equação com celular
- **Quando:** facilidade, mostrar que é simples (produto + pouco esforço = resultado).
- **Montagem:** pessoa segurando o celular e apontando para a tela; equação em 4 linhas ("[produto]" / "+ [esforço pequeno]" / "= [resultado]" / "[onde]"); caixa branca "TUDO PRONTO, SÓ COPIAR E COLAR".
- **Ref:** `A-equacao-celular_anuncio-pronto.jpg`
```
Subject: [descrição], cut out from the waist up on the right side, smiling, holding a modern smartphone in [his/her] left hand turning the screen toward the camera, right hand pointing at it. [âncora leve]. The phone screen, sharp and visible, shows [tela do produto em uso, ilustrativa]. The phone is lit by the same studio light as the hand and clothes.
Text (left side): "[produto]" (yellow) / "+ [esforço]" (white) / "= [resultado]" (white) / "[onde]" (yellow).
Bottom: rounded white box "[FACILIDADE]" and the logo small.
```

### A6 · Segredo do mecanismo
- **Quando:** sofisticação alta, revelar o mecanismo pelo nome ("O segredo não é X. É o [Mecanismo].").
- **Montagem:** manchete em 2 linhas no topo com o nome do mecanismo em amarelo; pessoa apontando para um celular grande em primeiro plano mostrando o produto em uso; selo verde "+N [algo]"; caixa branca explicando o mecanismo; "Imagem ilustrativa" pequeno no canto.
- **Ref:** `A-segredo-mecanismo_anuncio-pronto.jpg`
```
Text (top, centered): "O segredo não é [crença comum]." / "É o [Mecanismo]." with "[Mecanismo]" in yellow.
Main element: a large smartphone in the right half, in the foreground, held by [his/her] hand so it is physically connected and lit by the same light, screen showing [produto em uso, ilustrativo, sem valor de venda].
Bottom: rounded white box "[mecanismo em 1 frase]" + outline box "CLIQUE EM SAIBA MAIS". Bottom left corner, very small white text: "Imagem ilustrativa".
```

---

## LINHA B: Manchete com cena fotográfica

Base: cena fotográfica realista e dramática ocupando a arte; manchete branca grande no topo com palavra em caixa vermelha (#E11D2E) ou em vermelho; frase de apoio; caixa amarela ou vermelha "Clique em SAIBA MAIS e..."; logo pequeno no rodapé.

```
Vertical social media ad creative, 4:5 (1080x1350), bold Brazilian news-style ad.
Scene: ultra-realistic [cena], cinematic contrast, [luz]. [elementos físicos integrados à cena com a mesma luz e sombra].
Text (top, centered, white, heavy bold sans-serif): "[linha 1]" / "[linha 2]" with "[palavra]" inside a red (#E11D2E) highlight box.
Below the headline, smaller white bold text: "[apoio]".
Bottom: a rounded yellow (#FFD43B) box with black text "Clique em SAIBA MAIS e [benefício]." Under it, small, [logo].
Style: dramatic, high-contrast, attention-grabbing feed ad, sharp legible text, exact Brazilian Portuguese with accents. No other text, no real brand logos besides the attached one.
```

### B1 · Cena do mecanismo
- **Quando:** revelação, tornar visível o mecanismo (raio no bairro, pasta abrindo, linha do tempo).
- **Ref:** `B-cena-mecanismo_anuncio-pronto.jpg`

### B2 · Inimigo / erro comum
- **Quando:** contra-crença, indignação ("O botão impulsionar queimou seus R$ 50"). Mostra o erro que a persona comete, sem culpar a pessoa.
- **Ref:** `B-inimigo_anuncio-pronto.jpg`

### B3 · Preço comparado
- **Quando:** objeção de custo, ancoragem ("R$ 10 POR DIA: menos que uma marmita"). Comparar com algo do dia a dia da persona.
- **Ref:** `B-preco-comparacao_anuncio-pronto.jpg`

### B4 · Persona na dor
- **Quando:** identificação ("Pare de postar só para os amigos"). Pessoa parecida com o avatar, no ambiente dela, vivendo a dor.
- **Ref:** `B-persona-dor_anuncio-pronto.jpg`

### B5 · Contraste lado a lado
- **Quando:** "por que o do lado tem fila?". Duas situações na mesma cena.

### B6 · Notícia real (newsjacking)
- **Quando:** um fato real e recente conversa com a dor ("A Bolsa já caiu 4,3%...", "O Estreito de Ormuz fechou").
- **Regra dura:** só fato verificado em fonte confiável, com data, número exato e link anotado no arquivo. Sem fato real, não existe esse criativo. Nada de bandeira real de forma ofensiva nem tragédia explorada.
- **Montagem:** manchete do fato com o número em vermelho, cena dramática do tema, pergunta "E o seu [dinheiro/negócio]? Está protegido ou exposto?", caixa "Clique em SAIBA MAIS e, em menos de 1 hora, [benefício]."
- **Ref:** `B-noticia_bolsa-1.jpg`, `B-noticia_bolsa-2.jpg`, `B-noticia_bolsa-3.jpg`, `B-noticia_ormuz.jpg`

---

## LINHA C: Alerta em fundo escuro tech

Base: fundo escuro com gráfico/linhas neon (rosa, azul, vermelho), tipografia condensada branca com palavras em caixas coloridas (verde = positivo, vermelho = negativo), ícone de alerta 3D, chips com ✕ vermelho para objeções.

### C1 · Alerta com objeções
- **Quando:** contra-crença forte, quebrar uma promessa velha do mercado ("Liberdade financeira não vem comprando cursos ultrapassados").
- **Montagem:** ícone ⚠ 3D vermelho no topo; manchete em caixa alta com 1 palavra verde e 1 vermelha sublinhada; frase "Você só precisa [ação fácil] para [resultado] sem [esforço]" com destaques; 2 chips "✕ Não precisa de [objeção]".
- **Ref:** `C-alerta-e-previsao_erl.jpg` (peças 3 e 4)

### C2 · Previsão / tendência com especialista
- **Quando:** urgência de mercado com opinião do especialista ("O tráfego pago vai ficar mais caro em 2026 e quem souber X vai dominar"). Sempre como opinião, nunca como fato inventado.
- **Montagem:** especialista pensativo (mão no queixo), gráfico em queda atrás, frase com 2 destaques em caixa (vermelha e verde), caixa amarela "Clique em Saiba Mais e [benefício]".
- **Ref:** `C-alerta-e-previsao_erl.jpg` (peças 1 e 2)

---

## LINHA D: Cartão de texto (sem cena, sem foto)

Base: fundo liso claro (branco ou cinza muito claro), sem especialista e sem cena, só tipografia. Manchete preta grande com 1 palavra em caixa vermelha ou texto vermelho; parágrafo de apoio em 2 a 3 frases (pergunta + virada); frase final em negrito; CTA no estilo link sublinhado azul, como texto clicável, sem caixa de botão.

### D1 · Manchete com palavra vermelha e CTA link
- **Quando:** público de nicho profissional/B2B (gestão, direito, saúde) que desconfia de anúncio "gritado". Funciona pela limpeza visual, lê como um post de blog ou card de citação, não como propaganda.
- **Montagem:** manchete em 3 a 4 linhas, preta, com 1 palavra em vermelho (#E11D2E ou similar) dando o contraste da virada; abaixo, parágrafo de apoio com uma pergunta e a resposta que reposiciona a crença; frase final em negrito reforçando a solução; CTA como texto sublinhado azul "Cadastre-se no [nome da oferta]."
- **Ref:** `D-cartao-texto_acelerador-empresarial.png`
```
Vertical social media ad creative, 4:5 (1080x1350), clean minimal text-card style, no photo, no illustration, flat light background (#FFFFFF or very light grey).
Text (top, left-aligned, heavy bold sans-serif, dark near-black): "[linha 1]" / "[linha 2 com a palavra X em vermelho (#E11D2E)]" / "[linha 3]" / "[linha 4]".
Below, a shorter paragraph in regular weight dark grey text, 2 to 3 lines: "[pergunta de apoio]" / "[virada em 1 frase]".
Below that, bold dark text, 1 line: "[frase que nomeia a solução]."
Below, blue underlined link-style text (not a button, just styled like a hyperlink): "Cadastre-se no [nome da oferta]."
Style: minimal, editorial, generous white space, sharp legible text, exact Brazilian Portuguese with accents. No other text, no real brand logos besides the attached one.
```

---

## LINHA E: Cena com destaque manual e checklist

Base: cena fotográfica realista de fundo (ambiente do nicho, sem especialista em pé), manchete branca grande sobreposta com 1 palavra marcada à mão (círculo ou sublinhado vermelho tipo caneta), parágrafo curto de apoio, checklist com ✅ verde, CTA discreta no rodapé com setas/emoji e sem caixa.

### E1 · Palavra circulada à mão + checklist
- **Quando:** contra-crença sobre liderança/gestão/equipe, quando o traço "desenhado à mão" dá um ar de anotação pessoal, menos vendedor que a caixa vermelha da linha B.
- **Montagem:** cena de fundo escurecida (ambiente do nicho) com overlay escuro para legibilidade; manchete em 3 linhas brancas bold, 1 palavra com um círculo vermelho desenhado à mão por cima (estilo caneta/marcador); parágrafo de apoio de 1 a 2 frases; checklist de 3 itens com ✅ verde; CTA pequena no rodapé "[verbo] os detalhes" com emoji de seta para baixo.
- **Ref:** `E-circulada-checklist_gestao-time.png`
```
Vertical social media ad creative, 4:5 (1080x1350), cinematic realistic scene ad with dark overlay for text legibility.
Scene: ultra-realistic [ambiente do nicho], moody low-key lighting, slightly out of focus background so the text stays readable.
Text (centered, white, heavy bold sans-serif, upper-middle area): "[linha 1]" / "[linha 2 com a palavra X]" / "[linha 3]", with a hand-drawn red circle (marker/pen style, slightly imperfect) around the word "[X]" in line 2.
Below, smaller regular-weight white text, 2 lines: "[frase de apoio com a virada]".
Below, a checklist with 3 lines, each starting with a green checkmark emoji: "✅ [benefício 1]" / "✅ [benefício 2]" / "✅ [benefício 3]".
Bottom, small, centered: "👇 [verbo] os detalhes 👇".
Style: cinematic, high-contrast, premium feed ad, sharp legible text, exact Brazilian Portuguese with accents. No other text, no real brand logos besides the attached one.
```

---

## LINHA F: Resultado projetado com funil (B2B serviço)

Base: cena fotográfica escura do nicho profissional, manchete em caixa vermelha translúcida no topo com o resultado numérico ("N [resultado] EM X DIAS PARA [PROFISSÃO]!"), aviso "CENÁRIO ILUSTRATIVO" obrigatório, checklist de métricas em caixa vermelha, chamada para o funil/vídeo com ícone de play, frase que remove objeção de curso/mentoria, CTA de agendamento.

### F1 · Funil com cenário ilustrativo
- **Quando:** oferta de serviço (não curso) para prestador de serviço B2B (advogado, contador, corretor, dentista), quando o ângulo é projeção de resultado com transparência sobre ser ilustrativo, não promessa de faturamento real. Linha que soma com a política do Meta: numera cenário, não resultado garantido.
- **Montagem:** manchete vermelha translúcida no topo com o número do resultado no formato "[N] [RESULTADO] EM [X] DIAS PARA [PROFISSÃO]!"; logo abaixo, em caixa vermelha: "CENÁRIO ILUSTRATIVO para [PROFISSÃO]:" seguido de 1 linha de contexto e um checklist com ✅ branco de 2 a 3 métricas (quantidade, valor unitário, total); segunda caixa vermelha com a chamada de ação "[Agende/Conheça] uma reunião de 20 minutos..." ; frase "Não é curso. Não é mentoria. É prestação de serviço: você contrata e nossa equipe executa a implementação."; rodapé com ícone de play vermelho + "Funil no Youtube" + "Conteúdo para prestadores de serviços".
- **Regra dura:** sempre escrever "CENÁRIO ILUSTRATIVO", nunca indicar que é resultado garantido ou real de cliente. Números são exemplo de cálculo, não promessa de faturamento.
- **Ref:** `F-funil-resultado_advogado-tributario.png`, `F-funil-resultado_contador.png`
```
Vertical social media ad creative, 4:5 (1080x1350), bold Brazilian B2B service ad, dark cinematic scene.
Scene: ultra-realistic [ambiente da profissão, ex: escritório de advocacia com livros de direito / mesa de contabilidade com planilhas], dramatic low-key lighting, dark overlay for text legibility.
Text (top, centered, inside a semi-transparent red (#E11D2E) box, white heavy bold): "[N] [RESULTADO] EM [X] DIAS PARA [PROFISSÃO]!"
Below, inside a solid red (#E11D2E) box, white text: "CENÁRIO ILUSTRATIVO para [PROFISSÃO]:" then "[contexto da conta]" then a checklist with white checkmarks: "✅ [N] [resultado] no período" / "✅ R$[valor] por [unidade]" / "✅ R$[total] em [métrica final]".
Below, bold white text, centered: "Conheça o funil de 3 vídeos no Youtube."
Below, inside a second red (#E11D2E) box: bold white text "[Agende/Conheça] uma [reunião/conversa] de 20 minutos e veja como [implementamos/instalamos] isso na sua operação." then, smaller, "Não é curso. Não é mentoria. É prestação de serviço: você contrata e nossa equipe executa a implementação."
Bottom, small, left-aligned: a red play button icon, "Funil no Youtube" and below it, smaller, "Conteúdo para prestadores de serviços".
Style: dramatic, high-contrast, B2B service ad, sharp legible text, exact Brazilian Portuguese with accents. No other text, no real brand logos besides the attached one.
```
