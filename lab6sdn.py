import yaml

data = {
    "alumnos": [],
    "cursos": [],
    "servidores": []
}

def importar_datos(nombre_archivo):
    """Importar datos desde un archivo YAML."""
    global data
    try:
        with open(nombre_archivo, 'r') as archivo:
            datos_importados = yaml.safe_load(archivo)
            if "alumnos" in datos_importados:
                data["alumnos"] = datos_importados["alumnos"]
            if "cursos" in datos_importados:
                data["cursos"] = datos_importados["cursos"]
            if "servidores" in datos_importados:
                data["servidores"] = datos_importados["servidores"]
            print(f"Datos importados correctamente desde {nombre_archivo}.")
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo} no existe.")
    except yaml.YAMLError as e:
        print(f"Error al leer el archivo YAML: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

def exportar_datos(nombre_archivo):
    global data
    try:
        with open(nombre_archivo, 'w') as archivo:
            yaml.dump(data, archivo)
        print(f"Datos exportados correctamente a {nombre_archivo}.")
    except Exception as e:
        print(f"Error al exportar datos: {e}")

def listar_alumnos():
    if not data["alumnos"]:
        print("No hay alumnos disponibles para listar.")
        return

    print("\nOpcional: Puedes aplicar un filtro por nombre.")
    filtro = input("Ingrese una parte del nombre del alumno (o presione Enter para mostrar todos): ").strip().lower()

    alumnos_filtrados = [alumno for alumno in data["alumnos"] if filtro in alumno["nombre"].lower()]
    
    if not alumnos_filtrados:
        print("No se encontraron alumnos que coincidan con el filtro.")
        return
    
    print("\nAlumnos existentes:")
    for alumno in alumnos_filtrados:
        print(f"- {alumno['nombre']} (Código: {alumno['codigo']}, MAC: {alumno['mac']})")


def listar_servidores():
    global data
    servidores = data.get("servidores", [])
    if servidores:
        print("Servidores:")
        for servidor in servidores:
            nombre = servidor.get("nombre", "Nombre")
            ip = servidor.get("ip", "IP")
            print(f"- Nombre: {nombre}, IP: {ip}")
    else:
        print("No hay servidores registrados.")



def mostrar_detalle_servidor(nombre_servidor):
    global data
    servidores = data.get("servidores", [])
    for servidor in servidores:
        if servidor.get("nombre") == nombre_servidor:
            print("\nDetalles del Servidor:")
            for clave, valor in servidor.items():
                print(f"{clave.capitalize()}: {valor}")
            return
    print(f"No se encontró un servidor con el nombre '{nombre_servidor}'.")



def mostrar_detalle_alumno():
    if not data["alumnos"]:
        print("No hay alumnos disponibles para mostrar.")
        return

    codigo_alumno = input("\nIngrese el código del alumno para mostrar detalles: ").strip()
    alumno_encontrado = next((alumno for alumno in data["alumnos"] if str(alumno["codigo"]) == codigo_alumno), None)

    if alumno_encontrado:
        print(f"\nDetalles del alumno {codigo_alumno}:")
        print(f"Nombre: {alumno_encontrado['nombre']}")
        print(f"Código: {alumno_encontrado['codigo']}")
        print(f"MAC: {alumno_encontrado['mac']}")
    else:
        print(f"No se encontró un alumno con el código {codigo_alumno}.")

def listar_cursos():
    if not data["cursos"]:
        print("No hay cursos disponibles para listar.")
        return

    print("\nCursos existentes:")
    for curso in data["cursos"]:
        print(f"- {curso['nombre']} (Código: {curso['codigo']}, Estado: {curso['estado']})")

def mostrar_detalle_curso():
    if not data["cursos"]:
        print("No hay cursos disponibles para mostrar.")
        return

    codigo_curso = input("\nIngrese el código del curso para mostrar detalles: ").strip()
    curso_encontrado = next((curso for curso in data["cursos"] if curso["codigo"] == codigo_curso), None)

    if curso_encontrado:
        print(f"\nDetalles del curso {codigo_curso}:")
        print(f"Nombre: {curso_encontrado['nombre']}")
        print(f"Código: {curso_encontrado['codigo']}")
        print(f"Estado: {curso_encontrado['estado']}")
        print("Alumnos matriculados:")
        for alumno_codigo in curso_encontrado['alumnos']:
            alumno = next((alumno for alumno in data["alumnos"] if alumno["codigo"] == alumno_codigo), None)
            if alumno:
                print(f"- {alumno['nombre']} (Código: {alumno['codigo']})")
        print("Servidores asociados:")
        for servidor in curso_encontrado['servidores']:
            print(f"- {servidor['nombre']} (Servicios permitidos: {', '.join(servidor['servicios_permitidos'])})")
    else:
        print(f"No se encontró un curso con el código {codigo_curso}.")

def menu_principal():
    while True:
        print("\nMenú Principal")
        print("1) Importar")
        print("2) Exportar")
        print("3) Cursos")
        print("4) Alumnos")
        print("5) Servidores")
        print("8) Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            nombre_archivo = input("Ingrese el nombre del archivo YAML a importar: ")
            importar_datos(nombre_archivo)
        elif opcion == '2':
            nombre_archivo = input("Ingrese el nombre del archivo YAML para exportar: ")
            exportar_datos(nombre_archivo)
        elif opcion == '3':
            print("\nOpciones de Cursos:")
            print("1) Listar cursos")
            print("2) Mostrar detalle de un curso")
            sub_opcion = input("Seleccione una opción: ")
            
            if sub_opcion == '1':
                listar_cursos()
            elif sub_opcion == '2':
                mostrar_detalle_curso()
            else:
                print("Opción inválida.")
        elif opcion == '4':
            print("\nOpciones de Alumnos:")
            print("1) Listar alumnos")
            print("2) Mostrar detalle de un alumno")
            sub_opcion = input("Seleccione una opción: ")
            
            if sub_opcion == '1':
                listar_alumnos()
            elif sub_opcion == '2':
                mostrar_detalle_alumno()
            else:
                print("Opción inválida.")

        elif opcion == '5':
            print("\nOpciones de Servidores:")
            print("1) Listar Servidores")
            print("2) Mostrar detalle de servidores")
            sub_opcion = input("Seleccione una opción: ")

            if sub_opcion == '1':
                listar_servidores()
            elif sub_opcion == '2':
                sub_opcion2 = input("Ingrese el servidor para ver el detalle: ")
                mostrar_detalle_servidor(sub_opcion2)

            else:
                print("Opción inválida.")

        elif opcion == '8':
            print("Cerrando programa en 3 2 1 ...")
            break
        else:
            print("Ingrese una opción válida.")


def main():
    importar_datos('database.yaml') 
    menu_principal()


if __name__ == "__main__":
    main()

