import signaldesk_contracts


def test_package_imports() -> None:
    assert hasattr(signaldesk_contracts, "__doc__")
