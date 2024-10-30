import redis
from config import settings


class RedisPool:
    def __init__(self, host, port, db, max_connections):
        self._pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            max_connections=max_connections
        )
        self.redis_client = redis.Redis(connection_pool=self._pool)

    def check_conversation_id(self, conversation_id):
        if not self.redis_client.exists(str(conversation_id)):
            return False
        else:
            return True

    def add_conversation(self, conversation_id, role, content):
        conversation_data = {"role": role, "content": content}
        self.redis_client.lpush(str(conversation_id), str(conversation_data))
        self.redis_client.ltrim(conversation_id, 0, 5)
        return 1

    def get_conversation_history(self, conversation_id):

        conversation_data = self.redis_client.lrange(str(conversation_id), 0, -1)
        conversation_list = [eval(data.decode('utf-8')) for data in conversation_data]
        conversation_list.reverse()
        return conversation_list


# Example usage with LPUSH
# def main():
#     a = RedisPool(settings.REDIS_HOST, settings.REDIS_PORT, 0, 100)
#
#     list_items = a.add_conversation(22222, "1", "2313")
#     z = a.get_conversation_history(22222)
#     print(z)
#
#     print(list_items)  # Output: [b'item3', b'item2', b'item1']
#
# main()
