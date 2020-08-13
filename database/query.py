import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Query:
    def __init__(
        self,
        conn=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.connection = conn

    @staticmethod
    def list_to_words(columns):
        if columns[0] is '*':
            is_more_one_column = True
            return columns[0], is_more_one_column

        # Casting list to words comma separated
        is_more_one_column = len(columns) > 1
        return ', '.join(columns) if is_more_one_column else columns[0], is_more_one_column

    def select_all(self, table, columns):
        """ Select all rows from chosen table and columns
        :param table: (str) table that query will made
        :param columns: (list) columns chosen to table query
        :return: list contaning query result
        """
        columns, is_more_one_column = self.list_to_words(columns)

        try:
            sql = f"""
                SELECT
                    {columns}
                FROM   
                    {table}
            """
            self.connection.cursor.execute(sql)

            if is_more_one_column:
                return self.connection.cursor.fetchall()

            return [row[0] for row in self.connection.cursor]

        except Exception as e:
            logging.info(f'Error on query:\n{e}')
            return False

    def select_all_joined(self, from_table, join_table, on, columns, how='INNER'):
        """ Select all rows from chosen table and columns
        with inner join table included in sql
        :param from_table: (str) from table that query will made
        :param join_table: (str) join table that query will made
        :param on: column to join table. Can be unique column or list containing keys for each table
        :param how: join type (left, right, inner)
        :param columns: (list) columns chosen to table query
        :return: list contaning query result
        """
        columns, is_more_one_column = self.list_to_words(columns)

        is_one_key_join = not isinstance(on, list)

        joining = f'USING ({on})' if is_one_key_join else f'ON {from_table}.{on[0]} = {join_table}.{on[1]}'

        try:
            sql = f"""
                SELECT {columns}
                FROM {from_table}
                {how} JOIN {join_table}
                {joining}
            """
            self.connection.cursor.execute(sql)

            if is_more_one_column:
                return self.connection.cursor.fetchall()

            return [row[0] for row in self.connection.cursor]

        except Exception as e:
            logging.info(f'Error on query:\n{e}')
            return False

    def select_custom_sql(self, which_query, where_value=False, replace_pattern='%value%'):
        try:
            current_dir = os.path.dirname(__file__)
            file_path = f"custom_queries/{which_query}.sql"
            path = os.path.join(current_dir, file_path)

            sql = open(path, "r").read()

            if where_value:
                sql = sql.replace(replace_pattern, where_value)

            self.connection.cursor.execute(sql)

            return self.connection.cursor.fetchall()

        except Exception as e:
            logging.info(f'Error on execute custom query:\n{e}')
            return False