#EJERCICIO COMPLETO CON LA PARTE BONUS DE OPTIMIZACIÓN DEL INVENTARIO


import random
from collections import Counter

class Biblioteca:
    def __init__(self):
        self.libros = {}
        self.historial_lecturas = {}
        self.usuarios = {}
        self.reseñas = {}
        self.calificaciones = {}

    def agregar_libro(self, titulo, autor, cantidad, genero):
        """Agrega un libro con su título, autor, cantidad disponible y género."""
        self.libros[titulo] = {"autor": autor, "cantidad": cantidad, "genero": genero}
        print(f"Libro agregado: {titulo} por {autor} (Cantidad: {cantidad}, Género: {genero})")

    def prestar_libro(self, usuario, titulo):
        """Presta un libro, reduciendo su cantidad disponible."""
        if titulo in self.libros and self.libros[titulo]["cantidad"] > 0:
            self.libros[titulo]["cantidad"] -= 1
            self.historial_lecturas.setdefault(usuario, []).append(titulo)
            self.calificaciones.setdefault(usuario, {}).setdefault(titulo, None)
            print(f"{usuario} ha tomado prestado '{titulo}'.")
        else:
            print(f"Lo sentimos, '{titulo}' no está disponible.")

    def devolver_libro(self, usuario, titulo):
        """Devuelve un libro, aumentando su cantidad disponible."""
        if titulo in self.libros:
            self.libros[titulo]["cantidad"] += 1
            print(f"{usuario} ha devuelto '{titulo}'.")
        else:
            print(f"El libro '{titulo}' no pertenece a nuestra biblioteca.")

    def libro_disponible(self, titulo):
        """Consulta si un libro está disponible."""
        disponible = self.libros.get(titulo, {}).get("cantidad", 0) > 0
        print(f"'{titulo}' está {'disponible' if disponible else 'no disponible'}.")
        return disponible

    def sugerir_siguiente_libro(self, usuario):
        """Sugiere el próximo libro basado en el género del último libro leído."""
        if usuario in self.historial_lecturas and self.historial_lecturas[usuario]:
            ultimo_libro = self.historial_lecturas[usuario][-1]
            genero = self.libros.get(ultimo_libro, {}).get("genero")
            sugerencias = [
                titulo for titulo, info in self.libros.items()
                if info["genero"] == genero and titulo != ultimo_libro
            ]
            if sugerencias:
                sugerencia = random.choice(sugerencias)
                print(f"Sugerencia para {usuario}: '{sugerencia}'.")
                return sugerencia
        print("No hay recomendaciones disponibles.")
        return None

    def dejar_reseña(self, usuario, titulo, calificacion, comentario):
        """Permite a un usuario dejar una reseña y calificación de un libro."""
        if titulo in self.libros:
            self.reseñas.setdefault(titulo, []).append({"usuario": usuario, "calificacion": calificacion, "comentario": comentario})
            self.calificaciones.setdefault(usuario, {}).setdefault(titulo, calificacion)
            print(f"{usuario} ha dejado una reseña para '{titulo}'.")
        else:
            print(f"El libro '{titulo}' no está registrado en la biblioteca.")

    def mostrar_reseñas(self, titulo):
        """Muestra las reseñas de un libro."""
        if titulo in self.reseñas:
            print(f"Reseñas para '{titulo}':")
            for reseña in self.reseñas[titulo]:
                print(f"- {reseña['usuario']} (Calificación: {reseña['calificacion']}): {reseña['comentario']}")
        else:
            print(f"No hay reseñas para '{titulo}'.")

    def recomendar_libro(self, usuario):
        """Recomienda un libro utilizando análisis colaborativo."""
        if usuario not in self.historial_lecturas or not self.historial_lecturas[usuario]:
            print("No hay suficiente información para recomendar.")
            return None

        usuarios_similares = [
            u for u in self.historial_lecturas
            if u != usuario and set(self.historial_lecturas[u]) & set(self.historial_lecturas[usuario])
        ]

        recomendaciones = Counter()
        for u in usuarios_similares:
            for libro, calificacion in self.calificaciones[u].items():
                if calificacion and libro not in self.historial_lecturas[usuario]:
                    recomendaciones[libro] += calificacion

        if recomendaciones:
            mejor_libro = max(recomendaciones, key=recomendaciones.get)
            print(f"Recomendación para {usuario}: '{mejor_libro}' basado en usuarios similares.")
            return mejor_libro
        else:
            print("No hay recomendaciones disponibles.")
            return None

# Ejemplo de uso
biblioteca = Biblioteca()
biblioteca.agregar_libro("1984", "George Orwell", 3, "Ciencia ficción")
biblioteca.agregar_libro("Brave New World", "Aldous Huxley", 2, "Ciencia ficción")
biblioteca.agregar_libro("Orgullo y Prejuicio", "Jane Austen", 1, "Romance")

usuario1 = "Carlos"
biblioteca.prestar_libro(usuario1, "1984")
biblioteca.dejar_reseña(usuario1, "1984", 5, "¡Un muy buen libro!")

usuario2 = "Ana"
biblioteca.prestar_libro(usuario2, "1984")
biblioteca.prestar_libro(usuario2, "Brave New World")
biblioteca.dejar_reseña(usuario2, "1984", 4, "Muy bueno, pero un poco sombrío.")
biblioteca.dejar_reseña(usuario2, "Brave New World", 5, "¡Me ha encantado!")

biblioteca.sugerir_siguiente_libro(usuario1)
biblioteca.recomendar_libro(usuario1)
biblioteca.mostrar_reseñas("1984")

