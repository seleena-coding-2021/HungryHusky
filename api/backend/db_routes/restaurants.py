from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for NGO routes
restaurant = Blueprint("restaurant", __name__)

#retrieve the /restaurant/{restaurant_id}/waittime route
# required field: restaurant_id
@restaurant.route("/restaurant/<int:restaurant_id>/waittime", methods = ["GET"])
def get_restaurant_waittime(restaurant_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            """SELECT R.Name,
                        W.EstimatedMin
            FROM Restaurant R JOIN WaitTime W ON R.RestaurantId = W.RestaurantId
            WHERE W.RestaurantId = %s""", (restaurant_id,))
        
        wait_time = cursor.fetchall()
        return jsonify(wait_time), 200
    except Error as e:
        return jsonify({"error" : str(e)}), 500
    finally:
        cursor.close()

#create new restaurant wait time estimate
#required fields: EstimatedMin, RestaurantId, TimeStamp
@restaurant.route("/restaurant/<int:restaurant_id>/waittime", methods = ["POST"])
def create_restaurant_waittime(restaurant_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        
        required_fields = ["EstimatedMin", "TimeStamp"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error" : f"Missing required field: {field}"}), 400

        
        query = """
            INSERT INTO WaitTime (EstimatedMin, RestaurantId, TimeStamp),
            Values(%s, %s, %s)
        """

        cursor.execute(query, (
            data["EstimatedMin"],
            restaurant_id,
            data["TimeStamp"]
        ))

        get_db().commit()
        
        return jsonify({"message": "Wait time created successfully"}), 201
        
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        
#delete restaurant review
#required field is student id and review id
@student.route("/students/<int:student_id>/reviews/<int:review_id>", methods = ["DELETE"])
def delete_review(student_id, review_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT ReviewId FROM Review WHERE ReviewId = %s AND StudentId = %s", (review_id, student_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Review not found"}), 404
        
        query = """DELETE FROM Review WHERE StudentId = %s AND ReviewId = %s"""
        cursor.execute(query, (student_id, review_id))
        get_db().commit()
        return jsonify({"message": "Review deleted successfully"}), 200

    
    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
