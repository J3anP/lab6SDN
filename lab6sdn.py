import yaml
import requests
import random
import string
from prettytable import PrettyTable

# -------------------------------------------------
#               VARIABLES GLOBALES:
# -------------------------------------------------

controller_ip = '10.20.12.4'

servidor_mac = 'fa:16:3e:94:7e:5b'

data = {
    "alumnos": [],
    "cursos": [],
    "servidores": []
}

connections = {}

handlers = []

# -------------------------------------------------
#                  BASE DE DATOS:
# -------------------------------------------------

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

# -------------------------------------------------
#                    ALUMNOS:
# -------------------------------------------------

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

# -------------------------------------------------
#                   SERVIDORES:
# -------------------------------------------------

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


# -------------------------------------------------
#                    ALUMNOS:
# -------------------------------------------------

def agregar_alumno(archivo_yaml):
    nombre = input("Ingrese el nombre del alumno: ")
    codigo = input("Ingrese el código del alumno: ")
    mac = input("Ingrese la dirección MAC del alumno: ")
    
    nuevo_alumno = {
        'nombre': nombre,
        'codigo': codigo,
        'mac': mac
    }


    data['alumnos'].append(nuevo_alumno)
    
    try:
        with open(archivo_yaml, 'w') as archivo:
            yaml.dump(data, archivo, default_flow_style=False, allow_unicode=True)
        print("Alumno agregado exitosamente.")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
    



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

# -------------------------------------------------
#                      CURSOS:
# -------------------------------------------------

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


def agregar_alumno_a_curso(archivo_yaml):

    alumnos = data.get("alumnos")
    cursos = data.get("cursos")

    codigo_alumno = input("Ingrese el código del alumno: ").strip()
    alumno = next((a for a in alumnos if str(a["codigo"]) == str(codigo_alumno)), None)

    if not alumno:
        print("El alumno con el código ingresado no existe.")
        return


    codigo_curso = input("Ingrese el código del curso: ").strip()
    curso = next((c for c in cursos if str(c["codigo"]) == str(codigo_curso)), None)

    if not curso:
        print("El curso con el código ingresado no existe.")
        return

    if curso["estado"] != "DICTANDO":
        print(f"El curso '{curso['nombre']}' no se está dictando. No se pueden agregar más alumnos.")
        return

    if codigo_alumno in str(curso["alumnos"]):
        print(f"El alumno con código {codigo_alumno} ya está inscrito en el curso '{curso['nombre']}'.")
        return

    curso["alumnos"].append(int(codigo_alumno))

    try:
        with open(archivo_yaml, 'w') as archivo:
            yaml.dump(data, archivo, default_flow_style=False, allow_unicode=True)
        print(f"Alumno con código {codigo_alumno} agregado exitosamente al curso '{curso['nombre']}'.")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

def buscar_curso_por_servicio(nombre_servicio):
    global data
    aux = True
    data.get("cursos")

    for curso in data.get("cursos", []):
        for servidor in curso.get("servidores", []):
            if nombre_servicio in servidor.get("servicios_permitidos", []):
                if aux:
                    print(f"Cursos encontrados con el servicio '{nombre_servicio}':")
                    aux = False
                print(f"- {curso['nombre']} (Código: {curso['codigo']}, Estado: {curso['estado']})")
                return
    print("No se encontró algún curso que permita el servicio ingresado.")
    return

# -------------------------------------------------
#                   CONEXIONES:
# -------------------------------------------------

def get_attachement_points(dato,flag):
    if flag:
        url = f'http://{controller_ip}:8080/wm/device/?mac={dato}'
    else:
        url = f'http://{controller_ip}:8080/wm/device/?ipv4={dato}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if not data:
            print('No existe un host con la MAC ingresada!')
            return '',0
        else:
            data = data[0]
            switch_DPID,port = data['attachmentPoint'][0]['switchDPID'],data['attachmentPoint'][0]['port']
            #print(switch_DPID,port)
            return switch_DPID,port
    else:
        print(f'Ocurrió un error con el request!')
        return '',0

def get_route(src_dpid,src_port,dst_dpid,dst_port):
    url = f'http://{controller_ip}:8080/wm/topology/route/{src_dpid}/{src_port}/{dst_dpid}/{dst_port}/json'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if not data:
            print('No existe una ruta entre estos dos puntos de conexión!')
            return []
        else:
            lista_ruta = []
            for switch in data:
                switch_DPID, port = switch['switch'], switch['port']['portNumber']
                lista_ruta.append([switch_DPID, port])
            return lista_ruta
    else:
        print(f'Ocurrió un error con el request!')
        return []

def generar_handler():
    handler = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    if handler not in connections.keys():
        return handler
    else:
        generar_handler()


def validar_acceso_servicio(codigo_alumno, nombre_servicio):
    global data
    alumnos = data.get("alumnos")
    cursos = data.get("cursos", [])
    servidores = data.get("servidores", [])

    alumno = next((a for a in alumnos if str(a["codigo"]) == codigo_alumno),None)
    if not alumno:
        print("El alumno con el código ingresado no existe.")
        return False, {}

    for curso in cursos:
        if curso["estado"] == "DICTANDO" and codigo_alumno in str(curso["alumnos"]):
            for servidor_curso in curso["servidores"]:
                if nombre_servicio in servidor_curso["servicios_permitidos"]:
                    servidor = next((s for s in servidores if s["nombre"] == servidor_curso["nombre"]), None)
                    if servidor:
                        servicio = next((svc for svc in servidor["servicios"] if svc["nombre"] == nombre_servicio),None)
                        if servicio:
                            print(f"Acceso autorizado para el servicio '{nombre_servicio}' en '{servidor['nombre']}'")
                            return True, {"servidor": servidor, "servicio": servicio, "alumno": alumno}

    print("El alumno no está autorizado para acceder a este servicio.")
    return False, {}


def crear_conexion():
    global data
    global connections
    global servidor_mac

    codigo_alumno = input("Ingrese el código del alumno: ")
    nombre_servicio = input("Ingrese el nombre del servicio: ")

    print("\n")

    validacion_acceso, datos_servidor_servicio = validar_acceso_servicio(codigo_alumno, nombre_servicio)

    if not validacion_acceso:
        return

    servidor = datos_servidor_servicio.get("servidor")
    servicio = datos_servidor_servicio.get("servicio")
    alumno = datos_servidor_servicio.get("alumno")

    src_dpid, src_port = get_attachement_points(alumno.get("mac"),True)

    if not src_dpid or not src_port:
        print("No se pudo obtener el punto de conexión del alumno.")
        return

    #dst_dpid, dst_port = get_attachement_points(servidor.get("ip"),False)
    dst_dpid, dst_port = get_attachement_points('fa:16:3e:94:7e:5b', True)
    if not dst_dpid or not dst_port:
        print("No se pudo obtener el punto de conexión del servidor.")
        return

    ruta = get_route(src_dpid, src_port, dst_dpid, dst_port)
    if not ruta:
        print("No se pudo encontrar una ruta entre los puntos.")
        return

    handler = generar_handler()
    handlers.append(handler)
    connections[handler] = []
    connections[handler+"-ARP"] = []
    connections[handler +"-INFO"] = [handler,alumno.get("nombre"),alumno.get("mac"),servicio.get("nombre"),servicio.get("protocolo"),servicio.get("puerto"),servidor.get("ip"),servidor.get("nombre")]

    # Flujos normales

    for i in range(0, len(ruta) - 1, 2):
        switch_dpid = ruta[i][0]
        in_port = ruta[i][1]
        out_port = ruta[i + 1][1]

        # Host a Servidor:

        flow = crear_flow(
            switch_dpid=switch_dpid,
            in_port=in_port,
            out_port=out_port,
            mac_src=alumno.get("mac"),
            ip_dst=servidor.get("ip"),
            protocol=servicio.get("protocolo"),
            port_dst=servicio.get("puerto"),
            handler=handler,
            flow_number=len(connections[handler]) + 1
        )
        connections[handler].append(flow)

        flow_arp = crear_arp_flow(
            switch_dpid=switch_dpid,
            in_port=in_port,
            out_port=out_port,
            handler=handler,
            flow_number=len(connections[handler]) + 1)

        connections[handler+"-ARP"].append(flow_arp)

        # Servidor a host:
        flow_reverse = crear_flow_inverso(
            switch_dpid=switch_dpid,
            in_port=out_port,
            out_port=in_port,
            mac_dst=alumno.get("mac"),
            ip_src=servidor.get("ip"),
            protocol=servicio.get("protocolo"),
            port_src=servicio.get("puerto"),
            handler=handler,
            flow_number=len(connections[handler])
        )
        connections[handler].append(flow_reverse)

        flow_arp_reverse = crear_arp_flow(
            switch_dpid=switch_dpid,
            in_port=out_port,
            out_port=in_port,
            handler=handler,
            flow_number=len(connections[handler]))

        connections[handler + "-ARP"].append(flow_arp_reverse)


    print(f"Conexión creada con handler: {handler}")


def crear_flow(switch_dpid, in_port, out_port, mac_src, ip_dst, protocol, port_dst, handler, flow_number):
    flow_name = f"{handler}-{flow_number}"
    flow = {
        "switch": switch_dpid,
        "name": flow_name,
        "priority": "5",
        "eth_type": "0x0800",
        "eth_src": mac_src,
        "ipv4_dst": ip_dst,
        "ip_proto": 6 if protocol == "TCP" else 17,
        "tp_dst": port_dst,
        "in_port": in_port,
        "active": "true",
        "cookie": "0",
        "actions": f"output={out_port}"
    }
    enviar_flow_al_controller(flow)
    #print(flow)
    return flow

def crear_flow_inverso(switch_dpid, in_port, out_port, mac_dst, ip_src, protocol, port_src, handler, flow_number):
    flow_name = f"{handler}-reverse-{flow_number}"
    flow = {
        "switch": switch_dpid,
        "name": flow_name,
        "priority": "5",
        "eth_type": "0x0800",
        "eth_dst": mac_dst,
        "ipv4_src": ip_src,
        "ip_proto": 6 if protocol == "TCP" else 17,
        "tp_src": port_src,
        "in_port": in_port,
        "active": "true",
        "cookie": "0",
        "actions": f"output={out_port}"
    }
    enviar_flow_al_controller(flow)
    #print(flow)
    return flow


def crear_arp_flow(switch_dpid, in_port, out_port, handler, flow_number):
    flow_name = f"{handler}-arp-{flow_number}"
    flow = {
        "switch": switch_dpid,
        "name": flow_name,
        "priority": "5",
        "eth_type": "0x0806",
        "in_port": in_port,
        "active": "true",
        "cookie": "0",
        "actions": f"output={out_port}"
    }
    enviar_flow_al_controller(flow)
    return flow


def enviar_flow_al_controller(flow):
    url = f"http://{controller_ip}:8080/wm/staticflowpusher/json"
    response = requests.post(url, json=flow)
    if response.status_code == 200:
        response
        #print(f"Flow {flow['name']} enviado correctamente al controlador.")
    else:
        print(f"Error al enviar el flow {flow['name']} al controlador.")
        print(response.content)


def eliminar_conexion(handler):
    global connections

    if handler not in connections:
        print("El handler ingresado no existe.")
        return

    for flow in connections[handler]:
        eliminar_flow(flow)
    del connections[handler]

    for flow in connections[handler+"-ARP"]:
        eliminar_flow(flow)
    del connections[handler+"-ARP"]

    del connections[handler + "-INFO"]

    handlers.remove(handler)

    print(f"Conexión con handler {handler} eliminada.")


def eliminar_flow(flow):
    url = f"http://{controller_ip}:8080/wm/staticflowpusher/json"
    response = requests.delete(url, json={"name": flow["name"]})
    if response.status_code == 200:
        response
        #print(f"Flow {flow['name']} eliminado correctamente del controlador.")
    else:
        print(f"Error al eliminar el flow {flow['name']} del controlador.")

def listar_conexiones():
    global handlers
    global connections

    if not handlers:
        print("No hay conexiones.")
    else:
        tablita = PrettyTable(["Handler","Alumno","MAC alumno","Nombre servicio","Protocolo servicio","Puerto servicio","IP servidor","Nombre servidor"])
        for handler in handlers:
            tablita.add_row(connections[handler+"-INFO"])
        print(tablita)


# -------------------------------------------------
#             FUNCIONES PRINCIPALES:
# -------------------------------------------------

def menu_principal():
    while True:
        print("\n###############################################")
        print("      Network Policy Manager de la UPSM")
        print("###############################################")
        print("\n-> Menú Principal\n")
        print("1) Importar")
        print("2) Exportar")
        print("3) Cursos")
        print("4) Alumnos")
        print("5) Servidores")
        print("7) Conexiones")
        print("8) Salir")
        
        opcion = input("Seleccione una opción: ").strip()

        print("\n")

        if opcion == '1':
            nombre_archivo = input("Ingrese el nombre del archivo YAML a importar: ").strip()
            importar_datos(nombre_archivo)
        elif opcion == '2':
            nombre_archivo = input("Ingrese el nombre del archivo YAML para exportar: ").strip()
            exportar_datos(nombre_archivo)
        elif opcion == '3':
            print("\nOpciones de Cursos:")
            print("1) Listar cursos")
            print("2) Mostrar detalle de un curso")
            print("3) Agregar alumno a un curso")
            print("4) Buscar curso por servicio")
            sub_opcion = input("Seleccione una opción: ").strip()
            print("\n")
            if sub_opcion == '1':
                listar_cursos()
            elif sub_opcion == '2':
                mostrar_detalle_curso()
            elif sub_opcion == '3':
                agregar_alumno_a_curso('database.yaml')
            elif sub_opcion == '4':
                sub_opcion4 = input("Ingrese el nombre del servicio: ")
                buscar_curso_por_servicio(sub_opcion4)
            else:
                print("Opción inválida.")
        elif opcion == '4':
            print("\nOpciones de Alumnos:")
            print("1) Listar alumnos")
            print("2) Mostrar detalle de un alumno")
            print("3) Agregar alumno")
            sub_opcion = input("Seleccione una opción: ").strip()
            print("\n")
            if sub_opcion == '1':
                listar_alumnos()
            elif sub_opcion == '2':
                mostrar_detalle_alumno()
            elif sub_opcion =='3':
                agregar_alumno('database.yaml')
            else:
                print("Opción inválida.")

        elif opcion == '5':
            print("\nOpciones de Servidores:")
            print("1) Listar Servidores")
            print("2) Mostrar detalle de servidores")
            sub_opcion = input("Seleccione una opción: ").strip()
            print("\n")
            if sub_opcion == '1':
                listar_servidores()
            elif sub_opcion == '2':
                sub_opcion2 = input("Ingrese el servidor para ver el detalle: ").strip()
                mostrar_detalle_servidor(sub_opcion2)

            else:
                print("Opción inválida.")

        elif opcion == '7':
            print("\nOpciones de Conexiones:")
            print("1) Crear conexión")
            print("2) Listar conexiones activas")
            print("3) Eliminar conexión")
            sub_opcion = input("Seleccione una opción: ")
            print("\n")
            if sub_opcion == '1':
                crear_conexion()
            elif sub_opcion == '2':
                listar_conexiones()
            elif sub_opcion == '3':
                sub_opcion3 = input("Ingrese el handler de la conexión que desee eliminar: ").strip()
                eliminar_conexion(sub_opcion3)
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

