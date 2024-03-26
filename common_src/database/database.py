import psycopg2
import os

from dotenv import load_dotenv

from utils.init_env import init_url

load_dotenv()


def get_end_point():
    return init_url('DB_MARTEC_ENDPOINT')


def get_pass(env_name):
    if 'dev' in env_name:
        # print(f"PASS: {os.getenv('DB_PASS_DEV')}")
        return os.getenv('DB_PASS_DEV')
    elif 'staging' in env_name:
        # print(f"PASS: {os.getenv('DB_PASS_STG')}")
        return os.getenv('DB_PASS_STG')
    else:
        raise Exception("Un-defined password")


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

    def __init__(self):
        self.conn = psycopg2.connect(
            database="themartec",
            user='themartec',
            password=get_pass(os.getenv('test_env')),
            host=get_end_point(),
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

    def remove_videos_of_save_to_story(self, links_path: list):
        for file_path in links_path:
            med_id = self.get_media_id(file_path)
            print(f"[DB Connection] Remove for media id {med_id}")
            self.remove_media_by_file_path(file_path)
            self.remove_media_history_by_id(med_id)

    def close(self):
        self.conn.close()

    def make_adv_invitation_expire(self, email_address, date_tobe_expire):
        query_str = f"UPDATE advocate_invites SET updated_at = '{date_tobe_expire} 08:00:00.000+00' WHERE email = '{email_address}'"
        print(f"[DB CONN] ---> query_str: {query_str}")
        do_query_without_fetch(self.conn, query_str)
