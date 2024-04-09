import xarray as xr
from kerchunk.hdf import SingleHdf5ToZarr
from kerchunk.combine import MultiZarrToZarr
import fsspec
import ujson
import pathlib
import datetime
import pandas as pd
import os
import dask
from dask.distributed import Client

base_folder = "/wopr1/users/sfreeman/goes16_data/L1B/C14/2020/"

start_date = datetime.datetime(2020, 2, 2)
end_date = datetime.datetime(2020, 12, 31)
channel = 14


def gen_json(u, folder_name):
    goes_filnm = u.split("/")[-1]
    full_file_name = folder_name + "/{0}.json".format(goes_filnm)
    if pathlib.Path(full_file_name).exists() and os.stat(full_file_name).st_size > 1000:
        return
    so = dict(mode="rb", anon=True, default_fill_cache=False, default_cache_type="none")
    with fsspec.open(u, **so) as inf:
        h5chunks = SingleHdf5ToZarr(inf, u, inline_threshold=300)
        with open(
            full_file_name,
            "wb",
        ) as outf:
            translated_chunks = h5chunks.translate()
            encoded_string = ujson.dumps(translated_chunks).encode()
            outf.write(encoded_string)


if __name__ == "__main__":
    from dask import config as cfg

    cfg.set({"distributed.scheduler.worker-ttl": 1000})

    dates_to_examine = pd.date_range(
        start_date, end_date, freq=datetime.timedelta(days=1)
    )
    for curr_date in dates_to_examine:
        date_base_folder = base_folder + "/" + curr_date.strftime("%m/%d/")
        pathlib.Path(date_base_folder).mkdir(parents=True, exist_ok=True)
        print("Processing {curr_date}".format(curr_date=curr_date.strftime("%Y/%m/%d")))
        folder_name = date_base_folder
        pathlib.Path(folder_name).mkdir(exist_ok=True)
        doy = curr_date.strftime("%j")
        yearstr = curr_date.strftime("%Y")
        fs = fsspec.filesystem("s3", anon=True)
        urls = [
            "s3://" + f
            for f in fs.glob(
                "s3://noaa-goes16/ABI-L1b-RadF/{1}/{0}/*/*C{2:02d}*.nc".format(
                    doy, yearstr, channel
                )
            )
        ]
        _ = [gen_json(u, folder_name) for u in urls]
