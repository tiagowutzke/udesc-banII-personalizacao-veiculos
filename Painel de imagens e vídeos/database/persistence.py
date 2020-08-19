import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Persistence:
    def __init__(
        self,
        conn=None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.connection = conn

    def get_cols_values(self, cols_values):
        cols_values = cols_values.get('cols_values') or cols_values

        columns, _ = self.get_cols_param(list(cols_values.keys()))
        values, _ = self.get_cols_param(list(cols_values.values()))

        return columns, values

    @staticmethod
    def get_cols_param(columns):
        # Casting list to words comma separated
        is_more_one_column = len(columns) > 1
        return ', '.join(columns) if is_more_one_column else columns[0], is_more_one_column

    def update_by_col(self, table, where_col=None, where_value=None, cast_to='text', **cols_values):

        columns, values = self.get_cols_values(cols_values)
        try:
            sql = f"""
                 UPDATE {table}
                 SET ({columns}) = ({values})
                 WHERE {where_col}::{cast_to} = '{where_value}'::{cast_to}
             """
            print(sql)

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

    def insert_row(self, table, **cols_values):

        columns, values = self.get_cols_values(cols_values)

        try:
            sql = f"""
                INSERT INTO {table} ({columns})
                VALUES ({values})
            """
            self.connection.commit_transaction(sql)
            return True

        except Exception as e:
            self.connection.rollback();
            message = f'Error on insert values:\n{e}'
            logging.info(message)
            return False

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
