from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Students routes
students = Blueprint("students", __name__)

# Gets all the saved spots for a given user
@students.route('/students/<student_id>/savedspots', methods=["GET"])
def get_saved_spots(student_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM SavedSpot WHERE StudentId = %s", (student_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# Saves a spot to eat at
@students.route('/students/<student_id>/savedspots', methods=["POST"])
def create_saved_spot(student_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        hall_id = data.get("HallId")
        restaurant_id = data.get("RestaurantId")

        required_fields = ["DateAdded"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error:": f"Missing required field: {field}"}), 400
        
        if not hall_id and not restaurant_id:
            return jsonify({"error": f"A restaurant or dining hall must be entered"}), 400
        
        if restaurant_id and hall_id:
            return jsonify({"error": f" Both a restaurant and dining hall cannot be saved"}), 400
        
        query = """
            INSERT INTO SavedSpot (StudentId, HallId, RestaurantId, TagId, DateAdded, Notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
        student_id,
        hall_id,
        restaurant_id,
        data.get("TagId"),
        data["DateAdded"],
        data.get("Notes")
        ))
        get_db().commit()
        return jsonify({"message": "Spot saved successfully", "saved_id": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# Remove a saved spot from a students list
@students.route("/students/<student_id>/savedspots/<saved_id>", methods=["DELETE"])
def delete_saved_spot(student_id, saved_id):
    cursor = get_db().cursor(dictionary=True)

    query = """DELETE FROM SavedSpot WHERE StudentId = %s AND SavedId = %s"""
    data = (student_id, saved_id)
    cursor.execute(query, data)
    get_db().commit()
    return 'Saved Spot successfully deleted'

# Get all reviews written by a student
@students.route("/students/<student_id>/reviews", methods=["GET"])
def get_reviews(student_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM Review WHERE StudentId = %s", (student_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
