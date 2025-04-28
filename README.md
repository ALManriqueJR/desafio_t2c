# Desagio T2C

Este projeto é um **scraper automatizado** que coleta informações de notebooks no site da Magazine Luiza, organiza os dados em uma planilha Excel e envia o arquivo por e-mail usando o serviço **SendGrid**.

## 📂 Estrutura do Projeto

| Tipo          | Item                       | Descrição                          |
|---------------|----------------------------|------------------------------------|
| Pasta         | dependencies/              | Ambiente virtual (não versionado)  |
| Arquivo       | .env                       | Variáveis de ambiente              |
| Arquivo       | main.py                    | Código principal                   |
| Arquivo       | send_to_email.py     		 | Função de envio de e-mail          |
| Arquivo       | requirements.txt           | Dependências do projeto            |
| Pasta         | Output/                    | Arquivos Excel gerados             |


## Como Rodar o Projeto ?

pip install -r requirements.txt
SENDGRID_TOKEN=seu_token_sendgrid_aqui (dentro do .env)

executar

## 📈 Resultado

O script irá gerar um arquivo Notebooks.xlsx na pasta Output, e enviá-lo por e-mail.

O Excel gerado possui duas abas:
	- Melhores: notebooks com 100 ou mais avaliações.
	- Piores: notebooks com menos de 100 avaliações.

## ⚠️ Atenção

- **O scraper depende da estrutura atual do site Magazine Luiza, logo, mudanças no site podem exigir atualização dos seletores!**
- **Nunca publique seu token de API's publicamente.** 
- **Respeite os termos de uso do site ao utilizar scraping. Consulte as [Regras da MagazineLuiza](https://www.magazineluiza.com.br/robots.txt)**

## 🤝 Contribuições

- *Contribuições são bem-vindas! Sinta-se à vontade para abrir Issues ou enviar Pull Requests. Também estou aprendendo :)*
