from django.db import connection
from django.test import TestCase


class DatabaseConfigurationTests(TestCase):
    """HMS-02: Django runs on MySQL 8 with the settings the SRS relies on."""

    def query_one(self, sql):
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()[0]

    def test_connects_to_mysql_8(self):
        self.assertEqual(connection.vendor, 'mysql')
        self.assertFalse(connection.mysql_is_mariadb)
        self.assertGreaterEqual(connection.mysql_version, (8, 0))

    def test_strict_mode_is_enabled(self):
        self.assertIn('STRICT_TRANS_TABLES', self.query_one('SELECT @@SESSION.sql_mode'))

    def test_all_tables_use_innodb(self):
        # SRS 7: referential integrity through MySQL InnoDB.
        non_innodb = self.query_one(
            "SELECT COUNT(*) FROM information_schema.tables "
            "WHERE table_schema = DATABASE() AND engine <> 'InnoDB'"
        )
        self.assertEqual(non_innodb, 0)
