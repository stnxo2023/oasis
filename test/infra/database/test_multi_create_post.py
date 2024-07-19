import os
import os.path as osp
import sqlite3

import pytest

from social_simulation.social_platform.platform import Platform
from social_simulation.testing.show_db import print_db_contents

parent_folder = osp.dirname(osp.abspath(__file__))
test_db_filepath = osp.join(parent_folder, "test.db")


class MockChannel:

    def __init__(self, user_actions):
        """
        user_actions: A list of tuples representing actions.
        Each tuple is in the format (user_id, message, action_type)
        """
        self.user_actions = user_actions
        self.messages = []  # 用于存储发送的消息
        self.action_index = 0  # Track the current action

    async def receive_from(self):
        if self.action_index < len(self.user_actions):
            action = self.user_actions[self.action_index]
            self.action_index += 1
            return ('id_', action)
        else:
            return ('id_', (None, None, "exit"))

    async def send_to(self, message):
        self.messages.append(message)  # 存储消息以便后续断言


def generate_user_actions(n_users, posts_per_user):
    """
    Generate a list of user actions for n users with different posting
    behaviors. 1/3 of the users each sending m posts, 1/3 sending 1 post,
    and 1/3 not posting at all.
    """
    actions = []
    users_per_group = n_users // 3

    for user_id in range(1, n_users + 1):
        # Add sign up action for each user
        user_message = ("username" + str(user_id), "name" + str(user_id),
                        "No descrption.")
        actions.append((user_id, user_message, "sign_up"))

        if user_id <= users_per_group:
            # This group of users sends m posts each
            for post_num in range(1, posts_per_user + 1):
                actions.append(
                    (user_id, f"This is post {post_num} from User{user_id}",
                     "create_post"))
        elif user_id <= 2 * users_per_group:
            # This group of users sends 1 post each
            actions.append(
                (user_id, f"This is post 1 from User{user_id}", "create_post"))
        # The last group does not send any posts

    return actions


# 定义一个fixture来初始化数据库和Platform实例
@pytest.fixture
def setup_platform():
    # 测试前确保test.db不存在
    if os.path.exists(test_db_filepath):
        os.remove(test_db_filepath)


@pytest.mark.asyncio
async def test_signup_and_create_post(setup_platform,
                                      n_users=30,
                                      posts_per_user=4):
    try:
        # 为了简化模拟，假设n_users是3的倍数
        assert n_users % 3 == 0, "n_users should be a multiple of 3."

        # Generate user actions based on n_users and posts_per_user
        user_actions = generate_user_actions(n_users, posts_per_user)

        mock_channel = MockChannel(user_actions)
        platform_instance = Platform(test_db_filepath, mock_channel)

        await platform_instance.running()

        # 验证数据库中是否正确插入了数据
        conn = sqlite3.connect(test_db_filepath)
        cursor = conn.cursor()

        # 验证用户(user)表是否正确插入了数据
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        assert len(users) == n_users, ("The number of users in the database"
                                       "should match n_users.")

        # 验证推文(post)表是否正确插入了数据
        cursor.execute("SELECT * FROM post")
        posts = cursor.fetchall()
        expected_posts = (n_users // 3) * posts_per_user + (n_users // 3)
        assert len(posts) == expected_posts, (
            "The number of posts should match the expected value.")

        conn.close()
        print_db_contents(test_db_filepath)

    finally:
        if os.path.exists(test_db_filepath):
            os.remove(test_db_filepath)