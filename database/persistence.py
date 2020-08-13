import logging

from database.query import Query

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Persistence:
    def __init__(
        self,
        conn=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.connection = conn

    @staticmethod
    def apply_string_quotes(values, no_string_quotes):
        if isinstance(no_string_quotes, list):
            not_in_string_quotes = lambda x: x not in no_string_quotes
        else:
            not_in_string_quotes = lambda x: x != no_string_quotes

        return [
            "'" + str(value) + "'" if not_in_string_quotes(value) else value
            for value in values
        ]

    def update_by_col(self, table, where_col, where_value, cast_to='text', no_string_quotes='', **cols_values):
        query = Query()

        cols_values = cols_values.get('cols_values')
        columns, _ = query.list_to_words(list(cols_values.keys()))

        values = self.apply_string_quotes(list(cols_values.values()), no_string_quotes)
        values, _ = query.list_to_words(values)

        try:
            sql = f"""
                 UPDATE {table}
                 SET ({columns}) = ({values})
                 WHERE {where_col}::{cast_to} = '{where_value}'::{cast_to}
             """
            self.connection.commit_transaction(sql)

            return {
                'success': True,
                'message': ''
            }

        except Exception as e:
            message = f'Error on insert values:\n{e}'
            logging.info(message)
            return {
                'success': False,
                'message': message
            }

    def insert_row(self, table, no_string_quotes='', **cols_values):
        query = Query()

        cols_values = cols_values.get('cols_values')
        columns, _ = query.list_to_words(list(cols_values.keys()))

        values = self.apply_string_quotes(list(cols_values.values()), no_string_quotes)
        values, _ = query.list_to_words(values)

        try:
            sql = f"""
                INSERT INTO {table} ({columns})
                VALUES ({values})
            """
            self.connection.commit_transaction(sql)
            return {
                'success': True,
                'message': ''
            }

        except Exception as e:
            self.connection.rollback();
            message = f'Error on insert values:\n{e}'
            logging.info(message)
            return {
                'success': False,
                'message': message
            }

    def delete_by_col(self, table, where_col, where_value):
        try:
            sql = f"""
                DELETE FROM {table}
                WHERE {where_col} = '{where_value}'
            """
            self.connection.commit_transaction(sql)
            return {
                'success': True,
                'message': ''
            }

        except Exception as e:
            message = f'Error on delete row:\n{e}'
            logging.info(message)
            return {
                'success': False,
                'message': message
            }
