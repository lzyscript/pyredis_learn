import redis


rdb = redis.Redis(host='localhost', port=6379, db=0)


if __name__ == "__main__":
	if rdb.ping():
		print("redis connected!")
	else:
		print("redis not connected!")