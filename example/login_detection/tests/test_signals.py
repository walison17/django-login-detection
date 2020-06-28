def test_store_login(mocker, client, rf, user, ip_address, location):
    mocker.patch(
        "example.login_detection.signals.get_client_ip_address",
        return_value=ip_address
    )
    mocker.patch(
        "example.login_detection.signals.get_location_from_ip_address",
        return_value=location,
    )

    client.force_login(user)

    assert user.logins.count() == 1
    assert user.logins.first().location == location
