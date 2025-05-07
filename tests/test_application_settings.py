import pytest
from application import Settings


@pytest.fixture
def settings_instance():
    return Settings()


@pytest.mark.parametrize(
    "new_color",
    [
        "bg-gradient-green-blue",
        "bg-gradient-teal-green",
        "bg-gradient-yellow-green",
    ]
)
def test_change_back_ground_home_valuebox_valid(settings_instance, new_color):
    settings_instance.change_back_ground_home_valuebox(new_color)
    assert settings_instance.background_home_value_box == new_color


def test_change_back_ground_home(settings_instance):
    settings_instance.change_back_ground_home("bg-gradient-green-pink")
    assert settings_instance.background_home == "bg-gradient-green-pink"


@pytest.mark.parametrize(
    "invalid_color",
    [
        "bg-gradient-unknown",
        "green-white",
        "",
        None
    ]
)
def test_change_back_ground_home_valuebox_invalid(settings_instance, invalid_color):
    with pytest.raises(
            ValueError,
            match="La nouvelle couleur doit être parmis celles disponibles"
    ):
        settings_instance.change_back_ground_home_valuebox(invalid_color)
