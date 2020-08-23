from database.connection import Connection
from database.persistence import Persistence
from database.query import Query


class DatabaseAdapter:
    def __init__(
            self,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.conn = Connection()
        self.query = Query(self.conn)
        self.persistence = Persistence(self.conn)

    def select_all(self, table, *columns):
        return self.query.select_all(table, columns)

    def select_all_joined(self, from_table, join_table, on, columns, how='INNER'):
        return self.query.select_all_joined(from_table, join_table, on, columns, how)

    def select_custom_sql(self, which_query, where_value=False, replace_pattern='%value%'):
        return self.query.select_custom_sql(which_query, where_value, replace_pattern)

    def close(self):
        return self.conn.close()