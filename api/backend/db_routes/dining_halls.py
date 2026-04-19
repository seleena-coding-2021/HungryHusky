from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Dining Halls routes
dining_halls = Blueprint("dining_halls", __name__)

# Update an existing dining menu item
# Can update any field except menu item id
@dining_halls.route('/dininghalls/menuitems/<menu_item_id>', methods=["PUT"])
def update_menu_item(menu_item_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        cursor.execute("SELECT ItemId FROM MenuItem WHERE ItemId = %s", (menu_item_id,))
        if not cursor.fetchone():
            return jsonify({"error": "MenuItem not found"}), 404
        
        # Build update query dynamically based on provided fields
        allowed_fields = ["HallId", "ItemName", "Description", "Category", "IsAvailable"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.append(menu_item_id)
        query = f"UPDATE MenuItem SET {', '.join(update_fields)} WHERE ItemId = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "MenuItem updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        


# Get info on what cuisines students prefer
@dining_halls.route("/dininghalls/<hall_id>/studentfeedback", methods=["GET"])
def get_cuisine_prefs(hall_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute('''SELECT dh.Name AS DiningHall, sf.CuisinePref, COUNT(*) AS Responses
                        FROM   StudentFeedback  sf
                        JOIN   DiningHall       dh  ON  dh.HallId = sf.HallId
                        WHERE dh.HallId = %s
                        GROUP  BY dh.HallId, dh.Name, sf.CuisinePref
                        ORDER  BY dh.Name, Responses DESC;''', (hall_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        
# Get all dining halls
@dining_halls.route("/dininghalls", methods=["GET"])
def get_all_halls():
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT HallId, Name FROM DiningHall")
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# Update operating hours for a dining hall
@dining_halls.route("/dininghalls/<hall_id>/operatinghours/<day_of_week>", methods=["PUT"])
def update_dh_hours(hall_id, day_of_week):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        cursor.execute("SELECT HallId, DayOfWeek FROM OperatingHours WHERE HallId = %s and DayOfWeek = %s", (hall_id, day_of_week,))
        if not cursor.fetchone():
            return jsonify({"error": "OperatingHours entry not found"}), 404
        
        # Build update query dynamically based on provided fields
        allowed_fields = ["OpenTime", "CloseTime", "Note"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400
        
        params.extend([hall_id, day_of_week])
        query = f"UPDATE OperatingHours SET {', '.join(update_fields)} WHERE HallId = %s AND DayOfWeek = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "OperatingHours updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# GET /dininghalls/{hall_id}/menuitems — get all menu items for a dining hall
@dining_halls.route('/dininghalls/<int:hall_id>/menuitems', methods=["GET"])
def get_menu_items(hall_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM MenuItem WHERE HallId = %s", (hall_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# POST /dininghalls/{hall_id}/menuitems — create a new menu item
@dining_halls.route('/dininghalls/<int:hall_id>/menuitems', methods=["POST"])
def create_menu_item(hall_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        required_fields = ["ItemName", "Category", "IsAvailable"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        valid_categories = ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert", "Other"]
        if data["Category"] not in valid_categories:
            return jsonify({"error": f"Category must be one of: {', '.join(valid_categories)}"}), 400

        cursor.execute(
            "INSERT INTO MenuItem (HallId, ItemName, Description, Category, IsAvailable) VALUES (%s, %s, %s, %s, %s)",
            (hall_id, data["ItemName"], data.get("Description"), data["Category"], data["IsAvailable"])
        )
        get_db().commit()
        return jsonify({"message": "Menu item created successfully", "itemId": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# GET /dininghalls/{hall_id}/stations — get all stations for a dining hall
@dining_halls.route('/dininghalls/<int:hall_id>/stations', methods=["GET"])
def get_stations(hall_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM DiningStation WHERE HallId = %s", (hall_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()