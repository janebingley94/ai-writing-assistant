import pytest

from services.structured_output import StructuredOutputError, StructuredOutputParser


def test_parse_json_valid():
    data = StructuredOutputParser.parse_json('{"subject":"hi","body":"x","suggested_cta":"y"}')
    assert data["subject"] == "hi"


def test_parse_json_invalid():
    with pytest.raises(StructuredOutputError):
        StructuredOutputParser.parse_json("{not json}")


def test_parse_json_missing_keys():
    with pytest.raises(StructuredOutputError):
        StructuredOutputParser.parse_json('{"subject":"hi"}', required_keys=["subject", "body"])
