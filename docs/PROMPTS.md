# Especificação e prompts da dashboard

## Solicitação de origem

O projeto foi solicitado como uma **dashboard em arquivo HTML único** a partir de uma planilha Porsche já sanitizada, com três perguntas de negócio, filtros interativos, indicadores de topo, identidade visual coerente e documentação para publicação no GitHub Pages.

## Prompt de implementação — versão consolidada/reconstituída

> Este é um prompt **reconstituído a partir da solicitação e das decisões registradas no projeto**, documentado para permitir reproduzir a construção. **Não é transcrição de uma mensagem histórica literal de um chat com várias revisões.**

```text
Atue como analista de dados e desenvolvedor front-end. A partir do arquivo
"Planilha base Porsche (sanitizada).xlsx", produza um único index.html,
pronto para GitHub Pages, contendo CSS, JavaScript e registros embutidos
(sem bibliotecas externas, API, backend ou arquivos adicionais obrigatórios).

Considere somente colunas não pessoais: identificador da venda, data, modelo,
ano do modelo, preço em USD, quilometragem, método de pagamento, cidade,
estado, status de entrega e sinalizador de data válida.

Exclua registros Cancelled dos indicadores de negócio, mas mantenha-os na
base auditável. Não trate pendências/em trânsito como receita contábil
reconhecida. Preserve datas inválidas como ausentes, sem fabricar datas.

Responda a exatamente três perguntas:
1. Quais modelos geram mais valor? Ranking por receita/soma dos preços.
2. Em quais estados o valor se concentra? Ranking geográfico por receita.
3. Como os clientes pagam? Distribuição de MODALIDADES por quantidade.

Crie KPIs de soma dos preços, quantidade de registros elegíveis, ticket médio
e quantidade de estados. Crie filtros combináveis por modelo, estado, ano do
modelo e pagamento, com botão de limpar. Os gráficos devem reagir a cada
filtro e permitir clicar para aplicar filtros. Exporte os registros filtrados
para CSV.

Aparência: editorial premium, fundo off-white, preto grafite e vermelho
escuro, tipografia sans-serif acessível, cards com espaçamento, títulos que
explicitem a pergunta de negócio, notas metodológicas e design responsivo.

Garanta que o site funcione ao abrir index.html localmente e no GitHub Pages.
Inclua estados vazios, acessibilidade de teclado e aviso de que o trabalho é
independente da marca. Forneça README, evidências de interface sem filtro,
com filtros aplicados e versão mobile, além de instruções de publicação.
```

## Refinamentos incorporados à versão final

| Decisão/refinamento | Motivo | Resultado observável |
| --- | --- | --- |
| Substituir um painel genérico por **3 perguntas explícitas** | Cada visual precisa apoiar uma decisão | Títulos de cards no formato de pergunta |
| Distinguir **valor total** de **faturamento reconhecido** | Há pedidos não entregues e datas futuras | KPI explicativo, rodapé metodológico e ressalvas no README |
| Excluir status `Cancelled` dos KPIs | Cancelamentos não devem inflar as métricas | 100 registros brutos, 93 elegíveis |
| Usar **ano do modelo** como filtro | O ano é numérico e confiável; há datas inválidas | Filtro claramente rotulado “Ano do modelo” |
| Medir pagamento por **quantidade** | Evita confundir frequência com volume financeiro | Rosca e percentuais baseados em número de vendas |
| Tornar os gráficos clicáveis | Facilita drill-down sem navegação adicional | Clique em barra ou modalidade ajusta o filtro |
| Adicionar download CSV do recorte | Permite auditoria e análise de detalhes | Botão “Exportar recorte CSV” |
| Criar versão responsiva sem dependências | Página estática deve funcionar em qualquer aparelho | Layout para desktop e celular, HTML autossuficiente |
| Mostrar qualidade da base | Há dados temporais problemáticos | 24 datas inválidas e 20 futuras informadas |

## Ferramenta utilizada

Nesta versão, a dashboard foi produzida **diretamente com auxílio do ChatGPT** e testada localmente. **Não foi usado Canvas** (recurso antigo) nem um agente com skill separado. Comparar a versão atual com um agente especialista é uma **evolução sugerida**, e não algo já realizado.
