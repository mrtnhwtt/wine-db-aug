from bs4 import BeautifulSoup
import urllib.request

with urllib.request.urlopen('https://www.vivino.com/search/wines?q=Rainstorm%202013%20Pinot%20Gris') as webPageResponse:
    outputHtml = webPageResponse.read()
with open('out.html', 'w') as f:
        f.write(str(outputHtml))
getpage_soup= BeautifulSoup(outputHtml, 'html.parser')
all_class_topsection= getpage_soup.findAll('figure', {'class':'wine-card__image'})
style = str(all_class_topsection[0]['style'])
style = style.replace('background-image: url(', 'https:')[:-1]
print(style)