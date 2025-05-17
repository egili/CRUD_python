
def obtem_nome_validado(solicitacao: str) -> str:
    nome = input(solicitacao).strip()

    while True:
        if nome.replace(" ", "").isalpha():
            return nome
        else:
            print("Entrada inválida. Use apenas letras e espaços.")