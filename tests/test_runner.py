from mobile_virtual_testing.runner import run_request


def test_fake_provider_emits_standard_evidence():
    request = {
        "version": "1",
        "request_id": "qualification-1",
        "application": {"artifact": "fixture.apk"},
        "device": {"platform": "fake"},
        "steps": [
            {"id": "launch", "action": "launch"},
            {"id": "capture", "action": "screenshot"},
            {"id": "stop", "action": "terminate"},
        ],
        "evidence": {
            "screenshots": True,
            "video": False,
            "device_logs": True,
            "app_logs": True,
        },
    }

    evidence = run_request(request)

    assert evidence["request_id"] == "qualification-1"
    assert evidence["status"] == "passed"
    assert evidence["provider"]["name"] == "fake"
    assert evidence["device"]["platform"] == "fake"
    assert [step["status"] for step in evidence["steps"]] == ["passed", "passed", "passed"]
    assert {artifact["kind"] for artifact in evidence["artifacts"]} == {
        "device_log",
        "app_log",
        "screenshot",
    }
