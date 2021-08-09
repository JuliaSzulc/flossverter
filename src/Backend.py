import pandas as pd

from src import metrics


class Backend:
    def __init__(self, dmc_path, ariadna_path):
        self.dmc_df = pd.read_csv(dmc_path, index_col='number')
        self.ariadna_df = pd.read_csv(ariadna_path, index_col='number')
        
        self.metrics = {
            'RGB euclidean': metrics.rgb_euclidean,
            'RGB with gamma correction': metrics.rgb_gamma_correction,
            'CIE76': metrics.cie76,
            'CIE94': metrics.cie94,
            'CIEDE2000': metrics.ciede2000,
            'CMC 1:1': metrics.cmc_1_1,
            'CMC 2:1': metrics.cmc_2_1
        }
        self.default_metric = 'CIEDE2000'
    
    def get_dmc_rgb(self, code):
        return self.dmc_df.at[code, 'rgb']
    
    def find_similar(self, base_number, metric, n=5):
        base_color = self.get_dmc_rgb(base_number)
        
        metric_f = self.metrics[metric]

        self.ariadna_df['score'] =\
            [metric_f(base_color, c) for c in self.ariadna_df['rgb']]
        top_colors_rows = self.ariadna_df.nsmallest(n, 'score')
        
        top_codes = top_colors_rows.index.to_list()
        top_colors = top_colors_rows['rgb'].to_list()

        return top_codes, top_colors
    