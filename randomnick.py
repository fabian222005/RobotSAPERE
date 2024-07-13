import random

# Listas de sustantivos y adjetivos
sustantivos = ["Cubo", "Gato", "León", "Dragón", "Héroe", "Mago", "Rey", "Carro", "Ninja", "Robot"]
adjetivos = ["Juguetón", "Valiente", "Rápido", "Feliz", "Tranquilo", "Astuto", "Feroz", "Amable", "Poderoso", "Misterioso"]

def generar_nick():
    # Escoge un sustantivo y un adjetivo al azar
    sustantivo = random.choice(sustantivos)
    adjetivo = random.choice(adjetivos)
    # Genera un número aleatorio entre 100 y 999
    numero = random.randint(100, 999)
    # Combina las partes para formar el nick
    nick = f"{sustantivo}{adjetivo}{numero}"
    return nick

