from chat_client import DeepSeekClient
from logger import ConversationLogger
import time
import os
import colorama
from colorama import Fore, Back, Style

# Inicializar colorama para Windows
colorama.init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Fore.GREEN}
╔═══════════════════════════════════════════════════════════════╗
║                   🤪 EsquizoAI - Psycho Bot 🚀                ║
║              El bot más loko del multiverso 💀                ║
╚═══════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""
    print(banner)

def print_message(role, content, timestamp):
    if role == "user":
        print(f"{Fore.LIGHTGREEN_EX}👤 Tú [{timestamp}]:{Style.RESET_ALL}")
        print(f"{Fore.LIGHTGREEN_EX}{content}{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.RED}🤖 EsquizoAI [{timestamp}]:{Style.RESET_ALL}")
        print(f"{Fore.RED}{content}{Style.RESET_ALL}\n")

def main():
    clear_screen()
    print_banner()
    
    # Inicializar el cliente y el logger
    client = DeepSeekClient()
    logger = ConversationLogger()
    messages = []
    
    try:
        while True:
            try:
                # Input del usuario
                user_input = input(f"{Fore.LIGHTGREEN_EX}💭 Escribe tu mensaje (o 'q' para salir, 'c' para limpiar): {Style.RESET_ALL}")
                
                if user_input.lower() == 'q':
                    print(f"\n{Fore.RED}💀 ¡Hasta la próxima revolución, psycho!{Style.RESET_ALL}")
                    logger.log_system_event("Sesión terminada por el usuario")
                    logger.close_session()
                    break
                    
                if user_input.lower() == 'c':
                    clear_screen()
                    print_banner()
                    messages = []
                    client.clear_context()
                    logger.log_system_event("Chat limpiado por el usuario")
                    continue
                    
                if not user_input.strip():
                    continue
                
                # Agregar mensaje del usuario
                timestamp = time.strftime('%H:%M')
                messages.append({"role": "user", "content": user_input})
                print_message("user", user_input, timestamp)
                logger.log_message("user", user_input)
                
                # Mantener solo los últimos 5 mensajes
                if len(messages) > 10:
                    messages = messages[-10:]
                
                # Procesar respuesta
                try:
                    print(f"{Fore.YELLOW}🤪 Procesando respuesta loka...{Style.RESET_ALL}")
                    full_response = ""
                    
                    # Limpiar la línea de "Procesando..."
                    print('\r' + ' ' * 50 + '\r', end='', flush=True)
                    
                    # Imprimir el header una sola vez
                    print(f"{Fore.RED}🤖 EsquizoAI [{time.strftime('%H:%M')}]: {Style.RESET_ALL}", end='', flush=True)
                    
                    # Usar el stream directamente
                    for chunk in client.send_message(user_input):
                        if chunk:
                            print(f"{Fore.RED}{chunk}{Style.RESET_ALL}", end='', flush=True)
                            full_response += chunk
                    
                    print("\n")  # Nueva línea al final
                    
                    if full_response:
                        messages.append({"role": "assistant", "content": full_response})
                        logger.log_message("assistant", full_response)
                        
                except Exception as e:
                    error_msg = f"¡ERROR PSYCHO! Algo salió mal: {str(e)}"
                    print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}\n")
                    messages.append({"role": "assistant", "content": "💀 Error en la comunicación psycho..."})
                    logger.log_system_event(error_msg)
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}💀 ¡Interrupción detectada! Hasta la próxima, psycho.{Style.RESET_ALL}")
                logger.log_system_event("Sesión interrumpida por el usuario (KeyboardInterrupt)")
                logger.close_session()
                break
                
    finally:
        # Asegurarnos de cerrar la sesión correctamente
        try:
            logger.close_session()
        except:
            pass

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Fore.RED}¡ERROR FATAL PSYCHO!  {str(e)}{Style.RESET_ALL}")
    finally:
        colorama.deinit() 