from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated database with sensitive user information
users_db = {
    "1": {
        "id": 1,
        "name": "Haruna Idris",
        "email": "haruna@example.com",
        "phone": "08138276405",
        "role": "user",
        "salary": 250000,
        "ssn": "123-45-6789",
        "password_hash": "5f4dcc3b5aa765d61d8327deb882cf99",
        "account_balance": 450000,
        "date_of_birth": "1998-11-14",
        "address": "Kano State, Nigeria"
    },
    "2": {
        "id": 2,
        "name": "Shehu Garba",
        "email": "shehu@example.com",
        "phone": "08012345678",
        "role": "admin",
        "salary": 850000,
        "ssn": "987-65-4321",
        "password_hash": "d8578edf8458ce06fbc5bb76a58c5ca4",
        "account_balance": 2500000,
        "date_of_birth": "1985-03-22",
        "address": "Bauchi, Nigeria"
    },
    "3": {
        "id": 3,
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "08087654321",
        "role": "user",
        "salary": 180000,
        "ssn": "456-78-9012",
        "password_hash": "96e79218965eb72c92a549dd5a330112",
        "account_balance": 125000,
        "date_of_birth": "1995-07-10",
        "address": "Abuja, Nigeria"
    }
}

def get_current_user(token):
    tokens = {
        "user_token": "1",
        "admin_token": "2"
    }
    user_id = tokens.get(token)
    if user_id:
        return users_db.get(user_id)
    return None

# ❌ VULNERABLE endpoint — returns entire user object
@app.route("/api/user/profile", methods=["GET"])
def get_profile_vulnerable():
    token = request.headers.get("Authorization")
    user = get_current_user(token)

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    # BUG: Returns ALL fields including sensitive data
    # trusting the frontend to filter what to display
    return jsonify(user), 200


# ❌ VULNERABLE endpoint — returns all users with full details
@app.route("/api/users", methods=["GET"])
def get_all_users_vulnerable():
    token = request.headers.get("Authorization")
    user = get_current_user(token)

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    # BUG: Returns complete user objects for everyone
    return jsonify({"users": list(users_db.values())}), 200


# ✅ SECURE endpoint — returns only necessary fields
@app.route("/api/secure/user/profile", methods=["GET"])
def get_profile_secure():
    token = request.headers.get("Authorization")
    user = get_current_user(token)

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    # FIXED: Only return what the client actually needs
    safe_data = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"]
    }
    return jsonify(safe_data), 200


# ✅ SECURE endpoint — returns filtered user list
@app.route("/api/secure/users", methods=["GET"])
def get_all_users_secure():
    token = request.headers.get("Authorization")
    user = get_current_user(token)

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    # FIXED: Only return safe public fields
    safe_users = []
    for u in users_db.values():
        safe_users.append({
            "id": u["id"],
            "name": u["name"],
            "role": u["role"]
        })

    return jsonify({"users": safe_users}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)