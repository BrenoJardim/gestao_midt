from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, flash
import sqlite3
import random
import string
import os
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)
app.secret_key = os.urandom(24)

users = {
    'admin': 'admin123',
    'SchimidtCereais': '01052044'
}

# Simulação de um usuário logado (você pode substituir isso por uma lógica real de autenticação)
usuario_logado = False

# Rota padrão para a página inicial
@app.route('/')
def index():
    global usuario_logado  # Definindo usuario_logado como global
    if usuario_logado:
        # Se o usuário estiver logado, redirecione para a página inicial
        return redirect(url_for('venda_balcao'))
    else:
        # Se o usuário não estiver logado, redirecione para a tela de login
        return redirect(url_for('login'))

# Rota para a tela de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aqui você pode verificar as credenciais do usuário e fazer o login
        # Por simplicidade, vamos apenas simular o login definindo usuario_logado como True
        global usuario_logado
        usuario_logado = True
        # Após o login bem-sucedido, redirecione para a página inicial
        return redirect(url_for('venda_balcao'))
    else:
        # Se a solicitação for GET, renderize a página de login
        return render_template('login.html')

@app.route('/erp_dashboard')
def erp_dashboard():
    # Aqui você renderiza a página principal do seu ERP após o login bem-sucedido
    return 'Página principal do seu ERP'

# Função para conectar ao banco de dados
def conectar_bd():
    conn = sqlite3.connect('erp.db')
    return conn

# Função para conectar ao banco de dados SQLite
def connect_db():
    conn = sqlite3.connect('erp.db')
    return conn

# Função para adicionar um novo usuário ao banco de dados
def add_user(username, password):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Verificar se o usuário já existe
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        print("Usuário já existe")
    else:
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, password))
        conn.commit()
        print("Usuário adicionado com sucesso")

    conn.close()

# Exemplo de uso da função add_user
add_user('admin', 'admin123')
add_user('user', 'user123')


# Função para obter produtos do banco de dados
def obter_produtos_do_banco_de_dados():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    
    conn.close()

    return produtos

# Função para obter produtos do banco de dados por ID
def obter_produto_por_id(id_produto):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Execute a consulta para obter o produto pelo ID
    cursor.execute('SELECT * FROM produtos WHERE id=?', (id_produto,))
    
    # Obtenha o produto encontrado
    produto = cursor.fetchone()
    
    # Feche a conexão com o banco de dados
    conn.close()
    
    return produto

# Função para obter fornecedores do banco de dados
def obter_fornecedores_do_banco_de_dados():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM fornecedores')
    fornecedores = cursor.fetchall()
    
    conn.close()

    # Adicione instruções print para verificar os dados recuperados
    print("Fornecedores recuperados do banco de dados:")
    for fornecedor in fornecedores:
        print(fornecedor)
    
    return fornecedores

# Função para obter adições do sítio do banco de dados
def obter_adicoes_sitio_do_banco_de_dados():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM adicoes_sitio')
    adicoes_sitio = cursor.fetchall()
    
    conn.close()

    return adicoes_sitio

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

# Rota para o cadastro de clientes
@app.route('/cadastro_clientes', methods=['GET', 'POST'])
def cadastro_clientes():
    if request.method == 'POST':
        # Lógica para cadastrar o cliente aqui
        # Certifique-se de capturar os dados do formulário corretamente
        
        # Exemplo de como acessar os dados do formulário
        nome = request.form['nome']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        
        # Aqui você pode adicionar a lógica para inserir os dados do cliente no banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()

        # Não inclua o ID na inserção, pois é autoincrementado
        cursor.execute('INSERT INTO clientes (nome, telefone, endereco) VALUES (?, ?, ?)',
                       (nome, telefone, endereco))
        conn.commit()
        conn.close()
        
        # Depois de cadastrar o cliente, você pode redirecionar para outra página, se necessário
        return redirect(url_for('listar_clientes'))
        
    # Se for uma requisição GET, simplesmente renderize a página de cadastro de clientes
    return render_template('cadastro_clientes.html')

# Rota para listar os clientes cadastrados
@app.route('/listar_clientes', methods=['GET'])
def listar_clientes():
    # Abra uma conexão com o banco de dados
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Execute uma consulta de teste
    cursor.execute('SELECT * FROM clientes LIMIT 5')  # Limita a consulta para retornar apenas 5 clientes
    test_data = cursor.fetchall()
    print(test_data)  # Verifica se há dados retornados pela consulta de teste
    
    # Execute a consulta para obter todos os clientes
    cursor.execute('SELECT * FROM clientes')
    
    # Obtenha todos os resultados da consulta
    clientes = cursor.fetchall()
    
    # Feche a conexão com o banco de dados
    conn.close()
    
    # Renderize o template HTML e passe os clientes recuperados
    return render_template('listagem_clientes.html', clientes=clientes)

# Rota para editar um cliente específico
@app.route('/editar_cliente/<int:id_cliente>', methods=['GET', 'POST'])
def editar_cliente(id_cliente):
    if request.method == 'POST':
        # Lógica para editar o cliente com o ID especificado
        nome = request.form['nome']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('UPDATE clientes SET nome=?, telefone=?, endereco=? WHERE id=?',
                       (nome, telefone, endereco, id_cliente))
        conn.commit()
        conn.close()
        
        return redirect(url_for('listar_clientes'))
    
    # Lógica para recuperar os detalhes do cliente do banco de dados e exibir o formulário de edição
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE id=?', (id_cliente,))
    cliente = cursor.fetchone()
    conn.close()
    
    return render_template('editar_cliente.html', cliente=cliente)

# Rota para excluir um cliente específico
@app.route('/excluir_cliente/<int:id_cliente>', methods=['GET'])
def excluir_cliente(id_cliente):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM clientes WHERE id=?', (id_cliente,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_clientes'))

@app.route('/api/fornecedores')
def obter_fornecedores_api():
    fornecedores = obter_fornecedores_do_banco_de_dados()
    return jsonify(fornecedores)

# Rota para o cadastro de fornecedores
@app.route('/cadastro_fornecedores', methods=['GET', 'POST'])
def cadastro_fornecedores():
    if request.method == 'POST':
        # Lógica para cadastrar o fornecedor aqui
        # Certifique-se de capturar os dados do formulário corretamente
        
        # Exemplo de como acessar os dados do formulário
        nome = request.form['nome']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        
        # Aqui você pode adicionar a lógica para inserir os dados do fornecedor no banco de dados
        conn = conectar_bd()
        cursor = conn.cursor()
        
        # Não inclua o ID na inserção, pois é autoincrementado
        cursor.execute('INSERT INTO fornecedores (nome, telefone, endereco) VALUES (?, ?, ?)',
                       (nome, telefone, endereco))
        conn.commit()
        conn.close()
        
        # Depois de cadastrar o fornecedor, você pode redirecionar para outra página, se necessário
        return redirect(url_for('listar_fornecedores'))
        
    # Se for uma requisição GET, simplesmente renderize a página de cadastro de fornecedores
    return render_template('cadastro_fornecedores.html')

# Rota para listar os fornecedores cadastrados
@app.route('/listar_fornecedores', methods=['GET'])
def listar_fornecedores():
    # Abra uma conexão com o banco de dados
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Execute uma consulta de teste
    cursor.execute('SELECT * FROM fornecedores LIMIT 5')  # Limita a consulta para retornar apenas 5 fornecedores
    test_data = cursor.fetchall()
    print(test_data)  # Verifica se há dados retornados pela consulta de teste
    
    # Execute a consulta para obter todos os fornecedores
    cursor.execute('SELECT * FROM fornecedores')
    
    # Obtenha todos os resultados da consulta
    fornecedores = cursor.fetchall()
    
    # Feche a conexão com o banco de dados
    conn.close()
    
    # Renderize o template HTML e passe os fornecedores recuperados
    return render_template('listagem_fornecedores.html', fornecedores=fornecedores)

# Rota para editar um fornecedor específico
@app.route('/editar_fornecedor/<int:id_fornecedor>', methods=['GET', 'POST'])
def editar_fornecedor(id_fornecedor):
    if request.method == 'POST':
        # Lógica para editar o fornecedor com o ID especificado
        nome = request.form['nome']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('UPDATE fornecedores SET nome=?, telefone=?, endereco=? WHERE id=?',
                       (nome, telefone, endereco, id_fornecedor))
        conn.commit()
        conn.close()
        
        return redirect(url_for('listar_fornecedores'))
    
    # Lógica para recuperar os detalhes do fornecedor do banco de dados e exibir o formulário de edição
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM fornecedores WHERE id=?', (id_fornecedor,))
    fornecedor = cursor.fetchone()
    conn.close()
    
    return render_template('editar_fornecedor.html', fornecedor=fornecedor)

# Rota para excluir um fornecedor específico
@app.route('/excluir_fornecedor/<int:id_fornecedor>', methods=['GET'])
def excluir_fornecedor(id_fornecedor):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM fornecedores WHERE id=?', (id_fornecedor,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_fornecedores'))

# Rota para api produtos

@app.route('/api/produtos')
def obter_produtos_api():
    produtos = obter_produtos_do_banco_de_dados()
    return jsonify(produtos)

# Rota para o cadastro de produtos
@app.route('/cadastro_produtos', methods=['GET', 'POST'])
def cadastro_produtos():
    if request.method == 'POST':
        # Verifica se todos os campos obrigatórios estão presentes no formulário
        if 'nome' in request.form and 'codigo' in request.form and 'custo' in request.form and 'valor_venda' in request.form and 'tipo_medida' in request.form:
            # Lógica para cadastrar o produto aqui
            # Certifique-se de capturar os dados do formulário corretamente
            # Exemplo de como acessar os dados do formulário
            nome = request.form['nome']
            codigo = request.form['codigo']
            custo = request.form['custo']
            valor_venda = request.form['valor_venda']
            tipo_medida = request.form['tipo_medida']
            
            # Aqui você pode adicionar a lógica para inserir os dados do produto no banco de dados
            conn = conectar_bd()
            cursor = conn.cursor()
            
            # Não inclua o estoque na inserção, pois não está presente no formulário de cadastro
            cursor.execute('INSERT INTO produtos (nome, codigo, custo, valor_venda, tipo_medida) VALUES (?, ?, ?, ?, ?)',
                           (nome, codigo, custo, valor_venda, tipo_medida))
            conn.commit()
            conn.close()
            
            # Depois de cadastrar o produto, você pode redirecionar para outra página, se necessário
            return redirect(url_for('listar_produtos'))
        else:
            # Se algum campo obrigatório estiver ausente, renderize o formulário novamente com uma mensagem de erro
            return render_template('cadastro_produtos.html', error_message="Todos os campos são obrigatórios.")
    
    # Se for uma requisição GET, simplesmente renderize a página de cadastro de produtos
    return render_template('cadastro_produtos.html')

# Rota para listar os produtos cadastrados
@app.route('/listar_produtos', methods=['GET'])
def listar_produtos():
    # Obter os produtos do banco de dados
    produtos = obter_produtos_do_banco_de_dados()
    
    # Renderizar o template HTML e passar os produtos recuperados
    return render_template('listagem_produtos.html', produtos=produtos)

@app.route('/editar_produto/<int:id_produto>', methods=['GET', 'POST'])
def editar_produto(id_produto):
    if request.method == 'POST':
        # Lógica para editar o produto com o ID especificado
        nome = request.form['nome']
        codigo = request.form['codigo']
        custo = request.form['custo']
        valor_venda = request.form['valor_venda']
        tipo_medida = request.form['tipo_medida']
        estoque = request.form['estoque']  # Adicionado o campo de estoque
        
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('UPDATE produtos SET nome=?, codigo=?, custo=?, valor_venda=?, tipo_medida=?, estoque=? WHERE id=?',
                       (nome, codigo, custo, valor_venda, tipo_medida, estoque, id_produto))  # Atualizado para incluir o campo de estoque
        conn.commit()
        conn.close()
        
        return redirect(url_for('listar_produtos'))
    
    # Lógica para recuperar os detalhes do produto do banco de dados e exibir o formulário de edição
    produto = obter_produto_por_id(id_produto)
    
    return render_template('editar_produto.html', produto=produto)

# Rota para excluir um produto específico
@app.route('/excluir_produto/<int:id_produto>', methods=['GET'])
def excluir_produto(id_produto):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produtos WHERE id=?', (id_produto,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_produtos'))

# Rota para carregar os fornecedores via AJAX
@app.route('/api/fornecedores')
def carregar_fornecedores():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM fornecedores')
    fornecedores = cursor.fetchall()
    conn.close()
    return jsonify(fornecedores)

# Rota para carregar os produtos via AJAX
@app.route('/api/produtos')
def carregar_produtos():
    fornecedor_id = request.args.get('fornecedor_id')
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    if fornecedor_id:
        cursor.execute('SELECT id, nome, custo FROM produtos WHERE fornecedor_id = ?', (fornecedor_id,))
    else:
        cursor.execute('SELECT id, nome, custo FROM produtos')
    produtos = cursor.fetchall()
    conn.close()
    return jsonify(produtos)

# Rota para cadastrar uma compra
@app.route('/cadastro_compras', methods=['POST'])
def cadastrar_compra():
    if request.method == 'POST':
        try:
            # Extrair os dados do formulário
            fornecedor = request.form['fornecedor']
            data = request.form['data']
            forma_pagamento = request.form['forma_pagamento']
            desconto = request.form['desconto']
            valor_final = request.form['valor-final']
            
            # Subtrair valor final da compra da tabela "transacoes" com base na forma de pagamento
            conn = conectar_bd()
            cursor = conn.cursor()
            if forma_pagamento == 'Débito':
                cursor.execute("UPDATE transacoes SET debito = debito - ? WHERE id = 1", (valor_final,))
            elif forma_pagamento == 'Crédito':
                cursor.execute("UPDATE transacoes SET credito = credito - ? WHERE id = 1", (valor_final,))
            elif forma_pagamento == 'A Vista':
                cursor.execute("UPDATE transacoes SET avista = avista - ? WHERE id = 1", (valor_final,))
            elif forma_pagamento == 'Pix':
                cursor.execute("UPDATE transacoes SET pix = pix - ? WHERE id = 1", (valor_final,))
            
            # Inserir os dados da compra no banco de dados
            cursor.execute("INSERT INTO compras (fornecedor, data, forma_pagamento, desconto, valor_final) VALUES (?, ?, ?, ?, ?)",
                           (fornecedor, data, forma_pagamento, desconto, valor_final))
            
            # Obter o ID da compra inserida
            id_compra = cursor.lastrowid
            
            # Obter os produtos da compra do formulário
            produtos = request.form.getlist('produto[]')
            quantidades = request.form.getlist('quantidade[]')
            custos_unitarios = request.form.getlist('preco[]')
            
            # Iterar sobre os produtos e inserir cada um deles na tabela de compras_produtos
            for produto, quantidade, custo_unitario in zip(produtos, quantidades, custos_unitarios):
                cursor.execute("INSERT INTO compras_produtos (id_compra, id_produto, nome_produto, quantidade, custo_unitario, valor_total) VALUES (?, ?, ?, ?, ?, ?)",
                               (id_compra, produto, '', quantidade, custo_unitario, float(quantidade) * float(custo_unitario)))
                
                # Atualizar o estoque do produto na tabela "produtos"
                cursor.execute("UPDATE produtos SET estoque = estoque + ? WHERE id = ?", (quantidade, produto))
            
            # Commit para confirmar as mudanças no banco de dados
            conn.commit()
            
            # Flash a mensagem de sucesso
            flash('Compra cadastrada com sucesso!', 'success')
            
            # Redirecionar para a página de listar compras
            return redirect(url_for('listar_compras'))
        
        except Exception as e:
            # Em caso de erro, faça o rollback das alterações no banco de dados
            conn.rollback()
            flash(f'Erro ao cadastrar compra: {str(e)}', 'error')
            return redirect(url_for('listar_compras'))
        finally:
            # Sempre feche a conexão com o banco de dados
            conn.close()

# Rota para listar as compras
@app.route('/listar_compras')
def listar_compras():
    # Conectar-se ao banco de dados
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Consulta SQL para recuperar as compras e seus produtos associados
    cursor.execute("""
        SELECT c.id_compra, f.nome, c.data, c.valor_final
        FROM compras c
        INNER JOIN fornecedores f ON c.fornecedor = f.id
        ORDER BY c.id_compra
    """)
    compras = cursor.fetchall()  # Recupera todas as compras e seus produtos

    # Feche a conexão com o banco de dados
    conn.close()

    # Renderize o template HTML e passe os dados das compras para ele
    return render_template('listar_compras.html', compras=compras)

# Rota para exibir os detalhes da compra para edição
@app.route('/editar_compra/<int:id_compra>')
def editar_compra(id_compra):
    # Conectar-se ao banco de dados
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Consulta SQL para obter os detalhes da compra, incluindo a forma de pagamento
    cursor.execute("""
        SELECT c.id_compra, f.nome, c.data, c.valor_final, c.forma_pagamento
        FROM compras c
        INNER JOIN fornecedores f ON c.fornecedor = f.id
        WHERE c.id_compra = ?
    """, (id_compra,))
    compra = cursor.fetchone()  # Recupera os detalhes da compra

    # Consulta SQL para obter os produtos associados à compra
    cursor.execute("""
        SELECT cp.id_produto, p.nome, cp.quantidade, cp.custo_unitario, cp.valor_total
        FROM compras_produtos cp
        INNER JOIN produtos p ON cp.id_produto = p.id
        WHERE cp.id_compra = ?
    """, (id_compra,))
    produtos = cursor.fetchall()  # Recupera os produtos associados à compra

    # Fechar a conexão com o banco de dados
    conn.close()

    # Renderize o template HTML e passe os detalhes da compra e seus produtos associados para ele
    return render_template('editar_compra.html', compra=compra, produtos=produtos)

def obter_nome_produto_por_id(produto_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()
    conn.close()
    if produto:
        return produto[0]
    return None

@app.route('/api/cadastro_adicao_sitio', methods=['POST'])
def cadastro_adicao_sitio():
    if request.method == 'POST':
        # Certifique-se de capturar os dados do formulário corretamente
        produto_id = request.form['produto']
        quantidade = int(request.form['quantidade'])
        data = request.form['data']
        
        # Obtém o nome do produto com base no seu ID
        nome_produto = obter_nome_produto_por_id(produto_id)
        if not nome_produto:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        # Atualize o estoque do produto no banco de dados 'produtos'
        produto = obter_produto_por_id(produto_id)
        if not produto:
            return jsonify({'error': 'Produto não encontrado'}), 404
        
        estoque_atual = int(produto[6])  # Converte a string para inteiro
        novo_estoque = estoque_atual + quantidade
        
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('UPDATE produtos SET estoque=? WHERE id=?', (novo_estoque, produto_id))
        conn.commit()
        
        # Insira os dados da adição do sítio na tabela 'adicoes_sitio'
        cursor.execute('INSERT INTO adicoes_sitio (produto_id, quantidade, data_adicao, nome_produto) VALUES (?, ?, ?, ?)',
                        (produto_id, quantidade, data, nome_produto))
        conn.commit()
        conn.close()
        
        # Aqui você precisa retornar uma resposta válida
        return jsonify({'success': 'Adição cadastrada com sucesso!'})
    
# Rota para a página de relatório de vendas
@app.route('/relatorio_vendas', methods=['GET', 'POST'])
def relatorio_vendas():
    if request.method == 'POST':
        # Obter os filtros enviados pelo formulário
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')
    
        # Adicionar instruções de registro para verificar os valores dos filtros
        print("Data de início:", data_inicio)
        print("Data de fim:", data_fim)
      
        # Conectar ao banco de dados
        conn = sqlite3.connect('erp.db')
        cursor = conn.cursor()
        
        # Construir a consulta SQL com base nos filtros
        query = "SELECT * FROM vendas WHERE 1=1"
        params = []
        if data_inicio:
            query += f" AND data >= ?"
            params.append(data_inicio)
        if data_fim:
            query += f" AND data <= ?"
            params.append(data_fim)
        
        # Executar a consulta
        cursor.execute(query, params)
        vendas = cursor.fetchall()
        
        # Calcular o total de vendas e o total de lucros
        total_vendas = sum(venda[7] for venda in vendas)
        total_lucros = sum(venda[9] for venda in vendas)
        
        # Fechar a conexão com o banco de dados
        conn.close()
        
        # Renderizar o template com os dados
        return render_template('relatorio_vendas.html', vendas=vendas, total_vendas=total_vendas, total_lucros=total_lucros)
    
    # Se o método for GET, renderizar o formulário vazio
    return render_template('relatorio_vendas.html')

# Rota para a página de adição do sítio
@app.route('/adicao_sitio', methods=['GET', 'POST'])
def adicao_sitio():
    if request.method == 'POST':
        # Certifique-se de capturar os dados do formulário corretamente
        produto_id = request.form['produto']
        quantidade = request.form['quantidade']
        data = request.form['data']
        
        # Adicione a lógica para inserir os dados da adição do sítio na tabela 'adicoes_sitio'
        conn = conectar_bd()
        cursor = conn.cursor()
        
        # Insira os dados na tabela 'adicoes_sitio'
        cursor.execute('INSERT INTO adicoes_sitio (produto_id, quantidade, data) VALUES (?, ?, ?)',
                       (produto_id, quantidade, data))
        conn.commit()
        conn.close()
        
        # Redirecione para outra página após cadastrar a adição do sítio
        return redirect(url_for('adicao_sitio'))
    
    # Se for uma requisição GET, renderize a página de adição do sítio
    # Obtenha as adições do sítio do banco de dados e passe para o template HTML
    adicoes_sitio = obter_adicoes_sitio_do_banco_de_dados()  # Aqui está o problema
    return render_template('adicao_sitio.html', adicoes_sitio=adicoes_sitio)

# Rota para editar uma adicao sitio específico
@app.route('/adicao_sitio/<int:id_adicao_sitio>', methods=['GET', 'POST'])
def editar_adicao_sitio(id_adicao_sitio):
    if request.method == 'POST':
        # Lógica para editar a adição do sítio com o ID especificado
        nome_produto = request.form['nome_produto']
        quantidade = request.form['quantidade']
        data_adicao = request.form['data_adicao']
        
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('UPDATE adicoes_sitio SET nome_produto=?, quantidade=?, data_adicao=? WHERE id=?',
                       (nome_produto, quantidade, data_adicao, id_adicao_sitio))
        conn.commit()
        conn.close()
        
        return redirect(url_for('adicao_sitio'))
    
    # Lógica para recuperar os detalhes da adição do sítio do banco de dados e exibir o formulário de edição
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM adicoes_sitio WHERE id=?', (id_adicao_sitio,))
    adicao_sitio = cursor.fetchone()
    conn.close()
    
    return render_template('editar_adicoes.html', adicao_sitio=adicao_sitio)

# Rota para excluir uma adicao sitio
@app.route('/adicao_sitio/<int:id_adicao_sitio>/excluir', methods=['POST'])
def excluir_adicao_sitio(id_adicao_sitio):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM adicoes_sitio WHERE id=?', (id_adicao_sitio,))
    conn.commit()
    conn.close()
    return redirect(url_for('adicao_sitio'))

# Função para obter o valor em caixa
def get_valor_caixa():
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(debito + credito + avista + pix)
        FROM transacoes
    ''')
    valor_caixa = cursor.fetchone()[0]
    conn.close()
    return valor_caixa

def get_transacoes():
    # Conectar ao banco de dados e obter as transações
    conn = sqlite3.connect('erp.db')  # Substitua pelo seu banco de dados
    cursor = conn.cursor()
    cursor.execute("SELECT debito, credito, avista, pix FROM transacoes")
    transacoes = cursor.fetchall()
    conn.close()
    # Transformar em uma lista de dicionários para facilitar o uso no template
    transacoes_dict = [{'debito': t[0], 'credito': t[1], 'avista': t[2], 'pix': t[3]} for t in transacoes]
    return transacoes_dict

@app.route('/financeiro')
def financeiro():
    valor_caixa = get_valor_caixa()
    transacoes = get_transacoes()
    return render_template('financeiro.html', valor_caixa=valor_caixa, transacoes=transacoes)

# Rota para exibir o formulário de reforço de caixa
@app.route('/reforco_caixa')
def reforco_caixa():
    return render_template('reforco_caixa.html')

# Rota para processar o formulário de reforço ao clicar em "Realizar Reforço"
@app.route('/processar_reforco', methods=['POST'])
def processar_reforco():
    # Conectar ao banco de dados
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Obter os dados do formulário
    descricao_pagamento = request.form['descricao_pagamento']
    valor_reforco = float(request.form['valor_reforco'])
    forma_pagamento = request.form['forma_pagamento']
    data_pagamento = request.form['data_pagamento']

    # Executar a inserção de dados na tabela registro_financeiro com o tipo 'Reforço'
    cursor.execute("INSERT INTO registro_financeiro (descricao, valor, pagamento, data, tipo) VALUES (?, ?, ?, ?, ?)", (descricao_pagamento, valor_reforco, forma_pagamento, data_pagamento, 'Reforço'))
    
    # Commit das mudanças
    conn.commit()

    # Atualizar o saldo na tabela transacoes
    atualizar_saldo(forma_pagamento, valor_reforco, 'Reforço')

    # Fechar conexão
    conn.close()

    # Redirecionar de volta para a página financeiro após o processamento
    return redirect('/financeiro')

# Rota para renderizar a página de sangria de caixa (sangria_caixa.html)
@app.route('/sangria_caixa')
def sangria_caixa():
    return render_template('sangria_caixa.html')

# Rota para processar o formulário de sangria ao clicar em "Realizar Sangria"
@app.route('/processar_sangria', methods=['POST'])
def processar_sangria():
    # Conectar ao banco de dados
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Obter os dados do formulário
    descricao_pagamento = request.form['descricao_pagamento']
    valor_sangria = float(request.form['valor_sangria'])
    forma_pagamento = request.form['forma_pagamento']
    data_pagamento = request.form['data_pagamento']

    # Executar a inserção de dados na tabela registro_financeiro com o tipo 'Sangria'
    cursor.execute("INSERT INTO registro_financeiro (descricao, valor, pagamento, data, tipo) VALUES (?, ?, ?, ?, ?)", (descricao_pagamento, valor_sangria, forma_pagamento, data_pagamento, 'Sangria'))
    
    # Commit das mudanças
    conn.commit()

    # Atualizar o saldo na tabela transacoes
    atualizar_saldo(forma_pagamento, valor_sangria, 'Sangria')

    # Fechar conexão
    conn.close()

    # Redirecionar de volta para a página financeiro após o processamento
    return redirect('/financeiro')

# Função para atualizar o saldo na tabela transacoes
def atualizar_saldo(forma_pagamento, valor, tipo):
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Verificar se é reforço ou sangria e atualizar o saldo na coluna correspondente
    if tipo == 'Reforço':
        cursor.execute(f"UPDATE transacoes SET {forma_pagamento.lower()} = {forma_pagamento.lower()} + ?", (valor,))
    elif tipo == 'Sangria':
        cursor.execute(f"UPDATE transacoes SET {forma_pagamento.lower()} = {forma_pagamento.lower()} - ?", (valor,))

    conn.commit()
    conn.close()

# Rota para exibir o formulário de vendas
@app.route('/venda_balcao')
def venda_balcao():
    # Consultar clientes e produtos no banco de dados
    conn = conectar_bd()
    c = conn.cursor()
    c.execute("SELECT nome FROM clientes")
    clientes = [cliente[0] for cliente in c.fetchall()]
    c.execute("SELECT nome FROM produtos")
    produtos = [produto[0] for produto in c.fetchall()]
    conn.close()

    return render_template('venda_balcao.html', clientes=clientes, produtos=produtos)

# Função para buscar o valor de venda do produto no banco de dados
def buscar_valor_venda_no_banco_de_dados(produto):
    # Conectar ao banco de dados
    conn = sqlite3.connect('erp.db')
    cursor = conn.cursor()

    # Executar a consulta para obter o valor de venda do produto
    cursor.execute("SELECT valor_venda FROM produtos WHERE nome = ?", (produto,))
    resultado = cursor.fetchone()

    # Fechar a conexão com o banco de dados
    conn.close()

    # Se o produto foi encontrado, retornar o valor de venda, caso contrário, retornar None
    if resultado:
        return resultado[0]
    else:
        return None

@app.route('/buscar_valor_venda')
def buscar_valor_venda():
    produto = request.args.get('produto')
    # Lógica para buscar o valor de venda do produto no banco de dados
    valor_venda = buscar_valor_venda_no_banco_de_dados(produto)
    return jsonify({'valor_venda': valor_venda})

# Rota para registrar a venda
@app.route('/registrar_venda', methods=['POST'])
def registrar_venda():
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Data e hora atual
    cliente = request.form['cliente']
    produto = request.form['produto']
    quantidade = int(request.form['quantidade'])

    # Verificar se o campo de desconto foi preenchido
    if 'desconto' in request.form and request.form['desconto'] != '':
        desconto = float(request.form['desconto'])
    else:
        desconto = 0.0  # Defina um valor padrão de desconto caso o campo esteja vazio

    # Aqui pegamos o valor de venda do formulário, em vez do banco de dados
    valor_venda = float(request.form['valor_venda'])

    forma_pagamento = request.form['forma_pagamento']

    # Consultar o custo do produto no banco de dados
    conn = conectar_bd()
    c = conn.cursor()
    c.execute("SELECT custo, estoque FROM produtos WHERE nome=?", (produto,))
    row = c.fetchone()
    custo = row[0]
    estoque_atual = row[1]

    # Atualizar o estoque do produto
    novo_estoque = estoque_atual - quantidade
    c.execute("UPDATE produtos SET estoque=? WHERE nome=?", (novo_estoque, produto))

    total = (quantidade * valor_venda) - desconto
    custo_total = quantidade * custo
    lucro = total - custo_total

    # Inserir os dados da venda no banco de dados
    c.execute("INSERT INTO vendas (data, cliente, produto, quantidade, valor_venda, desconto, total, forma_pagamento, lucro) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (data, cliente, produto, quantidade, valor_venda, desconto, total, forma_pagamento, lucro))
    
    # Atualizar os valores na tabela transacoes com base na forma de pagamento
    if forma_pagamento == 'A vista':
        c.execute("UPDATE transacoes SET avista = avista + ? WHERE id = 1", (total,))
    elif forma_pagamento == 'Debito':
        c.execute("UPDATE transacoes SET debito = debito + ? WHERE id = 1", (total,))
    elif forma_pagamento == 'Credito':
        c.execute("UPDATE transacoes SET credito = credito + ? WHERE id = 1", (total,))
    elif forma_pagamento == 'Pix':
        c.execute("UPDATE transacoes SET pix = pix + ? WHERE id = 1", (total,))

    conn.commit()
    conn.close()

    return redirect(url_for('venda_balcao'))

# Rota para exibir a listagem de vendas
@app.route('/listar_vendas')
def listar_vendas():
    conn = sqlite3.connect('erp.db')
    c = conn.cursor()
    c.execute("SELECT * FROM vendas")
    vendas = c.fetchall()
    conn.close()
    return render_template('listagem_vendas.html', vendas=vendas)

# Rota para editar uma venda pelo ID
@app.route('/editar_venda/<int:venda_id>', methods=['GET', 'POST'])
def editar_venda(venda_id):
    if request.method == 'POST':
        # Atualize a venda no banco de dados
        conn = sqlite3.connect('erp.db')
        c = conn.cursor()
        c.execute("UPDATE vendas SET cliente=?, produto=?, quantidade=?, valor_venda=?, desconto=?, total=?, forma_pagamento=?, lucro=? WHERE id=?",
                  (request.form['cliente'], request.form['produto'], request.form['quantidade'], request.form['valor_venda'], request.form['desconto'], request.form['total'], request.form['forma_pagamento'], request.form['lucro'], venda_id))
        conn.commit()
        conn.close()
        flash('Venda atualizada com sucesso', 'success')
        return redirect(url_for('listar_vendas'))
    else:
        # Obtenha os detalhes da venda do banco de dados e exiba o formulário de edição
        conn = sqlite3.connect('erp.db')
        c = conn.cursor()
        c.execute("SELECT * FROM vendas WHERE id=?", (venda_id,))
        venda = c.fetchone()
        conn.close()
        return render_template('editar_venda.html', venda=venda, venda_id=venda_id)

# Rota para excluir uma venda pelo ID
@app.route('/excluir_venda/<int:venda_id>')
def excluir_venda(venda_id):
    # Exclua a venda do banco de dados
    conn = sqlite3.connect('erp.db')
    c = conn.cursor()
    c.execute("DELETE FROM vendas WHERE id=?", (venda_id,))
    conn.commit()
    conn.close()
    flash('Venda excluída com sucesso', 'success')
    return redirect(url_for('listar_vendas'))

# Rota para compras
@app.route('/compras')
def compras():
    return render_template('compras.html')

# Rota para fluxo de caixa
@app.route('/fluxo_caixa')
def fluxo_caixa():
    # Abra uma conexão com o banco de dados
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Execute uma consulta de teste
    cursor.execute('SELECT * FROM registro_financeiro LIMIT 30')  # Limita a consulta para retornar apenas 5 clientes
    test_data = cursor.fetchall()
    print(test_data)  # Verifica se há dados retornados pela consulta de teste
    
    # Execute a consulta para obter todos os clientes
    cursor.execute('SELECT * FROM registro_financeiro')
    
    # Obtenha todos os resultados da consulta
    registro_financeiro = cursor.fetchall()
    
    # Feche a conexão com o banco de dados
    conn.close()
    
    # Renderize o template HTML e passe os clientes recuperados
    return render_template('fluxo_caixa.html', registro_financeiro=registro_financeiro)


if __name__ == '__main__':
    app.run(debug=True)
