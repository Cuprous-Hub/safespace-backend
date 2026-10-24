from itertools import product
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

FIRST = ["Tunde", "Amaka", "Chidi", "Zainab", "Emeka", "Funke",
         "Ibrahim", "Ngozi", "Segun", "Halima", "Bola"]
LAST = ["Adeyemi", "Okafor", "Bello", "Eze", "Balogun"]

USERS = {
    f"{f}.{l}@example.com".lower(): {"password": "demo123", "name": f"{f} {l}"}
    for f, l in product(FIRST, LAST)
}
USERS["admin@example.com"] = {"password": "admin123", "name": "Admin"}


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    user = USERS.get(email)
    if not user or user["password"] != data.get("password"):
        return jsonify(error="Invalid email or password"), 401
    token = create_access_token(identity=email)
    return jsonify(token=token, user={"email": email, "name": user["name"]})


@auth_bp.get("/me")
@jwt_required()
def me():
    email = get_jwt_identity()
    return jsonify(email=email, name=USERS[email]["name"])


@auth_bp.get("/users")
@jwt_required()
def users():
    return jsonify(
        count=len(USERS),
        users=[{"email": e, "name": u["name"]} for e, u in USERS.items()],
    )