import psycopg2
import psycopg2.extras


class PGInspector:

    def __init__(self, connection):
        # TODO docstring

        self.connection = connection
        self.cursor = self.connection.cursor()

    def get_schema_list(self, include_internals=False):
        """Get the schema list of the database

        :param bool include_internals:
            flag to specify if return postgres internal schemas

        :return list<str>:
            a list containing the schema names in alphabetical order
        """

        query = 'select schema_name from information_schema.schemata '
        if not include_internals:
            query += 'where schema_name not in (\'information_schema\') '
            query += 'and schema_name not like \'pg\_%\''
        query += 'order by schema_name'

        self.cursor.execute(query)
        records = self.cursor.fetchall()

        result = []
        for record in records:
            result.append(str(record[0]))

        return result

    def get_table_list(self, schema=None, include_internals=False):
        """Get the table list of all the database or of a single schema

        :param str schema:
            if None, the method will return all the tables in the database,
            if has a value, the method will return the list of the table in
            the schema

        :param bool include_internals:
            flag to specify if return postgres internal tables

        :return list<str>:
            a list containing the tables names ordered by schema name and
            table names in the format 'schema.table'
        """

        query = 'select table_schema, table_name '
        query += 'from information_schema.tables '
        query += 'where table_type not like \'VIEW\' '
        if schema:
            query += 'and table_schema = \'{}\' '.format(schema)
        if not include_internals:
            query += 'and table_schema not in (\'information_schema\') '
            query += 'and table_schema not like \'pg\_%\' '
        query += 'order by table_schema, table_name '

        self.cursor.execute(query)
        records = self.cursor.fetchall()

        result = []
        for record in records:
            result.append(str(record[0] + '.' + record[1]))

        return result

    def search_table(self):
        pass

    def get_view_list(self):
        pass

    def get_column_list(self):
        pass

    def get_constraint_list(self):
        pass

    def get_sequence_list(self):
        pass

    def get_index_list(self):
        pass

    def get_trigger_list(self):
        pass

    def get_function_list(self):
        pass

    def get_rule_list(self):
        pass

    def get_connections_info_from_pg_service(self):
        pass
    
if __name__ == '__main__':
    conn = psycopg2.connect("dbname=veriti user=postgres password=postgres")

    inspector = PGInspector(conn)
    print(inspector.get_table_list(include_internals=True))
