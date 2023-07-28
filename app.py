from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime , timedelta
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    servico_banco = db.Column(db.String(200), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_agendamento = db.Column(db.DateTime, nullable=False)
    nome_cliente = db.Column(db.String(100), nullable=False)
    
    
    def __repr__(self):
        return '<Servico %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        servico = request.form['servico']
        data_agendamento = datetime.strptime(request.form['data_agendamento'], '%Y-%m-%dT%H:%M')
        cliente_nome = request.form['cliente_nome']  
        servicos = Agendamento(servico_banco=servico,nome_cliente=cliente_nome,data_agendamento=data_agendamento)

        
        db.session.add(servicos)
        db.session.commit()
        return redirect('/')
        

    else:
        novo_servico = Agendamento.query.order_by(Agendamento.data_criacao).all()
        return render_template('index.html', todos_serviços=novo_servico)


@app.route('/deletar/<int:id>')
def deletar(id):
    deletar_servico = Agendamento.query.get_or_404(id)

    try:
        db.session.delete(deletar_servico)
        db.session.commit()
        return redirect('/')
    except:
        return 'Não é possível deletar'

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    editar_sercico = Agendamento.query.get_or_404(id)

    if request.method == 'POST':
        editar_sercico.servico_banco = request.form['servico_editar']
        editar_data_agendamento = datetime.strptime(request.form['data_agendamento_editar'], '%Y-%m-%dT%H:%M')
        editar_sercico.nome_cliente = request.form['cliente_nome_editar']

       
        data_atual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
         
        if data_atual >= (editar_sercico.data_agendamento - timedelta(days=3)):
            return render_template('erro.html')
                    

        editar_sercico.data_agendamento = editar_data_agendamento
        db.session.commit()
        return redirect('/')
        

    else:
        return render_template('editar.html', todos_serviços=editar_sercico)


if __name__ == "__main__":
    app.run(debug=True)

