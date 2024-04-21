import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict, Union
import matplotlib.figure
import matplotlib.axes


class SpaceWeather:
    """
    Solution to Stack Overflow question https://stackoverflow.com/q/78293639/7758804
    """

    def __init__(self, file_path: str):
        """
        Initialize the SpaceWeather class.

        Parameters:
        file_path (str): The path to the CSV file containing the data.
        """
        self.file_path = file_path
        self.df = None
        self.img_data = None
        self.labels = None
        self.dates = None

    def load_and_clean_data(self):
        """
        Load and clean the space weather data.
        The code for which is from https://stackoverflow.com/a/78294905/7758804
        """
        # Load the necessary columns, parse dates, skip header, and rename columns
        self.df = pd.read_csv(
            self.file_path,
            parse_dates=[0],
            skiprows=1,
            usecols=[0, 4, 6],
            names=["date", "kp", "dst"],
            header=0,
        )

        # Extract day of year and hour into new columns
        self.df["day_of_year"] = self.df["date"].dt.day_of_year  # new columns
        self.df["hour"] = self.df["date"].dt.hour

        # Add event column
        self.df["event"] = ""
        self.df.loc[(self.df.kp > 40) | (self.df.dst < -30), "event"] = "S"
        self.df.loc[self.df.date == pd.Timestamp("2020/09/01 01:00"), "event"] = "E"

        # Create image data
        self.img_data = self.df.pivot_table(
            index="hour", columns="day_of_year", values="dst"
        ).values
        # Create labels to be used as annotations
        self.labels = self.df.pivot(
            index="hour", columns="day_of_year", values="event"
        ).values
        # Create date range for x-axis
        self.dates = pd.date_range(
            start=self.df.date.min(),
            end=self.df.date.max() + pd.offsets.Day(),
            freq="D",
            inclusive="both",
        )

    def plot_data(self, plot_type: str = "imshow"):
        """
        Plot the space weather data.
        The code for plotting is from https://stackoverflow.com/a/78294536/7758804

        Parameters:
        plot_type (str): The type of plot to create. Options are 'imshow', 'pcolormesh', 'contourf', 'plot_surface'.
        """
        common_params: Dict[str, Union[int, str]] = dict(
            vmin=-40, vmax=20, cmap="jet_r"
        )

        # Create meshgrid for non-imshow plots
        if plot_type != "imshow":
            x, y = np.meshgrid(
                mdates.date2num(self.dates), range(self.img_data.shape[0])
            )

        # Plot data based on a plot type
        if plot_type == "imshow":
            self.plot_imshow(common_params)
        elif plot_type == "pcolormesh":
            self.plot_pcolormesh(x, y, common_params)
        elif plot_type == "contourf":
            self.plot_contourf(x, y, common_params)
        elif plot_type == "plot_surface":
            self.plot_surface(x, y, common_params)

    def plot_imshow(self, common_params: Dict[str, Union[int, str]]):
        """
        Plot the space weather data using imshow.

        Parameters:
        common_params (Dict[str, Union[int, str]]): Common parameters for the plot.
        """
        f, ax = plt.subplots(figsize=(11, 3))
        im = ax.imshow(
            self.img_data,
            interpolation="none",
            aspect="auto",
            origin="lower",
            extent=(
                mdates.date2num(self.dates[0] - pd.offsets.Hour(12)),
                mdates.date2num(self.dates[-1] + pd.offsets.Hour(12)),
                float(self.df["hour"].min()),
                float(self.df["hour"].max()),
            ),
            **common_params,
        )
        self.format_plot(f, im, ax, "imshow")

    def plot_pcolormesh(
        self, x: np.ndarray, y: np.ndarray, common_params: Dict[str, Union[int, str]]
    ):
        """
        Plot the space weather data using pcolormesh.

        Parameters:
        x (np.ndarray): The X coordinates of the meshgrid.
        y (np.ndarray): The Y coordinates of the meshgrid.
        common_params (Dict[str, Union[int, str]]): Common parameters for the plot.
        """
        f, ax = plt.subplots(figsize=(11, 3))
        im = ax.pcolormesh(x, y, self.img_data, **common_params)
        self.format_plot(f, im, ax, "pcolormesh")

    def plot_contourf(
        self, x: np.ndarray, y: np.ndarray, common_params: Dict[str, Union[int, str]]
    ):
        """
        Plot the space weather data using contourf.

        Parameters:
        x (np.ndarray): The X coordinates of the meshgrid.
        y (np.ndarray): The Y coordinates of the meshgrid.
        common_params (Dict[str, Union[int, str]]): Common parameters for the plot.
        """
        f, ax = plt.subplots(figsize=(11, 3))
        im = ax.contourf(x, y, self.img_data, levels=10, **common_params)
        self.format_plot(f, im, ax, "contourf")

    def plot_surface(
        self, x: np.ndarray, y: np.ndarray, common_params: Dict[str, Union[int, str]]
    ):
        """
        Plot the space weather data using plot_surface.

        Parameters:
        x (np.ndarray): The X coordinates of the meshgrid.
        y (np.ndarray): The Y coordinates of the meshgrid.
        common_params (Dict[str, Union[int, str]]): Common parameters for the plot.
        """
        f = plt.figure(figsize=(11, 11))
        ax = f.add_subplot(projection="3d", proj_type="persp", focal_length=0.2)

        ax.view_init(azim=79, elev=25)
        ax.set_box_aspect(aspect=(3, 2, 1.5), zoom=0.95)

        im = ax.plot_surface(x, y, self.img_data, **common_params)
        ax.contourf(
            x,
            y,
            self.img_data,
            levels=10,
            zdir="z",
            offset=-35,
            alpha=0.3,
            **common_params,
        )
        ax.contour(
            x,
            y,
            self.img_data,
            levels=8,
            zdir="z",
            offset=24,
            alpha=0.5,
            linewidths=3,
            **common_params,
        )
        ax.set_zlabel("Dst")
        ax.invert_xaxis()  # Orders the dates from left to right
        ax.invert_yaxis()  # Orders the hours from front to back
        self.format_plot(f, im, ax, "plot_surface")

    def format_plot(
        self,
        f: matplotlib.figure.Figure,
        im: matplotlib.image.AxesImage,
        ax: matplotlib.axes.Axes,
        plot_type: str,
    ):
        """
        Format the plot.

        Parameters:
        f (matplotlib.figure.Figure): The figure.
        im (matplotlib.image.AxesImage): The image.
        ax (matplotlib.axes.Axes): The axes.
        plot_type (str): The type of plot.
        """
        # Add labels
        for (row, col), label in np.ndenumerate(self.labels):
            if plot_type == "plot_surface":
                break  # skip labels on 3d plot for simplicity

            if type(label) is not str:
                continue
            ax.text(
                self.dates[col] - pd.offsets.Hour(6),
                row,
                label,
                fontsize=9,
                fontweight="bold",
            )

        # Format x-axis with dates
        ax.set_xticks(self.dates)
        ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt="%b %d"))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))  # Tick every 5 days
        ax.tick_params(axis="x", rotation=90)

        # Format y axis
        ax.set_yticks([0, 6, 12, 18, 23])
        ax.set_ylabel("UT")

        # Add colorbar
        aspect, fraction = (10, 0.15) if plot_type != "plot_surface" else (5, 0.05)
        f.colorbar(im, aspect=aspect, fraction=fraction, pad=0.01, label="nT")

        # Add title
        ax.set_title(f"Dst\n(plot type: {plot_type})", fontweight="bold")

        # Adjust layout
        plt.tight_layout()

        # Save the plot
        plt.savefig(f"{plot_type}_plot.png", dpi=300)

        # Show the plot
        plt.show()


if __name__ == "__main__":
    sw = SpaceWeather("spaceWeather.csv")
    sw.load_and_clean_data()

    for plot_type in ["imshow", "pcolormesh", "contourf", "plot_surface"]:
        print(f"Plotting with plot type: {plot_type}")
        sw.plot_data(plot_type)
