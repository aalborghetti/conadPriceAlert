# Script per la ricerca di offerte tra i prodotti del sito Conad.
# L'elenco delle pagine web dei singoli prodotti vanno aggiunte al file prodotti.txt

from bs4 import BeautifulSoup
import requests
import asyncio
import telegram

# funzione di scrape del sito web
def scrape(site):
    global DESCRIZIONE, MARCA, PREZZO_PRECEDENTE, PREZZO_ATTUALE, PRODOTTO
    
    # acquisizione del contenuto della pagina web
    response = requests.get(site)
       
    # conversione del codice pagina in testo analizzabile
    soup = BeautifulSoup(response.text,"lxml")

    # porzione di pagina con l'elenco dei prodotti
    contenitore = soup.find("div", class_ = "add-to-cart-product-inner")
   
    # estrazione dati dalla pagina
    try:
        DESCRIZIONE = contenitore.find("h1", class_ = "product-title").get_text().strip()
        #print (DESCRIZIONE)
        MARCA = contenitore.find("div", class_ = "product-title").get_text().strip()
        #print (MARCA)
        PREZZO_PRECEDENTE = contenitore.find("div", class_ = "product-price").get_text().strip()
        #print (PREZZO_PRECEDENTE)
        PREZZO_ATTUALE = contenitore.find("div", class_ = "product-price").get_text().strip()
        #print (PREZZO_ATTUALE)
    except:
        PREZZO_PRECEDENTE = ""
        pass

# procedura di invio di un messaggio tramite bot di telegram
async def notifica():
    global DESCRIZIONE, MARCA, PREZZO_PRECEDENTE, PREZZO_ATTUALE, PRODOTTO

    bot = telegram.Bot('6689931169:AAFo47UCPlX1W5N702gA3iFtWaLfgJynW5A')

    if (PREZZO_PRECEDENTE):
        async with bot:
            await bot.send_message(text="Prodotto in offerta:\n" + DESCRIZIONE + "\n" + "Marca: " + MARCA + "\n" + "Vecchio Prezzo: " + PREZZO_PRECEDENTE + "\n" + "Nuovo Prezzo: " + PREZZO_ATTUALE + "\n" + PRODOTTO, chat_id=151081150)

# funzione principale
if __name__ =="__main__":
    global PRODOTTO

    file = open('prodotti.txt', 'r')
    prodotti = file.readlines()
 
    for PRODOTTO in prodotti:
        # avvio della scansione della pagina
        scrape(PRODOTTO)

        # invio notifica
        asyncio.run(notifica())
