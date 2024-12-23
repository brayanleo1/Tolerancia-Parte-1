
## Instalação

Baixe os arquivos do github e execute:

```bash
  docker-compose build
  docker-compose up
```
Os containers devem estar funcionando a partir daí.

## Funcionalidades

No postman envie uma requisição rest para http://localhost:5000/buy com um json com os campos product_id, user_id e ft. abaixo temos um exemplo em curl que você pode importar.
```bash
curl --request POST \
  --url http://localhost:5000/buy \
  --header 'Content-Type: application/json' \
  --data '{"product_id": "1",
  "user_id" : "2",
  "ft" : "True"}'
  ```

## Containers

Serão criados cinco containers no total:
### ecommerce-1 
Responsável pela requisição 0.
### store-1 
Responsável pelas requisições 1 e 3.
### exchange-1 
Responsável pela requisição 2.
### fidellity-1 
Responsável pela requisição 4. 
### database-1 
Responsável por  simular o funcionamento de um banco de dados.
