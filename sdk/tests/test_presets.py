from omniedu.presets import known_presets, resolve_model


def test_short_names_resolve() -> None:
    assert resolve_model("4B") == "OpenDCAI/Omni-Edu-4B"
    assert resolve_model("9b") == "OpenDCAI/Omni-Edu-9B"
    assert resolve_model("OmniEdu-27B") == "OpenDCAI/Omni-Edu-27B"
    assert resolve_model("omni-edu-27b") == "OpenDCAI/Omni-Edu-27B"


def test_full_ids_and_paths_pass_through() -> None:
    assert resolve_model("OpenDCAI/Omni-Edu-9B") == "OpenDCAI/Omni-Edu-9B"
    assert resolve_model("/models/Omni-Edu-4B") == "/models/Omni-Edu-4B"


def test_presets_are_complete() -> None:
    assert set(known_presets()) == {"4B", "9B", "27B"}


def test_empty_name_is_rejected() -> None:
    import pytest

    with pytest.raises(ValueError):
        resolve_model("  ")

