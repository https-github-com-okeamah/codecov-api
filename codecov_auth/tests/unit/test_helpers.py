import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from codecov_auth.helpers import (
    create_signed_value,
    current_user_part_of_org,
    decode_token_from_cookie,
    do_create_signed_value_v2,
)

from ..factories import OwnerFactory


def test_do_create_signed_value_v2():
    secret, name, value = "aaaaa", "name", "value"
    res = do_create_signed_value_v2(secret, name, value, clock=lambda: 12345678)
    assert decode_token_from_cookie(secret, res) == value
    assert (
        res
        == "2|1:0|8:12345678|4:name|8:dmFsdWU=|82ce7704ffb19faa13b0bd84f4f84fb4e17662c89eaf47a58683855305fa47f9"
    )


def test_create_signed_value():
    name, value = "name", "value"
    res = create_signed_value(name, value)
    assert len(res.split("|")) == 6
    (
        res_version,
        res_key_version,
        res_time,
        res_name,
        res_value,
        res_signature,
    ) = res.split("|")
    assert res_version == "2"
    assert res_key_version == "1:0"
    assert res_name == "4:name"
    assert res_value == "8:dmFsdWU="
    assert decode_token_from_cookie(settings.COOKIE_SECRET, res) == value


def test_create_signed_value_wrong_version():
    name, value = "name", "value"
    with pytest.raises(Exception) as exc:
        create_signed_value(name, value, version=4)
    assert exc.value.args == ("Unsupported version of signed cookie",)


def test_do_create_signed_value_v2_token_value():
    expected_result = "2|1:0|10:1557329312|15:bitbucket-token|48:dGVzdGFpb28xOHQzdnhzdnMzYWZ6N3A1Y2tpYnF2djB5ZTB5|86704719e8954838b5d7b666765682b4862d0ee695287f9d39a719ab01c96af1"
    value = "testaioo18t3vxsvs3afz7p5ckibqvv0ye0y"
    secret, name = "abc123", "bitbucket-token"
    res = do_create_signed_value_v2(secret, name, value, clock=lambda: 1557329312)
    assert decode_token_from_cookie(secret, res) == value
    assert res == expected_result


@pytest.mark.django_db
def test_current_user_part_of_org_when_user_not_authenticated():
    org = OwnerFactory()
    current_user = AnonymousUser()
    assert current_user_part_of_org(current_user, org) is False


@pytest.mark.django_db
def test_current_user_part_of_org_when_user_is_owner():
    current_user = OwnerFactory()
    assert current_user_part_of_org(current_user, current_user) is True


@pytest.mark.django_db
def test_current_user_part_of_org_when_user_doesnt_have_org():
    org = OwnerFactory()
    current_user = OwnerFactory(organizations=None)
    assert current_user_part_of_org(current_user, current_user) is False


@pytest.mark.django_db
def test_current_user_part_of_org_when_user_doesnt_have_org():
    org = OwnerFactory()
    current_user = OwnerFactory(organizations=[org.ownerid])
    current_user.save()
    assert current_user_part_of_org(current_user, current_user) is True
