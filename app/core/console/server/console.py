import os
import webbrowser


def run(server):
    """
    Determine ambiente variables for Flask runner
    :param server:
    :return:
    """

    print('###############################################')
    print('Open project on browser')
    ## print('Open project on browser. Please press "F5" Key after server load!')

    ## webbrowser.open('http://localhost:' + server)

    print('###############################################')
    print('Running server in port: ' + server)
    print('###############################################')

    os.environ['FLASK_ENV'] = "development"
    os.environ['FLASK_APP'] = "app.run:create_app"
    os.system('flask run --port ' + server)


def build():
    """
    Preparar pacote final para distribuição do app
    :return:
    """

    print('###############################################')