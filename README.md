# Testes de API - ParaBank

Este projeto simula e executa testes focados na API de um sistema bancário fictício, o ParaBank, da Parasoft, feitos de duas formas: Postman e Python + Pytest. O objetivo é ganhar experiência e montar meu portfólio.

A iniciativa desse projeto veio de uma grande vontade pessoal de ser inserido como QA no mercado financeiro. Por isso o foco são os cenários em que o dinheiro precisa bater: transferência entre contas, saldo e empréstimo.

## Arquivos

- `api_client.py` - classe `ParaBankClient` com a `base_url` e um método para cada endpoint (login, contas, transações, transferência, criar conta e empréstimo)
- `data.py` - dados de teste (usuário, valores e IDs inexistentes)
- `test_auth.py`, `test_accounts.py`, `test_transfer.py`, `test_loans.py` - os testes em si
- `ParaBank API.postman_collection.json` - a versão em Postman
- `requirements.txt` - dependências do projeto

## Testes

20 casos de teste planejados, divididos em positivo, negativo, valor limite e consistência. Eles estão na [planilha de casos de teste e bugs](https://docs.google.com/spreadsheets/d/1We7nMNFqiq426WOe8DPRD-YlZiW9yzYXN_-hJVHEH0U/edit), junto com o relatório de bugs.

18 deles estão automatizados com pytest. Os outros 2 (transações e criação de conta) foram testados só no Postman.

Os testes de transferência conferem o saldo da conta antes e depois, para garantir que o dinheiro saiu e entrou na quantia certa.

Resultado dos 20 casos: 14 aprovados, 4 reprovados e 2 bloqueados. Na última execução do pytest, 13 testes passam, 3 falham de propósito (cada um documenta um bug) e 2 estão com `skip`.

## Rodando

Sobe o ParaBank com Docker:

```
docker run -d -p 8080:8080 parasoft/parabank
```

Abre `http://localhost:8080/parabank/index.htm` e cadastra um usuário com o username e a senha que estão no `data.py`. O banco do container começa vazio toda vez que ele sobe, então o cadastro precisa ser refeito.

No `api_client.py`, confere a `base_url`:

```
base_url = "http://localhost:8080/parabank/services/bank"
```

Se o Docker estiver rodando em um Codespace, usa a URL pública da porta 8080 no lugar de `localhost:8080`.

Instala e roda:

```
pip install -r requirements.txt
pytest -v
```

A versão Postman é só importar o `.json` e preencher `base_url`, `username` e `password` nas variáveis da coleção.

## Bugs encontrados

- **BUG-01 (crítica):** `POST /transfer` aceita valor negativo e inverte a direção da transferência
- **BUG-02 (crítica):** `POST /transfer` aceita valor maior que o saldo e deixa a conta de origem negativa
- **BUG-04 (média):** a conta nova nasce com saldo de 515.50, diferente do Init. Balance (1000.50) do Admin Page, e sem nenhuma transação que explique o valor
- **BUG-05 (baixa):** `POST /transfer` aceita valor zero
- **BUG-06 (média):** `GET /customers/{id}/accounts` devolve 500 quando o cliente acumula muitas contas (causa provável, não isolada)

Os detalhes e os passos para reproduzir cada um estão na planilha.

## Decisões e limitações

- A API responde em XML por padrão, então todas as chamadas mandam o header `Accept: application/json`.
- Os 3 testes que falham de propósito (`test_transfer_negative_amount`, `test_transfer_amount_exceeds_balance` e `test_transfer_empty_amount`) ficam vermelhos enquanto o bug existir.
- O servidor do ParaBank piora com o uso repetido: depois de várias execuções, cada uma criando contas novas, o endpoint de contas passou a devolver 500. Reduzi as contas criadas por execução com uma fixture compartilhada no `test_transfer.py`, mas o problema continua. Quando acontecer, recria o container.
- Por causa disso, `test_transfer_decimal_amount` e `test_transfer_below_minimum_balance` falharam de forma intermitente com `JSONDecodeError` e estão com `skip`. Os casos 16 e 17 da planilha ficaram como bloqueados.
- Um bug foi descartado depois de investigar: eu tinha registrado que transferir para uma conta inexistente fazia o dinheiro sumir, mas o ID que usei (12345) já existia no banco de exemplo. Com o ID 999999, a API rejeita a transferência.
