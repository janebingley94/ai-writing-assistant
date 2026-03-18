import json


class StructuredOutputError(ValueError):
    pass


class StructuredOutputParser:
    @staticmethod
    def parse_json(text: str, required_keys: list[str] | None = None) -> dict:
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise StructuredOutputError(f"Invalid JSON: {exc}") from exc

        if not isinstance(data, dict):
            raise StructuredOutputError("JSON output must be an object.")

        if required_keys:
            missing = [key for key in required_keys if key not in data]
            if missing:
                raise StructuredOutputError(f"Missing required keys: {missing}")

        return data
