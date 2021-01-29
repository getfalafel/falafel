from textwrap import dedent
from os import path
import black


def create_controller(name):
    """
    Criar arquivo para tratamento de controles
    """

    name = name.lower()
    if path.exists('app/http/controllers/' + name.title() + 'Controller.py'):
        print("#######")
        print("-> Error!")
        print("-> Controller " + name.title() + " existe!")
        print("-> Verifique o arquivo app/http/controllers/" + name.title() + 'Controller.py')
        print("#######")

    else:
        with open('app/http/controllers/' + name.title() + 'Controller.py', 'w') as controller:
            content = dedent("""\
                def get():
                    # Edite 
                    # """ + name.title() + """ controllers
                    # Utilize para separar a lógica da aplicação de suas rotas

                    return "Hello, """ + name.title() + """ Controller "
                """)

            mode = black.FileMode()
            formatted = black.format_file_contents(content, fast=False, mode=mode)
            controller.write(formatted)

            print("#######")
            print("-> Controller " + name.title() + " criada com sucesso!")
            print("-> Verifique o arquivo em app/http/controllers/")
            print("#######")


def create_controller_cmd(model):
    """
    """
    name = model.lower()
    with open('app/http/controllers/' + model + 'Controller.py', 'w') as controller:
        content = "from app.database.Models." + model + " import " + model + " \n" + \
                  "from flask import jsonify, request\n" \
                  "from app.utils.helpers import http_error\n"\
                  "from app.core.database import db\n\n" + \
                  "def get():\n" \
                  "\t" + name + " = " + model + ".query.all() or http_error(204)\n"\
                  "\treturn jsonify({'data': " + name + "}), 200\n\n" \
                  "def create():\n" + \
                  "\treturn jsonify({'message': 'users'})\n\n" \
                  "def find(" + name + "_id):\n" + \
                  "\t" + name + " = " + model + ".query.filter_by(id=" + name + "_id).first() or http_error(204)\n" \
                  "\treturn jsonify({'message': " + name + "}), 200\n\n" \
                  "def update():\n" + \
                  "\treturn jsonify({'message': '" + name + "'}), 200\n\n" \
                  "\n\n"

        mode = black.FileMode()
        formatted = black.format_file_contents(content, fast=False, mode=mode)
        controller.write(formatted)


