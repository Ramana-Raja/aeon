"""Tests for RIST Regressor."""

import numpy as np
from sklearn.metrics import mean_squared_error
import pytest
from aeon.datasets import load_covid_3month
from aeon.regression.hybrid import RISTRegressor
from aeon.utils.validation._dependencies import _check_soft_dependencies


@pytest.mark.skipif(
    not _check_soft_dependencies(["statsmodels"], severity="none"),
    reason="statsmodels soft dependency not found.",
)
def test_rist_regressor():
    """Test RIST Regressor on covid 3-month data."""
    X, y = load_covid_3month()
    X, y = X[:10], y[:10]
    n = int(0.8 * len(X))

    X_train, X_test = X[:n], X[n:]
    y_train, y_test = y[:n], y[n:]

    reg = RISTRegressor(random_state=0)
    reg.fit(X_train, y_train)

    y_pred = reg.predict(X_test)

    assert y_pred.shape == y_test.shape
    mse = mean_squared_error(y_test, y_pred)
    assert np.isfinite(mse)
    assert not np.any(np.isnan(y_pred))
    assert mse < 1e6
