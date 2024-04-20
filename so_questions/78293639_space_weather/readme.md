# SpaceWeather

This Python script provides a way to visualize space weather data as a heatmap or image. The data represents various environmental and astronomical measurements over time, specifically the KP, DST, SSN, and F10.7 indices.

## Description

The `SpaceWeather` class encapsulates the data loading, cleaning, and plotting functionalities. It provides a structured and efficient approach to handling space weather data. The plotting logic for each plot type (`imshow`, `pcolormesh`, `contourf`, `plot_surface`) is divided into separate methods, enhancing code modularity and readability.

## Indices

- **KP**: A planetary geomagnetic activity index, which measures geomagnetic storms. KP values above 40 typically indicate significant geomagnetic activity or storms.
- **DST**: Another geomagnetic index, where values below -30 indicate geomagnetic storms.
- **SSN**: Sunspot number, which is an index of the number of sunspots and groups of sunspots present on the surface of the sun.
- **F10.7**: The solar radio flux at 10.7 cm (2800 MHz), which is a measurement of the solar emissions in the microwave range, and it's often used as a proxy for solar activity.

## Usage

```python
from spaceWeather import SpaceWeather

sw = SpaceWeather("spaceWeather.csv")
sw.load_and_clean_data()

for plot_type in ["imshow", "pcolormesh", "contourf", "plot_surface"]:
    print(f"Plotting with plot type: {plot_type}")
    sw.plot_data(plot_type)
```

## Data

The full data file can be found [here](https://raw.githubusercontent.com/trenton3983/stack_overflow/master/so_questions/78293639_space_weather/spaceWeather.csv).

## Dependencies

- Python
- pandas
- numpy
- matplotlib

## References

This project is based on the Stack Overflow question [Visualizing Time-Series Data with Heatmaps and 3D Surface Plots](https://stackoverflow.com/q/78293639/7758804). The question discusses the visualization of space weather data as a heatmap or image, with the aim of plotting hours on the y-axis, dates on the x-axis, and intensity values for each day. The `SpaceWeather` class in this project provides a structured and efficient approach to handle this kind of data and create the desired visualizations.

## License

This project is licensed under the terms of the MIT license.