"""
@Name: Sean Sill
@brief: This tests the overall Eido HtmlService

"""

import unittest

class TestHtmlService(EidoTestCase):
    TEST_DATA_QUERY = """
    CREATE (a:Entity {name:"a", type:"Buisness Memeber"}),
           (a)-[:HOME_PAGE]->(a_h:Url {link:"http%3A//www.a.com"}),
           (b:Entity {name:"b", type:"Individual Member"}),
           (b)-[:HOME_PAGE]->(b_h:Url {link:"http%3A//www.a.com"})"""

    def setUp(self):
        super(EidoTestCase, self).setUp()
        self._graph_db = neo4j.GraphDatabaseService(
            "http://localhost:7475/db/data")
        print self._graph_db

        # Clear database
        query = neo4j.CypherQuery(self._graph_db,
            "MATCH (n) OPTIONAL MATCH (n)-[r]->() DELETE n, r")
        results = query.execute()
        # Check results

        query = neo4j.CypherQuery(self._graph_db, self.TEST_DATA_QUERY)
        results = query.execute()
        # Check results
        return

    def test_get_url_list(self):
        file_service = MockFileService()
        service = HtmlService(self._graph_db, file_service)
        # First we test how it behaves with no arguments
        results = service.GetUrlList()

        # Next we test how it behaves with only the row_begin argument
        results = service.GetUrlList(5)

        # Next we test how it behaves with row_begin, and num_rows argument
        results = service.GetUrlList(5, 4)

        # Next we test how it behaves with bad arguments

        # 
