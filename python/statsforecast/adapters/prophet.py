# AUTOGENERATED! DO NOT EDIT! File to edit: ../../../nbs/src/adapters.prophet.ipynb.

# %% auto 0
__all__ = ['AutoARIMAProphet']

# %% ../../../nbs/src/adapters.prophet.ipynb 4
import sys

import pandas as pd
from ..arima import AutoARIMA

if sys.version_info.minor != 6 or (sys.platform not in ["win32", "cygwin"]):
    try:
        from prophet import Prophet
    except ModuleNotFoundError as e:
        msg = (
            "{e}. To use prophet adapters you have to install "
            "prophet. Please run `pip install prophet`. "
            "Note that it is recommended to install prophet "
            "using conda environments due to dependencies."
        )
        raise ModuleNotFoundError(msg) from e
elif sys.version_info.minor == 6 and (sys.platform in ["win32", "cygwin"]):
    try:
        from fbprophet import Prophet
    except ModuleNotFoundError as e:
        msg = (
            "{e}. To use prophet adapters you have to install "
            "fbprophet. Please run `pip install fbprophet`. "
            "Note that it is recommended to install prophet "
            "using conda environments due to dependencies."
        )
        raise ModuleNotFoundError(msg) from e

# %% ../../../nbs/src/adapters.prophet.ipynb 7
class AutoARIMAProphet(Prophet):
    """AutoARIMAProphet adapter.

    Returns best ARIMA model using external variables created by the Prophet interface.
    This class receives as parameters the same as prophet.Prophet and uses a `models.AutoARIMA`
    backend.

    If your forecasting pipeline uses Prophet the `AutoARIMAProphet` adapter helps to
    easily substitute Prophet with an AutoARIMA.

    Parameters
    ----------
    growth : string
        'linear', 'logistic' or 'flat' to specify a linear, logistic or flat trend.
    changepoints : List of dates
        Potential changepoints. Otherwise selected automatically.
    n_changepoints : int
        Number of potential changepoints to include.
    changepoint_range : float
        Proportion of history in which trend changepoints will be estimated.
    yearly_seasonality : str, bool or int
        Fit yearly seasonality. Can be 'auto', True, False, or a number of Fourier terms to generate.
    weekly_seasonality : str, bool or int
        Fit weekly seasonality. Can be 'auto', True, False, or a number of Fourier terms to generate.
    daily_seasonality : str, bool or int
        Fit daily seasonality. Can be 'auto', True, False, or a number of Fourier terms to generate.
    holidays : pandas.DataFrame
        DataFrame with columns holiday (string) and ds (date type).
    interval_width : float
        Uncertainty forecast intervals width. `StatsForecast`'s level

    Notes
    -----
    You can create automated exogenous variables from the Prophet data processing pipeline
    these exogenous will be included into `AutoARIMA`'s exogenous features. Parameters like
    `seasonality_mode`, `seasonality_prior_scale`, `holidays_prior_scale`, `changepoint_prior_scale`,
    `mcmc_samples`, `uncertainty_samples`, `stan_backend` are Prophet exclusive.

    References
    ----------
    [Sean J. Taylor, Benjamin Letham (2017). "Prophet Forecasting at Scale"](https://peerj.com/preprints/3190.pdf)

    [Oskar Triebe, Hansika Hewamalage, Polina Pilyugina, Nikolay Laptev, Christoph Bergmeir, Ram Rajagopal (2021). "NeuralProphet: Explainable Forecasting at Scale".](https://arxiv.org/pdf/2111.15397.pdf)

    [Rob J. Hyndman, Yeasmin Khandakar (2008). "Automatic Time Series Forecasting: The forecast package for R"](https://www.jstatsoft.org/article/view/v027i03).
    """

    def __init__(
        self,
        growth="linear",
        changepoints=None,
        n_changepoints=25,
        changepoint_range=0.8,
        yearly_seasonality="auto",
        weekly_seasonality="auto",
        daily_seasonality="auto",
        holidays=None,
        seasonality_mode="additive",
        seasonality_prior_scale=10.0,
        holidays_prior_scale=10.0,
        changepoint_prior_scale=0.05,
        mcmc_samples=0,
        interval_width=0.80,
        uncertainty_samples=1000,
        stan_backend=None,
        d=None,
        D=None,
        max_p=5,
        max_q=5,
        max_P=2,
        max_Q=2,
        max_order=5,
        max_d=2,
        max_D=1,
        start_p=2,
        start_q=2,
        start_P=1,
        start_Q=1,
        stationary=False,
        seasonal=True,
        ic="aicc",
        stepwise=True,
        nmodels=94,
        trace=False,
        approximation=False,
        method=None,
        truncate=None,
        test="kpss",
        test_kwargs=None,
        seasonal_test="seas",
        seasonal_test_kwargs=None,
        allowdrift=False,
        allowmean=False,
        blambda=None,
        biasadj=False,
        period=1,
    ):
        Prophet.__init__(
            self,
            growth,
            changepoints,
            n_changepoints,
            changepoint_range,
            yearly_seasonality,
            weekly_seasonality,
            daily_seasonality,
            holidays,
            seasonality_mode,
            seasonality_prior_scale,
            holidays_prior_scale,
            changepoint_prior_scale,
            mcmc_samples,
            interval_width,
            uncertainty_samples,
            stan_backend,
        )
        self.arima = AutoARIMA(
            d=d,
            D=D,
            max_p=max_p,
            max_q=max_q,
            max_P=max_P,
            max_Q=max_Q,
            max_order=max_order,
            max_d=max_d,
            max_D=max_D,
            start_p=start_p,
            start_q=start_q,
            start_P=start_P,
            start_Q=start_Q,
            stationary=stationary,
            seasonal=seasonal,
            ic=ic,
            stepwise=stepwise,
            nmodels=nmodels,
            trace=trace,
            approximation=approximation,
            method=method,
            truncate=truncate,
            test=test,
            test_kwargs=test_kwargs,
            seasonal_test=seasonal_test,
            seasonal_test_kwargs=seasonal_test_kwargs,
            allowdrift=allowdrift,
            allowmean=allowmean,
            blambda=blambda,
            biasadj=biasadj,
            period=period,
        )

    def fit(self, df, disable_seasonal_features=True):
        """Fit the AutoARIMAProphet adapter.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame with columns ds (date type) and y, the time series.
        disable_seasonal_features : bool (default=True)
            Disable Prophet's seasonal features.

        Returns
        -------
        AutoARIMAProphet
            Adapter object with `AutoARIMA` fitted model.
        """
        if self.history is not None:
            raise Exception(
                "Prophet object can only be fit once. " "Instantiate a new object."
            )
        if ("ds" not in df) or ("y" not in df):
            raise ValueError(
                'Dataframe must have columns "ds" and "y" with the dates and '
                "values respectively."
            )
        history = df[df["y"].notnull()].copy()
        if history.shape[0] < 2:
            raise ValueError("Dataframe has less than 2 non-NaN rows.")
        self.history_dates = pd.to_datetime(
            pd.Series(df["ds"].unique(), name="ds")
        ).sort_values()

        history = self.setup_dataframe(history, initialize_scales=True)
        self.history = history
        self.set_auto_seasonalities()
        seasonal_features, prior_scales, component_cols, modes = (
            self.make_all_seasonality_features(history)
        )
        self.train_component_cols = component_cols
        self.component_modes = modes
        if disable_seasonal_features:
            seas = tuple(self.seasonalities.keys())
            seasonal_features = seasonal_features.loc[
                :, ~seasonal_features.columns.str.startswith(seas)
            ]
        self.xreg_cols = seasonal_features.columns

        y = history["y"].values
        X = seasonal_features.values if not seasonal_features.empty else None
        self.arima = self.arima.fit(y=y, X=X)

        return self

    def predict(self, df=None):
        """Predict using the AutoARIMAProphet adapter.

        Parameters
        ----------
        df : pandas.DataFrame
            DataFrame with columns ds (date type) and y, the time series.

        Returns
        -------
        pandas.DataFrame
            DataFrame with the forecast components.
        """
        if self.history is None:
            raise Exception("Model has not been fit.")

        if df is None:
            df = self.history.copy()
        else:
            if df.shape[0] == 0:
                raise ValueError("Dataframe has no rows.")
            df = self.setup_dataframe(df.copy())

        seasonal_features = self.make_all_seasonality_features(df)[0].loc[
            :, self.xreg_cols
        ]

        ds_forecast = set(df["ds"])
        h = len(ds_forecast - set(self.history["ds"]))
        if h > 0:
            X = seasonal_features.values[-h:] if not seasonal_features.empty else None
            fcsts_df = self.arima.predict(
                h=h, X=X, level=int(100 * self.interval_width)
            )
        else:
            fcsts_df = pd.DataFrame()
        if len(ds_forecast) > h:
            in_sample = self.arima.predict_in_sample(
                level=int(100 * self.interval_width)
            )
            fcsts_df = pd.concat([in_sample, fcsts_df]).reset_index(drop=True)

        yhat = fcsts_df.pop("mean")
        fcsts_df.columns = ["yhat_lower", "yhat_upper"]
        fcsts_df.insert(0, "yhat", yhat)
        fcsts_df.insert(0, "ds", df["ds"])

        return fcsts_df
