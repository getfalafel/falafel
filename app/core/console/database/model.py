from textwrap import dedent
from os import listdir, path
from fnmatch import fnmatch
import inflect
import black
from dynaconf import settings


def create_model(name):
    """
    Criar nova Model
    :param name: string
    :return: void
    """
    name: name.lower()
    p = inflect.engine()
    class_name = ''
    class_name_array = name.split('-')
    for item in class_name_array:
        class_name = class_name + item.capitalize()

    for file in listdir(settings.get('FALAFEL_DIR') + settings.get('MODELS_DIR')):
        if (fnmatch(file, "*.py")) and fnmatch(file, class_name + ".py"):
            print("#######")
            print("-> Error!")
            print("-> Model " + class_name + " existe!")
            print("-> Verifique o arquivo em " + settings.get('FALAFEL_DIR')
                  + settings.get('MODELS_DIR') + '/')
            print("#######")
            raise SystemExit()

    with open(settings.get('FALAFEL_DIR') + settings.get('MODELS_DIR') + '/' + class_name + '.py', 'w') as model:
        table_name = p.plural(name)

        content = dedent("""\
        from app.core.database import db
        from sqlalchemy_serializer import SerializerMixin
        from datetime import datetime
        

        class """ + class_name + """(db.Model, SerializerMixin):
            __tablename__ = '""" + table_name + """'
            id = db.Column(db.Integer, primary_key=True)
            created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow, server_default=db.text('0'))
            updated_at = db.Column(db.TIMESTAMP, onupdate=datetime.utcnow, nullable=True)
            
            def __init__(self):
            
            
        """)

        mode = black.FileMode()
        formatted = black.format_file_contents(content, fast=False, mode=mode)

        model.write(content)

        print("#######")
        print("-> Model " + class_name + " criada com sucesso!")
        print("-> Verifique o arquivo em " + settings.get('FALAFEL_DIR') + settings.get(
            'MODELS_DIR') + '/' + class_name + '.py')
        print("#######")


def create_model_for_migration(migration):
    """
    Executar migration
    """
    p = inflect.engine()
    table_name = migration.get("table_name")
    class_name = p.singular_noun(table_name.title().replace('_', ''))

    if check_model_exists(class_name) is False:
        create_columns = []
        relationship_columns = []
        relationship_imports = []
        mk_column = ''
        columns_names = []
        for column in migration.get('create'):
            mk_column = '{} = db.Column('.format(column)
            if migration.get('create').get(column).get('type'):
                if migration.get('create').get(column).get('type') == 'String':
                    if migration.get('create').get(column).get('length'):
                        mk_column = mk_column + "db.String({})".format(migration.get('create').get(column).get('length'))
                    else:
                        mk_column = mk_column + "db.String(255)"
                elif migration.get('create').get(column).get('type') == 'Text':
                    if migration.get('create').get(column).get('length'):
                        mk_column = mk_column + "db.Text({})".format(migration.get('create').get(column).get('length'))
                    else:
                        mk_column = mk_column + "db.Text()"
                else:
                    mk_column = mk_column + "db.{}".format(migration.get('create').get(column).get('type'))
                if migration.get('create').get(column).get('unique'):
                    mk_column = mk_column + ", unique={}".format(migration.get('create').get(column).get('unique'))
                if migration.get('create').get(column).get('primary_key'):
                    mk_column = mk_column + ", primary_key={}".format(
                        migration.get('create').get(column).get('primary_key'))
                if migration.get('create').get(column).get('nullable'):
                    mk_column = mk_column + ", nullable={}".format(migration.get('create').get(column).get('nullable'))
                if migration.get('create').get(column).get('default'):
                    mk_column = mk_column + ", default={}".format(migration.get('create').get(column).get('default'))
                if migration.get('create').get(column).get('onupdate'):
                    mk_column = mk_column + ", onupdate={}".format(migration.get('create').get(column).get('onupdate'))
            else:
                SystemExit('Error!')

            create_columns.append(mk_column + ")")
            if column != 'created_at' and column != 'updated_at' and column != 'id':
                columns_names.append(column)

        if migration.get('relationship'):
            rel_column = ''
            extern_table = ''
            for relation in migration.get('relationship'):
                rel_column = '{} = orm.relationship('.format(relation)
                if migration.get('relationship').get(relation).get('mode') == 'OneToOne':
                    extern_table = migration.get('relationship').get(relation).get('table')
                    extern_table = p.singular_noun(extern_table.title().replace('_', ''))
                    rel_column = rel_column + '{}, remote_side=id'.format(extern_table) + ', back_populates="{}"'.format(table_name) + ')'
                    mk_column = "{column} = db.Column(db.Integer, db.ForeignKey('{extern_table}.id'), index=True)".format(
                        column=migration.get('relationship').get(relation).get('column'),
                        extern_table=migration.get('relationship').get(relation).get('table')
                    )
                relationship_imports.append("from app.database.Models." + extern_table + " import " + extern_table )
                relationship_columns.append(mk_column + "\n\t" + rel_column)

        content = "from app.core.database import db\n" \
                  "from sqlalchemy.ext.declarative import declarative_base\n" \
                  "from sqlalchemy import orm\n" \
                  "from sqlalchemy_serializer import SerializerMixin\n"\
                  "from datetime import datetime\n" +\
                  "\n".join(relationship_imports) + \
                  "\n\nBase = declarative_base()\n\n\n" \
                  "class " + class_name + " (db.Model, Base, SerializerMixin):\n"\
                  "\t__tablename__ = '" + table_name + "'" \
                  "\n\t" + \
                  "\n\t".join(create_columns) + \
                  "\n\t" + \
                  "\n\t".join(relationship_columns) +\
                  "\n\n\tdef __init__(self, " + ", ".join(columns_names) + "): \n\t\t" + \
                  "\n\t\t".join('self.{name} = {name}'.format(name=name) for name in columns_names) + \
                  "\n\n"

        return write_model_file(class_name, content)
    else:
        return class_name


def write_model_file(class_name, content):
    """
    Criar arquivos de Modelos de banco de dados para migrações
    """
    mode = black.FileMode()
    formatted = black.format_file_contents(content, fast=False, mode=mode)

    with open(settings.get('FALAFEL_DIR') + settings.get('MODELS_DIR') + '/' + class_name + '.py', 'w') as model:
        model.write(formatted)
        return class_name


def check_model_exists(class_name):
    """
    Checar se Arquivo Model existe
    """
    if path.exists(settings.get('FALAFEL_DIR') + settings.get('MODELS_DIR') + '/' + class_name + '.py'):
        return True
    else:
        return False



