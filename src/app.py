from chat_client import DeepSeekClient
from logger import ConversationLogger
import colorama
from colorama import Fore, Back, Style

colorama.init()

def print_banner():
    print(f"""{Fore.BLACK}{Back.WHITE}
▓█████▄  ▒█████   ██▀███   ██▓███   ██░ ██ 
▒██▀ ██▌▒██▒  ██▒▓██ ▒ ██▒▓██░  ██▒▓██░ ██▒
░██   █▌▒██░  ██▒▓██ ░▄█ ▒▓██░ ██▓▒▒██▀▀██░
░▓█▄   ▌▒██   ██░▒██▀▀█▄  ▒██▄█▓▒ ▒░▓█ ░██ 
░▒████▓ ░ ████▓▒░░██▓ ▒██▒▒██▒ ░  ░░▓█▒░██▓
 ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒▓▒░ ░  ░ ▒ ░░▒░▒
 ░ ▒  ▒   ░ ▒ ▒░   ░▒ ░ ▒░░▒ ░      ▒ ░▒░ ░
 ░ ░  ░ ░ ░ ░ ▒    ░░   ░ ░░        ░  ░░ ░
   ░        ░ ░     ░               ░  ░  ░
 ░{Style.RESET_ALL}""")

def main():
    print_banner()
    print(f"\n{Fore.MAGENTA}⚛️  Inicializando matriz de diálogo no-lineal...")
    
    model_choice = input(f"{Fore.CYAN}Selecciona tu interfaz:\n1. Esquizochat\n2. Razonador Cuántico\n{Fore.WHITE}» {Style.RESET_ALL}").strip()
    model_type = "reasoner" if model_choice == "2" else "chat"
    
    client = DeepSeekClient(model_type=model_type)
    logger = ConversationLogger()
    turno = 1
    
    try:
        while True:
            user_input = input(f"\n{Fore.YELLOW}🌀 [Ronda {turno}] ➔ {Style.RESET_ALL}").strip()
            
            if user_input.lower() == 'q':
                print(f"\n{Fore.RED}☠️  Protocolo de terminación iniciado...{Style.RESET_ALL}")
                break
                
            if user_input.lower() == 'c':
                client.clear_context()
                print(f"\n{Fore.BLUE}♻️  Contexto reiniciado:")
                if client.model_type == "chat":
                    print(f"{Fore.CYAN}{client.messages[-1]['content']}{Style.RESET_ALL}")
                turno = 1
                continue
                
            # Procesamiento seguro
            print(f"{Fore.WHITE}⚡ [Procesando en {model_type.upper()}]...", end='\r')
            logger.log_message("user", user_input)
            
            try:
                full_response = {"reasoning": "", "content": ""}
                print(f"\n{Fore.GREEN}🌀 [Salida neuronal]:")
                
                for chunk in client.send_message(user_input):
                    # Manejo a prueba de None
                    razonamiento = chunk.get('reasoning', '') or ''
                    contenido = chunk.get('content', '') or ''
                    
                    if razonamiento:
                        print(f"{Fore.YELLOW}{razonamiento}{Style.RESET_ALL}", end='', flush=True)
                        full_response['reasoning'] += razonamiento
                    
                    if contenido:
                        print(f"{Fore.RED}{contenido}{Style.RESET_ALL}", end='', flush=True)
                        full_response['content'] += contenido
                
                logger.log_message("assistant", f"RAZONAMIENTO:\n{full_response['reasoning']}\nRESPUESTA:\n{full_response['content']}")
                turno += 1
                print(f"\n{Fore.CYAN}⚡ Continúa la conversación (o 'q' para salir)...")
                
            except Exception as e:
                print(f"\n{Fore.RED}☢️  Error crítico: {str(e)}{Style.RESET_ALL}")
                client.clear_context()
                turno = 1
                
    finally:
        logger.close_session()
        colorama.deinit()

if __name__ == "__main__":
    main()