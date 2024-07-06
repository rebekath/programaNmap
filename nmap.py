import nmap
import os

def scan_network():
    # Crear el escáner nmap
    nm = nmap.PortScanner()

    # Solicitar información al usuario
    print("Bienvenido al escáner de red.")
    hosts = input("Ingrese los host(s) a escanear (ej. 192.168.1.1; 192.168.1.0/24): ")

    # Solicitar puertos y usar todos si no se proporciona ninguno
    ports = input("Ingrese los puerto(s) a escanear (ej. 22-443), deje en blanco para todos los puertos: ")
    if not ports:
        ports = '1-65535'  # Rango completo de puertos TCP

    # Solicitar argumentos adicionales
    print("Ingrese cualquier argumento adicional para nmap que desee incluir.")
    print("Por ejemplo, use '-sV -O' para detección de versión y detección de SO,")
    print("o '-A' para escaneo agresivo, '-v' para detallado, y '--script=default' para scripts predeterminados.")
    arguments = input("Argumentos: ")

    # Preguntar si se debe ejecutar como super usuario
    run_as_sudo = input("¿Desea ejecutar el escaneo como superusuario? [s/N]: ").lower() == 's'

    # Realizar el escaneo con las opciones proporcionadas
    try:
        if run_as_sudo:
            # Comando completo para ejecutar con sudo
            command = f"sudo nmap -p {ports} {arguments} {hosts}"
            print(f"Ejecutando comando: {command}")
            os.system(command)
        else:
            # Escaneo con la biblioteca nmap de Python
            nm.scan(hosts=hosts, ports=ports, arguments=arguments)

            # Mostrar los resultados
            for host in nm.all_hosts():
                print(f"Host : {host} ({nm[host].hostname()})")
                print(f"Estado : {nm[host].state()}")
                for proto in nm[host].all_protocols():
                    print(f"----------\nProtocolo : {proto}")
                    lport = nm[host][proto].keys()
                    sorted_ports = sorted(lport)
                    for port in sorted_ports:
                        print(f"puerto : {port}\testado : {nm[host][proto][port]['state']}")
    except Exception as e:
        print(f"Se produjo un error: {e}")

if __name__ == "__main__":
    scan_network()
