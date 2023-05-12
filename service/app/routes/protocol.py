from flask import Blueprint, jsonify
from app.models.protocol import Protocol

bp = Blueprint("protocol_routes", __name__)


@bp.get("/protocols")
def get_protocols():
    protocols = Protocol.query.all()
    protocols_dict_records = list(map(lambda protocol: protocol.as_dict(), protocols))

    return jsonify(protocols_dict_records)
