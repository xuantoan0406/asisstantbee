import redis




class RedisPoolAssistant:
    def __init__(self, host, redisPort, db_number):
        self.redis_pool = redis.ConnectionPool(host=host, port=redisPort, db=db_number)
        self.redis_client = redis.Redis(connection_pool=self.redis_pool)

    def checkConversationId(self, conversation_id):

        if not self.redis_client.exists(conversation_id):
            return False
        else:
            return True

    def add_conversation(self, conversation_id, role, content):

        conversation_data = {"role": role, "content": content}
        self.redis_client.lpush(conversation_id, str(conversation_data))
        self.redis_client.ltrim(conversation_id, 0, 4)
        return 1

    def get_conversation_history(self, conversation_id):

        conversation_data = self.redis_client.lrange(conversation_id, 0, -1)
        conversation_list = [eval(data.decode('utf-8')) for data in conversation_data]
        conversation_list.reverse()
        return conversation_list



from config import settings
a=RedisPoolAssistant(settings.HOST_IP,settings.REDIS_PORT,1)
a.add_conversation("12","23","adsadad")
a.get_conversation_history("12")