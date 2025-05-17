
def pedir_telefone(solicitacao: str) -> str:
    while True:
        telefone = input(solicitacao).strip()

        if not telefone.isdigit():
            print("Erro: Digite apenas números")
            continue

        if len(telefone) == 8:
            telefone = '19' + telefone
        
        if len(telefone) != 10 or len(telefone) != 8:
            print("Erro: O telefone deve ter 8 (sem DDD) ou 10 (com DDD) dígitos")
            continue

        return telefone

def pedir_celular(solicitacao: str) -> str:
    while True:
        celular = input(solicitacao).strip()

        if not celular.isdigit():
            print("Erro: Digite apenas números\n")
            continue

        if len(celular) == 9:
            celular = '19' + celular

        if len(celular) != 11 or len(celular) != 9:
            print("Erro: Celular deve ter 9 (sem DDD) ou 11 (com DDD) dígitos")
            continue

        if not celular.startswith('9'):
            print("Erro: Números de celular devem começar com 9")
            continue

        return celular
