from sqlalchemy import (
    Column, Integer, Boolean,
    MetaData, String, Table,
)


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

users_table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('telegram_id', Integer),
    Column('first_name', String(32)),
    Column('last_name', String(32)),
    Column('username', String(128)),
    Column('language_code', String(8)),
    Column('is_admin', Boolean),
    Column('api_token', String(32))
)