import unittest
import mongomock
from bson import ObjectId
from parameterized import parameterized
from unittest.mock import patch, MagicMock
from visitor_admin.visitor_index import (
    validate_string_input,
    validate_visitor_age,
    validate_date_format,
    validate_time_format,
    execute_using_visitors,
    check_visitor_exists,
    validate_visitor_exists,
    create_indexes,
    create_visitor_indexes,
    add_visitor_data,
    create_visitor,
    get_visitors,
    list_visitors,
    get_visitor_details,
    visitor_details,
    delete_all_visitors,
    delete_all,
    delete_single_visitor,
    delete_visitor,
    update_single_visitor,
    update_visitor,
)


class TestVisitorIndex(unittest.TestCase):

    def setUp(self):
        self.visitors_list = [
            {
                "_id": ObjectId(),
                "visitor_name": "John Doe",
                "visitor_age": 25,
                "visit_date": "2021-07-01",
                "visit_time": "10:00",
                "assistant_name": "Jane Doe",
                "comments": "First visit",
            },
            {
                "_id": ObjectId(),
                "visitor_name": "Lady Jane",
                "visitor_age": 30,
                "visit_date": "2021-07-02",
                "visit_time": "11:00",
                "assistant_name": "John Doe",
                "comments": "Fifth visit",
            },
            {
                "_id": ObjectId(),
                "visitor_name": "Jane Smith",
                "visitor_age": 35,
                "visit_date": "2021-07-03",
                "visit_time": "12:00",
                "assistant_name": "Lady Jane",
                "comments": "Third visit",
            },
            {
                "_id": ObjectId(),
                "visitor_name": "John Smith",
                "visitor_age": 40,
                "visit_date": "2021-07-04",
                "visit_time": "13:00",
                "assistant_name": "Jane Smith",
                "comments": "Second visit",
            },
        ]

    def setup_mock_visitors(self, mock_connection_manager):
        mock_client_instance = mongomock.MongoClient()
        mock_db = mock_client_instance["CompanyName"]
        mock_visitors = mock_db["Visitor"]
        mock_connection_manager.return_value.__enter__.return_value = mock_visitors
        mock_visitors.insert_many(self.visitors_list)

        return mock_visitors

    @parameterized.expand(
        [
            ("", ValueError, "Input cannot be an empty string"),
            (1, TypeError, "Input: 1 must be a string"),
            ([], TypeError, "Input: [] must be a string"),
            (True, TypeError, "Input: True must be a string"),
            ({}, TypeError, "Input: {} must be a string"),
        ]
    )
    def test_validate_string_input(self, input_string, error_type, error_message):
        with self.assertRaises(error_type) as context:
            validate_string_input(input_string)
        self.assertEqual(str(context.exception), error_message)

    @parameterized.expand(
        [
            (0, ValueError, "Visitor age must be greater than 0"),
            ("", TypeError, "Visitor age:  must be an integer"),
            ("25", TypeError, "Visitor age: 25 must be an integer"),
            ([], TypeError, "Visitor age: [] must be an integer"),
            ({}, TypeError, "Visitor age: {} must be an integer"),
        ]
    )
    def test_validate_visitor_age(self, visitor_age, error_type, error_message):
        with self.assertRaises(error_type) as context:
            validate_visitor_age(visitor_age)
        self.assertEqual(str(context.exception), error_message)

    @parameterized.expand(
        [
            (
                "21 March 2025",
                ValueError,
                "Incorrect date format: 21 March 2025, date format should be: (YYYY-MM-DD)",
            ),
            (
                "03/02/1970",
                ValueError,
                "Incorrect date format: 03/02/1970, date format should be: (YYYY-MM-DD)",
            ),
            (
                "01-01-2027",
                ValueError,
                "Incorrect date format: 01-01-2027, date format should be: (YYYY-MM-DD)",
            ),
            (
                "Mon Mar 3 2010",
                ValueError,
                "Incorrect date format: Mon Mar 3 2010, date format should be: (YYYY-MM-DD)",
            ),
        ]
    )
    def test_validate_date_format(self, visit_date, error_type, error_message):
        with self.assertRaises(error_type) as context:
            validate_date_format(visit_date)
        self.assertEqual(str(context.exception), error_message)

    @parameterized.expand(
        [
            (
                "21H00",
                ValueError,
                "Incorrect time format: 21H00, time format should be: (HH:MM)",
            ),
            (
                "09h00",
                ValueError,
                "Incorrect time format: 09h00, time format should be: (HH:MM)",
            ),
            (
                "8 am",
                ValueError,
                "Incorrect time format: 8 am, time format should be: (HH:MM)",
            ),
            (
                "08:19 PM",
                ValueError,
                "Incorrect time format: 08:19 PM, time format should be: (HH:MM)",
            ),
        ]
    )
    def test_validate_time_format(self, visit_time, error_type, error_message):
        with self.assertRaises(error_type) as context:
            validate_time_format(visit_time)
        self.assertEqual(str(context.exception), error_message)

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_execute_using_visitors(self, mock_connection_manager):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)
        arg_1 = "argument_1"
        arg_2 = "argument_2"

        def some_function(mock_visitors, arg_1, arg_2):
            return f"Operation on {mock_visitors} with args {arg_1, arg_2}"

        operation_result_with_args = execute_using_visitors(some_function, arg_1, arg_2)
        self.assertEqual(
            operation_result_with_args,
            f"Operation on {mock_visitors} with args {arg_1, arg_2}",
        )

        def different_function(mock_visitors):
            return f"Operation on {mock_visitors} with no args"

        operation_result = execute_using_visitors(different_function)
        self.assertEqual(
            operation_result,
            f"Operation on {mock_visitors} with no args",
        )

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_check_visitor_exists(self, mock_connection_manager):
        visitor_id = "60e4f5c7c2e6e6a4b3e0e4f5"
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)

        with self.assertRaises(ValueError) as context:
            check_visitor_exists(mock_visitors, visitor_id)
        self.assertEqual(
            str(context.exception),
            f"Visitor: {visitor_id} does not exist, please enter an existing visitor ID",
        )

    @patch("visitor_admin.visitor_index.execute_using_visitors")
    def test_validate_visitor_triggers_execute_using_visitors(
        self, mock_execute_using_visitors
    ):
        visitor_id = "60e4f5c7c2e6e6a4b3e0e4f5"
        validate_visitor_exists(visitor_id)

        mock_execute_using_visitors.assert_called_once_with(
            check_visitor_exists, visitor_id
        )

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_validate_visitor_exists(self, mock_connection_manager):
        visitor_id = "60e4f5c7c2e6e6a4b3e0e4f5"
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)

        with self.assertRaises(ValueError) as context:
            validate_visitor_exists(visitor_id)
        self.assertEqual(
            str(context.exception),
            f"Visitor: {visitor_id} does not exist, please enter an existing visitor ID",
        )

    def test_create_indexes(self):
        mock_visitors = MagicMock()

        create_indexes(mock_visitors)
        expected_fields = [
            [("visitor_name", 1)],
            [("visitor_age", 1)],
            [("visit_date", 1)],
            [("visit_time", 1)],
            [("assistant_name", 1)],
            [("comments", 1)],
        ]

        for field in expected_fields:
            mock_visitors.create_index.assert_any_call(field)

    @patch("visitor_admin.visitor_index.execute_using_visitors")
    def test_create_visitor_indexes(
        self,
        mock_execute_using_visitors,
    ):
        create_visitor_indexes()
        mock_execute_using_visitors.assert_called_once_with(create_indexes)

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_add_visitor_data(self, mock_connection_manager):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)

        initial_document_count = mock_visitors.count_documents({})

        visitor_data = {
            "visitor_name": "Johnny Boy",
            "visitor_age": 15,
            "visit_date": "2019-07-01",
            "visit_time": "9:00",
            "assistant_name": "Jane Lana",
            "comments": "First visit",
        }
        add_visitor_data(mock_visitors, visitor_data)

        created_visitor = mock_visitors.find_one({"visitor_name": "Johnny Boy"})

        final_document_count = mock_visitors.count_documents({})

        self.assertEqual(final_document_count, initial_document_count + 1)
        self.assertEqual(visitor_data["visitor_name"], created_visitor["visitor_name"])
        self.assertEqual(visitor_data["visitor_age"], created_visitor["visitor_age"])
        self.assertEqual(visitor_data["visit_date"], created_visitor["visit_date"])
        self.assertEqual(visitor_data["visit_time"], created_visitor["visit_time"])
        self.assertEqual(
            visitor_data["assistant_name"], created_visitor["assistant_name"]
        )
        self.assertEqual(visitor_data["comments"], created_visitor["comments"])

    @patch("visitor_admin.visitor_index.execute_using_visitors")
    def test_create_visitor_triggers_execute_using_visitors(
        self, mock_execute_using_visitors
    ):
        visitor_data = {
            "visitor_name": "Johnny Boy",
            "visitor_age": 15,
            "visit_date": "2019-07-01",
            "visit_time": "9:00",
            "assistant_name": "Jane Lana",
            "comments": "First visit",
        }

        create_visitor(
            visitor_data["visitor_name"],
            visitor_data["visitor_age"],
            visitor_data["visit_date"],
            visitor_data["visit_time"],
            visitor_data["assistant_name"],
            visitor_data["comments"],
        )

        mock_execute_using_visitors.assert_called_once_with(
            add_visitor_data, visitor_data
        )

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_create_visitor(self, mock_connection_manager):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)
        visitor_data = {
            "visitor_name": "Johnny Boy",
            "visitor_age": 15,
            "visit_date": "2019-07-01",
            "visit_time": "9:00",
            "assistant_name": "Jane Lana",
            "comments": "First visit",
        }

        initial_document_count = mock_visitors.count_documents({})

        created_visitor_confirmed = create_visitor(
            visitor_data["visitor_name"],
            visitor_data["visitor_age"],
            visitor_data["visit_date"],
            visitor_data["visit_time"],
            visitor_data["assistant_name"],
            visitor_data["comments"],
        )

        created_visitor = mock_visitors.find_one({"visitor_name": "Johnny Boy"})

        final_document_count = mock_visitors.count_documents({})

        self.assertEqual(final_document_count, initial_document_count + 1)
        self.assertEqual(visitor_data["visitor_name"], created_visitor["visitor_name"])
        self.assertEqual(visitor_data["visitor_age"], created_visitor["visitor_age"])
        self.assertEqual(visitor_data["visit_date"], created_visitor["visit_date"])
        self.assertEqual(visitor_data["visit_time"], created_visitor["visit_time"])
        self.assertEqual(
            visitor_data["assistant_name"], created_visitor["assistant_name"]
        )
        self.assertEqual(visitor_data["comments"], created_visitor["comments"])
        self.assertEqual(
            created_visitor_confirmed, "Visitor has been created successfully"
        )

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_get_visitors(self, mock_connection_manager):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)

        retrieved_visitors = get_visitors(mock_visitors)
        excepted_visitors = self.visitors_list

        self.assertIsInstance(retrieved_visitors, list)
        self.assertEqual(excepted_visitors, retrieved_visitors)

    @patch("visitor_admin.visitor_index.execute_using_visitors")
    def test_list_visitors_triggers_execute_using_visitors(
        self, mock_execute_using_visitors
    ):
        list_visitors()
        mock_execute_using_visitors.assert_called_once_with(get_visitors)

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_list_visitors(self, mock_connection_manager):
        self.setup_mock_visitors(mock_connection_manager)

        retrieved_visitors = list_visitors()
        excepted_visitors = self.visitors_list

        self.assertIsInstance(retrieved_visitors, list)
        self.assertEqual(excepted_visitors, retrieved_visitors)

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_get_visitor_details(self, mock_connection_manager):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)

        visitor_id = str(self.visitors_list[2]["_id"])
        details_of_visitor = get_visitor_details(mock_visitors, visitor_id)

        self.assertIsInstance(details_of_visitor, dict)
        self.assertEqual(self.visitors_list[2], details_of_visitor)

    @patch("visitor_admin.visitor_index.execute_using_visitors")
    def test_visitor_details_triggers_execute_using_visitors(
        self, mock_execute_using_visitors
    ):
        visitor_id = str(self.visitors_list[2]["_id"])
        visitor_details(visitor_id)

        mock_execute_using_visitors.assert_called_with(get_visitor_details, visitor_id)

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_visitor_details(self, mock_connection_manager):
        self.setup_mock_visitors(mock_connection_manager)
        visitor_id = str(self.visitors_list[2]["_id"])
        details_of_visitor = visitor_details(visitor_id)

        self.assertIsInstance(details_of_visitor, dict)
        self.assertEqual(self.visitors_list[2], details_of_visitor)

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_delete_all_visitors(self, mock_connection_manager):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)

        self.assertEqual(mock_visitors.count_documents({}), len(self.visitors_list))
        delete_all_visitors(mock_visitors)
        self.assertEqual(mock_visitors.count_documents({}), 0)

    @patch("builtins.input", return_value="yes")
    @patch("visitor_admin.visitor_index.execute_using_visitors")
    def test_delete_all_triggers_execute_using_visitors(
        self, mock_execute_using_visitors, mock_input
    ):
        delete_all()

        mock_input.assert_called_once_with(
            "Are you sure you want to delete all visitors? (yes/no): "
        )
        mock_execute_using_visitors.assert_called_once_with(delete_all_visitors)

    @patch("builtins.input", return_value="yes")
    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_delete_all_yes(self, mock_connection_manager, mock_input):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)

        self.assertEqual(mock_visitors.count_documents({}), len(self.visitors_list))
        deleted_visitors_confirmed = delete_all()

        mock_input.assert_called_once_with(
            "Are you sure you want to delete all visitors? (yes/no): "
        )

        self.assertEqual(mock_visitors.count_documents({}), 0)
        self.assertEqual(deleted_visitors_confirmed, "All visitors have been deleted")

    @patch("builtins.input", return_value="no")
    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_delete_all_no(self, mock_connection_manager, mock_input):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)

        self.assertEqual(mock_visitors.count_documents({}), len(self.visitors_list))
        no_visitors_deleted = delete_all()

        mock_input.assert_called_once_with(
            "Are you sure you want to delete all visitors? (yes/no): "
        )

        self.assertEqual(mock_visitors.count_documents({}), len(self.visitors_list))
        self.assertEqual(no_visitors_deleted, "No visitors were deleted")

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_delete_single_visitor(self, mock_connection_manager):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)
        visitor_id = str(self.visitors_list[3]["_id"])

        self.assertEqual(mock_visitors.count_documents({}), len(self.visitors_list))
        delete_single_visitor(mock_visitors, visitor_id)
        self.assertEqual(mock_visitors.count_documents({}), len(self.visitors_list) - 1)

    @patch("builtins.input", return_value="yes")
    @patch("visitor_admin.visitor_index.execute_using_visitors")
    def test_delete_visitor_triggers_execute_using_visitors(
        self, mock_execute_using_visitors, mock_input
    ):
        visitor_id = str(self.visitors_list[3]["_id"])
        delete_visitor(visitor_id)

        mock_input.assert_called_once_with(
            f"Are you sure you want to delete this visitor: {visitor_id}? (yes/no): "
        )
        mock_execute_using_visitors.assert_called_with(
            delete_single_visitor, visitor_id
        )

    @patch("builtins.input", return_value="yes")
    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_delete_visitor_yes(self, mock_connection_manager, mock_input):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)
        visitor_id = str(self.visitors_list[3]["_id"])

        self.assertEqual(mock_visitors.count_documents({}), len(self.visitors_list))
        deleted_visitor_confirmed = delete_visitor(visitor_id)
        mock_input.assert_called_once_with(
            f"Are you sure you want to delete this visitor: {visitor_id}? (yes/no): "
        )
        self.assertEqual(mock_visitors.count_documents({}), len(self.visitors_list) - 1)
        self.assertEqual(
            deleted_visitor_confirmed, f"Visitor: {visitor_id} has been deleted"
        )

    @patch("builtins.input", return_value="no")
    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_delete_visitor_no(self, mock_connection_manager, mock_input):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)
        visitor_id = str(self.visitors_list[3]["_id"])

        self.assertEqual(mock_visitors.count_documents({}), len(self.visitors_list))
        no_visitor_deleted = delete_visitor(visitor_id)
        mock_input.assert_called_once_with(
            f"Are you sure you want to delete this visitor: {visitor_id}? (yes/no): "
        )
        self.assertEqual(mock_visitors.count_documents({}), len(self.visitors_list))
        self.assertEqual(no_visitor_deleted, "No visitors were deleted")

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_update_single_visitor(self, mock_connection_manager):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)
        visitor_id = str(self.visitors_list[1]["_id"])
        new_info = {"assistant_name": "Some Guy", "comments": "Sixth visit"}
        search_criteria = {"_id": ObjectId(visitor_id)}
        info_update = {"$set": new_info}

        update_single_visitor(mock_visitors, search_criteria, info_update)

        expected_update = {
            "_id": ObjectId(visitor_id),
            "visitor_name": "Lady Jane",
            "visitor_age": 30,
            "visit_date": "2021-07-02",
            "visit_time": "11:00",
            "assistant_name": "Some Guy",
            "comments": "Sixth visit",
        }

        actual_update = dict(mock_visitors.find_one(search_criteria))

        self.assertEqual(expected_update, actual_update)

    @patch("visitor_admin.visitor_index.execute_using_visitors")
    def test_update_visitor_triggers_execute_using_visitors(
        self, mock_execute_using_visitors
    ):
        visitor_id = str(self.visitors_list[1]["_id"])
        new_info = {"assistant_name": "Some Guy", "comments": "Sixth visit"}
        search_criteria = {"_id": ObjectId(visitor_id)}
        info_update = {"$set": new_info}

        update_visitor(visitor_id, new_info)

        mock_execute_using_visitors.assert_called_with(
            update_single_visitor, search_criteria, info_update
        )

    @patch("visitor_admin.visitor_index.MongoDBConnectionManager")
    def test_update_visitor(self, mock_connection_manager):
        mock_visitors = self.setup_mock_visitors(mock_connection_manager)
        visitor_id = str(self.visitors_list[1]["_id"])
        new_info = "New information for update"

        with self.assertRaises(ValueError) as context:
            update_visitor(visitor_id, new_info)
        self.assertEqual(
            str(context.exception), f"Update data: '{new_info}' must be a dictionary"
        )

        new_info = {"assistant_name": "Some Guy", "comments": "Sixth visit"}
        update_visitor(visitor_id, new_info)

        expected_update = {
            "_id": ObjectId(visitor_id),
            "visitor_name": "Lady Jane",
            "visitor_age": 30,
            "visit_date": "2021-07-02",
            "visit_time": "11:00",
            "assistant_name": "Some Guy",
            "comments": "Sixth visit",
        }

        actual_update = dict(mock_visitors.find_one({"_id": ObjectId(visitor_id)}))

        self.assertEqual(expected_update, actual_update)


if __name__ == "__main__":
    unittest.main()
