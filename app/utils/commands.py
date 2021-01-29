import click
from sqlalchemy import create_engine, orm, exc
from os import listdir
from fnmatch import fnmatch
from importlib import import_module

## Register configs
from dynaconf import settings
###

engine = create_engine(settings.get('SQLALCHEMY_DATABASE_URI'))
Session = orm.sessionmaker(bind=engine)
session = Session()

###
seeds = []
for file in listdir(settings.get('SEEDS_DIR')):
    if(fnmatch(file, "*.py")) and (file != "__init__.py"):
        seeds.append('database.Seeds.' + file.replace('.py', ''))
                                               
migrations = []
for file in listdir(settings.get('MIGRATIONS_DIR')):
    if(fnmatch(file, "*.py")) and (file != "__init__.py"):
        migrations.append('database.Migrations.' + file.replace('.py', ''))
###

def migrate():
    """ Realiza a criação das tabelas no banco"""
    
    for migration in migrations:
        Module = import_module(migration)
        try:
            Module.Base.metadata.create_all(engine)
            print('Success when running the Model Import for ' + migration)
        except:
            print('Error on import Model: ' + migration)
            
    print('All Migrations running succesfull!')
    
def seed():
    """ Cria dados no banco"""
    for seeder in seeds:
        module = import_module(seeder)
        element = getattr(module, 'create')
        try:
            session.add(element)                
            session.commit()
            print('Success when running the Seeder ' + seeder)
        
        except exc.IntegrityError as error: 
            session.rollback()
            print('Could not execute Seeder ' + seed + '. Data already exists?')
            
    print('All seeders running seccesfull!')

def init_app(app):
    """ Registra os comandos"""
    for command in [migrate, seed]:
        app.cli.add_command(app.cli.command()(command))