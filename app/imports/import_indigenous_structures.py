import geopandas as gpd

"""
This dataset is not currently used, however it could be used as an alternative base layer to GNAF.
"""

"""
Data obtained from:
https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files
"""

boundary_file_path = "~/Downloads/ILOC_2021_AUST_GDA2020_SHP/ILOC_2021_AUST_GDA2020.shp"
boundaries = gpd.read_file(boundary_file_path)
print(boundaries.head())
"""
print(boundaries.columns)
['ILO_CODE21', 'ILO_NAME21', 'IAR_CODE21', 'IAR_NAME21', 'IRE_CODE21',
       'IRE_NAME21', 'STE_CODE21', 'STE_NAME21', 'AUS_CODE21', 'AUS_NAME21',
       'AREASQKM21', 'LOCI_URI21', 'SHAPE_Leng', 'SHAPE_Area', 'geometry']
"""