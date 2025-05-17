from mysql.connector import connect, Error
from date_utils      import pedir_data
from name_utils      import obtem_nome_validado
from email_utils     import pedir_email
from address_utils   import pedir_endereco
from phone_utils     import pedir_telefone, pedir_celular

def apresente_se():
    print('+-------------------------------------------------------------+')
    print('|                                                             |')
    print('| AGENDA PESSOAL DE ANIVERSÁRIOS E FORMAS DE CONTATAR PESSOAS |')
    print('|                                                             |')
    print('| Prof André Maligno                                          |')
    print('|                                                             |')
    print('| Eliseu Pereira Gili - 25009281                              |')
    print('|                                                             |')
    print('| Versão 2.0 de 17/maio/2025                                  |')
    print('|                                                             |')
    print('+-------------------------------------------------------------+')

def um_texto(solicitacao: str, mensagem: str, valido) -> str:
    
    digitou_direito = False
    
    while not digitou_direito:
        txt = input(solicitacao)

        if txt not in valido:
            print(mensagem,'- Favor redigitar...')
        else:
            digitou_direito = True

    return txt

def opcao_escolhida(mnu):
    print ()

    opcoes_validas = []
    posicao = 0
    while posicao < len(mnu):
        print (posicao + 1,') ', mnu[posicao], sep = '')
        opcoes_validas.append(str(posicao + 1))
        posicao += 1

    print()
    return um_texto('Qual é a sua opção? ', 'Opção inválida', opcoes_validas)

def obtem_conexao(servidor: str, usuario: str, senha: str, bd: str):
    
    if obtem_conexao.conexao is None:
        obtem_conexao.conexao = connect(
            host     = f"{servidor}",\
            user     = f"{usuario}",\
            password = f"{senha}",\
            database = f"{bd}"
        )

    return obtem_conexao.conexao

obtem_conexao.conexao = None

def is_contato_cadastrado(nome: str) -> bool:
    
    conexao = obtem_conexao("172.16.12.14", "BD240225237", "Stavk6", "BD240225237")
    cursor  = conexao.cursor()
    cursor.execute(f"SELECT * FROM CONTATOS WHERE nome='{nome}'")

    return cursor.fetchall() != [] # se vem [], nao selecionou nada, nome nao cadastrado

def insercao_contato(nome, aniversario, endereco, telefone, celular, email):
    
    comando= "INSERT INTO CONTATOS "+\
            "(Nome, Aniversario, Endereco, Telefone, Celular, Email) "+\
            "VALUES "+\
            f"('{nome}', STR_TO_DATE('{aniversario}','%d/%m/%Y'), '{endereco}', {telefone}, {celular}, '{email}')"

    conexao = obtem_conexao("172.16.12.14","BD240225237","Stavk6","BD240225237")
    cursor  = conexao.cursor()
    cursor.execute(comando)
    conexao.commit()

def incluir():
    
    nome = obtem_nome_validado('\nNome: ')

    try:
        ja_cadastrado = is_contato_cadastrado(nome)
    except Error:    
        print("Problema de conexão com o BD!")
    else:
        if ja_cadastrado:
            print("Nome já cadastrado!")
        else:
            aniversario = pedir_data('\nAniversário: ')
            endereco    = pedir_endereco('\nEndereço: ')
            telefone    = pedir_telefone('\nTelefone (com ou sem DDD): ')	
            celular     = pedir_celular('\nCelular (com ou sem DDD): ')
            email       = pedir_email('\nEmail: ')

            try:
                insercao_contato (nome, aniversario, endereco, telefone, celular, email)
            except Error:
                print("Erro nos dados digitados!")
            else:
                print('\nCadastro realizado com sucesso!\n')

def procurar():
    
    nome = obtem_nome_validado('\nNome do contato a procurar: ')
    try:
        comando = f"SELECT Nome, DATE_FORMAT(Aniversario,'%d/%m/%Y'), Endereco, Telefone, Celular, Email FROM CONTATOS WHERE nome='{nome}'"
        conexao = obtem_conexao("172.16.12.14", "BD240225237", "Stavk6", "BD240225237")
        cursor = conexao.cursor()
        cursor.execute(comando)
        contato = cursor.fetchone()
        
        if contato:
            print('\nDados do contato encontrado:')
            print('Nome.......:', contato[0])
            print('Aniversario:', contato[1])
            print('Endereco...:', contato[2])
            print('Telefone...:', contato[3])
            print('Celular....:', contato[4])
            print('e-mail.....:', contato[5])
        else:
            print('\nContato não encontrado!')
    except Error as e:
        print(f"Erro ao procurar contato: {e}")

def atualizar_campo(nome, campo, valor):
    try:
        if campo == 'Aniversario':
            dia, mes, ano = valor.split('/')
            valor = f"{ano}-{mes}-{dia}"
            comando = f"UPDATE CONTATOS SET {campo}='{valor}' WHERE nome='{nome}'"
        elif campo in ['Telefone', 'Celular']:
            comando = f"UPDATE CONTATOS SET {campo}={valor} WHERE nome='{nome}'"
        else:
            comando = f"UPDATE CONTATOS SET {campo}='{valor}' WHERE nome='{nome}'"
        
        conexao = obtem_conexao("172.16.12.14", "BD240225237", "Stavk6", "BD240225237")
        cursor  = conexao.cursor()
        cursor.execute(comando)
        conexao.commit()
        
    except ValueError:
        print("Erro: Para datas, use o formato DD/MM/YYYY")
        raise
    except Error as e:
        print(f"Erro ao atualizar campo: {e}")
        raise

def atualizar():
    
    nome = obtem_nome_validado('\nNome do contato a atualizar: ')
    try:
        if not is_contato_cadastrado(nome):
            print("Contato não encontrado!")
            return
            
        menu_atualizacao = [
            'Atualizar Aniversário',
            'Atualizar Endereço',
            'Atualizar Telefone',
            'Atualizar Celular',
            'Atualizar Email',
            'Finalizar Atualizações'
        ]
        
        while True:
            opcao = int(opcao_escolhida(menu_atualizacao))
            if opcao == 6: 
                break
                
            try:
                if opcao == 1:
                    valor = pedir_data('Informe a nova data de aniversário: ')
                    atualizar_campo(nome, 'Aniversario', valor)
                    
                elif opcao == 2:
                    valor = pedir_endereco('Informe o novo endereço: ')
                    atualizar_campo(nome, 'Endereco', valor)
                    
                elif opcao == 3:
                    valor = pedir_telefone('Informe o novo telefone (com ou sem DDD): ')
                    atualizar_campo(nome, 'Telefone', valor)
                    
                elif opcao == 4:
                    valor = pedir_celular('Informe o novo celular (com ou sem DDD): ')
                    atualizar_campo(nome, 'Celular', valor)
                    
                elif opcao == 5:
                    valor = pedir_email('Informe o novo email: ')
                    atualizar_campo(nome, 'Email', valor)
                    
                print('Atualização realizada com sucesso! \n')
                
            except Error as e:
                print(f"Erro ao atualizar campo: {e}")
                
    except Error as e:
        print(f"Erro ao atualizar contato: {e}")

def listagem_contatos():

    conexao = obtem_conexao("172.16.12.14","BD240225237","Stavk6","BD240225237")
    cursor  = conexao.cursor()
    cursor.execute("SELECT Nome, DATE_FORMAT(Aniversario,'%d/%m/%Y'), Endereco, Telefone, Celular, Email FROM CONTATOS")

    linhas = cursor.fetchall()
    return linhas

def listar():
    try:
        linha = listagem_contatos()
    except Error:    
        print("Problema de conexão com o BD!")
    else:
        atual = 0
        while atual < len(linha):
            print()
            print('Nome.......:', linha[atual][0])
            print('Aniversario:', linha[atual][1])
            print('Endereco...:', linha[atual][2])
            print('Telefone...:', linha[atual][3])
            print('Celular....:', linha[atual][4])
            print('e-mail.....:', linha[atual][5])
            atual += 1

        print()
        print("Listagem concluida com sucesso!\n")

def excluir():    
        
    nome = obtem_nome_validado('\nNome do contato a excluir: ')

    try:
        if not is_contato_cadastrado(nome):
            print("Contato não encontrado!\n")
            return
            
        conexao = obtem_conexao("172.16.12.14", "BD240225237", "Stavk6", "BD240225237")
        cursor = conexao.cursor()
        cursor.execute(f"SELECT Nome,DATE_FORMAT(Aniversario,'%d/%m/%Y'),Endereco,Telefone,Celular,Email FROM CONTATOS WHERE nome='{nome}'")
        
        contato = cursor.fetchone()
        print('\nDados do contato a ser excluído:')
        print('Nome.......:', contato[0])
        print('Aniversario:', contato[1])
        print('Endereco...:', contato[2])
        print('Telefone...:', contato[3])
        print('Celular....:', contato[4])
        print('e-mail.....:', contato[5])
        
        confirmacao = input('\nConfirma a exclusão deste contato? (S/N): ').upper()
        
        if confirmacao == 'S': 
            cursor.execute(f"DELETE FROM CONTATOS WHERE nome='{nome}'")
            conexao.commit()
            print('\nContato excluído com sucesso!\n')
        else:
            print('\nOperação cancelada!\n')
    except Error as e:
        print(f"Erro ao excluir contato: {e}")

def fecha_conexao():
    conexao = obtem_conexao("172.16.12.14","BD240225237","Stavk6","BD240225237")
    cursor = conexao.cursor()
    cursor.close()
    conexao.close()

apresente_se()

menu = [
    'Incluir Contato',\
    'Procurar Contato',\
    'Atualizar Contato',\
    'Listar Contatos',\
    'Excluir Contato',\
    'Sair do Programa'
]

deseja_finalizar = False
while not deseja_finalizar:
    opcao = int(opcao_escolhida(menu))

    if opcao == 1:
        incluir()
    elif opcao == 2:
        procurar()
    elif opcao == 3:
        atualizar()
    elif opcao == 4:
        listar()
    elif opcao == 5:
        excluir()
    else: 
        fecha_conexao()
        deseja_finalizar = True

print()       
print('PROGRAMA ENCERRADO; OBRIGADO POR USAR ESTE PROGRAMA! \n')
