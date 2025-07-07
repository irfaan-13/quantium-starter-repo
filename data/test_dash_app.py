import pytest
from dash.testing.application_runners import import_app

@pytest.fixture
def dash_app():
    app = import_app('dash_app')  # Adjust if your app filename differs
    return app

def test_header_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    header = dash_duo.find_element('h1')
    assert header is not None
    assert 'Soul Foods Pink Morsel Sales Visualiser' in header.text

def test_visualisation_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    graph = dash_duo.find_element('#sales-line-chart')
    assert graph is not None

def test_region_picker_present(dash_duo, dash_app):
    dash_duo.start_server(dash_app)
    radio_items = dash_duo.find_element('#region-radio')
    assert radio_items is not None
