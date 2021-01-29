from app.core.console.http import route, controller
from textwrap import dedent
from os import listdir, remove
from fnmatch import fnmatch
from sqlalchemy import create_engine, \
    MetaData, \
    orm, \
    exc, \
    inspect, \
    Table, \
    insert, \
    Column, \
    Integer, \
    TIMESTAMP, \
    Text
from dynaconf import settings
from datetime import datetime
import inflect
import toml
from importlib import import_module
from . import model


""" Comandos de interação com base de dados """
engine = create_engine(settings.get('SQLALCHEMY_DATABASE_URI'))
metadata = MetaData(bind=engine)
create_session = orm.sessionmaker(bind=engine)
session = create_session()


def create_migration(name):
    """
    Criar um arquivo de migration com a classe determinada
    :param name: string
    :return: void
    """
    name = name.lower()
    p = inflect.engine()

    for file in listdir(settings.get('FALAFEL_DIR') + settings.get('MIGRATIONS_DIR')):
        if (fnmatch(file, "*.toml")) and fnmatch(file, name + "*"):
            print("#######")
            print("-> Error!")
            print("-> Migration " + name + " existe!")
            print("-> Verifique o arquivo em " + settings.get('FALAFEL_DIR')
                  + settings.get('MIGRATIONS_DIR') + '/')
            print("#######")
            raise SystemExit()

    if "create" in name:
        with open(settings.get('FALAFEL_DIR') + settings.get('MIGRATIONS_DIR')
                  + '/' + datetime.now().strftime("%Y%m%d%H%M%S") + '_' + name
                  + '.toml', 'w') as migration:

            table_name = name.replace('create_', '')
            content = dedent("""\
                table_name = '""" + p.plural(table_name) + """'
                action = 'create'
                [create]
                    [create.id]
                    primary_key = "True"
                    type = "Integer"

                    [create.created_at]
                    default = "datetime.utcnow"
                    nullable = "False"
                    type = "TIMESTAMP"

                    [create.updated_at]
                    nullable = "False"
                    onupdate = "datetime.utcnow"
                    type = "TIMESTAMP"
            """)

            migration.write(content)

            print("#######")
            print("-> Migration " + name + " criada com sucesso!")
            print("-> Verifique o arquivo em " + settings.get('FALAFEL_DIR') +
                  settings.get('MIGRATIONS_DIR') + '/' + datetime.now().strftime("%Y%m%d%H%M%S") + '_' + name + '.toml')
            print("#######")

    elif "update" in name:
        with open(settings.get('FALAFEL_DIR') + settings.get('MIGRATIONS_DIR')
                  + '/' + datetime.now().strftime("%Y%m%d%H%M%S") + '_' + name
                  + '.toml', 'w') as migration:
            table_name = name.replace('update_', '')
            content = dedent("""\
                table_name = '""" + p.plural(table_name) + """'
                action = 'update'
                [update]
                    [update.example]
                    item = "String"
            """)

            migration.write(content)

            print("#######")
            print("-> Migration " + name + " criada com sucesso!")
            print("-> Verifique o arquivo em " + settings.get('FALAFEL_DIR') +
                  settings.get('MIGRATIONS_DIR') + '/' + name + '_' + datetime.now().strftime("%Y%m%d%H%M%S") + '.toml')
            print("#######")
    else:
        print("-> Não é possível criar migration, verifique a documentação!")
        print("-> Ex:")
        print("-> create: python3 fava.py -mkmigration create_name_table_singular")
        print("-> update: python3 fava.py -mkmigration update_name_table_singular")


def run_migrate(name):
    """
    Executar um todos arquivos de migração
    :param name: string
    :return: void
    """

    """ 
    Antes de executar qualquer migração, verificamos se a tabela de migração existe.
    """
    if check_exists('migrations') is False:
        create_migrations_table()

    tables = []
    if name == 'all' or name == '':
        print('############################')
        print('-> Running migrations...')
        print('############################\n')

        migration_files = sorted(listdir(settings.get('FALAFEL_DIR') + settings.get('MIGRATIONS_DIR')))
        for file in migration_files:
            if (fnmatch(file, "*.toml")) and (file != "__init__.py"):
                migration = toml.load(settings.get('FALAFEL_DIR') + settings.get('MIGRATIONS_DIR') + '/' + file)
                if check_exists(migration.get('table_name')) is False:
                    tables.append(file.replace('.toml', ''))
                    if migration.get('create'):
                        run_create_migration(migration)
                    elif migration.get('update'):
                        pass
                    elif migration.get('delete'):
                        pass
                    else:
                        print("-> Columns doesn't exists in " + migration.get('table_name'))
                        print("-> Check documentation in http://falafel.docs")

        if tables:
            save_migration_sate(str(tables))

        print('############################')
        print('All migrations processed')

    else:
        pass

    pass


def run_create_migration(migration):
    """
    Criar arquivos de Model para novas migrações
    """
    
    class_name = model.create_model_for_migration(migration)
    if class_name:
        route.create_route_cmd(class_name)
        controller.create_controller_cmd(class_name)
        model_path = settings.get('MODELS_DIR').replace('/', '.') + "." + class_name
        db_module = getattr(import_module(model_path), class_name)
        try:
            db_module.metadata.create_all(engine)
            print('Success when running the Model Import for ' + class_name)
        except Exception as err:
            remove(model_path)
            raise SystemExit(err)


def check_exists(table_name):
    """
    :param table_name: string
    :return: boolean
    """
    if table_name in inspect(engine).get_table_names():
        return True
    else:
        return False


def create_migrations_table():
    """
    Criação de tabela com informações de migrações
    :return: void
    """
    try:
        migration_table = Table('migrations', metadata,
                                Column('id', Integer, primary_key=True),
                                Column('table', Text, nullable=False),
                                Column('created_at', TIMESTAMP, nullable=False, default=datetime.utcnow))
        metadata.create_all(engine)
    except exc.SQLAlchemyError as err:
        print('#########################')
        print('-> Error in migration task!')
        print('#########################\n')
        raise SystemExit(err)


def save_migration_sate(name):
    """
    :param name:
    :return:
    """
    try:
        migration_table = Table('migrations', metadata, autoload=True)
        insert_migration = insert(migration_table)
        insert_migration = insert_migration.values(
            {"table": name, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        )
        session.execute(insert_migration)
        session.commit()
    except Exception as err:
        session.rollback()
        print(err)
