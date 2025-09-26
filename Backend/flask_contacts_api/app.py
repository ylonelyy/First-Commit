from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from bson.json_util import dumps
import database

app = Flask(__name__)
CORS(app, 
     resources={r"/*": {"origins": "http://localhost:5173"}}, 
     methods=["GET", "PUT", "DELETE", "POST", "OPTIONS"])

# ===========================
# ROTAS DE CONTATOS
# ===========================

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = database.get_all_contacts()
    if not contacts:
        return jsonify({'error': 'Nenhum contato encontrado'}), 404
    # Usa dumps para serializar ObjectId
    return Response(dumps({'contacts': contacts}), mimetype='application/json')

@app.route('/contacts/<email>', methods=['PUT'])
def update_contact(email):
    data = request.get_json()
    updated = database.update_contact(email, data)
    if not updated:
        return jsonify({'error': 'Contato não encontrado'}), 404
    return Response(dumps({'message': 'Contato atualizado com sucesso', 'contact': updated}), mimetype='application/json')

@app.route('/contacts/<email>', methods=['DELETE'])
def delete_contact(email):
    deleted = database.delete_contact(email)
    if not deleted:
        return jsonify({'error': 'Contato não encontrado'}), 404
    return jsonify({'message': 'Contato deletado com sucesso'}), 200

@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({'error': 'JSON inválido - campo "email" obrigatório'}), 400
    
    existing = database.get_contact_by_email(data['email'])
    if existing:
        return jsonify({'error': 'Contato já existe'}), 409

    created = database.add_contact(data)
    return Response(dumps({'message': 'Contato criado', 'contact': created}), mimetype='application/json'), 201

# ===========================
# INICIALIZAÇÃO DO SERVIDOR
# ===========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
