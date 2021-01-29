from flask import jsonify


def index():
    """Return Welcomme message"""
    return jsonify(
        {
            'status': 'ok',
            'message': 'Tudo funcionando por aqui!'
        }
    )


