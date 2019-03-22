import psycopg2
from uuid import uuid4
from faker import Faker
from datetime import datetime, timedelta

# psql -f create_dbs.sql -U postgres
# psql -f delete_dbs.sql -U postgres
# psql -f create_table_fly.sql -U postgres -d db_fly
# psql -f create_table_hotel.sql -U postgres -d db_hotel


class TransactionManager:
    def __init__(self):
        self.transactions = []

    def begin(self, cursor):
        cursor.execute('BEGIN;')
        return (cursor, uuid4())

    def prepare_transaction(self, transaction):
        cursor, transaction_id = transaction
        cursor.execute('PREPARE TRANSACTION \'%s\';' % transaction_id)
        print('Prepared transaction %s' % transaction_id)
        self.transactions.append(transaction)

    def add_queries(self, cursor, queries):
        transaction = self.begin(cursor)
        for q in queries:
            cursor.execute(q)
        self.prepare_transaction(transaction)

    def add_transaction(self, cursor, queries):
        try:
            self.add_queries(cursor, queries)
        except Exception as error:
            cursor.execute("rollback;")
            print("warning")
            self.rollback_transactions()
            print("Error while connecting to PostgreSQL", error)
            raise error

    def commit_transactions(self):
        for cursor, transaction_id in self.transactions:
            print('Commiting %s' % transaction_id)
            cursor.execute('COMMIT PREPARED \'%s\';' % transaction_id)

    def rollback_transactions(self):
        for cursor, transaction_id in self.transactions:
            print('Rolling back %s' % transaction_id)
            cursor.execute('ROLLBACK PREPARED \'%s\';' % transaction_id)
        self.transactions = []

    def get_unrolledbacked_transactions(self, cursor):
        cursor.execute('select * from pg_prepared_xacts')


class OrdersManager:
    def __init__(self, hotel_db_name='db_hotel', fly_db_name='db_fly'):
        self.hotel_db_name = hotel_db_name
        self.fly_db_name = fly_db_name
        self.__set_cursors()

    def __set_cursors(self):
        try:
            self.hotel_con = psycopg2.connect(
                database=self.hotel_db_name, user='postgres')
            self.fly_con = psycopg2.connect(
                database=self.fly_db_name, user='postgres')

            self.hotel_cur = self.hotel_con.cursor()
            self.fly_cur = self.fly_con.cursor()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def close(self):
        try:
            self.hotel_cur.close()
            self.fly_cur.close()
            self.hotel_con.close()
            self.fly_con.close()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def __gen_fly(self):
        faker = Faker()
        return {
            'client': faker.name().replace('\'', '\'\''),
            'number': faker.sha1(),
            'fly_from': faker.country_code(),
            'fly_to': faker.country_code(),
            'book_date': str(faker.date_time_this_month())
        }

    def __gen_hotel(self):
        faker = Faker()
        return {
            'client': faker.name().replace('\'', '\'\''),
            'hotel': faker.address().replace('\'', '\'\'').replace('\n', '; '),
            'arrival': str(faker.date_time_this_month()),
            'departure':
            str(datetime.now() + timedelta(days=faker.random_digit()))
        }

        return hotel_book, fly_book

    def create_hotel_query(self):
        values = self.__gen_hotel()

        query_string = "insert into hotel_booking (client_name, hotel_name, arrival_date, departure_date) values ('{client}', '{hotel}', '{arrival}', '{departure}');"

        return [query_string.format(**values)]

    def create_fly_query(self):
        values = self.__gen_fly()

        query_string = "insert into fly_booking (client_name, fly_number, fly_from, fly_to, book_date) values (' {client}', '{number}', '{fly_from}', '{fly_to}', '{book_date}');"

        return [query_string.format(**values)]

    def __print_hotel_table(self):
        postgreSQL_select_Query = "select * from hotel_booking"
        self.hotel_cur.execute(postgreSQL_select_Query)
        table = self.hotel_cur.fetchall()

        print('----------------------------------')
        print('---------- Hotel table -----------')
        print('----------------------------------')
        for row in table:
            print('hotel_id = ', row[0])
            print("client = ", row[1])
            print("hotel = ", row[2])
            print("arrival  = ", row[3])
            print("departure  = ", row[4], "\n")
        print('----------------------------------', "\n", "\n")

    def __print_fly_table(self):
        postgreSQL_select_Query = "select * from fly_booking"
        self.fly_cur.execute(postgreSQL_select_Query)
        table = self.fly_cur.fetchall()

        print('----------------------------------')
        print('----------- Fly table ------------')
        print('----------------------------------')
        for row in table:
            print('fly_id = ', row[0])
            print("client = ", row[1])
            print("number = ", row[2])
            print("fly_from  = ", row[3])
            print("fly_to  = ", row[4])
            print("book_date  = ", row[5], "\n")
        print('----------------------------------', "\n", "\n")

    def print_tables(self):
        self.__print_hotel_table()
        self.__print_fly_table()


if __name__ == '__main__':
    orders_manager = OrdersManager()
    transaction_manager = TransactionManager()

    transaction_manager.add_queries(orders_manager.fly_cur,
                                    orders_manager.create_fly_query())
    transaction_manager.add_queries(orders_manager.hotel_cur,
                                    orders_manager.create_hotel_query())

    transaction_manager.commit_transactions()
    orders_manager.print_tables()

    orders_manager.close()