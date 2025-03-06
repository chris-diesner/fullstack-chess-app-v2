from database.mongodb import games_collection
from models.chess_game import ChessGame

class ChessGameRepository:
    def insert_game(self, game: ChessGame):
        game_dict = game.model_dump(by_alias=True)
        game_dict["_id"] = game_dict.pop("game_id")
        games_collection.replace_one({"_id": game_dict["_id"]}, game_dict, upsert=True)

        
    def find_game_by_id(self, game_id: str) -> ChessGame | None:
        game_data = games_collection.find_one({"_id": game_id})
        if game_data:
            game_data["game_id"] = str(game_data.pop("_id")) 
            return ChessGame(**game_data)
        return None
