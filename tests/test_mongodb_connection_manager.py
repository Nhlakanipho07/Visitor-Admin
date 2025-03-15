import os
import unittest
from unittest.mock import patch, MagicMock
from visitor_admin.mongodb_connection_manager import MongoDBConnectionManager


class TestMongoDBConnectionManager(unittest.TestCase):
    @patch("visitor_admin.mongodb_connection_manager.MongoClient")
    @patch.dict(os.environ, {"MONGODB_URI": "mongodb://root:password@localhost:27017"})
    def test_get_connection_with_env_var(self, mock_mongo_client):
        mock_client_instance = MagicMock()
        mock_db = mock_client_instance["CompanyName"]
        mock_visitors = mock_db["Visitor"]
        mock_mongo_client.return_value = mock_client_instance

        with MongoDBConnectionManager() as visitors:
            self.assertEqual(visitors, mock_visitors)
            mock_mongo_client.assert_called_once_with(
                "mongodb://root:password@localhost:27017"
            )
            mock_client_instance.close.assert_not_called()
        mock_client_instance.close.assert_called_once()

    @patch("visitor_admin.mongodb_connection_manager.MongoClient")
    @patch.dict(os.environ, {}, clear=True)
    def test_get_connection_without_env_var(self, mock_mongo_client):
        mock_client_instance = MagicMock()
        mock_db = mock_client_instance["CompanyName"]
        mock_visitors = mock_db["Visitor"]
        mock_mongo_client.return_value = mock_client_instance

        with MongoDBConnectionManager() as visitors:
            self.assertEqual(visitors, mock_visitors)
            mock_mongo_client.assert_called_once_with("mongodb://localhost:27017")
            mock_client_instance.close.assert_not_called()
        mock_client_instance.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
