from datetime import datetime
from visitor_admin.mongodb_connection_manager import MongoDBConnectionManager
from bson import ObjectId


def validate_string_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError(f"Input: {input_string} must be a string")
    if not input_string:
        raise ValueError("Input cannot be an empty string")


def validate_visitor_age(visitor_age):
    if not isinstance(visitor_age, int):
        raise TypeError(f"Visitor age: {visitor_age} must be an integer")
    if visitor_age <= 0:
        raise ValueError("Visitor age must be greater than 0")


def validate_date_format(visit_date):
    try:
        datetime.strptime(visit_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Incorrect date format: {visit_date}, date format should be: (YYYY-MM-DD)"
        )


def validate_time_format(visit_time):
    try:
        datetime.strptime(visit_time, "%H:%M")
    except ValueError:
        raise ValueError(
            f"Incorrect time format: {visit_time}, time format should be: (HH:MM)"
        )


def execute_using_visitors(operation, *args):
    with MongoDBConnectionManager() as visitors:
        return operation(visitors, *args)


def check_visitor_exists(visitors, visitor_id):
    if not visitors.find_one({"_id": ObjectId(visitor_id)}):
        raise ValueError(
            f"Visitor: {visitor_id} does not exist, please enter an existing visitor ID"
        )


def validate_visitor_exists(visitor_id):
    validate_string_input(visitor_id)
    execute_using_visitors(check_visitor_exists, visitor_id)


def create_indexes(visitors):
    visitors.create_index([("visitor_name", 1)])
    visitors.create_index([("visitor_age", 1)])
    visitors.create_index([("visit_date", 1)])
    visitors.create_index([("visit_time", 1)])
    visitors.create_index([("assistant_name", 1)])
    visitors.create_index([("comments", 1)])


def create_visitor_indexes():
    execute_using_visitors(create_indexes)


def add_visitor_data(visitors, visitor):
    visitors.insert_one(visitor)


def create_visitor(
    visitor_name, visitor_age, visit_date, visit_time, assistant_name, comments
):
    for input_string in [
        visitor_name,
        visit_date,
        visit_time,
        assistant_name,
        comments,
    ]:
        validate_string_input(input_string)

    validate_visitor_age(visitor_age)
    validate_date_format(visit_date)
    validate_time_format(visit_time)

    visitor = {
        "visitor_name": visitor_name,
        "visitor_age": visitor_age,
        "visit_date": visit_date,
        "visit_time": visit_time,
        "assistant_name": assistant_name,
        "comments": comments,
    }

    execute_using_visitors(add_visitor_data, visitor)
    return "Visitor has been created successfully"


def get_visitors(visitors):
    return list(visitors.find())


def list_visitors():
    return execute_using_visitors(get_visitors)


def get_visitor_details(visitors, visitor_id):
    return dict(visitors.find_one({"_id": ObjectId(visitor_id)}))


def visitor_details(visitor_id):
    validate_visitor_exists(visitor_id)
    return execute_using_visitors(get_visitor_details, visitor_id)


def delete_all_visitors(visitors):
    visitors.delete_many({})


def delete_all():
    confirmation = input("Are you sure you want to delete all visitors? (yes/no): ")

    if confirmation.lower() == "yes":
        execute_using_visitors(delete_all_visitors)
        return "All visitors have been deleted"
    else:
        return "No visitors were deleted"


def delete_single_visitor(visitors, visitor_id):
    visitors.delete_one({"_id": ObjectId(visitor_id)})


def delete_visitor(visitor_id):
    validate_visitor_exists(visitor_id)
    confirmation = input(
        f"Are you sure you want to delete this visitor: {visitor_id}? (yes/no): "
    )

    if confirmation.lower() == "yes":
        execute_using_visitors(delete_single_visitor, visitor_id)
        return f"Visitor: {visitor_id} has been deleted"
    else:
        return "No visitors were deleted"


def update_single_visitor(visitors, search_criteria, info_update):
    visitors.update_one(search_criteria, info_update)


def update_visitor(visitor_id, new_info):
    validate_visitor_exists(visitor_id)

    if not isinstance(new_info, dict):
        raise ValueError(f"Update data: '{new_info}' must be a dictionary")

    for field_name, info in new_info.items():
        if field_name == "visitor_age":
            validate_visitor_age(info)
        else:
            validate_string_input(info)
            if field_name == "visit_date":
                validate_date_format(info)
            elif field_name == "visit_time":
                validate_time_format(info)

    search_criteria = {"_id": ObjectId(visitor_id)}
    info_update = {"$set": new_info}

    execute_using_visitors(update_single_visitor, search_criteria, info_update)
    return f"Visitor: {visitor_id} has been updated successfully"
