from mysql.connector import connect, Error

'''
BD preparado para a execução
deste programa com o comando:

CREATE TABLE CONTATOS (
ID INT AUTO_INCREMENT PRIMARY KEY,
NOME VARCHAR(80) NOT NULL,
ANIVERSARIO DATE NOT NULL,
ENDERECO VARCHAR(200) NOT NULL,
TELEFONE BIGINT NOT NULL,
CELULAR BIGINT NOT NULL,
EMAIL VARCHAR(100) NOT NULL
)
'''

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
            digitou_direito=True

    return txt

def opcao_escolhida(mnu):
    print ()

    opcoes_validas = []
    posicao = 0
    while posicao < len(mnu):
        print (posicao + 1,') ', mnu[posicao], sep='')
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

def contato_cadastrado(nome: str) -> bool:
    
    comando = f"Select * from CONTATOS where nome='{nome}'"

    conexao = obtem_conexao("172.16.12.14", "BD240225285", "Ozgia4", "BD240225285")
    cursor = conexao.cursor()
    cursor.execute(comando)

    linhas = cursor.fetchall()
    return linhas != [] # se vem [], nao selecionou nada, nome nao cadastrado

def insercao_contato(nome, aniversario, endereco, telefone, celular, email):
    
    comando= "Insert into CONTATOS "+\
            "(Nome,Aniversario,Endereco,Telefone,Celular,Email) "+\
            "values "+\
            f"('{nome}',STR_TO_DATE('{aniversario}','%d/%m/%Y'),'{endereco}',{telefone},{celular},'{email}')"

    conexao = obtem_conexao("172.16.12.14","BD240225285","Ozgia4","BD240225285")
    cursor = conexao.cursor()
    cursor.execute(comando)
    conexao.commit()

def incluir():
    nome = input('\nNome.......: ')

    try:
        ja_cadastrado = contato_cadastrado(nome)
    except Error:    
        print("Problema de conexão com o BD!")
    else:
        if ja_cadastrado:
            print("Nome já cadastrado!")
        else:
            aniversario = input('Aniversário: ')
            endereco    = input('Endereço...: ')
            telefone    = input('Telefone...: ')
            celular     = input('Celular....: ')
            email       = input('e-mail.....: ')

            try:
                insercao_contato (nome, aniversario, endereco, telefone, celular, email)
            except Error:
                print("Erro nos dados digitados!")
            else:
                print('Cadastro realizado com sucesso!')

def procurar():
    
    nome = input('\nNome do contato a procurar: ') # TODO adicionar validacoes quanto ao que pode ser digitado
    try:
        comando = f"SELECT Nome,DATE_FORMAT(Aniversario,'%d/%m/%Y'),Endereco,Telefone,Celular,Email FROM CONTATOS WHERE nome='{nome}'"
        conexao = obtem_conexao("172.16.12.14", "BD240225285", "Ozgia4", "BD240225285")
        cursor = conexao.cursor()
        cursor.execute(comando)
        contato = cursor.fetchone()
        
        if contato:
            print('\nDados do contato encontrado:')
            print('Nome.......:',contato[0])
            print('Aniversario:',contato[1])
            print('Endereco...:',contato[2])
            print('Telefone...:',contato[3])
            print('Celular....:',contato[4])
            print('e-mail.....:',contato[5])
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
        
        conexao = obtem_conexao("172.16.12.14", "BD240225285", "Ozgia4", "BD240225285")
        cursor = conexao.cursor()
        cursor.execute(comando)
        conexao.commit()
    except ValueError:
        print("Erro: Para datas, use o formato DD/MM/YYYY")
        raise
    except Error as e:
        print(f"Erro ao atualizar campo: {e}")
        raise

def atualizar():
    print('Opção não implementada!')
    # Ficar mostrando um menu oferecendo as opções de atualizar aniversário, ou
    # endereco, ou telefone, ou celular, ou email, ou finalizar as
    # atualizações; ficar pedindo para digitar a opção até digitar uma
    # opção válida; realizar a atulização solicitada; até ser escolhida a
    # opção de finalizar as atualizações.
    # USAR A FUNÇÃO opcao_escolhida, JÁ IMPLEMENTADA, PARA FAZER O MENU
    
    nome = input('\nNome do contato a atualizar: ')
    try:
        if not contato_cadastrado(nome):
            print("Contato não encontrado!")
            return
            
        menu_atualizacao = ['Atualizar Aniversário',
                        'Atualizar Endereço',
                        'Atualizar Telefone',
                        'Atualizar Celular',
                        'Atualizar Email',
                        'Finalizar Atualizações']
        
        while True:
            opcao = int(opcao_escolhida(menu_atualizacao))
            if opcao == 6:  
                break
                
            try:
                if opcao == 1:
                    valor = input('Novo aniversário (dd/mm/aaaa): ')
                    atualizar_campo(nome, 'Aniversario', valor)
                elif opcao == 2:
                    valor = input('Novo endereço: ')
                    atualizar_campo(nome, 'Endereco', valor)
                elif opcao == 3:
                    valor = input('Novo telefone: ')
                    atualizar_campo(nome, 'Telefone', valor)
                elif opcao == 4:
                    valor = input('Novo celular: ')
                    atualizar_campo(nome, 'Celular', valor)
                elif opcao == 5:
                    valor = input('Novo email: ')
                    atualizar_campo(nome, 'Email', valor)
                    
                print('Atualização realizada com sucesso!')
            except Error as e:
                print(f"Erro ao atualizar campo: {e}")
    except Error as e:
        print(f"Erro ao atualizar contato: {e}")

def listagem_contatos():
    comando = "SELECT Nome, DATE_FORMAT(Aniversario,'%d/%m/%Y'), Endereco, Telefone, Celular, Email FROM CONTATOS"
    conexao = obtem_conexao("172.16.12.14","BD240225285","Ozgia4","BD240225285")
    cursor = conexao.cursor()
    cursor.execute(comando)

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
        print("Listagem concluida com sucesso!")

def excluir():    
    nome = input('\nNome do contato a excluir: ')
    try:
        if not contato_cadastrado(nome):
            print("Contato não encontrado!")
            return
            
        comando = f"SELECT Nome,DATE_FORMAT(Aniversario,'%d/%m/%Y'),Endereco,Telefone,Celular,Email FROM CONTATOS WHERE nome='{nome}'"
        conexao = obtem_conexao("172.16.12.14", "BD240225285", "Ozgia4", "BD240225285")
        cursor = conexao.cursor()
        cursor.execute(comando)
        
        contato = cursor.fetchone()
        print('\nDados do contato a ser excluído:')
        print('Nome.......:',contato[0])
        print('Aniversario:',contato[1])
        print('Endereco...:',contato[2])
        print('Telefone...:',contato[3])
        print('Celular....:',contato[4])
        print('e-mail.....:',contato[5])
        
        confirmacao = input('\nConfirma a exclusão deste contato? (S/N): ').upper()
        
        if confirmacao == 'S':
            comando = f"DELETE FROM CONTATOS WHERE nome='{nome}'"
            cursor.execute(comando)
            conexao.commit()
            print('\nContato excluído com sucesso!')
        else:
            print('\nOperação cancelada!')
    except Error as e:
        print(f"Erro ao excluir contato: {e}")

def fecha_conexao():
    conexao = obtem_conexao("143.106.250.84","andre","andre","andre")
    cursor = conexao.cursor()
    cursor.close()
    conexao.close()

# daqui para baixo, implementamos o programa (nosso CRUD, C=create(inserir), R=read(recuperar), U=update(atualizar), D=delete(remover,apagar)

apresente_se()

menu=['Incluir Contato',\
    'Procurar Contato',\
    'Atualizar Contato',\
    'Listar Contatos',\
    'Excluir Contato',\
    'Sair do Programa']

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
    else: # if opcao==6:
        fecha_conexao()
        deseja_finalizar = True

print()       
print('PROGRAMA ENCERRADO; OBRIGADO POR USAR ESTE PROGRAMA!')
