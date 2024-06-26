from flask import Blueprint, request


from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """
    Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    id_param = args.get('id')
    name_param = args.get('name', '').lower()
    age_param = args.get('age')
    occupation_param = args.get('occupation', '').lower()

    # Convert age_param to an integer if it exists
    if age_param is not None:
        age_param = int(age_param)

    # Function to check the match priority for a user
    def match_priority(user):
        if id_param and user['id'] == id_param:
            return 1
        if name_param and name_param in user['name'].lower():
            return 2
        if age_param and (age_param - 1 <= user['age'] <= age_param + 1):
            return 3
        if occupation_param and occupation_param in user['occupation'].lower():
            return 4
        return 5

    # Filter users based on the matching criteria and assign match priority
    matching_users = [
        {'user': user, 'priority': match_priority(user)}
        for user in USERS if match_priority(user) != 5
    ]

    # Sort users by their match priority
    sorted_users = sorted(matching_users, key=lambda x: x['priority'])

    # Extract the user objects from the sorted list
    result_users = [item['user'] for item in sorted_users]

    return result_users