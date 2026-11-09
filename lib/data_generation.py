import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st


def get_dummy_returns_data(
    n: int,
    queue_lift_time: int,
    average_ski_down_time: int,
    min_ski_down_time: int,
    noise_sd: int,
    random_seed: int = 42,
) -> pd.DataFrame:
    """This function creates a dummy dataset of return times given a queue time, average
    number of returns per hour and the amplitude of the normally distributed noise
    applied.

    A return time is the time between a skier passing through the electronic gates at
    the bottom of the mountain before their run to them passing through the same gate
    again having gotten the lift to the top of the run and skiing back down.

    The queue + lift time is treated as a constant for all skiers.
    The average time to ski back down to the gate is treated as a Weibull (k=1.5) variable
    with lambda=average_returns_per_hour.
    There is assumed to be normal noise with zero-mean and standard deviation = noise_sd

    Args:
        n (int): the number of skiers in the dataset.
        queue_lift_time (int): the constant queue + lift time every skier experiences in
        minutes.
        average_ski_down_time (int): The average time to ski down the run in minutes.
        min_ski_down_time (int): the minimum time to ski down for the fastest skiers in
        minutes.
        noise_sd (int): The amplitude of noise to assume in the overall times to return.
        Measured in minutes.
        random_seed (int): random seed to make results replicable
    """
    data_dict = {
        "skier_id": pd.Series(np.arange(n), dtype="string").str.pad(
            len(str(n)) + 2, side="left", fillchar="0"
        ),
        "queue_lift_time": pd.Series([queue_lift_time] * n, dtype="Int64"),
        "ski_down_time": pd.Series(
            st.weibull_min(c=1.5, scale=average_ski_down_time).rvs(
                size=n, random_state=random_seed
            ),  # convert to minutes to match other inputs
            dtype="Float64",
        ).clip(min_ski_down_time),
        "noise": pd.Series(
            st.norm(loc=0, scale=noise_sd).rvs(size=n, random_state=random_seed),
            dtype="Float64",
        ),
    }
    df = pd.DataFrame(data_dict)
    df["total_return_time"] = (
        df["queue_lift_time"] + df["ski_down_time"] + df["noise"]
    ).clip(lower=0)
    return df


if __name__ == "__main__":
    short_queue_data = get_dummy_returns_data(1000, 15, 30, 15, 5)
    mid_queue_data = get_dummy_returns_data(1000, 45, 30, 15, 5)
    long_queue_data = get_dummy_returns_data(1000, 90, 30, 15, 5)
    print(f"Short queue data: \n{short_queue_data.describe()}")
    print(f"Mid queue data: \n{mid_queue_data.describe()}")
    print(f"Long queue data: \n{long_queue_data.describe()}")

    sd_fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    short_queue_bins = np.arange(0, short_queue_data["ski_down_time"].max(), 1)
    mid_queue_bins = np.arange(0, mid_queue_data["ski_down_time"].max(), 1)
    long_queue_bins = np.arange(0, long_queue_data["ski_down_time"].max(), 1)
    ax1.hist(short_queue_data["ski_down_time"], bins=short_queue_bins)
    ax2.hist(mid_queue_data["ski_down_time"], bins=mid_queue_bins)
    ax3.hist(long_queue_data["ski_down_time"], bins=long_queue_bins)

    tot_fig, (ax4, ax5, ax6) = plt.subplots(3, 1, sharex=True)
    short_queue_bins = np.arange(0, short_queue_data["total_return_time"].max(), 1)
    mid_queue_bins = np.arange(0, mid_queue_data["total_return_time"].max(), 1)
    long_queue_bins = np.arange(0, long_queue_data["total_return_time"].max(), 1)
    ax4.hist(short_queue_data["total_return_time"], bins=short_queue_bins)
    ax5.hist(mid_queue_data["total_return_time"], bins=mid_queue_bins)
    ax6.hist(long_queue_data["total_return_time"], bins=long_queue_bins)

    plt.show()
