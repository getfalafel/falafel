from dynaconf import settings
from textwrap import dedent
from os import path
import toml
import inflect
import black

p = inflect.engine()
mode = black.FileMode()


def create_route(name):
    """ Criar arquivo para tratamento de rotas """

    name = name.lower()
    if path.exists('app/http/controllers/' + name.capitalize() + 'Controller.py'):

        if check_route_exists(name):
            print("#######")
            print("-> Error!")
            print("-> Rota " + name + " existe!")
            print("-> Verifique o arquivo em app/http/routes/" + name + '.py')
            print("#######")

        else:
            with open(settings.get('FALAFEL_DIR') + settings.get('ROUTES_DIR') + '/' + name + '.py', 'w') as route:
                content = dedent("""\
                    from app.http.controllers import """ + name.capitalize() + """Controller
                    from flask import Blueprint
                    """ + name + """ = Blueprint('""" + name + """', __name__, url_prefix='/""" + p.plural(name) + """')

                    @""" + name + """.route("/", methods=['GET'])
                    def index():
                        # """ + name + """ routes
                        # Utilize para separar as rotas da lógica de sua aplicação
                    
                        return """ + name.capitalize() + """Controller.index()

                    def init_app(app):
                        app.register_blueprint(""" + name + """)

                    """)

                formatted = black.format_file_contents(content, fast=False, mode=mode)
                route.write(formatted)

                update_route_list(name)

                print("#######")
                print("-> Rota " + name + " criada com sucesso!")
                print("-> Verifique o arquivo em app/http/routes/")
                print("#######")
    else:
        print("#######")
        print("-> Error!")
        print("-> Controller " + name.capitalize() + " não existe!")
        print("-> Rota precisa de um controlador para funcionar adequadamente.")
        print("-> Crie o controlador primeiro!")
        print("-> Crie um controlador digitando:")
        print("#######")
        print("python3 fava.py -mkcontroller " + name.capitalize())
        print("#######")


def create_route_cmd(model):
    """
    """

    name = model.lower()
    if check_route_exists(name) is False:
        with open(settings.get('FALAFEL_DIR') + settings.get('ROUTES_DIR') + '/' + name + '.py', 'w') as route:
            content = dedent("""\
                from app.http.controllers import """ + name.capitalize() + """Controller
                from flask import Blueprint
                """ + name + """ = Blueprint('""" + name + """', __name__, url_prefix='/""" + p.plural(name) + """')
    
                @""" + name + """.route("/", methods=['GET'])
                def index():
                    return """ + name.capitalize() + """Controller.index()
                    
                @""" + name + """.route("/create", methods=['POST'])
                def index():
                    return """ + name.capitalize() + """Controller.create()
                    
                @""" + name + """.route("/<""" + name + """_id>", methods=['GET'])
                def find(""" + name + """_id):
                    return """ + name.capitalize() + """Controller.find()
                    
                @""" + name + """.route('/update', methods=['PUT'])
                def update():
                    return """ + name.capitalize() + """Controller.update()
    
                def init_app(app):
                    app.register_blueprint(""" + name + """)
    
                """)

            formatted = black.format_file_contents(content, fast=False, mode=mode)
            route.write(formatted)

            update_route_list(name)
            print("#######")
            print("-> Rota " + name + " criada com sucesso!")
            print("-> Verifique o arquivo em app/http/routes/")
            print("#######")


def update_route_list(route):
    """
    Atualizar arquivo de configuração com novas rotas
    """

    with open('app/config/app.toml', 'r+') as app_config_file:
        app_config_data = toml.load('app/config/app.toml')
        app_config_data.get('default').get('EXTENSIONS').append(
            'app.http.routes.' + route + ':init_app')
        toml.dump(app_config_data, app_config_file)


def check_route_exists(name):
    """
    Checar se Arquivo Model existe
    """
    if path.exists(settings.get('FALAFEL_DIR') + settings.get('ROUTES_DIR') + '/' + name + '.py'):
        return True
    else:
        return False
