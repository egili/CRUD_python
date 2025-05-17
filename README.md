<h1> CRUD Python + MySQL 🐬 </h1>

Projeto individual da disciplina de algoritmos de computação da PUC Campinas

<hr/>

## 📋 Descrição

Este projeto é um **CRUD** de contatos, construido em Python e integrado a um banco de dados **MySQL**

---

## ⚙️ Requisitos

* Python 3.8+
* MySQL (acesso a servidor e base de dados)
* Biblioteca Python para conexão MySQL:

  ```bash
  python -m pip install mysql-connector-python
  ```

---

## 📂 Estrutura do Projeto

```
.
├── address_utils.py      # validação de endereços
├── date_utils.py         # leitura e validação de datas
├── email_utils.py        # leitura e validação de e-mails
├── name_utils.py         # leitura e validação de nomes
├── phone_utils.py        # leitura/validação de telefone e celular
├── main.py               # menu e chamadas CRUD (inclusão, leitura, atualização, exclusão)
└── README.md             # este arquivo
```

---

## 🚀 Instalação

1. **Clone o repositório**

   ```bash
   git clone https://seu-repositorio.git
   cd seu-repositorio
   ```

2. **Instale a dependência do MySQL**

   ```bash
   python -m pip install mysql-connector-python
   ```

3. **Configure as credenciais de acesso ao MySQL**
   No arquivo `main.py` (ou em um módulo de configurações), ajuste host, usuário, senha e nome da base:

   ```python
   conecta_bd("seu_host", "seu_usuario", "sua_senha", "seu_banco")
   ```

4. **Crie a tabela no MySQL**

   ```sql
    CREATE TABLE CONTATOS (
    	ID INT AUTO_INCREMENT PRIMARY KEY,
    	NOME VARCHAR(80) NOT NULL,
    	ANIVERSARIO DATE NOT NULL,
    	ENDERECO VARCHAR(200) NOT NULL,
    	TELEFONE BIGINT NOT NULL,
    	CELULAR BIGINT NOT NULL,
    	EMAIL VARCHAR(100) NOT NULL
      );
   ```

---

## ▶️ Uso

Execute o script principal:

```bash
python main.py
```

O menu interativo permitirá escolher entre:

1. **Incluir Contato**
2. **Procurar Contato**
3. **Atualizar Contato**
4. **Listar Contatos**
5. **Excluir Contato**
6. **Sair do Programa**

Cada opção faz validações de entrada (nome, data, endereço, telefone, celular e e-mail) e se comunica com o MySQL para persistência dos dados.

---

## 🛠 Funcionalidades Principais

* **Incluir:** Novo contato com aniversários formatados e validados
* **Procurar:** Exibe dados de um contato pelo nome
* **Atualizar:** Permite alterar qualquer campo (data, endereço, telefone, celular ou e-mail)
* **Listar:** Mostra todos os contatos cadastrados
* **Excluir:** Remove contato após confirmação

Todas as operações usam **mysql-connector-python** para conectar, executar consultas e manipular resultados com commits automáticos.

---
