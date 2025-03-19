from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# with para ficar simples o código, connect para conectar ao banco de dados, conn joga tudo aí dentro do conn que é uma variável (o que e onde)
def init_db():
    # conn está colocando o conteudo no conn
    with sqlite3.connect('database.db') as conn:
        # tratamento de erros: create table if not exists
        conn.execute("""CREATE TABLE IF NOT EXISTS livros(
        id  INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        categoria TEXT NOT NULL,
        autor TEXT NOT NULL,
        imagem_url TEXT NOT NULL                                      
        )     
        """)

        print("Banco de dados inicializado com sucesso!")
init_db()

#Rota de início
@app.route('/')
def homepage():
    return '<h2>Minha página com Flask mais linda que a do Vini!</h2>'

@app.route("/doar", methods=['POST'])
def doar():

    dados = request.get_json()

    titulo = dados.get("titulo")
    categoria = dados.get("categoria")
    autor = dados.get("autor")
    imagem_url = dados.get("imagem_url")

    # if not titulo or not categoria or not autor or not imagem_url: pode ser assim também.

    if not all ([titulo, categoria, autor, imagem_url]):
        return jsonify({'erro':'Todos os campos são obrigatórios'}),400

    with sqlite3.connect('database.db') as conn:
        # o f é pro template string do python 
        conn.execute(f""" INSERT INTO livros (titulo,categoria,autor,imagem_url) VALUES (?,?,?,?)""",(titulo, categoria, autor, imagem_url))
        # sql injector (?,?,?,?)    
        conn.commit()
        return jsonify({'mensagem':'Livros cadastrados com sucesso'}), 201
    
    # no banco de dados usar aspas duplas
@app.route('/livros', methods=['GET'])
def listar_livros():
        with sqlite3.connect('database.db') as conn:
            livros = conn.execute("SELECT * FROM livros").fetchall()

        livros_formatados = []
        for livro in livros:
            dicionario_livros = {
                "id": livro[0],
                "titulo": livro[1],
                "categoria": livro[2],
                "autor": livro[3],
                "imagem_url": livro[4]
        }
        livros_formatados.append(dicionario_livros)
        return jsonify(livros_formatados)

if __name__ == "__main__":
        app.run(debug=True)
        
        