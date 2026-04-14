#  Sistema de Inventário (CLI + SQLite)

Este projeto é um sistema simples de inventário de computadores desenvolvido em Python, utilizando SQLite para persistência de dados e exportação automática para CSV.

## Funcionalidades

-  Adicionar computadores ao inventário
-  Remover computadores por ID
-  Atualizar informações (com controle de upgrades)
-  Listar todos os registros
-  Exportação automática para CSV
-  Registro de data e tipo de atualização

---

## Estrutura do Banco

Tabela: `invent1`

| Campo           | Tipo     | Descrição |
|----------------|----------|----------|
| id             | INTEGER  | Identificador único |
| tipo           | TEXT     | Tipo do equipamento |
| marca          | TEXT     | Marca |
| process        | TEXT     | Processador |
| storage        | INTEGER  | Armazenamento (GB) |
| ram            | INTEGER  | Memória RAM (GB) |
| num_up         | INTEGER  | Número de upgrades |
| last_up_data   | TEXT     | Data do último upgrade |
| update_type    | TEXT     | Tipo de atualização |
| sector         | TEXT     | Setor |

---
