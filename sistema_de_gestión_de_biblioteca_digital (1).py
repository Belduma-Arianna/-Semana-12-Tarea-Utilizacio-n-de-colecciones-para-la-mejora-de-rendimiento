class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        # Almacena el título y el autor como una tupla, asegurando que no cambien después de la creación.
        self.datos_base = (titulo, autor)
        # Almacena la categoría del libro.
        self.categoria = categoria
        # Almacena el ISBN del libro, usado como identificador único.
        self.isbn = isbn

    def __str__(self):
        # Representación en cadena del objeto Libro para una fácil visualización.
        return f"'{self.datos_base[0]}' - {self.datos_base[1]} [{self.categoria}]"

class Usuario:
    def __init__(self, nombre, user_id):
        # Nombre completo del usuario.
        self.nombre = nombre
        # ID único del usuario, para identificarlo en la biblioteca.
        self.user_id = user_id
        # Requisito: Lista para gestionar libros prestados
        # Almacena los objetos Libro que el usuario tiene actualmente prestados.
        self.libros_prestados = []

    def __str__(self):
        # Representación en cadena del objeto Usuario.
        return f"Usuario: {self.nombre} (ID: {self.user_id})"

class Biblioteca:
    def __init__(self):
        # Requisito: Diccionario para búsqueda eficiente por ISBN
        # Almacena los objetos Libro, usando el ISBN como clave para un acceso rápido.
        self.libros = {}
        # Requisito: Conjunto para IDs de usuarios únicos
        # Almacena los IDs de los usuarios registrados para garantizar su unicidad y eficiencia en la búsqueda.
        self.usuarios_ids = set()
        # Diccionario para almacenar los objetos Usuario, usando el user_id como clave.
        self.usuarios_objetos = {}

    def añadir_libro(self, libro):
        # Añade un objeto Libro al catálogo de la biblioteca.
        self.libros[libro.isbn] = libro
        print(f"Éxito: Libro '{libro.datos_base[0]}' añadido al catálogo.")

    def quitar_libro(self, isbn):
        # Elimina un libro del catálogo usando su ISBN.
        if isbn in self.libros:
            eliminado = self.libros.pop(isbn) # Elimina el libro del diccionario y lo retorna.
            print(f"Éxito: Libro '{eliminado.datos_base[0]}' eliminado.")
        else:
            print("Error: El ISBN no existe en la biblioteca.")

    def registrar_usuario(self, usuario):
        # Registra un nuevo usuario en el sistema de la biblioteca.
        if usuario.user_id not in self.usuarios_ids:
            self.usuarios_ids.add(usuario.user_id) # Añade el ID al conjunto de IDs únicos.
            self.usuarios_objetos[usuario.user_id] = usuario # Almacena el objeto Usuario.
            print(f"Éxito: Usuario '{usuario.nombre}' registrado correctamente.")
        else:
            print("Error: El ID de usuario ya está registrado.")

    def dar_de_baja_usuario(self, user_id):
        # Elimina un usuario del sistema de la biblioteca si no tiene libros prestados.
        if user_id in self.usuarios_ids:
            usuario = self.usuarios_objetos[user_id]
            # Solo se puede eliminar si no tiene libros pendientes
            if not usuario.libros_prestados:
                self.usuarios_ids.remove(user_id)
                del self.usuarios_objetos[user_id]
                print(f"Éxito: Usuario con ID {user_id} dado de baja.")
            else:
                print("Error: El usuario tiene libros prestados y no puede ser eliminado.")
        else:
            print("Error: Usuario no encontrado.")

    def prestar_libro(self, isbn, user_id):
        # Gestiona el préstamo de un libro a un usuario.
        if isbn in self.libros and user_id in self.usuarios_ids:
            libro = self.libros.pop(isbn) # Se saca del catálogo principal de la biblioteca.
            self.usuarios_objetos[user_id].libros_prestados.append(libro) # Se añade a la lista de libros prestados del usuario.
            print(f"Éxito: Libro '{libro.datos_base[0]}' prestado.")
        else:
            print("Error: El ISBN no está disponible o el Usuario no existe.")

    def devolver_libro(self, isbn, user_id):
        # Gestiona la devolución de un libro por parte de un usuario.
        if user_id in self.usuarios_ids:
            usuario = self.usuarios_objetos[user_id]
            # Itera sobre los libros prestados del usuario para encontrar el libro a devolver.
            for libro in usuario.libros_prestados:
                if libro.isbn == isbn:
                    usuario.libros_prestados.remove(libro) # Elimina el libro de la lista del usuario.
                    self.libros[isbn] = libro # Vuelve a añadir el libro al catálogo principal.
                    print(f"Éxito: Libro '{libro.datos_base[0]}' devuelto.")
                    return
            print("Error: El usuario no tiene ese libro prestado.")
        else:
            print("Error: Usuario no encontrado.")

    def buscar_libros(self, busqueda):
        # Busca libros por título, autor o categoría, ignorando mayúsculas/minúsculas.
        encontrados = [l for l in self.libros.values() if
                      busqueda.lower() in l.datos_base[0].lower() or
                      busqueda.lower() in l.datos_base[1].lower() or
                      busqueda.lower() in l.categoria.lower()]
        return encontrados

    def listar_prestados(self, user_id):
        # Retorna la lista de libros prestados a un usuario específico.
        if user_id in self.usuarios_ids:
            return self.usuarios_objetos[user_id].libros_prestados
        return None # Retorna None si el usuario no existe.

# --- MENÚ INTERACTIVO ---

def ejecutar_sistema():
    # Crea una instancia de la biblioteca.
    mi_biblioteca = Biblioteca()

    while True:
        # Muestra las opciones del menú principal.
        print("\n=== MENÚ BIBLIOTECA DIGITAL ===")
        print("1. Añadir Libro")
        print("2. Quitar Libro")
        print("3. Registrar Usuario")
        print("4. Dar de Baja Usuario")
        print("5. Prestar Libro")
        print("6. Devolver Libro")
        print("7. Buscar Libro")
        print("8. Listar Prestados")
        print("9. Salir")

        # Solicita al usuario que seleccione una opción.
        opc = input("\nSeleccione una opción: ")

        # Maneja las diferentes opciones del menú.
        if opc == "1":
            l = Libro(input("Título: "), input("Autor: "), input("Categoría: "), input("ISBN: "))
            mi_biblioteca.añadir_libro(l)
        elif opc == "2":
            mi_biblioteca.quitar_libro(input("ISBN del libro a eliminar: "))
        elif opc == "3":
            u = Usuario(input("Nombre completo: "), input("ID único: "))
            mi_biblioteca.registrar_usuario(u)
        elif opc == "4":
            mi_biblioteca.dar_de_baja_usuario(input("ID del usuario a eliminar: "))
        elif opc == "5":
            mi_biblioteca.prestar_libro(input("ISBN del libro: "), input("ID del usuario: "))
        elif opc == "6":
            mi_biblioteca.devolver_libro(input("ISBN del libro: "), input("ID del usuario: "))
        elif opc == "7":
            query = input("Escriba el título, autor o categoría a buscar: ")
            res = mi_biblioteca.buscar_libros(query)
            if res:
                print("\n--- Libros Encontrados ---")
                for r in res: print(f"-> {r}")
            else:
                print(f"\n[!] No se encontró ningún libro relacionado con: '{query}'")
        elif opc == "8":
            uid = input("ID del usuario: ")
            lista = mi_biblioteca.listar_prestados(uid)
            if lista is not None:
                print(f"\nLibros prestados al ID {uid}:")
                if not lista:
                    print(" - Ningún libro actualmente.")
                else:
                    for b in lista: print(f" -> {b}")
            else:
                print("Error: El usuario no existe.")
        elif opc == "9":
            print("Cerrando el sistema de biblioteca. ¡Hasta luego!")
            break # Sale del bucle y termina el programa.
        else:
            print("Opción no válida. Intente de nuevo.")

# Punto de inicio del programa
# Asegura que ejecutar_sistema() solo se llama cuando el script se ejecuta directamente.
if __name__ == "__main__":
    ejecutar_sistema()
