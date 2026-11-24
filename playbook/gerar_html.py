"""Gera PLAYBOOK-LOW-TICKET.html: o playbook em páginas (formato do Playbook Visual).
Os textos completos ficam nos .md desta pasta (playbook-pagina-lt, playbook-checkout-lt, prompts-imagens-lt).
Os prompts são lidos de prompts-imagens-lt.md, então editar lá e rodar de novo: python3 gerar_html.py"""
import re, html, pathlib

AQUI = pathlib.Path(__file__).parent
VERSAO = "versão 1 · 04/11/2026"
paginas = []


def pg(secao, titulo, corpo, sub=""):
    paginas.append((secao, titulo, sub, corpo))


def ul(itens):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in itens) + "</ul>"


def eb(t):
    return f'<div class="eb">{t}</div>'


def tabela(cab, linhas, cls=""):
    h = "".join(f"<th>{c}</th>" for c in cab)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in linhas)
    return f'<table class="{cls}"><tr>{h}</tr>{b}</table>'


def img(src, cap="", w=None, cls="shot"):
    st = f' style="width:{w}"' if w else ""
    c = f'<div class="cap">{cap}</div>' if cap else ""
    return f'<figure class="{cls}"{st}><img src="img/{src}" loading="lazy">{c}</figure>'


def g2(a, b, prop="1fr 1fr"):
    return f'<div class="g2" style="grid-template-columns:{prop}"><div>{a}</div><div>{b}</div></div>'


def cards(itens, cols=3):
    return f'<div class="cards c{cols}">' + "".join(
        f'<div class="card"><div class="n">{n}</div><div class="t">{t}</div><p>{d}</p></div>' for n, t, d in itens) + "</div>"


# ---------------- PARTE 1 · PÁGINA ----------------
S = "Página de vendas"

pg(S, "A página em uma tela",
   g2(eb("A lógica") + '<p class="lead">Uma descida só: <b>mostra o produto, prova, mostra por dentro, mostra usando, dá mais, pede.</b> Na primeira tela já aparecem 10 modelos do produto.</p>'
      + '<p class="note">Clique em qualquer tela abaixo para ampliar.</p>',
      tabela(["#", "Seção", "Função", "#", "Seção", "Função"], [
          ["1", "Topo", "Para quem é e qual resultado", "7", "Transição", "Se ver com o resultado antes do preço"],
          ["2", "Vitrine", "Mostra o produto antes de explicar", "8", "Oferta", "Preço pequeno, ação única"],
          ["3", "Depoimentos", "Gente como eu já usa", "9", "Garantia", "Tira o risco"],
          ["4", "Tudo em um só app", "Volume e “tem para todo momento”", "10", "Autoridade", "Quem fez e por quê"],
          ["5", "Como funciona", "Prova que é fácil, com vídeo real", "11", "FAQ", "Responde o que ainda trava"],
          ["6", "Bônus", "Tira as últimas objeções de uso", "12", "Rodapé", "Dados legais"]], "mini"),
      "0.7fr 1.6fr")
   + '<div class="strip">' + "".join(f'<img src="img/cel-{i:02d}.jpg" loading="lazy">' for i in range(0, 14)) + '</div><div class="cap">A página inteira no celular, de cima para baixo.</div>')

pg(S, "1 · Topo",
   g2(img("cel-00.jpg", "Celular (390 px)", cls="shot tall"),
      eb("Copy") + '<div class="quote"><small>✈️ EXCLUSIVO PARA QUEM AMA VIAJAR</small><br><b>Poste <em>fotos lindas</em> e criativas <em>da sua viagem</em> em menos de <em>15 segundos</em></b><br><span>Modelos prontos para cada momento da viagem. Tire a foto, escolha e poste.</span></div>'
      + eb("Por que funciona") + ul([
          "A faixa nomeia uma <b>identidade</b> (“quem ama viajar”), não uma profissão. A pessoa se reconhece antes de ler.",
          "O verbo da headline já é o resultado: <b>Poste</b>. Nada de “acesse” ou “baixe”.",
          "Especificidade pelo <b>tempo</b> (15 s). O número de volume (+100) vai para depois.",
          "O produto (“modelos prontos”) fica na sub, que termina em <b>3 verbos de uso</b>.",
          "Sem logo no topo: a marca aparece só na oferta e no rodapé."])
      + eb("Fórmula para adaptar") + '<p class="formula">[Verbo do resultado] [resultado desejado] em [tempo curto].<br>[Produto pronto] para cada [momento do avatar]. [Verbo], [verbo] e [verbo].</p>',
      "0.8fr 1.4fr"))

pg(S, "A promessa nos 4 pilares da Kamila",
   cards([
       ("1", "Facilidade", "“Poste” · “Modelos prontos” · “Tire a foto, escolha e poste”"),
       ("2", "Especificidade", "“em menos de 15 segundos” (prazo). Volume (+100) fica na seção 4"),
       ("3", "Consumo rápido", "Modelos prontos dentro de um app. Nada de curso, aula ou método"),
       ("4", "Desejo", "“fotos lindas e criativas da sua viagem”: ser vista bonita, registrar a viagem"),
       ("+", "Baixo esforço", "Implícito nos 15 segundos e nos 3 verbos. Sem precisar escrever “sem”"),
       ("✓", "Palavras proibidas", "Nenhuma: sem aprenda, descubra, método, estratégia, curso")], 3)
   + eb("Evolução em relação às páginas antigas")
   + tabela(["", "50 Viral Fit (antiga)", "Instravel (nova)"], [
       ["Faixa", "🔥 Exclusivo para nutricionistas e personal trainers", "✈️ Exclusivo para quem ama viajar"],
       ["Headline", "Acesse 50 modelos prontos de Reels virais para ganhar seguidores e vender mais consultorias online (17 palavras)", "Poste fotos lindas e criativas da sua viagem em menos de 15 segundos (12 palavras)"],
       ["Verbo", "de acesso", "de resultado"],
       ["Produto", "na headline", "na sub"],
       ["Especificidade", "volume (50)", "tempo (15 s)"]]))

pg(S, "2 · Vitrine e 3 · Depoimentos",
   g2(img("cel-01.jpg", "Nota, título e carrossel de Stories de clientes", cls="shot tall"),
      eb("Vitrine (logo abaixo da headline)") + ul([
          "Carrossel 3D em leque com 10 modelos, passando sozinho a cada 1 s.",
          "Botão “QUERO POSTAR FOTOS LINDAS ↓” travado 5 s, depois pulsa.",
          "Faixa rolante com mais 10 capas. <b>Prova de produto antes da prova social.</b>"])
      + eb("Depoimentos") + ul([
          "5,0 com ramos dourados · +1.795 avaliações · ⭐⭐⭐⭐⭐ · “O app queridinho de quem <em>ama viajar</em>”.",
          "Título fala de <b>fotos</b>, não de opiniões: “Veja as fotos de <em>quem já está usando!</em>”.",
          "Carrossel 3D <b>simétrico</b> com prints de Stories das clientes: o do meio de frente, os outros saindo iguais para a esquerda e para a direita.",
          "Trilho de 15 comentários em cartão (inicial colorida, nome, estrelas, tempo), passando a cada 3,5 s."])
      + eb("Regras da prova social (Paulo, 04/11)") + ul([
          "Nota pode vir das avaliações da marca como um todo.",
          "Comentário em texto (sem foto/@) a partir de retorno real: Google, direct, WhatsApp.",
          "Prints de uso sempre: Stories, carrossel, Instagram, WhatsApp.",
          "Não escrever depoimento do zero."]),
      "0.8fr 1.4fr"))

pg(S, "Depoimentos: por que cada um existe",
   '<p class="lead">Os 15 comentários são uma <b>matriz de objeções</b>: cada um responde uma dúvida ou abre um público. Use como roteiro para pedir depoimentos aos compradores.</p>'
   + tabela(["Quem", "Objeção ou ideia", "Quem", "Objeção ou ideia"], [
       ["Juliana", "Não sei tirar foto → perguntaram quem editou", "Vanessa", "Não sei montar story → é só trocar as fotos"],
       ["Camila", "Não tenho viagem marcada → usei no fim de semana", "Aline", "Vai ficar igual ao de todo mundo → fica com a minha cara"],
       ["Rafaela", "Prova da promessa: 40 min → 15 s", "Fernanda", "Comprei no impulso e não me arrependi"],
       ["Bruna", "Postei todo dia, cara profissional", "Marina", "Vergonha das fotos → ganhei confiança"],
       ["Patrícia", "Valor: melhor investimento do ano", "Débora", "Ocasião especial (lua de mel) + rapidez"],
       ["Larissa", "Variedade: praia, cidade, hotel, comidinha", "Gustavo", "Sem paciência pra editar · viagem a trabalho"],
       ["Thiago", "Abre o público masculino", "Isabela", "Indicação + post com mais curtidas do ano"],
       ["", "", "Sophia", "Ainda não viajei → usei com fotos antigas"]])
   + '<p class="note">Também variam: destinos reconhecíveis (Porto de Galinhas, Gramado, Maceió, Búzios, Chile), datas espaçadas (3 dias a 2 meses) e um ou dois homens.</p>')

pg(S, "4 · Tudo em um só app",
   g2(img("cel-03.jpg", "8 categorias em vídeo, 2 colunas no celular", cls="shot tall"),
      eb("Copy") + '<div class="quote"><small>TUDO EM UM SÓ APP ✈️</small><br><b><em>+100 modelos de fotos</em> lindas, criativos e personalizáveis 📷</b><br><span>Tudo que você precisa para postar cada momento da sua viagem está dentro do app.</span></div>'
      + eb("O que tem") + ul([
          "8 vídeos de tela, mudos e em loop, um por <b>momento da viagem</b>: Partiu & Mala · Aeroporto & Avião · Hotel & Piscina · Praia & Mar · Passeios & Lugares · Comidas & Drinks · Natureza & Pôr do Sol · Lifestyle & Colagens.",
          "Fecho com a dor: “<em>Nunca mais perca tempo da sua viagem</em> pensando no que postar ou criando post do zero. 😩”"])
      + eb("A ideia que mais vale copiar") + '<p class="formula">Organizar o produto pelos <b>momentos da vida do avatar</b>, não por tipo de arquivo. A pessoa pensa “estou no aeroporto”, não “preciso de um story”.</p>',
      "0.8fr 1.4fr"))

pg(S, "5 · Como funciona",
   g2(img("cel-05.jpg", "Vídeo vertical de tela", cls="shot tall") ,
      eb("Copy") + '<div class="quote"><small>COMO FUNCIONA</small><br><b>Veja como é simples postar uma foto linda em <em>menos de 15 segundos</em></b><br><span>Veja como é fácil usar o app 👇</span></div>'
      + eb("4 passos de até 3 palavras") + '<div class="steps"><span>01 Acesse o app</span>→<span>02 Escolha o modelo</span>→<span>03 Coloque sua foto</span>→<span>04 Baixe e poste</span></div>'
      + eb("Por que assim") + ul([
          "O título repete a promessa da headline. A seção existe para <b>provar o “15 segundos”</b>.",
          "Vídeo é gravação de tela real (não animação): mostra o produto de verdade.",
          "4 passos porque o uso tem 4. Use o número real, sempre curto.",
          "No celular: título, vídeo, ícones, botão. No computador: vídeo à direita.",
          "Botão ciano “QUERO ACESSAR O APP AGORA ✈️ ↓” desce para os bônus."]),
      "0.8fr 1.4fr"))

pg(S, "O vídeo de tela: estrutura",
   g2(img("video-quadros.jpg", "28 quadros do vídeo (70 s, 9:16)", cls="shot"),
      tabela(["Bloco", "Tempo", "O que fala e mostra"], [
          ["1 Facilidade", "0-5 s", "“É só entrar aqui e escolher o modelo.” Já dentro do app"],
          ["2 Organização", "5-12 s", "Momentos e categorias, com retângulo vermelho"],
          ["3 Escolha", "12-21 s", "Abre o modelo e mostra a inspiração de foto (bônus 1)"],
          ["4 Personalizar", "21-40 s", "Vai ao Canva, troca a foto, muda texto e cor"],
          ["5 Resultado", "40-46 s", "Baixa e posta no Story"],
          ["6 Fecho", "46 s", "“Viu como é simples?”"],
          ["7 CTA", "47-70 s", "Botão aqui embaixo · e-mail com link · tutorial (bônus 3) · botão de novo"]], "mini")
      + eb("Edição") + ul([
          "Tela do celular em moldura de iPhone sobre o fundo do tema. Sem rosto.",
          "Legenda palavra por palavra, branca com palavra-chave em ciano.",
          "Retângulo vermelho, mãozinha clicando, seta vermelha. Cortes secos."]),
      "1fr 1.15fr"))

pg(S, "O vídeo de tela: roteiro para gravar",
   g2(eb("Roteiro em branco") + '<pre class="prompt">[0-5 s]   E para usar o [produto] é muito simples: é só [ação 1] e escolher [o item].\n[5-12 s]  Dentro do [produto] você encontra [itens] para cada [momento do avatar], organizados por [categoria].\n[12-21 s] Depois de escolher, é só clicar e você já vê [diferencial / bônus 1].\n[21-40 s] Aí é só [ação 2] e [ação 3]. Com poucos cliques você [personaliza].\n[40-46 s] Quando terminar, é só [ação final] e [resultado].\n[46 s]    Viu como é simples?\n[47-70 s] Para liberar seu acesso, é só clicar no botão aqui embaixo.\n          Você recebe [como chega] e ainda [bônus 3].\n          Então aproveita e clica no botão aqui embaixo.</pre>',
      eb("Quando usar cada vídeo") + tabela(["Vídeo", "Quando"], [
          ["Gravação de tela (este)", "Produto já existe e tem interface: app, área de membros, Canva, planilha. Dá mais confiança"],
          ["Animação de 3 passos (lt-video-passos)", "Produto sem interface boa para mostrar, ou para anúncio"]])
      + eb("O vídeo faz duas coisas") + ul(["Vende a facilidade (mostra o uso).", "Responde “como eu recebo?” (e-mail, link, tutorial) antes do FAQ."]),
      "1.3fr 1fr"))

pg(S, "6 · Bônus: pela jornada de uso",
   '<div class="g3">' + img("bonus-1-instatravel.jpg", "<b>Bônus 1 · Inspirações de Fotos</b><br>Antes: “e se eu não souber que foto tirar?”")
   + img("bonus-2-instatravel.jpg", "<b>Bônus 2 · Posts para o Feed</b><br>Depois: “e se eu quiser postar no feed?”")
   + img("bonus-3-instatravel.jpg", "<b>Bônus 3 · Tutorial Passo a Passo</b><br>Durante: “e se eu não souber mexer?”") + "</div>"
   + g2(eb("Por que esses três") + ul([
       "Cada bônus responde uma pergunta de um momento diferente do uso: <b>antes, durante e depois</b>.",
       "O Bônus 1 é a objeção mais forte e aparece de novo no FAQ, com a mesma resposta.",
       "Nomes concretos, consumo rápido. Nada de “super bônus imensurável”."]),
      eb("Copy e layout") + ul([
          "Etiqueta “E NÃO PARA POR AÍ...” · título “Além do app, você ainda recebe <em>3 bônus exclusivos</em> 🎁”.",
          "Celular: imagem de 112 px à esquerda e texto à direita (3 bônus em uma tela).",
          "Computador: 3 colunas, texto em cima, imagem embaixo.",
          "Botão flutuante de 5 s leva à oferta."])))

pg(S, "7 · Transição e 8 · Oferta",
   g2(img("cel-08.jpg", "Cartão da oferta no celular", cls="shot tall"),
      eb("Transição (faixa azul-marinho)") + '<div class="quote"><b>Você está a um passo de ter <em>fotos lindas e criativas</em> para cada momento da sua próxima viagem. ✈️</b></div>'
      + '<p class="note">É o “Imagine...” resumido em uma frase. A faixa escura avisa: agora vem o preço.</p>'
      + eb("Oferta, na ordem") + ul([
          "🎉 Parabéns!!! Você ganhou 54% OFF (estoura com confete: recompensa antes do preço).",
          "Cabeçalho vermelho: Oferta por tempo limitado · cronômetro 15 min · Válida somente até o tempo acabar.",
          "Mockup + logo + “+3 bônus exclusivos” + <s>De R$ 147</s>.",
          "por apenas 12x de <b>R$ 6,73</b> (gigante, dançando) · ou R$ 67 à vista · Você economiza R$ 80.",
          "Botão verde: QUERO POSTAR FOTOS LINDAS ✈️ (o mesmo texto do topo).",
          "Bandeiras · Pagamento único | Sem mensalidade | Acesso imediato · alerta “Se fechar, o valor será R$ 147”."])
      + eb("Preço") + '<p class="formula">Âncora única e plausível (2,2x). Sem lista “Recapitulando”. R$ 67 é o preço depois de validar (tabela da Kamila: R$ 37 → R$ 67).</p>',
      "0.8fr 1.4fr"))

pg(S, "9 · Garantia e 10 · Autoridade",
   g2('<div class="g2" style="grid-template-columns:1fr 1fr;gap:14px">' + img("cel-09.jpg", "Garantia", cls="shot half") + img("cel-10.jpg", "Autoridade", cls="shot half") + '</div>',
      eb("Garantia") + ul(["Selo 7 dias · “Teste o app por 7 dias, conheça todos os modelos e veja como é fácil...”",
                           "Saiu o “Se apenas 1 X gerar 1 Y, o investimento já se paga”: serve para nicho profissional. Em consumo, a garantia fala de experimentar."])
      + eb("Autoridade em 5 parágrafos") + tabela(["#", "O quê", "Instravel"], [
          ["1", "Quem sou, ligada ao nicho", "Apaixonada por viagens, conhecendo o Nordeste"],
          ["2", "O que percebi (a dor, em negrito)", "Perder tempo pensando no que postar em vez de aproveitar"],
          ["3", "Como surgiu", "Entre viagens, fotos e muitos perrengues 😂"],
          ["4", "O que é (em negrito)", "Stories, posts e carrosséis prontos + inspirações"],
          ["5", "Para quem é + certeza", "“Tenho certeza de que você vai amar”"]], "mini")
      + '<p class="note">Autoridade por <b>vivência</b> (ela é o avatar), não por currículo. Em nicho profissional, “Não é teoria” e anos de mercado continuam valendo.</p>',
      "1fr 1.4fr"))

pg(S, "11 · Perguntas frequentes",
   g2(tabela(["Pergunta", "Objeção que mata"], [
       ["Como recebo acesso ao app?", "Vou receber mesmo? Como?"],
       ["Os modelos já vêm prontos?", "Vou ter trabalho?"],
       ["E se eu não souber que foto tirar?", "A mais forte (repete o Bônus 1)"],
       ["Posso acessar pelo celular?", "Preciso de computador?"],
       ["Funciona em Android e iOS?", "Técnica, com humor: “não ocupa espaço... você vai precisar dele para as fotos 😂”"],
       ["Tem mensalidade?", "Medo de cobrança recorrente"],
       ["Por quanto tempo terei acesso?", "1 ano: a informação “ruim” fica aqui, dita de forma neutra"],
       ["O produto tem garantia?", "Risco"]]),
      img("cel-12.jpg", "Abre uma de cada vez", cls="shot tall")
      + '<p class="note">Sem bloco de WhatsApp. Rodapé: logo, ©, empresa, CNPJ, links e o aviso legal do Facebook.</p>',
      "1.5fr 0.7fr"))

pg(S, "Os 6 argumentos de prova",
   '<p class="lead">A página prova a mesma promessa seis vezes, de seis jeitos. Nenhum é “confie em mim”.</p>'
   + cards([
       ("1", "Produto na tela", "Vitrine 3D e faixa rolante. Prova “é bonito” sem dizer nada."),
       ("2", "Uso real", "Prints de Stories de clientes. “Fica bonito com foto de gente comum.”"),
       ("3", "Volume organizado", "8 categorias em vídeo. “Tem para todo momento.”"),
       ("4", "Demonstração", "Vídeo de tela de 70 s. Prova o “15 segundos”."),
       ("5", "Vivência", "A criadora passou pelo mesmo problema."),
       ("6", "Risco zero", "Garantia de 7 dias.")], 3)
   + '<p class="formula">Antes de escrever, liste como provar a promessa em cada um dos 6. Em produto digital, 1, 3 e 4 sempre dá para fazer, mesmo sem nenhum cliente. A página mostra, mas não entrega o produto.</p>')

pg(S, "Design: o tema do nicho vira o design",
   g2(img("pc-topo.jpg", "Topo no computador: céu, avião, coral e limão", cls="shot"),
      eb("Cores por papel") + '<div class="sw">' + "".join(
          f'<div><i style="background:{c}"></i><b>{n}</b><span>{u}</span></div>' for c, n, u in [
              ("#2C5F9E", "Céu (foto)", "Topo e oferta"), ("linear-gradient(#fff,#EAF6FD)", "Leitura", "Seções"),
              ("#12294F", "Marinho", "Transição e rodapé"), ("#2D609F", "Texto", "Nunca preto"),
              ("#FFF3A6", "Limão", "Destaque sobre foto"), ("#FF7043", "Coral", "Destaque sobre claro"),
              ("#28C9E6", "Ciano", "Botão do meio"), ("#4CAF50", "Verde", "Só o de compra"),
              ("#DC2626", "Vermelho", "Urgência"), ("#A8E6FF", "Azul-bebê", "Faixa, bordas")]) + "</div>"
      + eb("Para adaptar") + '<p class="formula">Escolha a <b>imagem-mundo do nicho</b> (cozinha, academia, igreja, escritório): ela é o fundo do topo, da oferta e do checkout. Emoji do nicho em todo título. Divisória com a textura do tema (aqui, nuvens).</p>',
      "1.2fr 1fr"))

pg(S, "Design: tipografia, espaços e celular",
   g2(eb("Uma fonte só: Poppins 400 a 800") + tabela(["Elemento", "Celular", "Computador"], [
       ["Headline", "~21 px (5,5 vw), peso 600", "30 a 40 px"],
       ["Sub", "~13 px, peso 500", "15 a 19 px"],
       ["Título de seção", "~22 px, peso 700", "28 a 40 px"],
       ["Etiqueta", "11 px, caixa alta, espaçada", "igual"],
       ["Texto", "14 a 15 px", "15 a 16 px"],
       ["Comentário", "13,5 px", "igual"],
       ["Parcela", "48 px", "60 px"],
       ["Pergunta FAQ", "18 px", "igual"]], "mini"),
      eb("Espaços e formas") + ul([
          "Seção: 48 px (celular) e 64 px (computador) em cima e embaixo; 24 px nas laterais.",
          "Oferta: coluna estreita (448 px) até no computador.",
          "Cartão: canto 24 px, borda azul-bebê fina, sombra azulada.",
          "Botão: pílula, caixa alta, reflexo de vidro na metade de cima."])
      + eb("Celular primeiro") + ul([
          "Quebras de linha escolhidas à mão, uma versão para celular e outra para computador. Nunca sobra palavra solta.",
          "Mesmo texto nos dois (regra da Vissia). Só muda quebra, tamanho e ordem.",
          "Abre rápido: seções carregam ao chegar perto, vídeos só a 300 px, imagens em 2 larguras."])))


# ---------------- IDENTIDADE VISUAL ----------------
S = "Identidade visual"

def hero(v, faixa, h, sub, btn):
    return (f'<div class="dh" style="--q:{v["q"]};--qd:{v["qd"]};--lm:{v["lm"]};--sky:{v["sky"]}">'
            f'<div class="dfx">{faixa}</div><div class="dh1">{h}</div><div class="dsub">{sub}</div>'
            f'<div class="dbtn">{btn}</div></div>')

pg(S, "A estrutura é fixa, a marca ocupa os lugares",
   '<p class="lead">Cada cor, peso e tamanho da página tem uma <b>função</b>. Trocar de especialista é trocar <b>quem ocupa cada função</b>, nunca a função. Por isso qualquer marca cabe nesta página sem quebrar a metodologia.</p>'
   + cards([
       ("1", "Hierarquia", "O que é grande, grosso, fino e pequeno. Fixa: vem da metodologia."),
       ("2", "Destaques", "2 ou 3 trechos por título, peso 800 + cor. A cor muda conforme o fundo."),
       ("3", "Cores com significado", "A marca pinta a conversa. Verde e vermelho pintam o dinheiro."),
       ("4", "Preço", "A parcela é o maior número da página depois da headline."),
       ("5", "Botões", "Quente da marca para descer, verde para pagar."),
       ("6", "Mundo do nicho", "Uma imagem do universo do avatar no topo, na oferta, nos bônus e no checkout.")], 3)
   + '<p class="formula">Processo completo na página “Encaixar a identidade de qualquer especialista”. Texto detalhado: playbook-pagina-lt.md, seção 6A.</p>')

pg(S, "Hierarquia de texto: grosso, fino, grande, pequeno",
   g2('<div class="demo">'
      + hero({"q": "#FF7043", "qd": "#F4511E", "lm": "#FFF3A6", "sky": "linear-gradient(180deg,#1E7FD8,#45B4EE)"},
             "✈️ EXCLUSIVO PARA QUEM AMA VIAJAR", 'Poste <b>fotos lindas</b> e criativas <b>da sua viagem</b> em menos de <b>15 segundos</b>',
             '<b>Modelos prontos</b> para cada momento da viagem.', "QUERO POSTAR FOTOS LINDAS ↓")
      + '<div class="dlight"><span class="deb">E NÃO PARA POR AÍ...</span><div class="dh2">Além do app, você ainda recebe <b>3 bônus exclusivos</b> 🎁</div>'
      + '<div class="dh2 fino">Oie, eu sou a <b>Kamila!</b> 🤍</div><div class="dh2 fino up">GARANTIA DE <i>7 DIAS</i></div>'
      + '<p class="dp">Depois de tantas viagens, percebi uma coisa: <b>a última coisa que a gente quer é perder tempo pensando no que postar.</b></p></div></div>'
      + '<div class="cap">Réplica com as mesmas fontes, pesos e cores da página.</div>',
      tabela(["Nível", "Peso", "Por quê"], [
          ["Headline", "600, destaques 800", "O olho lê primeiro só os destaques: resultado, objeto, tempo"],
          ["Sub", "500, menor", "Explica, não compete"],
          ["Título de venda", "700, destaque 800", "Seções que vendem: grosso"],
          ["Título de conversa", "<b>400 fino</b>, nome/número 800", "Tom de pessoa falando; o contraste fino + grosso aponta o nome ou o número"],
          ["Etiqueta", "600, caixa alta, 11 px", "Dá para escanear a página só pelas etiquetas"],
          ["Texto corrido", "400, 14-15 px", "Negrito só na frase-chave"]], "mini")
      + eb("Regras de destaque") + ul([
          "2 ou 3 trechos por título: <b>resultado</b>, <b>público/objeto</b>, <b>número/tempo</b>. Nunca a frase inteira.",
          "Destaque = peso 800 + cor. Sem itálico, sem sublinhado.",
          "Sobre foto: cor clara e quente (limão). Sobre claro: cor quente forte (coral). Na seção de uso: a cor do botão dela (ciano).",
          "Um emoji do nicho fecha o título."]),
      "1fr 1.1fr"))

pg(S, "Cores com significado",
   g2(eb("Da marca (muda a cada especialista)") + '<div class="sw">' + "".join(
          f'<div><i style="background:{c}"></i><b>{n}</b><span>{u}</span></div>' for c, n, u in [
              ("url(img/pc-topo.jpg) center/cover", "Mundo do nicho", "Topo, oferta, bônus, checkout"),
              ("#2D609F", "Escura", "Texto e títulos (nunca preto)"),
              ("#FF7043", "Quente / primária", "Destaques no claro, botões de descer"),
              ("#FFF3A6", "Destaque sobre foto", "Headline e sub"),
              ("#28C9E6", "Secundária", "Seção de uso"),
              ("#A8E6FF", "Clara da secundária", "Faixa, etiquetas, bordas"),
              ("linear-gradient(#fff,#EAF6FD)", "Fundo de leitura", "Seções"),
              ("#12294F", "Mais escura", "Transição e rodapé")]) + "</div>",
      eb("Fixas (metodologia, não mudam)") + '<div class="sw">' + "".join(
          f'<div><i style="background:{c}"></i><b>{n}</b><span>{u}</span></div>' for c, n, u in [
              ("#10B981", "Verde: dinheiro e ganho", "Parabéns, +3 bônus, parcela, economia, compra"),
              ("#DC2626", "Vermelho: perda e urgência", "Cronômetro, preço riscado, alerta"),
              ("#F97316", "Laranja: checks", "Pagamento único, sem mensalidade")]) + "</div>"
      + '<p class="formula"><b>A marca pinta a conversa. Verde e vermelho pintam o dinheiro.</b><br>Verde = o que a pessoa ganha. Vermelho = o que ela perde. É assim que o cérebro lê preço em qualquer nicho.</p>'
      + eb("No gerador (pagina.json)") + tabela(["Campo", "Papel"], [
          ["primaria", "Quente da marca"], ["destaque", "Destaque sobre foto"], ["acento", "Secundária"],
          ["escura", "Texto e pausa"], ["fundo", "Fundo de leitura"], ["sucesso", "Verde (fixo)"], ["alerta", "Vermelho (fixo)"], ["laranja", "Checks"]], "mini")))

pg(S, "Anatomia do preço",
   g2('<div class="demo"><div class="doffer"><div class="dpill">🎉 Parabéns!!! Você ganhou 54% OFF</div><div class="dcard">'
      '<div class="dred"><small>OFERTA POR TEMPO LIMITADO</small><b>⏱ 00 : 14 : 59</b><span>Válida somente até o tempo acabar.</span></div>'
      '<div class="dbody"><div class="drow"><img src="img/mockup-oferta-instatravel.jpg"><div><div class="dlogo">Instravel</div><div class="dg">+3 bônus exclusivos</div><s>De R$ 147,00</s></div></div>'
      '<div class="dsm">por apenas 12x de</div><div class="dprice">R$ 6,73</div><div class="dsm">ou R$ 67,00 à vista</div>'
      '<div class="deco">Você economiza R$80 levando agora</div><div class="dbuy">QUERO POSTAR FOTOS LINDAS ✈️</div>'
      '<div class="dchk"><span>✓ Pagamento único</span><span>✓ Sem mensalidade</span><span>✓ Acesso imediato</span></div>'
      '<div class="dalert">⚠ Promoção exclusiva nesta página.<br>Se fechar, o valor será R$ 147,00.</div></div></div></div></div>',
      tabela(["Elemento", "Tamanho e peso", "Cor", "Função"], [
          ["Parabéns", "14 px, 600", "Verde (pílula)", "Recompensa antes do preço"],
          ["Faixa do tempo", "10 px caixa alta + 24-30 px", "Vermelho", "Urgência"],
          ["+3 bônus", "14-16 px, 600", "Verde", "Ganho"],
          ["De R$ 147", "14 px, riscado", "Vermelho", "O que não vai pagar"],
          ["por apenas 12x de", "12 px", "Cinza", "Passagem, quase some"],
          ["<b>R$ 6,73</b>", "<b>48 / 60 px, 700</b>", "<b>Verde</b>", "Maior elemento do cartão, dançando"],
          ["à vista", "14 px", "Cinza", "Honesto, sem destaque"],
          ["Economia", "12 px, 600", "Verde, borda tracejada", "Ganho em forma de cupom"],
          ["Botão", "16-18 px, 700", "Verde, largura toda", "A única ação"],
          ["Checks e alerta", "13 px", "Laranja / vermelho", "Tira medo / lembra a perda"]], "mini")
      + '<p class="formula">A parcela é o maior número da página depois da headline. A âncora é pequena e riscada. O à vista aparece, mas pequeno.</p>',
      "0.85fr 1.2fr"))

pg(S, "Botões, bônus e cartões",
   g2('<div class="demo dlight2"><div class="dbtns"><span class="b1">QUERO POSTAR FOTOS LINDAS ↓</span><span class="b2">QUERO ACESSAR O APP AGORA ✈️ ↓</span>'
      '<span class="b3">QUERO POSTAR FOTOS LINDAS ✈️</span><span class="b4">⌄</span></div>'
      '<div class="dbonus"><img src="img/bonus-1-instatravel.jpg"><div><span class="dtag">BÔNUS 1</span><b>Inspirações de Fotos</b><p>Cada modelo de Story acompanha um direcionamento de como tirar as melhores fotos.</p></div></div>'
      '<div class="dchips"><span class="deb">COMO FUNCIONA</span><span class="dchip">🏖️ Praia &amp; Mar</span><span class="dchip">🍹 Comidas &amp; Drinks</span></div></div>',
      tabela(["Botão", "Cor", "Uso"], [
          ["Avançar", "Degradê da quente da marca", "Topo e flutuantes: descem a página"],
          ["Meio", "Secundária da marca", "Como funciona"],
          ["Compra", "<b>Verde</b>, largura toda, halo", "Só o do checkout"],
          ["Flutuante", "Quente da marca, círculo 56 px", "Canto, só em depoimentos e bônus"]], "mini")
      + eb("Forma") + ul(["Pílula, caixa alta, 700, sombra no texto, reflexo de vidro na metade de cima.", "Sobem e descem a cada 2,2 s; o verde pulsa com halo."])
      + eb("Bônus e cartões") + ul([
          "Etiqueta quente “BÔNUS N” (presente) + título 16/24 px peso 800 + descrição 12/14 px.",
          "Imagem do bônus sobre o mundo do nicho: os três parecem da mesma família.",
          "Cartão branco, canto 24 px, borda fina na clara da marca, sombra puxada para a escura.",
          "Divisória entre seções com a textura do nicho (nuvens, farinha, folhas, luz)."]),
      "1fr 1.1fr"))

pg(S, "Encaixar a identidade de qualquer especialista",
   g2('<ol class="ol big">' + "".join(f"<li>{x}</li>" for x in [
       "<b>Pegue a identidade aprovada</b> (/identidade ou Playbook Visual do cliente). Sem ela, rode /identidade antes. O Instravel é estrutura, não identidade.",
       "<b>Preencha os 8 papéis da marca</b> (página “Cores com significado”). Faltou cor? Derive: clara da secundária para linhas, escuríssima da primária para texto e pausa.",
       "<b>Escolha a imagem-mundo do nicho</b> e a textura da divisória.",
       "<b>Fonte:</b> uma sem serifa com pesos 400 a 800 (Poppins, Plus Jakarta Sans, Montserrat, DM Sans). Serifada da marca só no nome da especialista.",
       "<b>Mantenha fixos:</b> escala de tamanhos, verde do dinheiro, vermelho da urgência, 2 ou 3 destaques por título.",
       "<b>Escolha o emoji assinatura</b> do nicho.",
       "<b>Confira contraste</b> em 390 px: destaque sobre foto legível, texto nunca preto, verde legível no branco.",
       "<b>Registre no pagina.json</b> (primaria, destaque, acento, escura, fundo; sucesso e alerta fixos)."]) + "</ol>",
      eb("Exemplo de encaixe") + tabela(["Papel", "Viagem", "Confeitaria", "Fé"], [
          ["Mundo do nicho", "Céu", "Bancada de mármore", "Céu ao amanhecer"],
          ["Escura", "Azul", "Marrom chocolate", "Azul-marinho"],
          ["Quente", "Coral", "Rosa framboesa", "Dourado"],
          ["Destaque sobre foto", "Limão", "Creme", "Branco quente"],
          ["Secundária", "Ciano", "Verde-menta", "Azul-céu"],
          ["Verde / vermelho", "Fixos", "Fixos", "Fixos"]], "mini")
      + '<p class="note">Os exemplos de confeitaria e fé mostram só o encaixe das cores. Não são ofertas aprovadas.</p>',
      "1.2fr 1fr"))

pg(S, "Mesma estrutura, outra identidade",
   '<p class="lead">O mesmo topo com três identidades. Mudam o mundo do nicho, a cor quente, o destaque e o emoji. Não mudam o tamanho, o peso, o lugar dos destaques e a forma do botão.</p>'
   + '<div class="g3 demo">'
   + hero({"q": "#FF7043", "qd": "#F4511E", "lm": "#FFF3A6", "sky": "linear-gradient(180deg,#1E7FD8,#45B4EE)"},
          "✈️ EXCLUSIVO PARA QUEM AMA VIAJAR", 'Poste <b>fotos lindas</b> e criativas <b>da sua viagem</b> em menos de <b>15 segundos</b>', '<b>Modelos prontos</b> para cada momento da viagem.', "QUERO POSTAR FOTOS LINDAS ↓")
   + hero({"q": "#E0457B", "qd": "#C2185B", "lm": "#FFE8C7", "sky": "linear-gradient(180deg,#5B3A29,#9C6B4E)"},
          "🧁 EXCLUSIVO PARA QUEM VENDE DOCES", 'Venda <b>bolos e doces</b> no WhatsApp com <b>fotos de vitrine</b> em <b>10 minutos</b>', '<b>Modelos prontos</b> para cada tipo de doce.', "QUERO VENDER MAIS DOCES ↓")
   + hero({"q": "#D4A537", "qd": "#B8860B", "lm": "#FFF6E0", "sky": "linear-gradient(180deg,#14284B,#3E6FB0)"},
          "🙏 EXCLUSIVO PARA MULHERES DE FÉ", 'Poste <b>stories cheios de fé</b> <b>todos os dias</b> em menos de <b>15 segundos</b>', '<b>Stories prontos</b> com versículos para cada dia.', "QUERO POSTAR COM FÉ ↓")
   + '</div><div class="cap">Viagem é o Instravel. Confeitaria e fé são exemplos de encaixe (frases ilustrativas, não ofertas aprovadas).</div>')


pg("Identidade visual", "Réplica fiel: o checklist (pontos do Paulo)",
   '<p class="lead">Quando a página segue uma referência, <b>o design dela é a regra</b>. Antes de mostrar: comparar_referencia.py (lado a lado, celular e computador) e este checklist.</p>'
   + '<div class="ficha">' + "".join(f"<div><b>☐</b>{x}</div>" for x in [
       "Mesma fonte, pesos e tamanhos em cada nível", "Quebras de linha iguais, versão celular e computador",
       "Destaques com o mesmo efeito (limão com sombra, degradê com brilho, coral simples)", "Etiquetas em pílula azul-clara",
       "Sem linhas que a referência não tem (topo esmaece em branco)", "Carrossel 3D sem sombra nem borda, simétrico, largura toda, movimento em mola", "Cartões inteiros sem corte reto e sem espaço extra até o botão",
       "Botão do topo do tamanho do texto, com espaço certo, sem contagem de 5 s", "Nota 5,0 com ramos dourados", "Depoimentos em pilha de profundidade, infinita dos dois lados",
       "Os 8 vídeos de categoria, grade 2/4", "Como funciona: etiqueta no alto, ícones de linha em caixas grandes",
       "Bônus: cartões estreitos, título 24 px, texto fino", "Oferta: mockup à esquerda, logo e bônus à direita",
       "Parcela dançando, cupom tracejado, bandeiras em imagem", "Alerta vermelho-claro com borda (não verde)",
       "Cronômetro zerado: nada muda", "Garantia em fundo claro, título fino, selo do produto",
       "Autoridade com foto redonda ao lado", "FAQ com etiqueta, rodapé com logo"]) + "</div>")

S = "Página de vendas"
pg(S, "Animações: tudo que se mexe",
   tabela(["Onde", "O que acontece", "Tempo"], [
       ["Todas as seções", "Título e blocos sobem 20 px e aparecem, uma vez só", "0,5 s · cascata 0,05 a 0,15 s"],
       ["Vitrine", "Carrossel 3D em leque, os de lado girados 8 a 12° e menores", "passa a cada 1 s, dá para arrastar"],
       ["Vitrine", "Faixa de capas correndo, bordas esmaecidas", "40 s por volta"],
       ["Botão do topo", "Travado com “5s, 4s...” e barra enchendo, depois libera", "5 s"],
       ["Botões coral e ciano", "Sobem 10 px e voltam; brilho passa por dentro", "2,2 s"],
       ["Comentários", "Trilho passando, pausa no mouse", "3,5 s"],
       ["Botão flutuante", "Só durante depoimentos e bônus; conta 5 s e vira seta", "2,2 s"],
       ["Categorias", "8 vídeos mudos em loop", "contínuo"],
       ["Como funciona", "Ícones um por um, depois as setas", "0,15 s entre eles"],
       ["Oferta", "Pílula “Parabéns” estoura e brilha; 26 confetes caem", "0,65 s · 1,8 s"],
       ["Oferta", "Parcela dança (cresce 12%, gira 2°)", "1,6 s"],
       ["Oferta", "Botão verde pulsa com halo verde", "1,8 s"],
       ["FAQ", "Abre e fecha, uma de cada vez", "0,2 s"]])
   + '<p class="note">O botão travado 5 s da página dela foi tirado no nosso modelo (decisão do Paulo, 04/11).</p>')

pg(S, "Botões (CTAs)",
   tabela(["#", "Texto", "Onde", "Leva para", "Cor"], [
       ["1", "QUERO POSTAR FOTOS LINDAS ↓", "Abaixo da vitrine", "Depoimentos", "Coral, travado 5 s"],
       ["2", "(seta flutuante)", "Durante os depoimentos", "Categorias", "Coral, 5 s"],
       ["3", "QUERO ACESSAR O APP AGORA ✈️ ↓", "Depois dos passos", "Bônus", "Ciano"],
       ["4", "(seta flutuante)", "Durante os bônus", "Oferta", "Coral, 5 s"],
       ["5", "QUERO POSTAR FOTOS LINDAS ✈️", "Cartão da oferta", "<b>Checkout</b>", "Verde"]])
   + cards([
       ("1", "Só um vai ao checkout", "Todos os outros descem a página. Ninguém pula a prova."),
       ("2", "QUERO + resultado", "1ª pessoa, com o desejo da headline. O primeiro e o último são iguais."),
       ("3", "Cor por função", "Coral desce, verde paga. A pessoa aprende sem perceber.")], 3))

pg(S, "Decisões por oferta (todas as páginas são validadas)",
   '<p class="lead">A 13S é a mesma em todas as páginas da Kamila. Onde elas diferem, <b>é uma decisão conforme a oferta</b>, não erro. Escolha uma opção em cada linha.</p>'
   + tabela(["Ponto", "Opção A", "Opção B", "Quando"], [
       ["Impacto visual", "Vitrine 3D do produto (Instravel)", "Pessoa + celulares (50 Viral Fit) ou mockup", "A: produto bonito de ver. B: produto é o resultado da pessoa"],
       ["Prova social", "Prints + nota + comentários", "Prints de uso · demonstração · passo a passo cedo + autoridade", "Conforme a prova que existe hoje"],
       ["Ordem 3 e 4", "Entregáveis antes do passo a passo", "Passo a passo antes", "A: vende pela variedade. B: dúvida é “consigo usar?”"],
       ["Vídeo", "Gravação de tela com narração", "Animação de 3 passos", "A: produto com interface. B: sem interface ou anúncio"],
       ["Entregáveis", "Categorias em vídeo", "Galeria com cadeado + “+N”", "A: muitos usos. B: biblioteca única"],
       ["Resultado imaginado", "Frase de transição", "Bloco “Imagine...”", "A: página curta. B: transformação grande"],
       ["Ancoragem", "Âncora única", "“Recapitulando” com total", "A: produto simples. B: muitos itens de valor"],
       ["Garantia", "Tom de experimentar", "+ “Se 1 X gerar 1 Y...”", "A: consumo. B: nicho profissional"],
       ["Autoridade", "Por vivência", "Por experiência (“Não é teoria”)", "Conforme a história real"],
       ["Suporte", "Sem WhatsApp", "Com “Ficou com alguma dúvida?”", "Decisão do Paulo por oferta"],
       ["Urgência", "Cronômetro por visitante", "Data real", "Os dois valem"]], "mini"))

pg(S, "O que cada página ensina",
   g2(tabela(["Página", "O que ela tem de melhor"], [
       ["<b>Instravel</b>", "Acabamento visual, vitrine no topo, categorias por momento, vídeo de tela, bônus pela jornada, cor por função do botão, checkout com 2 bumps + combo"],
       ["50 Viral Fit", "Faixa por profissão, galeria com cadeado, “Recapitulando”, garantia com “Se 1 X gerar 1 Y”"],
       ["50 Carrossel Fit", "Demonstração com exemplos antes da prova, comentários com @"],
       ["App Stories Bíblicos", "“Como é por dentro” para app (base do código do Instravel)"],
       ["Ativa FIT", "Funciona sem depoimento nenhum"]]),
      eb("Pilares da promessa") + '<p class="lead">Todas passam nos 4 pilares + baixo esforço. A forma de headline do Instravel (verbo de resultado + tempo, produto na sub) pode ser usada em qualquer oferta.</p>'
      + '<p class="formula">O playbook é da <b>metodologia</b>, com todas as páginas como referência. O Instravel é o exemplo principal porque é o mais bem acabado, não porque as outras estejam erradas.</p>'))

pg(S, "Velocidade: nota 95 e abrir em até 2 segundos",
   g2(eb("A regra") + '<p class="lead"><b>95 ou mais no PageSpeed do Google, no celular e no computador. Abrir em até 2 s. Sem perder qualidade de imagem.</b> Página lenta faz a pessoa fechar antes de carregar, o pixel não registra a visita e o connect rate cai.</p>'
      + tabela(["Métrica", "Meta"], [["Nota", "95+"], ["LCP (maior elemento da 1ª tela)", "até 2,0 s"], ["FCP (primeira coisa)", "até 1,2 s"], ["TBT (celular travado)", "até 150 ms"], ["CLS (página pulando)", "até 0,05"], ["Peso da 1ª tela", "~300 KB"]], "mini")
      + eb("Onde estamos (04/11, medição local)") + tabela(["Página", "Celular", "PC"], [["Instravel (React)", "36", "60"], ["Anúncio Pronto", "35 a 62", "95"], ["Meu Roteiro (nosso gerador)", "78", "92"]], "mini")
      + '<p class="note">A Kamila é referência de oferta, copy e design, não de técnica.</p>',
      eb("Como chegar lá sem perder qualidade") + '<ol class="ol">' + "".join(f"<li>{x}</li>" for x in [
          "<b>HTML puro</b>, sem React/Lovable.",
          "<b>Primeira tela leve:</b> imagem do topo com prioridade alta; o resto carrega ao chegar perto.",
          "<b>Imagens WebP/AVIF qualidade 80-85</b> em 2 ou 3 tamanhos (360, 560, 828 px), com largura e altura declaradas.",
          "<b>Uma fonte</b>, 3-4 pesos, arquivo próprio, headline carregada primeiro.",
          "<b>Animações em CSS</b>, pausadas fora da tela.",
          "<b>Pixel, UTMify e Clarity</b> carregam depois da página aparecer.",
          "<b>Vídeos</b> só perto de aparecer, com capa leve; até ~1,5 MB.",
          "<b>CSS dentro da página.</b>",
          "<b>Vercel</b>: servidor perto, compressão, cache.",
          "<b>Medir antes de publicar</b>: medir_velocidade.py (3 rodadas) ou pagespeed.web.dev."]) + "</ol>"))

pg(S, "Ficha para adaptar a uma oferta nova",
   '<div class="ficha">' + "".join(f"<div><b>{i}</b>{t}</div>" for i, t in enumerate([
       "Faixa: EXCLUSIVO PARA QUEM ___", "Promessa: [verbo do resultado] ___ em [tempo] ___",
       "Sub: [produto pronto] para cada [momento]. [verbo], [verbo] e [verbo]", "Vitrine: 10 itens do produto (teaser se for PDF)",
       "Prova real disponível: prints / textos de retorno / nada ainda", "Momentos do avatar: 6 a 8 categorias com emoji e vídeo de tela",
       "Número de volume: +___ [itens]", "Dor do fecho: “Nunca mais ___”", "Passos de uso: 3 ou 4, até 3 palavras",
       "Vídeo de tela: roteiro em branco", "3 bônus: antes ___ / durante ___ / depois ___",
       "Transição: “Você está a um passo de ___ para ___.”", "Preço: à vista, parcelas, âncora única (~2,5x), economia",
       "Urgência: cronômetro 15 min (ao zerar, nada muda) ou data real", "Garantia no tom do produto",
       "Autoridade: quem sou, o que percebi, como surgiu, o que é, para quem é", "FAQ: 6 a 8, repetindo a objeção do bônus 1",
       "Imagem-mundo do nicho, emoji, cor de destaque", "Botão: QUERO [resultado da headline]"], 1)) + "</div>")

# ---------------- PARTE 2 · CHECKOUT ----------------
S = "Checkout"

pg(S, "O checkout em uma tela",
   g2(img("checkout.jpg", "Checkout do Instravel (OnProfit)", cls="shot tall"),
      eb("De cima para baixo") + tabela(["Elemento", "Função"], [
          ["Faixa vermelha: cronômetro 10 min + “URGENTE!”", "Pressa (a oferta é daquela visita)"],
          ["Banner “ÚLTIMO PASSO”", "Lembra a promessa e diz o que fazer"],
          ["Produto: de R$ 147 por R$ 67 ou 12x R$ 6,73", "Confirma o que viu na página"],
          ["Formulário mínimo + confirmar e-mail", "Evita acesso perdido"],
          ["Cartão, Pix, Cartão + Pix, 2 cartões", "Ninguém fica sem forma de pagar"],
          ["12x já selecionado", "O número pequeno primeiro"],
          ["Selecionar todas (0/3) + 2 bumps + combo", "Aumentar o pedido"],
          ["Plataforma segura + fotos (lateral)", "Prova da plataforma"],
          ["Fundo: o mesmo céu da página", "Não parece que saiu do lugar"]], "mini")
      + '<p class="formula"><b>Continuidade é a regra número 1:</b> mesmo fundo, mockup, frase, preço e garantias da página. Diferença na hora do cartão gera desconfiança.</p>',
      "0.75fr 1.4fr"))

pg(S, "O banner do checkout",
   g2(img("banner-checkout.jpg", "1024 x 736", cls="shot"),
      tabela(["Bloco", "Por quê"], [
          ["Fundo do mundo do nicho (céu)", "Continuidade com a página"],
          ["Pílula verde “ÚLTIMO PASSO”", "Falta pouco"],
          ["“Você está a <em>um passo</em> de <em>postar fotos lindas</em> e <em>criativas</em> da sua viagem.”", "A promessa pela 3ª vez, idêntica"],
          ["Avião e câmera 3D nos cantos do cartão", "Emoji do nicho dá vida sem poluir"],
          ["Notebook + 2 celulares com o app real", "É isso que chega em segundos"],
          ["Pagamento único · Acesso imediato · 7 dias de garantia", "Os 3 medos da hora de pagar"],
          ["Barra verde: PREENCHA SEUS DADOS E ACESSE O APP AGORA", "Instrução, não venda"]], "mini")
      + eb("Mudou em relação ao modelo antigo (lt-banner-checkout)") + ul([
          "Fundo cinza → fundo do nicho.", "Selos pretos com neon → selos na cor da marca.",
          "“Finalize seus dados” → “Preencha seus dados e acesse <b>o app</b> agora”.", "Celulares → notebook + celulares."]),
      "1.15fr 1fr"))

pg(S, "Bônus x order bump",
   tabela(["", "Bônus", "Order bump"], [
       ["Serve para", "Tirar uma <b>objeção</b> da compra", "Atender uma <b>vontade a mais</b> de quem já decidiu"],
       ["Responde", "“E se eu não conseguir?” (medo)", "“E se ficar ainda melhor?” (desejo)"],
       ["Sem ele a promessa se cumpre?", "<b>Não</b>, para parte do público", "<b>Sim</b>, igual"],
       ["Onde aparece", "Na página, antes do preço", "No checkout, depois da decisão"],
       ["Preço", "Grátis (sobe o valor percebido)", "Pago e barato (sobe o valor do pedido)"],
       ["Mede", "Conversão da página", "Ticket médio"]])
   + g2(eb("Teste de duas perguntas") + '<p class="formula">1. Se eu tirar isso, a promessa ainda acontece? <b>Não → bônus.</b> Sim → pode ser bump.<br>2. Responde a um medo ou a uma vontade? <b>Medo → bônus. Vontade → bump.</b></p>',
        eb("No Instravel") + ul([
            "Inspirações de Fotos = bônus: sem ela, quem não sabe fotografar não posta foto linda.",
            "Tutorial = bônus: medo de não saber mexer.",
            "Figurinhas = bump: o Story já fica lindo sem elas.",
            "Quadro para imprimir = bump: nada a ver com postar, é vontade."])
        + '<p class="note">Bump não vai como bônus porque, depois de 3 bônus, mais um não aumenta a venda e o produto perde a chance de cobrar. E não vai na página porque a página vende uma coisa só.</p>'))

pg(S, "Os 3 bumps e a ordem",
   g2(img("bumps-1-2.jpg", "Bumps 1 e 2", cls="shot") + img("bump-combo.jpg", "Combo", cls="shot"),
      tabela(["#", "Cabeçalho (benefício)", "Produto", "Preço"], [
          ["1", "✨ DEIXE SEUS STORIES AINDA MAIS CRIATIVOS", "StikTravel: Figurinhas", "de R$ 67 por <b>R$ 25,90</b>"],
          ["2", "IMPRIMA AS MELHORES FOTOS DA SUA VIAGEM 📸", "Quadro de Viagens Premium", "de R$ 67 por <b>R$ 21,90</b>"],
          ["3", "🔥 LEVE OS 2 JUNTOS COM DESCONTO ESPECIAL", "Combo 2 em 1", "de R$ 134 por <b>R$ 29,90</b>"]], "mini")
      + eb("Por que essa ordem") + ul([
          "<b>1º o mais próximo do produto</b> (o mesmo Story) e o mais caro: é o sim mais fácil.",
          "<b>2º outro uso</b> (a parede de casa) e mais barato: segunda porta para quem recusou.",
          "<b>Combo por último</b>: só faz sentido depois de ver os dois preços (47,80 → 29,90)."])
      + eb("Como escrever") + ul([
          "Cabeçalho = verbo + benefício + emoji. Nunca o nome do produto.",
          "Linha da caixa = nome curto + “de R$ X por R$ Y” (X = preço do principal).",
          "Descrição = o que é, com número + resultado emocional, com os pilares da promessa."]),
      "0.95fr 1.3fr"))

pg(S, "Como criar os bumps e conferir o checkout",
   g2(eb("Passo a passo dos bumps") + '<ol class="ol">' + "".join(f"<li>{x}</li>" for x in [
       "Liste o que o cliente vai querer depois de usar: no mesmo uso (“ainda mais...”) e em outro uso da mesma vida.",
       "Passe cada ideia no teste de duas perguntas. Fica só o que for vontade.",
       "Escolha 2: o primeiro grudado no uso principal (mais caro), o segundo em outro uso (mais barato).",
       "Combo dos 2 por pouco mais que o mais caro.",
       "Âncora de cada bump = preço do principal. Âncora do combo = soma.",
       "Consumo rápido e pronto, igual ao principal.",
       "Anote a taxa de cada bump: o que vende bem vira produto próprio ou upsell."]) + "</ol>"
      + eb("Duas tabelas de preço válidas") + tabela(["Modelo", "Bumps", "Combo"], [
          ["Kamila padrão", "3 de R$ 15,90 a 17,90", "3 em 1 a R$ 35,90"],
          ["Instravel", "2 de R$ 21,90 e 25,90", "2 em 1 a R$ 29,90"]], "mini"),
      eb("Checklist do checkout") + '<div class="check">' + "".join(f"<div>☐ {x}</div>" for x in [
          "Fundo do checkout = mundo da página",
          "Banner: ÚLTIMO PASSO + “Você está a um passo de [promessa]” + mockup + 3 garantias + barra verde",
          "Mesmo de/por e parcela da página", "Parcelamento máximo já selecionado",
          "2 bumps + combo, cabeçalho de benefício, na ordem certa", "Imagem quadrada de cada bump",
          "Cronômetro: por visitante (ao zerar, nada muda) ou data real", "Compra testada no celular"]) + "</div>"
      + '<p class="note">Ainda não visto: upsell, downsell e e-mail de acesso. Completar quando tiver prints.</p>'))

# ---------------- PARTE 3 · PROMPTS ----------------
S = "Prompts das imagens"
md = (AQUI / "prompts-imagens-lt.md").read_text()
pg(S, "Mapa das imagens",
   g2(tabela(["#", "Imagem", "Onde", "IA?"], [
       ["1", "Fundo do mundo do nicho", "Topo, oferta, checkout", "Sim"],
       ["2", "Modelos da vitrine", "Carrossel e faixa", "<b>Não</b>: exportar do produto"],
       ["3", "Vídeos das categorias", "Tudo em um só app", "<b>Não</b>: gravar a tela"],
       ["4", "Mockup da oferta", "Oferta e banner", "Sim, com prints reais"],
       ["5", "Bônus 1, coleção", "Bônus", "Sim"], ["6", "Bônus 2, grade do feed", "Bônus", "Sim, com prints"],
       ["7", "Bônus 3, tutorial", "Bônus", "Sim, com prints"], ["8", "Selo de garantia", "Garantia", "Sim"],
       ["9", "Ramos dourados", "Nota", "Sim"], ["10", "Banner do checkout", "Checkout", "Sim"],
       ["11", "Bumps e combo", "Checkout", "Sim"], ["12", "Ícone do produto", "Checkout", "Sim"],
       ["13", "Foto da especialista", "Autoridade", "<b>Não</b>: foto real"], ["14", "Capa do vídeo", "Como funciona", "Print do vídeo"]], "mini"),
      eb("Como usar") + ul([
          "ChatGPT (imagem) ou Gemini / Nano Banana. Um prompt por conversa, com os anexos pedidos.",
          "Prompt em inglês; texto da arte em português, entre aspas.",
          "Troque tudo que está entre [colchetes]. Os valores de exemplo são do Instravel.",
          "<b>Tela do produto é sempre print real anexado.</b> A IA monta o cenário, não inventa o produto.",
          "Gere primeiro o fundo do nicho e anexe nas outras peças.",
          "Clique em “Copiar” em cima de cada prompt."]),
      "1.2fr 1fr"))

blocos = re.split(r"\n## ", md)
pares = []
for b in blocos[1:]:
    titulo = b.split("\n", 1)[0]
    codes = re.findall(r"```\n(.*?)```", b, re.S)
    if not codes:
        continue
    nomes = re.findall(r"\*\*(.+?)\*\*\n(?:Anexar[^\n]*\n)?```", b)
    anexar = re.findall(r"Anexar: ([^\n]+)", b)
    for k, c in enumerate(codes):
        nome = nomes[k] if k < len(nomes) and len(codes) > 1 else titulo
        pares.append((nome, anexar[k] if k < len(anexar) else "", c.strip()))
for k in range(0, len(pares), 2):
    lado = []
    for nome, anexo, c in pares[k:k + 2]:
        a = f'<p class="note"><b>Anexar:</b> {html.escape(anexo)}</p>' if anexo else ""
        lado.append(eb(html.escape(nome)) + a + f'<div class="pw"><button class="cp">Copiar</button><pre class="prompt">{html.escape(c)}</pre></div>')
    if len(lado) == 1:
        lado.append("")
    pg(S, "Prompts: " + " · ".join(p[0].split(" (")[0] for p in pares[k:k + 2]), g2(lado[0], lado[1]))


# ---------------- PARTE 4 · CRIATIVOS EM VÍDEO ----------------
import markdown as _md
S = "Criativos em vídeo"
_cv = (AQUI / "playbook-criativos-video.md").read_text()
_secs = re.split(r"\n## ", _cv)
_intro = _secs[0].split("\n", 2)[2] if _secs[0].count("\n") > 1 else ""
pg(S, "O que já existia e o que este playbook acrescenta", _md.markdown(_intro))
for _s in _secs[1:]:
    _tit, _corpo = _s.split("\n", 1)
    _tit = re.sub(r"^\d+\.\s*", "", _tit.strip())
    if _tit.startswith("Os 11 vídeos"):
        _vids = re.split(r"\n### ", "\n" + _corpo)[1:]
        for k in range(0, len(_vids), 2):
            _cols = []
            for v in _vids[k:k + 2]:
                _h, _b = v.split("\n", 1)
                _img = re.search(r"!\[\]\((img/[^)]+)\)", _b)
                _b = re.sub(r"!\[\]\([^)]+\)\n?", "", _b)
                _cols.append(eb(html.escape(_h)) + (img(_img.group(1)[4:], "", cls="shot") if _img else "") + _md.markdown(_b))
            if len(_cols) == 1:
                _cols.append("")
            pg(S, "Vídeos desmontados (%d de %d)" % (k // 2 + 1, (len(_vids) + 1) // 2), g2(_cols[0], _cols[1]))
    else:
        _corpo = re.sub(r"!\[[^\]]*\]\([^)]+\)\n?", "", _corpo)
        pg(S, _tit, _md.markdown(_corpo, extensions=["tables"]))

pg("Próximos passos", "Decisão sobre as skills",
   g2(eb("Recomendação") + '<p class="lead">Uma esteira só (<b>low-ticket</b>), com todas as páginas como referência. O gerador <b>ganha</b> as peças novas do Instravel como opções, sem perder nenhuma das antigas.</p>'
      + eb("Onde está cada coisa") + ul([
          "<b>playbook-pagina-lt.md</b>: a página, completa, em texto (a IA lê este).",
          "<b>playbook-checkout-lt.md</b>: checkout, banner e bumps.",
          "<b>prompts-imagens-lt.md</b>: todos os prompts.",
          "<b>PLAYBOOK-LOW-TICKET.html</b>: este caderno (gerado por gerar_html.py).",
          "Referência crua: 4-conhecimento › … › Página de Vendas › referencia-instravel."]),
      eb("A fazer, com sua aprovação") + tabela(["Skill", "O que muda"], [
          ["lt-oferta", "Fórmula da headline, faixa por identidade, produto por momentos, bônus pela jornada, âncora única, bumps 2 + combo"],
          ["lt-copy-pagina", "Nova ordem, transição, botão “QUERO + resultado”, FAQ repetindo o bônus, depoimentos de retornos reais"],
          ["lt-pagina", "Acrescentar opções ao gerador (vitrine 3D, categorias em vídeo, vídeo de tela, flutuante, cronômetro por visitante) e deixar a página com nota 95+"],
          ["lt-banner-checkout", "Variante “mundo do nicho” (já tem o prompt)"],
          ["lt-video-demo", "Feito: roteiro do vídeo de tela"],
          ["lt-nova-oferta", "Feito: conduz a oferta inteira, do briefing à página no ar"]], "mini")))

# ---------------- MONTAGEM ----------------
def montar(lista, titulo, sub, arquivo):
    total = len(lista) + 1
    partes = []
    for s in dict.fromkeys(p[0] for p in lista):
        partes.append((s, next(k for k, p in enumerate(lista) if p[0] == s) + 2))
    sumario = "".join(f'<a href="#p{i}"><b>{s}</b><span>a partir da página {i}</span></a>' for s, i in partes)
    indice = "".join(f'<a href="#p{k + 2}">{k + 2}. {t}</a>' for k, (_, t, _, _) in enumerate(lista))
    capa = f'''<section class="page capa" id="p1"><div class="hd"><span>{titulo}</span><span>Vissia</span></div>
<div class="ft"><span>{titulo} · {VERSAO}</span><span>1/{total}</span></div>
<div class="capa-in"><div class="eb">{sub}</div><h1>Playbook<br><b>{titulo.replace("Playbook ", "")}</b></h1>
<div class="partes">{sumario}</div><div class="indice">{indice}</div></div></section>'''
    corpo = capa + "".join(
        f'<section class="page" id="p{k + 2}"><div class="hd"><span>{titulo}</span><span>{s}</span></div>'
        f'<h2>{t}</h2>{c}<div class="ft"><span>{titulo} · {VERSAO}</span><span>{k + 2}/{total}</span></div></section>'
        for k, (s, t, sub2, c) in enumerate(lista))
    topo = f'<nav class="top"><span class="t">{titulo}</span><a href="#p1">Início</a>' + "".join(f'<a href="#p{i}">{s}</a>' for s, i in partes) + "</nav>"
    doc = f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet"><style>{CSS}</style></head>
<body>{topo}{corpo}<script>{JS}</script></body></html>'''
    (AQUI / arquivo).write_text(doc)
    print("ok", arquivo, total, "páginas")


CSS = """
:root{--ink:#12294F;--tx:#3A5478;--mut:#6B84A3;--blue:#1E63D6;--co:#F4511E;--line:#D4E6F7;--bg:#F3F8FD}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:#DDE7F1;font-family:'DM Sans',system-ui,sans-serif;color:var(--tx);-webkit-font-smoothing:antialiased}
.top{position:sticky;top:0;z-index:20;display:flex;gap:6px;align-items:center;padding:10px 20px;background:var(--ink);overflow-x:auto}
.top a{color:#fff;text-decoration:none;font-size:13px;font-weight:600;padding:7px 14px;border-radius:99px;background:#ffffff18;white-space:nowrap}.top a:hover{background:var(--co)}
.top .t{color:#9FC3EA;font-size:12px;letter-spacing:.18em;text-transform:uppercase;margin-right:10px;white-space:nowrap}
.page{position:relative;width:min(1500px,96vw);min-height:min(940px,62vw);margin:28px auto;padding:92px 90px 80px;
 background:radial-gradient(circle,#c9dcf0 1px,transparent 1.3px) 0 0/22px 22px,linear-gradient(160deg,#fff 0%,#F3F8FD 55%,#E6F1FB 100%);
 box-shadow:0 20px 60px -30px #12294f66;border-radius:6px;scroll-margin-top:60px}
.hd,.ft{position:absolute;left:90px;right:90px;display:flex;justify-content:space-between}
.hd{top:36px;font-size:13px;letter-spacing:.22em;text-transform:uppercase;color:var(--blue);font-weight:600}
.ft{bottom:30px;font-size:13px;color:var(--mut)}
h1{font-size:96px;line-height:1;margin:16px 0 28px;color:var(--ink);font-weight:300;letter-spacing:-.03em}h1 b{font-weight:700}
h2{font-size:42px;line-height:1.1;margin:0 0 22px;color:var(--ink);font-weight:600;letter-spacing:-.02em}
.eb{font-size:12.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--blue);font-weight:600;margin:20px 0 10px}
.eb:first-child{margin-top:0}
.lead{font-size:20px;line-height:1.5;color:var(--tx);margin:0 0 18px}.lead b{color:var(--ink)}
ul,ol{margin:0;padding-left:20px;font-size:16.5px;line-height:1.55}li{margin:4px 0}li b,p b,td b{color:var(--ink)}
em{font-style:normal;color:var(--co);font-weight:600}
.g2{display:grid;gap:48px;align-items:start}.g2>div,.g3>*{min-width:0}.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-bottom:22px}
figure{margin:0 0 14px}figure img{width:100%;display:block;border:1px solid var(--line);border-radius:10px;background:#fff;cursor:zoom-in}
.shot.tall img{max-height:620px;width:auto;max-width:100%;margin:0 auto}
.cap{font-size:13.5px;color:var(--mut);margin-top:7px;line-height:1.4}.cap b{color:var(--ink)}
table{width:100%;border-collapse:collapse;font-size:14.5px;line-height:1.45;margin:6px 0 14px;background:#ffffffcc;border:1px solid var(--line)}
th{text-align:left;font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--blue);padding:10px 12px;border-bottom:2px solid var(--line);font-weight:600}
td{padding:8px 12px;border-top:1px solid #E7F0F9;vertical-align:top}table.mini{font-size:13.5px}table.mini td{padding:6px 10px}
.quote{background:#fff;border:1px solid var(--line);border-left:4px solid var(--co);padding:16px 20px;border-radius:8px;font-size:18px;line-height:1.45;color:var(--ink);margin-bottom:6px}
.quote small{font-size:11.5px;letter-spacing:.16em;color:var(--blue);font-weight:600}.quote span{font-size:15px;color:var(--tx)}
.formula{background:var(--ink);color:#E8F2FF;padding:14px 18px;border-radius:8px;font-size:15.5px;line-height:1.55;margin:8px 0}.formula b{color:#FFD9C7}
.note{font-size:14px;color:var(--mut);line-height:1.5;margin:10px 0}
.cards{display:grid;gap:16px;margin:4px 0 18px}.cards.c3{grid-template-columns:repeat(3,1fr)}
.card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px 20px}.card .n{font-size:30px;font-weight:700;color:var(--co);line-height:1}
.card .t{font-size:17px;font-weight:700;color:var(--ink);margin:8px 0 4px}.card p{margin:0;font-size:14.5px;line-height:1.45}
.steps{display:flex;flex-wrap:wrap;gap:8px;align-items:center;color:var(--mut);font-size:18px;margin-bottom:6px}.steps span{background:#fff;border:1px solid var(--line);border-radius:99px;padding:7px 14px;font-size:14.5px;color:var(--ink);font-weight:600}
.strip{display:flex;gap:6px;overflow-x:auto;padding-bottom:6px}.strip img{height:330px;border:1px solid var(--line);border-radius:6px;cursor:zoom-in}
.sw{display:grid;grid-template-columns:1fr 1fr;gap:8px 18px;margin-bottom:8px}.sw div{display:grid;grid-template-columns:34px 1fr;column-gap:10px;align-items:center;font-size:13.5px}
.sw i{grid-row:span 2;width:34px;height:34px;border-radius:8px;border:1px solid var(--line)}.sw b{color:var(--ink)}.sw span{color:var(--mut);font-size:12.5px}
.ficha{display:grid;grid-template-columns:1fr 1fr;gap:8px 30px}.ficha div{background:#fff;border:1px solid var(--line);border-radius:8px;padding:10px 14px;font-size:15px;display:flex;gap:12px}
.ficha b{color:var(--co);min-width:22px}.check div{font-size:15.5px;padding:7px 0;border-bottom:1px solid #E7F0F9}
.ol li{margin:6px 0}
.pw{position:relative}.cp{position:absolute;top:8px;right:8px;font:600 12px 'DM Sans',sans-serif;background:var(--co);color:#fff;border:0;border-radius:99px;padding:6px 12px;cursor:pointer}
pre.prompt{white-space:pre-wrap;background:var(--ink);color:#DDEBFF;border-radius:8px;padding:16px 18px;font:12.5px/1.55 ui-monospace,Menlo,monospace;margin:0;max-height:560px;overflow:auto}
.capa-in{margin-top:70px}.partes{display:flex;gap:14px;margin:30px 0 26px;flex-wrap:wrap}
.partes a{background:var(--ink);color:#fff;text-decoration:none;padding:16px 22px;border-radius:10px;display:flex;flex-direction:column}.partes a span{font-size:13px;color:#9FC3EA}
.partes a b{font-size:19px}.indice{columns:3;font-size:14px;line-height:1.9}.indice a{color:var(--tx);text-decoration:none;display:block}.indice a:hover{color:var(--co)}
.z{position:fixed;inset:0;z-index:99;background:#000d;display:flex;align-items:center;justify-content:center;cursor:zoom-out}.z img{max-width:94vw;max-height:94vh;border-radius:8px}

.shot.half img{max-height:520px;width:auto;max-width:100%;margin:0 auto}
.demo{font-family:Poppins,sans-serif}.demo b{color:inherit}
.dh{background:var(--sky);border-radius:10px;padding:0 18px 22px;text-align:center;color:#fff;overflow:hidden}
.dfx{display:inline-block;background:color-mix(in srgb,var(--lm) 55%,#fff);color:#2C3E5C;font-size:10px;font-weight:600;letter-spacing:.14em;padding:9px 16px;border-radius:0 0 14px 14px;margin-bottom:16px}
.dh1{font-size:24px;font-weight:600;line-height:1.18;letter-spacing:-.03em;text-shadow:0 2px 10px #0003}.dh1 b{color:var(--lm);font-weight:800}
.dsub{font-size:13.5px;font-weight:500;margin:10px 0 16px}.dsub b{color:var(--lm);font-weight:500}
.dbtn{display:inline-block;background:linear-gradient(180deg,color-mix(in srgb,var(--q) 75%,#fff),var(--q),var(--qd));padding:12px 22px;border-radius:99px;font-weight:700;font-size:13px;box-shadow:inset 0 2px #fff7,0 10px 20px -8px var(--qd)}
.dlight,.dlight2{background:linear-gradient(#fff,#EAF6FD);border:1px solid var(--line);border-radius:10px;padding:18px;margin-top:12px;text-align:center;color:#2D609F}
.deb{display:inline-block;font-size:10px;font-weight:600;letter-spacing:.18em;background:#DCF1FB;border:1px solid #A8E6FF;border-radius:99px;padding:5px 12px;color:#2D609F}
.dh2{font-size:22px;font-weight:700;line-height:1.2;margin:10px 0}.dh2 b{color:#FF7043;font-weight:800}.dh2.fino{font-weight:400}.dh2.up i{font-style:normal;color:#2C5F9E;font-weight:400}
.dp{font-size:13.5px;color:#4D6B8F;text-align:left;margin:8px 0 0}.dp b{color:#12294F}
.doffer{background:linear-gradient(180deg,#2F7FD0,#7CC8F2);padding:18px;border-radius:10px;text-align:center}
.dpill{display:inline-block;background:linear-gradient(90deg,#10B981,#34D399);color:#fff;font-size:13px;font-weight:600;padding:7px 16px;border-radius:99px;margin-bottom:12px}
.dcard{background:#fff;border-radius:22px;overflow:hidden;max-width:380px;margin:0 auto;box-shadow:0 20px 40px -20px #0006}
.dred{background:#DC2626;color:#fff;padding:12px;display:flex;flex-direction:column;gap:2px}.dred small{font-size:9px;letter-spacing:.22em;font-weight:600}.dred b{font-size:24px;font-weight:600;font-variant-numeric:tabular-nums}.dred span{font-size:10px;opacity:.85}
.dbody{padding:16px 18px 18px;color:#1a1a1a}.drow{display:flex;gap:12px;align-items:center;text-align:left;margin-bottom:8px}.drow img{width:46%;border-radius:12px}
.dlogo{font-size:22px;font-weight:700;color:#1E63D6}.dg{color:#059669;font-weight:600;font-size:13px}.drow s{color:#EF4444;font-size:12.5px}
.dsm{font-size:11.5px;color:#737373}.dprice{font-size:46px;font-weight:700;color:#10B981;line-height:1.1;animation:dz 1.6s ease-in-out infinite}
@keyframes dz{0%,to{transform:scale(1)}20%{transform:scale(1.1) rotate(-2deg)}40%{transform:scale(.97) rotate(2deg)}60%{transform:scale(1.08)}}
.deco{display:inline-block;border:2px dashed #10B981;color:#059669;font-size:11px;font-weight:600;border-radius:99px;padding:6px 12px;margin:10px 0}
.dbuy{background:linear-gradient(90deg,#66BB6A,#4CAF50,#43A047);color:#fff;font-weight:700;border-radius:99px;padding:13px;font-size:14.5px;box-shadow:0 0 24px 2px #1fe08670}
.dchk{display:flex;flex-wrap:wrap;justify-content:center;gap:4px 12px;font-size:11.5px;color:#404040;margin:10px 0}.dchk span:before{color:#F97316}
.dalert{background:#FEF2F2;border:1px solid #F87171;color:#DC2626;font-size:11.5px;font-weight:600;border-radius:12px;padding:10px}
.dbtns{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;align-items:center;margin-bottom:16px}
.dbtns span{color:#fff;font-weight:700;font-size:13px;padding:13px 20px;border-radius:99px;box-shadow:inset 0 2px #fff8,0 10px 20px -10px #0007;text-shadow:0 1px 2px #0003}
.b1{background:linear-gradient(180deg,#FF8A65,#FF7043 55%,#F4511E)}.b2{background:#28C9E6}.b3{background:linear-gradient(90deg,#66BB6A,#4CAF50,#43A047);width:100%}.b4{background:linear-gradient(180deg,#FF8A65,#F4511E);width:52px;height:52px;padding:0!important;display:flex;align-items:center;justify-content:center;font-size:22px}
.dbonus{display:flex;gap:12px;background:#fff;border:1px solid #A8E6FF;border-radius:20px;padding:12px;text-align:left;box-shadow:0 14px 30px -18px #12294f66}.dbonus img{width:110px;border-radius:12px}
.dbonus b{display:block;font-size:16px;font-weight:800;color:#2D609F;margin-top:6px}.dbonus p{font-size:12px;color:#4D6B8F;margin:4px 0 0}
.dtag{background:#FF7043;color:#fff;font-size:9.5px;font-weight:600;letter-spacing:.18em;border-radius:99px;padding:4px 11px;box-shadow:0 6px 14px #ff6e4266}
.dchips{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:14px}.dchip{background:#ffffffe6;border:1px solid #A8E6FF;color:#2C5F9E;font-size:11px;font-weight:600;border-radius:99px;padding:4px 10px}
.ol.big li{font-size:16px;margin:9px 0}
@media(max-width:900px){.page{padding:70px 18px 60px;min-height:0}.hd,.ft{left:18px;right:18px}.hd{top:24px;font-size:10.5px}.ft{bottom:18px;font-size:11px}
 .g2,.g3,.cards.c3,.ficha,.sw{grid-template-columns:1fr!important}h1{font-size:56px}h2{font-size:28px}.indice{columns:1}table{display:block;overflow-x:auto}.shot.tall img{max-height:480px}}
@media print{.top{display:none}body{background:#fff}.page{box-shadow:none;margin:0;page-break-after:always;width:100%}}
"""
JS = """document.querySelectorAll('figure img,.strip img').forEach(i=>i.onclick=()=>{const d=document.createElement('div');d.className='z';d.innerHTML='<img src="'+i.src+'">';d.onclick=()=>d.remove();document.body.appendChild(d)});
document.querySelectorAll('.cp').forEach(b=>b.onclick=()=>{navigator.clipboard.writeText(b.nextElementSibling.textContent).then(()=>{b.textContent='Copiado';setTimeout(()=>b.textContent='Copiar',1500)})});"""
montar(paginas, "Playbook Low Ticket", "Metodologia Kamila · todas as páginas como referência · exemplo principal: Instravel", "PLAYBOOK-LOW-TICKET.html")
montar([p for p in paginas if p[0] == "Criativos em vídeo"], "Playbook Criativos em Vídeo", "Os 11 anúncios da Kamila desmontados · complemento da skill lt-criativos-video e do Meu Roteiro que Vende", "PLAYBOOK-CRIATIVOS-VIDEO.html")
