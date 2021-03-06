import os
from unittest import mock

import numpy as np
import pytest
from plotly.graph_objects import Figure

from einsteinpy.metric import Schwarzschild
from einsteinpy.coordinates.utils import four_position, stacked_vec
from einsteinpy.geodesic import Geodesic
from einsteinpy.plotting import InteractiveGeodesicPlotter


@pytest.fixture()
def dummy_data():
    M = 6e24
    t = 0.
    x_vec = np.array([130.0, np.pi / 2, -np.pi / 8])
    v_vec = np.array([0.0, 0.0, 1900.0])

    ms_cov = Schwarzschild(M=M)
    x_4vec = four_position(t, x_vec)
    ms_cov_mat = ms_cov.metric_covariant(x_4vec)
    init_vec = stacked_vec(ms_cov_mat, t, x_vec, v_vec, time_like=True)

    end_lambda = 0.002
    step_size = 5e-8

    geod = Geodesic(metric=ms_cov, init_vec=init_vec, end_lambda=end_lambda, step_size=step_size)

    return geod


def test_interactive_plotter_has_figure(dummy_data):
    geodesic = dummy_data
    cl = InteractiveGeodesicPlotter()
    assert isinstance(cl.fig, Figure)
    assert cl.attractor_present is False


def test_plot_draws_fig(dummy_data):
    geodesic = dummy_data
    cl = InteractiveGeodesicPlotter()
    cl.plot(geodesic)
    fig = cl.show()
    assert cl.attractor_present
    assert fig


@mock.patch("einsteinpy.plotting.geodesics.interactive.saveplot")
def test_save_saves_plot(mock_save, dummy_data):
    geodesic = dummy_data
    cl = InteractiveGeodesicPlotter()
    cl.plot(geodesic)
    name = "test_plot.png"
    cl.save(name)
    basename, ext = os.path.splitext(name)
    mock_save.assert_called_with(
        cl.fig, image=ext[1:], image_filename=basename, show_link=False
    )


def test_plot_calls_draw_attractor_Manualscale(dummy_data):
    geodesic = dummy_data
    cl = InteractiveGeodesicPlotter(attractor_radius_scale=1500)
    cl.plot(geodesic)
    assert cl.attractor_present
    assert cl.attractor_radius_scale == 1500


def test_plot_calls_draw_attractor_AutoScale(dummy_data):
    geodesic = dummy_data
    cl = InteractiveGeodesicPlotter()
    cl.plot(geodesic)
    assert cl.attractor_present
