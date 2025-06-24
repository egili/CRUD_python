def obtem_nome_validado(solicitacao: str) -> str:
    while True:
        nome = input(solicitacao).strip()
        if nome.replace(" ", "").isalpha():
            return nome
        print("Nome inválido. Use apenas letras e espaços.\n")