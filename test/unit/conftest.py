import pytest


@pytest.fixture(scope="module")
def python_failing_tests():
    return [
        {
            "TestId": "test/test_demo.py::test_fail",
            "TestResult": "Failed",
            "TestName": "test_fail",
            "TestMessage": "assert (4 + 4) == 1",
        }
    ]


@pytest.fixture(scope="module")
def csharp_failing_tests():
    return [
        {
            "TestId": "f4189c78-aabf-361e-cf7f-1ab19f4bc38c",
            "TestResult": "Failed",
            "TestName": "Engi.Substrate.KeypairTests.Export_WithPassword",
            "TestMessage": "System.NotSupportedException : The combination of OSArchitecture and OSPlatform is not supported.",
        },
        {
            "TestId": "9445f183-bff2-ff58-3d33-753868952577",
            "TestResult": "Failed",
            "TestName": "Engi.Substrate.KeypairTests.Keyring_CreateFromMnemonic_NoPassword",
            "TestMessage": "System.NotSupportedException : The combination of OSArchitecture and OSPlatform is not supported.",
        },
        {
            "TestId": "ef10e76d-0d13-306b-796c-d7bc66a2f7a9",
            "TestResult": "Failed",
            "TestName": "Engi.Substrate.KeypairTests.Export",
            "TestMessage": "System.NotSupportedException : The combination of OSArchitecture and OSPlatform is not supported.",
        },
        {
            "TestId": "3ccdc37b-3c09-388f-097d-3c3c10fb48a6",
            "TestResult": "Failed",
            "TestName": "Engi.Substrate.KeypairTests.Keyring_CreateFromMnemonic_WithKeyPassword",
            "TestMessage": "System.NotSupportedException : The combination of OSArchitecture and OSPlatform is not supported.",
        },
    ]
