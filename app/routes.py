from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix="/boards")

@board_bp.route("", methods=["GET", "POST"])
def handle_boards():
    if request.method == "GET":
        boards = Board.query.all()  # list of board objects
        boards_response = []
        for board in boards:
            boards_response.append({
                "board_id": board.board_id,
                "title": board.title,
                "owner": board.owner
            })

        return make_response(jsonify(boards_response), 200)

    elif request.method == "POST":
        request_body = request.get_json()
        new_board = Board(title = request_body["title"],owner = request_body["owner"])

        db.session.add(new_board)
        db.session.commit()

        return make_response(jsonify({       #make method in Board Model for this
                "board_id": new_board.board_id,
                "title": new_board.title,
                "owner": new_board.owner
            }), 201)

@board_bp.route("/<board_id>/cards", methods=["GET", "POST"])
def handle_board_card(board_id):
    if request.method == "GET":
        
        cards = Card.query.filter(Card.board_id == board_id)

        return jsonify([card.to_json() for card in cards])

    if request.method == "POST":
        pass


# Some notes about routes
#   - POST /boards/board_id/cards
#     - Create new card for a specific board
#       - request body includes:
#         - message
#   - GET /boards/board_id/cards (repeated from above)
#     - Return a list of cards [ { card_id: card_id, message: message, likes_count: likes_count }]
#   - DELETE /cards/card_id
#     - Delete the selected card
#   - PATCH /cards/card_id
#       - Like card
