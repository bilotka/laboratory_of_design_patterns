#Варіант 6. Підсистему для генерування об'єкту, що зберігає структуру SQL запиту SELECT. Запит повинен містити назву таблиці, а також може містити 
# перелік полів (якщо не вказано жодного поля то використати *), тільки одну умову вибору, а також можливість сортувати за певним полем. 
# Підготувати такі запити: запити всіх полі із вказаної таблиці. Запит ID та одного вказаного поля із вказаної таблиці, впорядкованих за цим полем.
# Я думаю тут підходить шаблон  "Будівельник" 
class SQLQuery:
    def __init__(self):
        self.tables = []
        self.fields = []
        self.condition = None
        self.order_field = None

    def build(self) -> str:
        fields_part = ", ".join(self.fields) if self.fields else "*"
        tables_part = ", ".join(self.tables) if self.tables else ""

        query = f"SELECT {fields_part}"
        if tables_part:
            query += f" FROM {tables_part}"
        if self.condition:
            query += f" WHERE {self.condition}"
        if self.order_field:
            query += f" ORDER BY {self.order_field}"
        return query + ";"

class QueryBuilder:
    def __init__(self):
        self.query = SQLQuery()

    def select(self, *fields):
    
        if not fields:
            self.query.fields = ["*"]
        else:
            self.query.fields = [str(f) for f in fields]
            tables = set(f.split(".")[0] for f in self.query.fields if "." in f)
            self.query.tables = list(tables)
        return self

    def from_table(self, *tables):
        self.query.tables = list(tables)
        return self

    def where(self, condition):
        if condition:
            self.query.condition = str(condition)
        return self

    def order_by(self, field):
        if field:
            self.query.order_field = str(field)
        return self

    def build(self):

        return self.query.build()

class QueryDirector:
    def __init__(self, builder: QueryBuilder):
        self.builder = builder

    def make_select_all(self, table_name: str) -> str:

        self.builder = QueryBuilder()
        self.builder.query.tables = [table_name]
        return self.builder.select().build()

    def make_select_with_sort(self, table_name: str, field_name: str) -> str:
        self.builder = QueryBuilder()
        self.builder.query.tables = [table_name]
        return (
            self.builder
            .select(f"{table_name}.id", f"{table_name}.{field_name}")
            .order_by(f"{table_name}.{field_name}")
            .build()
        )

# Приклад використання
def test_builder() -> None:
    builder = QueryBuilder()
    director = QueryDirector(builder)
    query1 = director.make_select_all("user_account")
    print(query1)

    query2 = director.make_select_with_sort("user_account", "email_address")
    print(query2)

    custom_query = (
        builder
        .select("user_account.name", "address.email_address", "address.user_id")
        .where("user_account.id = address.user_id")
        .order_by("address.id")
        .build()
    )
    print(custom_query)

if __name__ == "__main__":
     test_builder()