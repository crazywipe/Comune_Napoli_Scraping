import requests
import bs4
import time

#funzione di notifica email
def notifica_mail(news):
    import smtplib
    from email.message import EmailMessage

    # imposta email e password
    email_address = "inserire mail mittente"
    email_password = "inserire password mittente"

    # crea email
    msg = EmailMessage()
    msg['Subject'] = "Aggiornamento sito web Comune di Napoli"
    msg['From'] = email_address
    msg['To'] = "inserire mail destinatario"
    msg.set_content(f"Il sito web è stato aggiornato.\n\nUltima news inserita: \n{news}.\n\nPer consultare gli aggiornamenti clicca qui: https://www.comune.napoli.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/46073")

    # invia email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)



#get request della pagina web
pagina_web = requests.get("https://www.comune.napoli.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/46073")

#utilizzo di librerie beautiful soup per la formattazione
soup = bs4.BeautifulSoup(pagina_web.text,"lxml")

#punta all'ultimo aggiornamento del sito in ordine cronologico
ultimo_aggiornamento = soup.select(".viewAnchor")[0]

#invia via mail l'ultimo aggiornamento disponibile in ordine cronologico
notifica_mail(ultimo_aggiornamento.text)

#ciclo infinito che controlla aggiornamenti della pagina web a intervalli di 60 sec
while True:
    
    nuovo_aggiornamento = soup.select(".viewAnchor")[0]
    
    if nuovo_aggiornamento.text != ultimo_aggiornamento.text:
        print(f"Ultima news inserita: {nuovo_aggiornamento.text}. |*** Per consultare gli aggiornamenti clicca qui: https://www.comune.napoli.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/46073")
        ultimo_aggiornamento = soup.select(".viewAnchor")[0]
        notifica_mail(ultimo_aggiornamento.text)
        
    time.sleep(60)
