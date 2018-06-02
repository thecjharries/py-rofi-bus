# pylint:disable=W,C,R

from mock import call, MagicMock, patch

from py_rofi_bus.components.mixins import HasConfig


@patch('py_rofi_bus.components.mixins.has_config.Config')
def test_without_config(mock_config):
    result = MagicMock()
    mock_config.return_value = result
    mock_config.assert_not_called()
    has_config = HasConfig()
    mock_config.assert_called_once()
    assert(has_config.config == result)


@patch('py_rofi_bus.components.mixins.has_config.Config')
def test_with_config(mock_config):
    result = MagicMock()
    mock_config.return_value = result
    mock_config.assert_not_called()
    has_config = HasConfig(config=result)
    mock_config.assert_not_called()
    assert(has_config.config == result)
