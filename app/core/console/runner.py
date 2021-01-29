from .server import console
from .database import migration, model
from .http import route, controller


def run_server(server):
    """
    """
    return console.run(server)


def create_migration(name):
    """
    :param name:
    :return:
    """
    return migration.create_migration(name)


def migrate(name):
    """
    Executa migrações de bancos
    :param name: string
    :return:
    """
    return migration.run_migrate(name)


def create_model(name):
    """
    Criar um novo arquivo de interação com banco de dados.
    """
    return model.create_model(name)


def create_controller(name):
    """
    """
    return controller.create_controller(name)


def create_route(name):
    """
    """
    return route.create_route(name)
