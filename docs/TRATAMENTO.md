# Tratamento dos dados e regras da análise

## Origem e escopo

O insumo recebido foi `Planilha base Porsche (sanitizada).xlsx`. A planilha já foi fornecida como **sanitizada**, por isso este projeto não afirma ter validado, reconstruído ou aplicado regras da base crua original. A etapa adicional consistiu em selecionar os campos de trabalho, preparar tipos para consumo em JavaScript, conferir métricas e manter o CSV tratado como referência.

## Dicionário de dados publicado

| Campo | Tipo no HTML | Papel na análise |
| --- | --- | --- |
| `sale_id` | inteiro | Identificador técnico da linha, não do cliente |
| `sale_date` | texto ISO `AAAA-MM-DD` ou `null` | Informação temporal, sujeita a qualidade |
| `porsche_model` | texto | Dimensão / filtro / ranking de modelos |
| `model_year` | inteiro | Ano do veículo, usado no filtro de ano |
| `sale_price_usd` | número | Preço da venda/pedido, em dólares americanos |
| `vehicle_mileage_mi` | número | Quilometragem registrada, em milhas |
| `payment_method` | texto | Modalidade de pagamento / gráfico de frequência |
| `city` | texto | Cidade informada |
| `state` | texto | Sigla do estado norte-americano / filtro e ranking |
| `delivery_status` | texto | Status do pedido/venda, para separar cancelamentos |
| `date_valid` | booleano | Identifica se `sale_date` foi reconhecida como válida |

**Campos excluídos da publicação:** não há nomes, e-mails, endereços de clientes, telefone ou informações de vendedores no CSV e no conjunto JSON usado pelo HTML. Não há dados pessoais necessários às três perguntas escolhidas.

## Transformações e validações

1. Conservar apenas as **11 colunas explicitamente listadas** acima na versão de publicação.
2. Usar `model_year` e `sale_id` como **inteiros**; `sale_price_usd` e `vehicle_mileage_mi` como **números**, sem símbolos de moeda nem fórmulas.
3. Usar data no formato ISO (`YYYY-MM-DD`) somente quando validada. Para uma data inválida, manter o campo ausente (`null` no HTML, célula vazia no CSV) e `date_valid=false`.
4. Conservar a grafia existente de modelos, siglas de estados, métodos de pagamento e status; não inventar categorias.
5. Preservar os cancelamentos no CSV, mas excluir `delivery_status="Cancelled"` do universo de cálculo. Não excluir pedidos pendentes/em trânsito por padrão; essa decisão fica visível na nota metodológica.
6. Embutir registros JSON em `index.html`. Sem fontes remotas, a dashboard funciona mesmo se aberta localmente.

## Auditoria em 18/10/2026

| Teste | Resultado |
| --- | ---: |
| Registros totais | 100 |
| Cancelados | 7 |
| Elegíveis para o painel | 93 |
| Datas inválidas ou ausentes | 24 |
| Datas futuras relativamente a 18/10/2026 | 20 |
| Estados no recorte elegível | 32 |
| Modelos distintos no recorte elegível | 39 |
| Métodos de pagamento no recorte elegível | 9 |

**Atenção:** datas futuras foram **mantidas** e contabilizadas no indicador de qualidade. Não são interpretadas como transações que efetivamente ocorreram até 18/10/2026. A métrica denominada “Receita registrada” é a soma descritiva do campo `sale_price_usd` e inclui pedidos em diferentes estágios, não faturamento contábil. Os dados são demonstrativos.

## Definições dos indicadores

- **Volume de vendas:** contagem de registros que não têm status `Cancelled`, após filtros.
- **Valor registrado:** soma de `sale_price_usd` dos registros elegíveis após filtros.
- **Ticket médio:** valor registrado dividido pelo volume elegível (quando o volume é zero, a interface mostra travessão).
- **Estados com vendas:** contagem de estados diferentes presentes no recorte.
- **Modelo e estado líderes:** máximo de valor registrado agregado por categoria.
- **Pagamentos:** contagem e percentual do número de registros elegíveis por forma de pagamento, não a soma financeira.

## Atualização futura

Para incorporar **outra base sanitizada** com o mesmo esquema, substitua `data/porsche_sales_clean.csv` e execute `python scripts/update_dashboard.py`. O script rejeita colunas extras, ausências de colunas obrigatórias, números inválidos, valores não positivos de preço, datas incoerentes e IDs repetidos; o HTML só é atualizado após a validação completa. Em seguida, teste e publique novamente o arquivo modificado.

O script **não recebe XLSX cru** e **não substitui uma política de privacidade ou o processo de sanitização**.
