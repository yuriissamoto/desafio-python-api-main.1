from flask import json, jsonify, request, Flask
from api import db, app
from datetime import datetime

def health():
    """
    Status da API
    """
    responseBody = {
        "status": "Service Running"
    }
    return jsonify(responseBody)


class despesa(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    data = db.Column(db.Text, default=datetime.utcnow)
    tipo = db.Column(db.Text)
    categoria = db.Column(db.Text)

    def serialize(self):
        return {
            'id': self.id,
            'valor': self.valor,
            'descricao': self.descricao,
            'data': self.data,
            'tipo': self.tipo,
            'categoria': self.categoria
        }

    def set_data(self, data, dialect):
        if type(data) is str:
            return datetime.datetime.strptime(data, '%d/%m/%Y')
        return data

    allowed_tipos = ['Dinheiro', 'Débito', 'Crédito', 'Pix']

    def set_tipo(self, tipo):
        if tipo in self.allowed_tipos:
            self.tipo = tipo
        else:
            self.tipo = "Tipo inválido! " \
                        "Digite um dos seguintes tipos de pagamentos: " \
                        "Dinheiro, Débito, Crédito, Pix"

    allowed_categorias = ['custos fixos', 'alimentação', 'transporte', 'medicamentos']

    def set_categorias(self, categoria):
        if categoria in self.allowed_categorias:
            self.categoria = categoria
        else:
            self.categoria = "Tipo inválido! " \
                             "Digite um dos seguintes tipos de pagamentos: " \
                             "custos fixos, alimentação, transporte, medicamentos"

despesas = []

def incluir_despesa():
    parametros = request.json
    me = despesa()
    me.id = parametros['id']
    me.valor = parametros['valor']
    me.descricao = parametros['descricao']
    me.set_data = parametros['data']
    me.tipo = parametros['tipo']
    me.categoria = parametros['categoria']


    despesa_list = me
    despesas.append(despesa_list)

    db.create_all()
    db.session.add(me)
    db.session.commit()
    return jsonify(me.serialize())

def lista_despesa():
    mes_atual = datetime.now().month

    # Filtrar as despesas pelo mês atual
    despesas_mes_atual = [despesa for despesa in despesas if despesa.data.month == mes_atual]

    # Retornar a resposta da API
    response_data = {'data': despesas_mes_atual, 'success': True}
    return jsonify(response_data)


    #despesas = request.json
    #return jsonify(despesas.serialize())


