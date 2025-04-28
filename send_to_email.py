import os
import base64

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from dotenv import load_dotenv

load_dotenv()

def get_anexo(caminho:str):
    with open(caminho, 'rb') as f:
        conteudo = f.read()
    return conteudo

def enviar(caminho:str):
    TOKEN = os.getenv('SENDGRID_TOKEN')
    
    if not TOKEN:
        print('Erro no TOKEN!')
        return
    
    conteudo_encoded = base64.b64encode(get_anexo(caminho)).decode()
    
    anexo = Attachment(
        FileContent(conteudo_encoded),
        FileName(os.path.basename(caminho)),
        FileType('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
        Disposition('attachment')
    )
    
    message = Mail(
        from_email=os.getenv('EMAIL'),
        to_emails=os.getenv('EMAIL'),
        subject='Relatório Notebooks',
        html_content='<p>Olá, aqui está o seu relatório dos notebooks extraídos da Magazine Luiza.<br>Atenciosamente,<br>Robô</p>'
    )
    
    message.attachment = [anexo]
    
    sg = SendGridAPIClient(TOKEN)
    sg.send(message)