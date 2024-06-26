import time
from flask import Blueprint

from .data.match_data import MATCHES


bp = Blueprint("match", __name__, url_prefix="/match")


@bp.route("<int:match_id>")
def match(match_id):
    if match_id < 0 or match_id >= len(MATCHES):
        return "Invalid match id", 404

    start = time.time()
    msg = "Match found" if (is_match(*MATCHES[match_id])) else "No match"
    end = time.time()

    return {"message": msg, "elapsedTime": end - start}, 200


def is_match(fave_numbers_1, fave_numbers_2):
    # Convert fave_numbers_1 to a set for O(1) average time complexity for membership tests
    fave_numbers_1_set = set(fave_numbers_1)
    
    # Check if every number in fave_numbers_2 is in fave_numbers_1_set
    return all(number in fave_numbers_1_set for number in fave_numbers_2)