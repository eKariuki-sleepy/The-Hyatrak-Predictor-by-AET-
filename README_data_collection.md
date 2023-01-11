## The main features of this package are:

This repository allows for collection of data crucial to the monitoring and prediction of Hyacinth prevalence patterns.

This notebook shows you how to use GeoPandas and Google Earth Engine to:

- Download Modis and Landsat 8 data
- Download and use CHIRPS dataset
- Calculate NDVI, NDBI and NDWI
- Perform area (km²) calculation

<br />

## Requirements

- Access to Google Earth Engine. The data collection and processing happens entirely on the cloud.
- Area of interest as a geojson (in this case Winam lake and Winam's surrounding area buffer)

<br />

## Workflow

1. Fetch AOI (in this case saved in google drive) and generate an Earth Engine polygon of the input coordinates

```python

winam_lake_path = './drive/My Drive/Winam_buffer.geojson'#Change this to your geojson file destination path

winam_without_lake_path='./drive/My Drive/Winam_buffer_minus_lake.geojson'

##load the geojson
winam_lake=gpd.read_file(winam_lake_path)
winam_without_lake=gpd.read_file(winam_without_lake_path)

#identify the geomety enclosing our dataset. the imagery will be clipped to this area of interest

winam_lake_geom=winam_lake["geometry"][0]
winam_without_lake_geom=winam_without_lake["geometry"][0]


#consists of a polygon in a multipolygon set up. Get the polygon.
winam_lake_poly=winam_lake_geom[0]
winam_without_lake_poly=winam_without_lake_geom[0]


#get the outside coords
ext_coord_winam_lake=list(winam_lake_poly.exterior.coords)
ext_coord_winam_without_lake=list(winam_without_lake_poly.exterior.coords)


#generate an Earth Engine polygon of the input coordinates
geometry_winam_lake=ee.Geometry.Polygon(ext_coord_winam_lake)
geometry_winam_without_lake=ee.Geometry.Polygon(ext_coord_winam_without_lake)



```

2. Generate Landsat , Chirps and MODIS data using Google Earth Engine

```python
# this function identifies relevant chirps, landsat and modis data and calculates monthly temperature, rainfall, NDVI and NDBI statistics from them


def calculate_stats(year,duration_in_years,region_aoi,lake_aoi)
'''
year: start year
duration_in_years : the number of years to do calculation
region_aoi: the geometry of the area bordering the lake
lake_aoi: the geometry of the lake
'''

landsat_winam_data,ndvi=calculate_stats(1984,39,geometry_winam_without_lake,geometry_winam_lake)


```

3. Put the dictionaries into a pandas dataframe and export to your folder of interest.

```python

landsat_winam_data_df=pd.DataFrame(landsat_winam_data)


landsat_winam_data_df.to_csv( './drive/My Drive/landsat_winam_data_.csv')

```

## Data structure

The data exported as a csv file will be used for training in the next step. It consists of the following fields.

- Digital_count - this is added later in the excel to ensure that the count of the records omits the field names.
- Year
- month
- mean_monthly_temp - mean monthly temperature
- mean_monthly_rainfall - mean monthly rainfall
- littoral_mean_monthly_ndvi - the mean montly ndvi values for the land surrounding the lake
- littoral_vegetation_area - the area bordering the lake in km² covered in vegetation
- mean_monthly_ndbi - the mean monthly NDBI values. It is used to identify uncultivated or bare land
- Bare_soil_area - the area bordering the lake in km² covered which is bare
- mean_monthly_ndwi - the mean monthly NDWI values
- water_area - The monthly surface area of the water surface in km²
- hyacinth_mean_monthly_ndvi - the mean monthly ndvi of the hyacinth
- hyacinth_area- the area in the lake covered with hyacinth in km²

<br />

## License

Copyright: ©AET 2022
<br />
Supported by the International Sustainability Academy (ISA), Hamburg - Germany

<br />

## Contact 
<br />
Caleb Masinde: ***caleb.masinde@motor_ai.com*** / ***calebjuma27@gmail.com***
<br />
Eric G Kariuki: ***gathirwa@aquaethanol.co.ke*** / ***ericgathirwak@gmail.com***
