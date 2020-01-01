# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 14:05:55 2019

@author: GUSTAVOM
"""

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Parte 1 - Criar Blockchain

class Blockchain:
    # Inicialização da classe:
    def __init__(self):
        # Inicializa lista:
        self.chain = []
        
        # Criação do bloco Genesis:
        self.create_block(proof = 1, previous_hash = '0')
    
    # Definição da função create_block:
    def create_block(self, proof, previous_hash):
        # Dicionário:
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        
        # Criar bloco:
        self.chain.append(block)
        return block
    
    # Método para retornar o bloco anterior:    
    def get_previous_block(self):
        return self.chain[-1]
    
    # Obtendo o valor do hash, através de "new_proof" (golden nonce) --> Mineração
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            # Geração do Hash, com nível de dificuldade com 4 zeros à esquerda (**2)
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            
            # Verifica se atende o nível de dificuldade (4 zeros à esquerda):
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # Retorna o Hash de um bloco:
    def hash(self, block):
        # Transforma o bloco para o formato Json
        encoded_block = json.dumps(block, sort_keys = True).encode()
        
        # Obtem o hash do bloco em formato Hexadecinal:
        return hashlib.sha256(encoded_block).hexdigest()
    
    #Faz a validação de toda cadeia de blocos:
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            
            # Verifica se o previous_hash do bloco que está sendo analisado é igual ao hash do bloco anterior. Caso não seja, interrompe o processo:
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
             # Verifica se atende o nível de dificuldade (4 zeros à esquerda):
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            # Incrementa o index do Loop
            previous_block = block
            block_index += 1
            
        return True


# Cria a aplicação Web com Flask:    
app = Flask(__name__)

# Instancia o objeto Blockchain:
blockchain = Blockchain()

# Faz a mineração do bloco:
@app.route('/mine_block', methods = ['GET'])

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    
    # Cria o bloco:
    block = blockchain.create_block(proof, previous_hash)
    # Exibe na página:
    response = {'message': 'Parabéns! Você minerou o bloco.',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    
    return jsonify(response), 200

# Retorna todo o Blockchain    
@app.route('/get_chain', methods = ['GET'])

def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Faz a validação de toda o Blockchain:
@app.route('/is_valid', methods = ['GET'])

def is_valid():
    
    if blockchain.is_chain_valid(blockchain.chain):
        response = {'message': 'Toda a Blockchain foi validada com sucesso!'}
    else:
        response = {'message': 'Ocorreram erros ao validar a Blockchain'}
        
    return jsonify(response), 200

app.run(host= '0.0.0.0', port = 5000)
    
