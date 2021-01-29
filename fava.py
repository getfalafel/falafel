import sys
import argparse
from app.core.console import runner


def main(shell_arguments):
    """
    Verifica a opção utilizado e executa comando correspondente
    :param shell_arguments: shell_arguments
    :return: void
    """

    args = parse_command_line(shell_arguments)
    if args.dbmigrate is not None:
        runner.migrate(args.dbmigrate)

    elif args.dbseed is not None:
        runner.runSeeder(args.dbseed)

    elif args.makemigration is not None:
        runner.create_migration(args.makemigration)

    elif args.makemodel is not None:
        runner.create_model(args.makemodel)

    elif args.makeseeder is not None:
        runner.createSeed(args.makeseeder)

    elif args.makecontroller is not None:
        runner.create_controller(args.makecontroller)

    elif args.makeroute is not None:
        runner.create_route(args.makeroute)

    elif args.server is not None:
        runner.run_server(args.server)

    return 0


def parse_command_line(args):
    """
    Parse commands for trader tool
    """

    description = "Use -h to list all commands."

    #
    parser = argparse.ArgumentParser(description=description)

    # Run server
    parser.add_argument('-s', '--server', nargs='?', type=str, help='Run application in development', const='5000')

    # Create database
    parser.add_argument('-mkmigration', '--makemigration', nargs='?', type=str, help='Create a new migration file')
    parser.add_argument('-mkseeder', '--makeseeder', nargs='?', type=str, help='Create a new seeder class')
    parser.add_argument('-mkmodel', '--makemodel', nargs='?', type=str, help='Create a new Model file')

    # Database Commands
    parser.add_argument('-migrate', '--dbmigrate', nargs='?', type=str, help='Run all Migration', const='all')
    parser.add_argument('-seed', '--dbseed', nargs='?', type=str, help='Run all database seeds', const='all')

    # Create Controllers
    parser.add_argument('-mkcontroller', '--makecontroller', nargs='?', type=str, help='Create a new Controller file')

    # Create Routes
    parser.add_argument('-mkroute', '--makeroute', nargs='?', type=str, help='Create a new Route file')

    ###
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
