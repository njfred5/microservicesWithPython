# Application layer — business logic.
#
# Calls repository functions and returns Pydantic schemas (not raw ORM objects).
# Raises ValueError when a game is not found — routes.py turns it into a 404.
#
# Implement these four functions:
# - add_game(db, data) -> GameOut
# - fetch_game(db, game_id) -> GameOut        (raises ValueError if not found)
# - fetch_all_games(db, limit, offset) -> GameList
# - find_games(db, q, limit, offset) -> GameList   (delegates to search_games in repository)
#
# Module 5 — CQRS:
# In add_game(), after saving to the DB, also write to the Redis cache:
#   from app.infrastructure.cache import set_game_summary
#   set_game_summary(game.id, {"id": game.id, "title": game.title,
#                               "genre": game.genre, "platform": game.platform,
#                               "cover_url": game.cover_url})
from app.infrastructure.cache import set_game_summary
def add_game(db: Session, data: GameCreate) -> GameOut:
    game = repository.create_game(db, data)
    set_game_summary(game.id, {
        "id": game.id,
        "title": game.title,
        "genre": game.genre,
        "platform": game.platform,
        "cover_url": game.cover_url,
    })
    return GameOut.model_validate(game)

def fetch_game_summary(game_id: str) -> dict | None:
    from app.infrastructure.cache import get_game_summary
    return get_game_summary(game_id)