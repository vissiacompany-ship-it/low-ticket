# Copy da página (modelo v2): [Nome do produto]

Campos iguais aos do `pagina.json` do modelo v2 (`lt-pagina/modelos/pagina.v2.exemplo.json`). Exemplo de referência em cada campo: Instravel.
Marcação: `[[destaque]]` (limão no topo, degradê com brilho nos títulos), `{{destaque simples}}` (cor quente sem brilho), `**negrito**`, `|` quebra de linha. Campos `_pc` = versão do computador (se não tiver, vale a do celular). Sem travessão.

## faixa
- faixa_emoji: [emoji do nicho] (✈️)
- faixa: Exclusivo para quem [identidade do avatar] (Exclusivo para quem ama viajar)

## hero
- titulo (celular, 3 linhas): [Verbo do resultado] [[resultado]] e|[...] [[objeto]]|em menos de [[tempo]]
  (Poste [[fotos lindas]] e|criativas [[da sua viagem]]|em menos de [[15 segundos]])
- titulo_pc (2 linhas): (Poste [[fotos lindas]] e criativas [[da sua viagem]]|em menos de [[15 segundos]])
- sub (2 linhas): [[Produto pronto]] para cada [momento]|[...]. [Verbo], [verbo] e [verbo].
  ([[Modelos prontos]] para cada momento|da viagem. Tire a foto, escolha e poste.)
- sub_pc: ([[Modelos prontos]] para cada momento da sua viagem.|É só tirar a foto, escolher o modelo, baixar e postar.)
- botao: QUERO [RESULTADO DA HEADLINE] ↓ (QUERO POSTAR FOTOS LINDAS ↓)
- imagens: vitrine (10 itens do produto, 9:16), faixa_rolante (10 outros), fundo (mundo do nicho)

## depoimentos (só retornos reais: prints e textos de Google, direct, WhatsApp)
- nota: valor (5,0) · linha1 (+[N] avaliações, da marca como um todo) · linha2 (O [produto] queridinho de quem {{[identidade]}} [emoji])
- titulo: Veja [o resultado] de|{{quem já está usando!}} [emoji]
- titulo_pc: Veja [o resultado] de {{quem já está usando!}} [emoji]
- prints: [5 prints de uso real]
- comentarios: [nome] / [quando] / [texto real], um por objeção (matriz do playbook, seção 5)

## categorias (momentos do avatar)
- etiqueta: Tudo em um só [formato] [emoji]
- titulo: [[+N [itens]]] [adjetivos], [adjetivos] [emoji]
- titulo_pc: [[+N [itens]]] [adjetivos],|[adjetivos] [emoji]
- sub: Tudo que você precisa para [resultado] em cada [momento] está dentro do [produto].
- itens (6 a 8): [emoji] [momento] + vídeo de tela curto (otimizar_video.py)
- fecho: {{Nunca mais [dor]}} [complemento da dor]. [emoji]

## passos
- etiqueta: Como funciona
- titulo: Veja como é simples [resultado] em [[tempo]]
- linha: Veja como é fácil usar o [produto] 👇
- video: embed (Panda/YouTube) ou mp4 do vídeo de tela (roteiro: `lt-video-demo`)
- itens (3 ou 4, até 3 palavras): ícone (smartphone, grid, camera, download, mensagem, editar, enviar, play, estrela, check, arquivo, coracao) + título
- botao: QUERO ACESSAR [O PRODUTO] AGORA [emoji] (desce para os bônus)

## bonus (3, pela jornada de uso: antes, durante, depois)
- etiqueta: E não para por aí...
- titulo (celular, 3 linhas): Além do [produto],|você ainda recebe|[[3 bônus exclusivos]] 🎁
- titulo_pc: Além do [produto], você ainda recebe|[[3 bônus exclusivos]] 🎁
- itens: rotulo (Bônus N) / titulo / texto (1 a 2 frases) / imagem (prompts-imagens-lt.md)

## transicao
Você está a um passo de [[resultado]] para [momento futuro]. [emoji]

## oferta
- parabens: 🎉 Parabéns!!! Você ganhou [N]% OFF
- cronometro_minutos: 15 (ao zerar, nada muda)
- mockup / logo / pagamentos_img (imagem das bandeiras)
- bonus_linha: +3 bônus exclusivos
- de: [âncora] / avista: [preço] / parcelas: [N]x / parcela: [valor] / economia: R$[de menos à vista]
- botao: QUERO [RESULTADO DA HEADLINE] [emoji] (igual ao do topo, sem a seta)
- checks: Pagamento único / Sem mensalidade / Acesso imediato (só o que for verdade)
- alerta: Promoção exclusiva nesta página.|Se fechar, o valor será R$ [de].

## garantia
- selo (imagem) · titulo: GARANTIA DE · titulo_destaque: [N] DIAS
- texto: Teste o [produto] por [N] dias, [o que conhecer] e veja como é fácil [resultado]. Se achar que não é para você, é só solicitar o reembolso dentro do prazo e receber 100% do seu dinheiro de volta. [emoji]

## autor (fatos reais, 1ª pessoa)
- titulo: Oie, eu sou a [[Nome!]] 🤍
- cargo: Criadora do [produto] [emoji]
- paragrafos (5): quem sou ligada ao nicho · o que percebi (**dor em negrito**) · como surgiu · o que é (**lista em negrito**) · para quem é + **certeza**
- foto: real

## faq (6 a 8)
- etiqueta: Ainda tem dúvidas? · titulo: Perguntas frequentes
- itens: acesso · já vem pronto? · [objeção do bônus 1] · celular? · Android/iOS? · mensalidade? · tempo de acesso · garantia

## whatsapp (opcional, decisão por oferta)
- numero / titulo: Ficou com alguma dúvida? / botao

## rodape
- logo / marca / empresa / cnpj (real) / politica / termos
