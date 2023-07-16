import json

from httpx import AsyncClient

# import pytest


async def test_create_user(ac: AsyncClient, get_user_from_database):
    user_data = {
        "email": "user@example.com",
        "password": "string123",
        "is_active": False,
        "is_superuser": True,
        "is_verified": True,
        "username": "User"
    }
    resp = await ac.post("/auth/register", content=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 201
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["username"] == user_data["username"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["id"]) == data_from_resp["id"]


async def test_create_user_duplicate_email_error(ac: AsyncClient, get_user_from_database):
    user_data = {
        "email": "user@example.com",
        "password": "string123",
        "username": "User"
    }
    user_data_same = {
        "username": "Li",
        "email": "user@example.com",
        "password": "SamplePass1!",
    }
    resp = await ac.post("/auth/register", content=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 201
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["username"] == user_data["username"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["id"]) == data_from_resp["id"]
    resp = await ac.post("/auth/register", content=json.dumps(user_data_same))
    assert resp.status_code == 400
    assert (
        'REGISTER_USER_ALREADY_EXISTS'
        in resp.json()["detail"]
    )


# @pytest.mark.parametrize(
#     "user_data_for_creation, expected_status_code, expected_detail",
#     [
#         (
#             {},
#             422,
#             {
#                 "detail": [
#                     {
#                         "loc": ["body", "username"],
#                         "msg": "field required",
#                         "type": "value_error.missing",
#                     },
#                     {
#                         "msg": "field required",
#                         "type": "value_error.missing",
#                     },
#                     {
#                         "loc": ["body", "email"],
#                         "msg": "field required",
#                         "type": "value_error.missing",
#                     },
#                     {
#                         "loc": ["body", "password"],
#                         "msg": "field required",
#                         "type": "value_error.missing",
#                     },
#                 ]
#             },
#         ),
#         (
#             422,
#             {"detail": "username should contains only letters"},
#         ),
#         (
#             422,
#         ),
#         (
#             422,
#             {
#                 "detail": [
#                     {
#                         "loc": ["body", "email"],
#                         "msg": "value is not a valid email address",
#                         "type": "value_error.email",
#                     },
#                     {
#                         "loc": ["body", "password"],
#                         "msg": "field required",
#                         "type": "value_error.missing",
#                     },
#                 ]
#             },
#         ),
#     ],
# )
# async def test_create_user_validation_error(
#     client, user_data_for_creation, expected_status_code, expected_detail
# ):
#     resp = client.post("/user/", data=json.dumps(user_data_for_creation))
#     data_from_resp = resp.json()
#     assert resp.status_code == expected_status_code
#     assert data_from_resp == expected_detail
