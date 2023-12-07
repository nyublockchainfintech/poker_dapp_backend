
# testing join_room
curl -X POST -H "Content-Type: application/json" -d '{"game_id": 1, "name": "Noah", "balance": 100, "hand": [], "status": 0}' http://127.0.0.1:8000/ws/join_room

# testing update profile
curl -X POST -H "Content-Type: application/json" -d '{"game_id": 1, "old_name": "Noah", "new_name": "Anish"}' http://127.0.0.1:8000/ws/update_profile


# testing leave_room
# curl -X POST -H "Content-Type: application/json" -d '{"game_id": 1, "name": "Anish", "balance": 100, "hand": [], "status": 0}' http://127.0.0.1:8000/ws/leave_room
