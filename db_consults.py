import os
import pymysql
#import aiomysql


def insert_message(
                    message_id: str, 
                    profile_name: str,
                    client_number: str, 
                    to: str, 
                    message: str,
                    from_client: bool = 1
                    ) -> None:
    
    connection = pymysql.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_NAME'],
        port=int(os.environ['DB_PORT'])
    )
    
    try:
        with connection.cursor() as cursor:
        # Query Example
            sql = "INSERT INTO messages(smsid, profile_name, client_number, user_number, message, from_client) VALUES(%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (message_id, profile_name, client_number, to, message, from_client))
    finally:
        connection.commit()
        connection.close()


#async def insert_message(message_id: str, profile_name: str, client_number: str, to: str, message: str) -> None:
#    pool = await aiomysql.create_pool(
#        host=os.environ['DB_HOST'],
#        port=int(os.environ['DB_PORT']),
#        user=os.environ['DB_USER'],
#        password=os.environ['DB_PASSWORD'],
#        db=os.environ['DB_NAME']
#    )
#    async with pool.acquire() as conn:
#        async with conn.cursor() as cursor:
#            sql = "INSERT INTO messages(smsid, profile_name, client_number, user_number, message) VALUES(%s, %s, %s, %s, %s)"
#            await cursor.execute(sql, (message_id, profile_name, client_number, to, message))
#            print("consult executed")
#            await conn.commit()
#    pool.close()
#    await pool.wait_closed()