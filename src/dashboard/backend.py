"""
Dashboard backend class.
"""
from pathlib import Path
from typing import Union

import pandas as pd

from src.metrics import (
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

    Args:
        dmc_path (Union[Path, str],): Path to DMC convertion sheet in CSV.
        ariadna_path (Union[Path, str],): Path to Ariadna convertion sheet in CSV.
    """

    def __init__(self, dmc_path: Union[Path, str], ariadna_path: Union[Path, str]):
        self._dmc_df = pd.read_csv(dmc_path, index_col="number")
        self._ariadna_df = pd.read_csv(ariadna_path, index_col="number")
        self.METRICS = {
            "RGB euclidean": rgb_euclidean,
            "RGB with gamma correction": rgb_euclidean_gamma_correction,
            "CIE76": cie76,
            "CIE94": cie94,
            "CIEDE2000": ciede2000,
            "CMC 1:1": cmc_1_1,
            "CMC 2:1": cmc_2_1,
        }
        self.DEFAULT_METRIC = "CIEDE2000"

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

    def find_similar(
        self, base_color: str, metric: str, n: int = 5
    ) -> tuple[list[str], list[str]]:
        """
        Finds colors similar to the given one using passed.

        Args:
            base_color (str): Hex RGB code of the base color.
            metric (str): Metric to use.
            n (int, optional): Expected number of similar colors. Defaults to 5.

        Returns:
            tuple[list[str], list[str]]: Lists of Ariadna identifiers and hexadecimal
                codes of similar colors.
        """
        metric_f = self.METRICS[metric]

        self._ariadna_df["score"] = [
            metric_f(base_color, c) for c in self._ariadna_df["rgb"]
        ]
        top_colors_rows = self._ariadna_df.nsmallest(n, "score")

        top_ariadna_codes = top_colors_rows.index.to_list()
        top_colors = top_colors_rows["rgb"].to_list()

        return top_ariadna_codes, top_colors
