from unittest.mock import patch, Mock
from nose.tools import assert_dict_equal, assert_is_not_none, assert_is_not
from nhl_lights import bulb_current

@patch('nhl_lights.requests.get')
def test_bulb_current(mock_get):
    lights={'action':{'on': True, 'bri': 254, 'hue': 8402, 'sat': 140, 'effect': 'none', 'xy': [0.4575, 0.4099], 'ct': 366, 'alert': 'none', 'colormode': 'hs'}}
    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value=lights

    r = bulb_current()

    assert_dict_equal(r, {'sat': r['sat'], 'bri': r['bri'], 'hue': r['hue'], 'alert': 'none'})

'''
@patch('nhl_lights.requests.get')
def test_bulb_flash(mock_get):
'''