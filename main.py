from get_module import get_info
from poke_validation import validate
from string import Template
from genera_spanol import genera_spanol
import random

#================================================================================================================
# Validacion del nombre "de datos"


nombre = input('Introduzca el nombre del Pokemon: ')
nombre = validate(nombre)
p_nombre = nombre.capitalize()
print(p_nombre)

url1 = f"https://pokeapi.co/api/v2/pokemon/{nombre}"

datos_base = get_info(url1)
p_id = datos_base["id"]


p_img = datos_base["sprites"]["front_default"]#Obtener img atraves del nombre
print(datos_base["id"])
#==================================================================================================================

# Obtener atributos del pokémon
stats = []
for item in datos_base["stats"]:
    stats.append(item["base_stat"])

print(stats)
p_hp, p_at, p_de, p_ate, p_dee, p_ve = stats
print(p_ve)

#============================================================================================================
#Obtener tipos del pokémon
tipos_lista = datos_base["types"]
tipos = []
for item in tipos_lista:
    tipos.append(item["type"]["name"])
print(tipos)

#=================================================================================================================
#Obtencion de la descripción
#Obtener descripcion del pokémon pre evolucionado
url2 =  f"https://pokeapi.co/api/v2/pokemon-species/{nombre}"
datos_ps = get_info(url2)
if datos_ps["evolves_from_species"] is None:
    p_etapa=""
else:
    evolves_from = datos_ps["evolves_from_species"]["name"]#Solicitar API evolucion y atributo name
    p_etapa = f"Etapa previa: {evolves_from.capitalize()}"#Respuesta primera letra mayuscula
print (p_etapa)

comentarios = datos_ps["flavor_text_entries"]
comentarios_es = []
for item in comentarios:
    if item["language"]["name"] == "es":
        comentarios_es.append(item["flavor_text"].replace("\n"," "))
#print(comentarios_es)
p_comentario = random.choice(comentarios_es)

#================================================================================================================================
""" #Obtener tipo de efectividad
tipos_sec = get_info(url1)
p_id = datos_base["id"]
print(datos_base["id"])

#================================================================================================

#Obtener tipo de debilidad
tipos_dc = get_info(url1)
p_id = datos_base["id"]
print(datos_base["id"])

 """

#============================================================================
#Obtener lista de tipos
def procesa_tipos(lista_tipos,caracteristica):
    tipos_total = []
    for type in lista_tipos:
        url3 = f" https://pokeapi.co/api/v2/type/{type}"

        datos_type = get_info(url3)
        lista_sec = datos_type["damage_relations"][caracteristica]

        for item in lista_sec:
            tipos_total.append(item["name"])
    
    tipos_total_filtrado = set(tipos_total) #Elimina los datos repetidos
    tipos_total = list(tipos_total_filtrado) # Ordena los datos ya filtrados 
    tipos_total.sort() # Ordena los datos en orden alfabético
    return tipos_total
#================================================================
# Obtener tipo de Pokemon
p_tipos = genera_spanol(tipos)
print(p_tipos)

#Obtener caracteristicas del Pokemon

#Generar lista super efectivo contra
tipos_sec = genera_spanol(procesa_tipos(tipos, "double_damage_to")) # 

tipos_dc = genera_spanol(procesa_tipos(tipos, "double_damage_from"))

tipos_rc = genera_spanol(procesa_tipos(tipos,"half_damage_from"))

tipos_pec = genera_spanol(procesa_tipos(tipos,"half_damage_to"))

tipos_imc = genera_spanol(procesa_tipos(tipos, "no_damage_from"))

tipo_inc = genera_spanol(procesa_tipos(tipos,"no_damage_to"))








# ===========================================================================
# Reemplazar los valores del template por nuevos entregados por API python

#Abrir html en modo lectura
with open('input.html','r') as infile:
    entrada = infile.read()

#La Clase Template del módulo string reemplaza los valores en un Template. las variables son identificadas al anteponer el nombre con $
document_template = Template(entrada)


#variable HTML = variable Python
document_template_nuevo = document_template.substitute(
    p_id = p_id, p_nombre = p_nombre, p_img= p_img, p_etapa = p_etapa,p_hp = p_hp, 
    p_at = p_at, p_de = p_de, p_ate = p_ate, p_dee = p_dee, p_ve = p_ve, p_tipos = p_tipos,
    p_comentario = p_comentario, tipos_sec = tipos_sec, tipos_dc = tipos_dc, tipos_imc = tipos_imc, tipos_inc = tipo_inc,
    tipos_rc = tipos_rc, tipos_pec = tipos_pec)

#Escribir resultado en un archivo html
with open('output.html','w') as outfile:
    outfile.write(document_template_nuevo)

