# Desaﬁo Técnico

_Pessoa Engenheira de Machine Learning_

## Contexto

O objetivo desse desafio é dar a oportunidade para ambas as partes
conhecerem um pouco mais sobre cada um, compartilhamos um exemplo de
problema que já tenhamos resolvido para entender um pouco do seu processo
de raciocínio e também para você ter a oportunidade de entender o tipo de
problema que resolvemos diariamente.

## Desafio

Em anexo você recebeu as seguintes bases de dados:

1. client.csv: Contém informações de clientes
2. chat_history.csv: Contém histórico de mensagens de alguns clientes
3. client_conditions.csv: Tabela de exemplo de possível output do modelo com a identificação de alguns clientes e suas condições
4. seed_*.csv: Tabelas estáticas que utilizamos para mapear 


O desafio é desenvolver um modelo que retorne as
condições de saúde de cada cliente baseado em suas mensagens, por
exemplo:

- Obesidade;
- Tabagismo;
- Diabetes;
- Hipertensão e outros.

Esse modelo deve avaliar todas as mensagens, extrair as condições de saúde
e guardá-las em um banco de dados, esse banco de dados pode ser um
simples arquivo CSV que será consultado pela API.
O projeto deve ser conter uma API, que vai receber um ID de cliente e retorna
todas as condições de saúde dele como uma lista, se o cliente não existe na
base devemos retornar um erro de 404 Not Found.

## Expectativas

> Não buscamos a solução perfeita, o foco é entender o seu processo de
investigação, estudo e desenvolvimento

- A solução do problema deve estar em um repositório público no Github;
- A solução deve ter um documento por escrito explicando o racional, as
tomadas de decisões e os “assumptions" tomados;
- Visão de futuro, o que poderia ser feito além do que foi pedido, quais outras
oportunidades temos dado o contexto do problema.
