"""
Dashboard backend class.
"""
from pathlib import Path
from typing import Union

import pandas as pd

from src.metrics import (
    rgb_euclidean,
    cie76,
    cie94,
    ciede2000,
    cmc_1_1,
    cmc_2_1,
    rgb_euclidean,
    rgb_euclidean_gamma_correction,
)


class Backend:
    """
    Class storing all CSV files with mouline codes to RGB convertions.
    """

    def __init__(self, dmc_path: Union[Path, str], ariadna_path: Union[Path, str]):
        """
        Args:
            dmc_path (Union[Path, str],): Path to DMC convertion sheet in CSV.
            ariadna_path (Union[Path, str],): Path to Ariadna convertion sheet in CSV.
        """
        self._dmc_df = pd.read_csv(dmc_path, index_col="number")
        self._ariadna_df = pd.read_csv(ariadna_path, index_col="number")

        self.metrics = {
            "RGB euclidean": rgb_euclidean,
            "RGB with gamma correction": rgb_euclidean_gamma_correction,
            "CIE76": cie76,
            "CIE94": cie94,
            "CIEDE2000": ciede2000,
            "CMC 1:1": cmc_1_1,
            "CMC 2:1": cmc_2_1,
        }
        self.default_metric = "CIEDE2000"

    @property
    def dmc_df(self) -> pd.DataFrame:
        """
        Returns DMC dataframe.
        """
        return self._dmc_df.copy()

    @property
    def ariadna_df(self) -> pd.DataFrame:
        """
        Returns Ariadna dataframe.
        """
        return self._ariadna_df.copy()

    def dmc_to_hex(self, dmc: str) -> str:
        """
        Converts given DMC identifier to a hexadecimal color code.

        Args:
            dmc (str): DMC mouline identifier.

        Returns:
            str: Hexadecimal color code preceded by '#'.
        """
        return self._dmc_df.at[dmc, "rgb"]

    def find_similar(self, dmc: str, metric: str, n=5) -> tuple[list[str], list[str]]:
        """
        Finds colors similar to the given one using passed

        Args:
            dmc (str): DMC mouline identifier.
            metric (str): Metric to use.
            n (int, optional): Expected number of similar colors. Defaults to 5.

        Returns:
            tuple[list[str], list[str]]: Lists of DMC identifiers and hexadecimal codes
                of similar colors.
        """
        base_color = self.dmc_to_hex(dmc)

        metric_f = self.metrics[metric]

        self._ariadna_df["score"] = [
            metric_f(base_color, c) for c in self._ariadna_df["rgb"]
        ]
        top_colors_rows = self._ariadna_df.nsmallest(n, "score")

        top_dmc_codes = top_colors_rows.index.to_list()
        top_colors = top_colors_rows["rgb"].to_list()

        return top_dmc_codes, top_colors
