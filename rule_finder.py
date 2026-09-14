from bs4 import BeautifulSoup
from urllib.request import urlopen
import json

html = urlopen("https://www.dndbeyond.com/sources/dnd/br-2024?srsltid=AfmBOopmBJQJTTB7ewIUEWCXlGSOokg0SZAHUiuwidz63pRzOmnFMDgr").read()
soup = BeautifulSoup(html, features="html.parser")

rule_items = soup.select("h3 ~ ul a")

spells_html = urlopen("https://www.dndbeyond.com/sources/dnd/br-2024/spell-descriptions")
spell_soup = BeautifulSoup(spells_html, features="html.parser")

spell_items = spell_soup.find_all("a", {"class": "tooltip-hover spell-tooltip"})

rule_dict = {link.text.lower(): "https://www.dndbeyond.com" + link.get("href") for link in rule_items}

spell_dict = {spell.text.lower():"https://dndbeyond.com" + spell.get("href") for spell in spell_items}

rule_dict.update(spell_dict)

for i in rule_dict:
    print(i , rule_dict[i])

with open("rules.json","w") as f:
    json.dump(rule_dict, f)