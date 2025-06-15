from chat_client import DeepSeekClient
from logger import ConversationLogger
import colorama
from colorama import Fore, Back, Style
import config

colorama.init()

def print_banner(mode: str):
    banners = {
        "esquizo": f"""{Fore.BLACK}{Back.WHITE}
▓█████▄  ▒█████   ██▀███   ██▓███   ██░ ██ 
▒██▀ ██▌▒██▒  ██▒▓██ ▒ ██▒▓██░  ██▒▓██░ ██▒
░██   █▌▒██░  ██▒▓██ ░▄█ ▒▓██░ ██▓▒▒██▀▀██░
░▓█▄   ▌▒██   ██░▒██▀▀█▄  ▒██▄█▓▒ ▒░▓█ ░██ 
░▒████▓ ░ ████▓▒░░██▓ ▒██▒▒██▒ ░  ░░▓█▒░██▓
 ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒▓▒░ ░  ░ ▒ ░░▒░▒
 ░ ▒  ▒   ░ ▒ ▒░   ░▒ ░ ▒░░▒ ░      ▒ ░▒░ ░
 ░ ░  ░ ░ ░ ░ ▒    ░░   ░ ░░        ░  ░░ ░
   ░        ░ ░     ░               ░  ░  ░
 ░{Style.RESET_ALL}""",
        "nethacker": f"""{Fore.GREEN}{Back.BLACK}
███╗   ██╗███████╗████████╗██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
████╗  ██║██╔════╝╚══██╔══╝██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██╔██╗ ██║█████╗     ██║   ███████║███████║██║     █████╔╝ █████╗  ██████╔╝
██║╚██╗██║██╔══╝     ██║   ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║ ╚████║███████╗   ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
{Style.RESET_ALL}""",
        "mirror": f"""{Fore.MAGENTA}{Back.BLACK}
 __  __ _                     
|  \/  (_)___  ___  _ __  
| |\/| | / __|/ _ \| '_ \ 
| |  | | \__ \ (_) | | | |
|_|  |_|_|___/\___/|_| |_| 
{Style.RESET_ALL}"""
    }
    print(banners[mode])

def main():
    print(f"{Fore.CYAN}Selecciona tu modo de operación:")
    print(f"1. {Fore.MAGENTA}EsquizoAI - Modo Psico-activo")
    print(f"2. {Fore.GREEN}NetHacker - Especialista en Redes")
    print(f"3. {Fore.MAGENTA}MirrorReflex - Modo Introspectivo{Style.RESET_ALL}")

    mode_choice = input(f"{Fore.WHITE}» {Style.RESET_ALL}").strip()
    if mode_choice == "2":
        mode = "nethacker"
    elif mode_choice == "3":
        mode = "mirror"
    else:
        mode = "esquizo"
    
    print_banner(mode)
    print(f"\n{getattr(Fore, config.MODES[mode]['banner_color'])}⚛️  Inicializando {config.MODES[mode]['name']}...")
    
    model_choice = input(f"{Fore.CYAN}Selecciona tu interfaz:\n1. Chat\n2. Razonador\n{Fore.WHITE}» {Style.RESET_ALL}").strip()
    model_type = "reasoner" if model_choice == "2" else "chat"
    
    client = DeepSeekClient(mode=mode, model_type=model_type)
    logger = ConversationLogger(mode_name=config.MODES[mode]["name"])
    turno = 1
    
    try:
        while True:
            prompt_color = getattr(Fore, config.MODES[mode]['prompt_color'])
            user_input = input(f"\n{prompt_color}🌀 [Ronda {turno}] ➔ {Style.RESET_ALL}").strip()
            
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
                print(f"\n{Fore.GREEN}🌀 [Salida {config.MODES[mode]['name']}]:")
                
                for chunk in client.send_message(user_input):
                    razonamiento = chunk.get('reasoning', '') or ''
                    contenido = chunk.get('content', '') or ''
                    
                    if razonamiento:
                        print(f"{prompt_color}{razonamiento}{Style.RESET_ALL}", end='', flush=True)
                        full_response['reasoning'] += razonamiento
                    
                    if contenido:
                        print(f"{Fore.WHITE}{contenido}{Style.RESET_ALL}", end='', flush=True)
                        full_response['content'] += contenido
                
                logger.log_message("assistant", f"RAZONAMIENTO:\n{full_response['reasoning']}\nRESPUESTA:\n{full_response['content']}")
                turno += 1
                print(f"\n{prompt_color}⚡ Continúa la conversación (o 'q' para salir)...")
                
            except Exception as e:
                print(f"\n{Fore.RED}☢️  Error crítico: {str(e)}{Style.RESET_ALL}")
                client.clear_context()
                turno = 1
                
    finally:
        logger.close_session()
        colorama.deinit()

if __name__ == "__main__":
    main()
