import psycopg2
import os

from dotenv import load_dotenv

load_dotenv()


def get_end_point(env_id):
    if env_id == '2':
        return "apidev-db.cudhblxsw6t8.us-west-1.rds.amazonaws.com"
    elif env_id == '1':
        return "apistaging-db.cudhblxsw6t8.us-west-1.rds.amazonaws.com"
    else:
        return ""


def get_pass(env_id):
    if env_id == '2':
        print(f"PASS: {os.getenv('DB_PASS_DEV')}")
        return os.getenv('DB_PASS_DEV')
    elif env_id == '1':
        print(f"PASS: {os.getenv('DB_PASS_STG')}")
        return os.getenv('DB_PASS_STG')
    else:
        return ""


def do_query(conn, query_string):
    cursor = conn.cursor()
    cursor.execute(query_string)
    result = cursor.fetchall()
    return result


def do_query_without_fetch(conn, query_string):
    cursor = conn.cursor()
    cursor.execute(query_string)
    conn.commit()
    cursor.close()


class MartecDatabase:

    def __init__(self, env_test_id):
        self.conn = psycopg2.connect(
            database="themartec",
            user='themartec',
            password=get_pass(env_test_id),
            host=get_end_point(env_test_id),
            port='5432'
        )

    def get_media_id(self, file_path):
        query_str = f"SELECT id FROM media WHERE filepath = '{file_path}'"
        returned_id = do_query(self.conn, query_str)[0][0]
        return returned_id

    def remove_media_by_file_path(self, file_path: str):
        print(f"[DB CONNECTION] Remove file_path: {file_path}")
        if file_path:
            query_str = f"DELETE FROM media WHERE filepath = '{file_path}'"
            do_query_without_fetch(self.conn, query_str)
            return True
        else:
            print(f"[ERROR] Delete For EMPTY file path is skipped !")
            return False

    def remove_media_history_by_id(self, id_input: str):
        if id_input:
            query_str = f"DELETE FROM media_histories WHERE media_id = '{id_input}'"
            do_query_without_fetch(self.conn, query_str)
            return True
        else:
            print(f"[ERROR] Delete For EMPTY id_input is skipped !")
            return False

    def remove_video_of_save_to_story(self, file_path: str):
        med_id = self.get_media_id(file_path)
        print(f"[DB Connection] Remove for media id {med_id}")
        assert self.remove_media_by_file_path(file_path) is True
        assert self.remove_media_history_by_id(med_id) is True

    def close(self):
        self.conn.close()
