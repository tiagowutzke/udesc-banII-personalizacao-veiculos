# BLIP | Painel de imagens e vídeos

Este repositório contém a implementação de um app criado para o upload de imagens e vídeos no 
AWS S3 com a finalidade da utilização desses contéudos nas trilhas do chatbot.
 
O app está disponível [aqui](#).

## Escopo
Para a disponibilização de imagens, vídeos ou áudios no chatbot da Blip, é necessário informar um link público do arquivo. 
Com isso, é necessário um ambiente para armazenamento desses conteúdos e que contemplem os requisitos:

1 - Que o ambiente seja seguro, sem risco de perda dos conteúdos armazenados

2 - Que seja possível disponibilizar um link público de acesso ao arquivo, para que seja disponibilzado na janela de
conversa do chatbot.  

## ESPECIFICAÇÕES TÉCNICAS

### Deploy

Os passos contendo asterísco são realizados apenas uma única vez. 

1* - Caso ainda não tenha o Heroku instalado, instale-o através do seguinte comando:
```shell script
sudo snap install --classic heroku
```

2 - Navegue até a pasta do repositório de operations (exemplo):
```shell script
cd Github/operations/
```

3* - Faça login no heroku:
 
*as credencias estão no LastPass, na pasta BA Internal*
```
heroku login
``` 
 
4* - Sincronize seu ambiente git com o ambiente git do app no Heroku:
 ```shell script
heroku git:remote -a blip-multimedia-panel
```

5 - Faça o deploy **apenas da pasta do projeto Blip Multimedia**:
```shell script
git subtree push --prefix Take/heroku/Painel\ de\ imagens\ e\ vídeos/ heroku master
```




### Stack utilizada

**Python**
- Lóginas de interface para persistência de dados

**Python Flask**
- Conteúdo dinâmico nas páginas html da aplicação
- Configuração de rotas das páginas da aplicação e das APIs

**Html, Css, Javascript**
- Front-end da aplicação

**Postgres**
- Persistência dos dados referentes ao conteúdo multimídia

**AWS S3**
- Para armazenamento e consulta do conteúdo multimídia


