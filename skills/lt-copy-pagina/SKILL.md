---
name: lt-copy-pagina
description: Escreve a copy da página de vendas low ticket, bloco a bloco, na estrutura 13S da Kamilla, para uma oferta já aprovada (saída da lt-oferta). Entrega o esqueleto para aprovação e depois o texto em copy-pagina-vendas.md, nos campos do pagina.json que a lt-pagina lê. Cada oferta tem a sua copy: as frases validadas da Kamilla e da Carlos & Kamila são referência e entram só quando fazem sentido. Use quando o Paulo disser "escreve a copy da página low ticket", "copy da página do produto X", "/lt-copy-pagina", ou depois da lt-oferta aprovada e antes da lt-pagina.
---

# Copy da página low ticket

> **Playbook (04/11/2026):** antes de começar, leia `.claude/skills/low-ticket/playbook/playbook-pagina-lt.md` (metodologia da Kamila com todas as páginas dela como referência, Instravel como exemplo principal; diferenças entre páginas são decisões por oferta, seção 10; oferta, copy, prova, design, animações, CTAs e vídeo, seção por seção). Versão visual: `PLAYBOOK-LOW-TICKET.html`. Onde o playbook e esta skill divergirem, vale esta skill até o Paulo aprovar a atualização (seção 12 do playbook).

Papel só de **copy**. Não decide oferta (isso é da `lt-oferta`) e não monta nem desenha a página (isso é da `lt-pagina`). Entrada: oferta aprovada. Saída: `copy-pagina-vendas.md`.

## Antes de escrever, leia

1. A oferta aprovada: `<projeto>/oferta/oferta.md` (Núcleo, promessa, produto, bônus, preço, garantia, 3 passos, FAQ). Se não existir ou não estiver aprovada, pare e rode a `lt-oferta`.
2. A estrutura 13S e a referência real: `.claude/skills/low-ticket/fontes/0-vissia/operacao/processos/pagina-de-vendas-low-ticket.md`. Os textos das páginas da Carlos & Kamila estão copiados em `.claude/skills/low-ticket/fontes/2-aplicativos/banco-de-ofertas/page_archive-21-22.md` (tabela `page_archive`, ids 21 e 22); os prints completos ("pv ..." e "ck ..." das ofertas 11 a 14) estão em `.claude/skills/low-ticket/fontes/2-aplicativos/banco-de-ofertas/storage/`, com a lista em `.claude/skills/low-ticket/fontes/2-aplicativos/banco-de-ofertas/offer_files-11-14.md`. Use para entender **ângulo, ritmo e função de cada bloco**, nunca para copiar frase.
3. Os 12 blocos de texto validados da Kamilla: `.claude/skills/low-ticket/fontes/4-conhecimento/cursos-e-sistemas/Low Ticket Kamilla/Página de Vendas/framework-pagina-vendas-lt.md`.
4. Exemplo nosso: `.claude/skills/low-ticket/fontes/1-clientes/primeiro-cnpj/5-produtos/anuncio-pronto/oferta/copy-pagina-vendas.md` (feito antes da 13S: o bloco `dor` dele não existe na referência, ignorar).
5. Banco de copy da Vissia (`.claude/skills/low-ticket/fontes/4-conhecimento/copy/3-banco-copy/`) por referência de tom.
6. Modelo de saída: `modelos/copy-pagina-modelo-v2.md` para a página modelo v2 (padrão, réplica do Instravel) ou `modelos/copy-pagina-modelo.md` para o modelo clássico.

## Os blocos (13S)

1 Impacto visual + promessa, 2 Prova social, 3 Passo a passo, 4 Entregáveis, 5 Bônus, 6 Resultado imaginado, 7 Ancoragem, 8 Oferta, 9 Garantia, 10 Autoridade, 11 FAQ, 12 Suporte, 13 Rodapé. Nenhum bloco fora desta lista. A ordem de 3 e 4, o formato de 6 e 7 e a presença de 12 são decisões por oferta (passo 2b).

## Passo a passo

1. **Confirme o que decide a copy:** funil (tráfego frio para low ticket), avatar, oferta exata, o que existe de **prova real** e quem assina como especialista. Pergunte só o que a oferta não responde.
2. **Escolha o formato da prova social (bloco 2)** com o Paulo. Ela nunca some, muda de formato: depoimentos reais; prints de uso real; demonstração do produto com exemplos e vídeo; ou passo a passo cedo + autoridade. Sem prova real, nunca inventar nota, avaliação ou depoimento.
2b. **Tome as decisões por oferta** (playbook, seção 10) e mostre no esqueleto: tipo de impacto visual (vitrine do produto ou pessoa + celulares), ordem (entregáveis antes ou depois do passo a passo), tipo de vídeo (tela ou animação), entregáveis (categorias em vídeo ou galeria com cadeado), resultado imaginado (frase de transição ou "Imagine..."), ancoragem (âncora única ou "Recapitulando"), garantia (experimentar ou "Se 1 X gerar 1 Y"), autoridade (vivência ou experiência), suporte (com ou sem WhatsApp), urgência (cronômetro por visitante ou data). Nenhuma opção é erro: escolha pela oferta e diga por quê em uma linha.
3. **Mostre o esqueleto antes do texto** (regra da Vissia): uma linha por bloco com o ângulo de cada um, a promessa, o formato da prova social e quais frases da Kamilla você pretende manter ou trocar, e por quê. O Paulo aprova.
4. **Escreva o texto completo** em `oferta/copy-pagina-vendas.md`, seguindo `modelos/copy-pagina-modelo.md` (cada bloco já indica o campo do `pagina.json`).
5. **Passe nas regras abaixo** e entregue para aprovação. Só depois a `lt-pagina` monta.

## Frases da Kamilla: referência, não obrigação

O que ela validou (transição da ancoragem "Tudo isso custaria R$ X...", "Ficou com alguma dúvida?", "Pagamento único / Sem mensalidade / Acesso imediato", "Se apenas 1 X gerar 1 Y, o investimento já se paga. Agora imagine o potencial de N.", "Não é teoria.") funciona e pode entrar. Para cada uma, decida por oferta:
- **Serve como está:** mantenha.
- **Serve adaptada:** reescreva com a voz do produto.
- **Não faz sentido** (ex.: "Sem mensalidade" num produto com mensalidade, "acesso vitalício" num app por assinatura): troque ou tire. A `lt-pagina` aceita isso por `oferta.frase_transicao`, `oferta.checks`, `whatsapp.titulo` e `whatsapp.botao`.
Só o aviso legal do rodapé é fixo.

## Regras que não mudam

- **Headline é só a promessa de resultado.** A prova e o "como" vão para a subheadline.
- Começa pela dor do avatar e nunca pela solução, na linguagem dele, um CTA claro por bloco, sem jargão.
- **Promessa sem renda garantida** (o Meta reprova). Resultado tangível e verificável.
- **Nunca inventar** depoimento do zero, print, número de alunos ou resultado. Depoimentos em texto vêm de retornos reais que o Paulo manda (Google, direct, WhatsApp). Urgência: data real ou cronômetro por visitante (ao zerar, nada muda). Item que ainda não existe entra como "a produzir".
- **Sem travessão (—).** Vírgula, ponto ou dois-pontos.
- **Mesmo texto no celular e no computador.** Só muda tamanho e espaço.
- Referência (Carlos & Kamila, 50 Viral Fit) é estrutura e ritmo, não texto.
- Os 3 passos e a frase "É só ..., ... e ...!" são curtos: viram o vídeo dos passos e a frase abaixo dele.
- **Botões:** texto em 1ª pessoa "QUERO + resultado da headline" ("QUERO POSTAR FOTOS LINDAS"). O primeiro e o da oferta são iguais. Só o da oferta vai ao checkout.
- **Destaques:** 2 ou 3 trechos por título (resultado, público ou objeto, número ou tempo), nunca a frase inteira. Um emoji do nicho fecha o título.
- **Etiqueta por seção** (ex.: COMO FUNCIONA, E NÃO PARA POR AÍ..., AINDA TEM DÚVIDAS?): dá para escanear a página só por elas.
- **FAQ repete a objeção do bônus mais forte**, com a mesma resposta.
- **Depoimentos:** escolha um retorno real por objeção (matriz da seção 5 do playbook) e espalhe ocasiões, lugares e perfis. Textos copiados de Google, direct ou WhatsApp podem ir em cartão sem foto.
- **Títulos de conversa** (autoridade, garantia, transição) em tom de pessoa falando; títulos de venda curtos e diretos.
