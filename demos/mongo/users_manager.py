from demos.config.database_connection import mongo_client


db = mongo_client["test-openai"]
collection = db["users"]


def save_to_chat(new_chat_list, user_phone):
    try:
        collection.update_one(
            {"user_phone": user_phone}, {"$set": {"chats": new_chat_list}}, upsert=True
        )
        print("Save to chat successfully")
    except Exception as e:
        return e

    # mongo_client.close()


def find_user(user_phone):
    try:
        usuario = collection.find_one({"user_phone": user_phone})
        return usuario
    except Exception as e:
        return e
