from get_module import get_info
from poke_validation import validate
from string import Template
import random

nombre = input('Introduzca el nombre del Pokemon: ')
nombre = validate(nombre)
p_nombre = nombre.capitalize()

url1 = f"https://pokeapi.co/api/v2/pokemon/{nombre}"

datos_base = get_info(url1)
p_id = datos_base["id"]

print(p_nombre)
print(datos_base["id"])

p_img = datos_base["sprites"]["front_default"]

url2 =  f"https://pokeapi.co/api/v2/pokemon-species/{nombre}"

datos_ps = get_info(url2)
if datos_ps["evolves_from_species"] is None:
    p_etapa=""
else:
    evolves_from = datos_ps["evolves_from_species"]["name"]
    p_etapa = f"Etapa previa: {evolves_from.capitalize()}"
print (p_etapa)

stats = []
for item in datos_base["stats"]:
    stats.append(item["base_stat"])

print(stats)
p_hp, p_at, p_de, p_ate, p_dee, p_ve = stats

print(p_ve)

tipos_lista = datos_base["types"]

tipos = []
for item in tipos_lista:
    tipos.append(item["type"]["name"])
print(tipos)

comentarios = datos_ps["flavor_text_entries"]
comentarios_es = []

for item in comentarios:
    if item["language"]["name"] == "es":
        comentarios_es.append(item["flavor_text"].replace("\n"," "))
#print(comentarios_es)

p_comentario = random.choice(comentarios_es)

def genera_span(lista):
    diccionario_es = {
    "normal": "Normal", "fire": "Fuego", "flying": "Volador",
    "steel": "Acero", "water": "Agua", "electric": "Eléctrico",
    "grass": "Planta", "ice": "Hielo", "fighting": "Lucha",
    "poison": "Veneno", "ground": "Tierra", "psychic": "Psíquico",
    "bug": "Bicho", "rock": "Roca", "ghost": "Fantasma",
    "dragon": "Dragón", "dark": "Siniestro", "fairy": "Hada" }

    span_str = ""
    for item in lista:
        item_es = diccionario_es[item]
        span_str = span_str + f'<span class="label{item}">{item_es}</span>'

    return span_str

p_tipos = genera_span(tipos)

print(p_tipos)

with open('input.html','r') as infile:
    entrada = infile.read()

document_template = Template(entrada)

document_template_nuevo = document_template.substitute(
    p_id = p_id, p_nombre = p_nombre, p_img= p_img, p_etapa = p_etapa,p_hp = p_hp, 
    p_at = p_at, p_de = p_de, p_ate = p_ate, p_dee = p_dee, p_ve = p_ve, p_tipos = p_tipos,
    p_comentario = p_comentario)

with open('output.html','w') as outfile:
    outfile.write(document_template_nuevo)


def procesa_tipos(lista_tipos,caracteristica):
    tipos_total = []
    for type in lista_tipos:
        url3 = f" https://pokeapi.co/api/v2/type/{type}"

        datos_type = get_info(url3)
        lista_sec = datos_type["damage_relations"][caracteristica]

        for item in lista_sec:
            tipos_total.append(item["name"])
    
    tipos_total_filtrado = set(tipos_total)
    tipos_total = list(tipos_total_filtrado)
    tipos_total.sort()

    return tipos_total

tipos_sec = procesa_tipos(tipos, "double_damage_to")
print(tipos_sec)

tipos_dc = procesa_tipos(tipos, "double_damage_from")
print(tipos_dc)

tipos_imc = procesa_tipos(tipos, "no_damage_from")
print(tipos_imc)

tipo_inc = procesa_tipos(tipos,"no_damage_to")
print(tipo_inc)











