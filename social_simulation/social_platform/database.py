# File: SandboxTwitterModule/twitter_infra_core/create_database.py
from __future__ import annotations

import os
import os.path as osp
import sqlite3
from typing import Any, Dict, List

SCHEMA_DIR = "social_platform/schema"
DB_DIR = "db"
DB_NAME = "twitter.db"

USER_SCHEMA_SQL = "user.sql"
TWEET_SCHEMA_SQL = "tweet.sql"
FOLLOW_SCHEMA_SQL = "follow.sql"
MUTE_SCHEMA_SQL = "mute.sql"
LIKE_SCHEMA_SQL = "like.sql"
DISLIKE_SCHEMA_SQL = "dislike.sql"
TRACE_SCHEMA_SQL = "trace.sql"
REC_SCHEMA_SQL = "rec.sql"
COMMENT_SCHEMA_SQL = "comment.sql"
COMMENT_LIKE_SCHEMA_SQL = "comment_like.sql"
COMMENT_DISLIKE_SCHEMA_SQL = "comment_dislike.sql"

TABLE_NAMES = {
    "user", "tweet", "follow", "mute", "like", "dislike", "trace", "rec",
    "comment.sql", "comment_like.sql", "comment_dislike.sql"
}


def get_db_path() -> str:
    curr_file_path = osp.abspath(__file__)
    parent_dir = osp.dirname(osp.dirname(curr_file_path))
    db_dir = osp.join(parent_dir, DB_DIR)
    os.makedirs(db_dir, exist_ok=True)
    db_path = osp.join(db_dir, DB_NAME)
    return db_path


def get_schema_dir_path() -> str:
    curr_file_path = osp.abspath(__file__)
    parent_dir = osp.dirname(osp.dirname(curr_file_path))
    schema_dir = osp.join(parent_dir, SCHEMA_DIR)
    return schema_dir


def create_db(db_path: str | None = None):
    r"""Create the database if it does not exist. A :obj:`twitter.db`
    file will be automatically created  in the :obj:`data` directory.
    """
    schema_dir = get_schema_dir_path()
    if db_path is None:
        db_path = get_db_path()

    # Connect to the database:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Read and execute the user table SQL script:
        user_sql_path = osp.join(schema_dir, USER_SCHEMA_SQL)
        with open(user_sql_path, 'r') as sql_file:
            user_sql_script = sql_file.read()
        cursor.executescript(user_sql_script)

        # Read and execute the tweet table SQL script:
        tweet_sql_path = osp.join(schema_dir, TWEET_SCHEMA_SQL)
        with open(tweet_sql_path, 'r') as sql_file:
            tweet_sql_script = sql_file.read()
        cursor.executescript(tweet_sql_script)

        # Read and execute the follow table SQL script:
        follow_sql_path = osp.join(schema_dir, FOLLOW_SCHEMA_SQL)
        with open(follow_sql_path, 'r') as sql_file:
            follow_sql_script = sql_file.read()
        cursor.executescript(follow_sql_script)

        # Read and execute the mute table SQL script:
        mute_sql_path = osp.join(schema_dir, MUTE_SCHEMA_SQL)
        with open(mute_sql_path, 'r') as sql_file:
            mute_sql_script = sql_file.read()
        cursor.executescript(mute_sql_script)

        # Read and execute the like table SQL script:
        like_sql_path = osp.join(schema_dir, LIKE_SCHEMA_SQL)
        with open(like_sql_path, 'r') as sql_file:
            like_sql_script = sql_file.read()
        cursor.executescript(like_sql_script)

        # Read and execute the dislike table SQL script:
        dislike_sql_path = osp.join(schema_dir, DISLIKE_SCHEMA_SQL)
        with open(dislike_sql_path, 'r') as sql_file:
            dislike_sql_script = sql_file.read()
        cursor.executescript(dislike_sql_script)

        # Read and execute the trace table SQL script:
        trace_sql_path = osp.join(schema_dir, TRACE_SCHEMA_SQL)
        with open(trace_sql_path, 'r') as sql_file:
            trace_sql_script = sql_file.read()
        cursor.executescript(trace_sql_script)

        # Read and execute the rec table SQL script:
        rec_sql_path = osp.join(schema_dir, REC_SCHEMA_SQL)
        with open(rec_sql_path, 'r') as sql_file:
            rec_sql_script = sql_file.read()
        cursor.executescript(rec_sql_script)

        # Read and execute the comment table SQL script:
        comment_sql_path = osp.join(schema_dir, COMMENT_SCHEMA_SQL)
        with open(comment_sql_path, 'r') as sql_file:
            comment_sql_script = sql_file.read()
        cursor.executescript(comment_sql_script)

        # Read and execute the comment_like table SQL script:
        comment_like_sql_path = osp.join(schema_dir, COMMENT_LIKE_SCHEMA_SQL)
        with open(comment_like_sql_path, 'r') as sql_file:
            comment_like_sql_script = sql_file.read()
        cursor.executescript(comment_like_sql_script)

        # Read and execute the comment_dislike table SQL script:
        comment_dislike_sql_path = osp.join(schema_dir,
                                            COMMENT_DISLIKE_SCHEMA_SQL)
        with open(comment_dislike_sql_path, 'r') as sql_file:
            comment_dislike_sql_script = sql_file.read()
        cursor.executescript(comment_dislike_sql_script)

        # Commit the changes:
        conn.commit()

        print("All tables created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while creating tables: {e}")
    finally:
        # Close the database connection
        conn.close()


def print_db_tables_summary():
    # Connect to the SQLite database
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Retrieve a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Print a summary of each table
    for table in tables:
        table_name = table[0]
        if table_name not in TABLE_NAMES:
            continue
        print(f"Table: {table_name}")

        # Retrieve the table schema
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        print("- Columns:", column_names)

        # Retrieve and print foreign key information
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = cursor.fetchall()
        if foreign_keys:
            print("- Foreign Keys:")
            for fk in foreign_keys:
                print(f"    {fk[2]} references {fk[3]}({fk[4]}) on update "
                      f"{fk[5]} on delete {fk[6]}")
        else:
            print("  No foreign keys.")

        # Print the first few rows of the table
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print()  # Adds a newline for better readability between tables

    # Close the database connection
    conn.close()


def fetch_table_from_db(cursor: sqlite3.Cursor,
                        table_name: str) -> List[Dict[str, Any]]:
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [description[0] for description in cursor.description]
    data_dicts = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return data_dicts


def fetch_rec_table_as_matrix(cursor: sqlite3.Cursor) -> List[List[int]]:

    # 首先，查询user表中的所有user_id, 假设从1开始，连续
    cursor.execute("SELECT user_id FROM user ORDER BY user_id")
    user_ids = [row[0] for row in cursor.fetchall()]

    # 接着，查询rec表中的所有记录
    cursor.execute(
        "SELECT user_id, tweet_id FROM rec ORDER BY user_id, tweet_id")
    rec_rows = cursor.fetchall()
    # 初始化一个字典，为每个user_id分配一个空列表
    user_tweets = {user_id: [] for user_id in user_ids}
    # 使用查询到的rec表记录填充字典
    for user_id, tweet_id in rec_rows:
        if user_id in user_tweets:
            user_tweets[user_id].append(tweet_id)
    # 将字典转换为矩阵形式
    matrix = [None] + [user_tweets[user_id] for user_id in user_ids]
    return matrix


def insert_matrix_into_rec_table(cursor: sqlite3.Cursor,
                                 matrix: List[List[int]]) -> None:
    # 遍历matrix，跳过索引0的占位符
    for user_id, tweet_ids in enumerate(matrix[1:], start=1):
        for tweet_id in tweet_ids:
            # 对每个user_id和tweet_id的组合，插入到rec表中
            cursor.execute("INSERT INTO rec (user_id, tweet_id) VALUES (?, ?)",
                           (user_id, tweet_id))


if __name__ == "__main__":
    create_db()
    print_db_tables_summary()