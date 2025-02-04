Here are the steps required in order to prepare a dataset for OnePose.

1. Clone OpenSfM

```
git clone -b onepose --single-branch https://github.com/gfloros/OpenSfM.git
```

2. Create a folder inside the data folder and name it as you like.

```
mkdir data/my_awesome_project
```


3. Copy your video inside this folder and extract the frames from it. Pay special attention if your video has variable framerate. In that case, check the metadata for the average framerate and extract with that.

```
cp <whereever_i_have_my_video>/Frames.m4v data/my_awesome_project
cd data/my_awesome_project
mkdir images
ffmpeg -i Frames.m4v images/%04d.png 
# for variable framerates use this one
# ffmpeg -i Frames.m4v -r <avg_framerate> images/%04d.png 
```

4. In the folder `data/my_awesome_project` create a `config.yaml` with the following contents:

```
processes: 40                  # the number of cpu cores
matching_order_neighbors: 20   # number of ordered neighbors for pair selection
feature_process_size: 1024     # image size in which features are extracted
```

if the camera intrinsics are available you can pass them by creating the file `camera_models_overrides.json` with the following contents:

```
    {
        "all": {
            "projection_type": "perspective",
            "width": 1920,
            "height": 1080,
            "focal": 0.9,
            "k1": 0.0,
            "k2": 0.0,
        }
    }
```

5. Build the docker image. You can do that by running

```
make local
```

6. Enter the docker container by running

```
make bash
```

The root folder is mounted in the folder `/code` and the data folder in the folder `/data`.

Go to the `/code` folder and run

```
cd /code
python3 setup.py install
```

7. Now, you are ready to run the SfM pipeline. Once you have a folder `/data/my_awesome_project` that contains

    - a folder called `images` containing the video frames
    - a file called `config.yaml` with the parameters
    - optionally, a file called `camera_models_overrides.json` with the camera intrinsics

you can run

```
bin/opensfm_run_onepose /data/my_awesome_project
```

8. The files `ARposes.txt`, `Frames.txt` and `reconstruction.ply` will be output in the `/data/my_awesome_project` folder. You can exit the docker instance and access through your standard filesystem. The `reconstruction.ply` can then be loaded to [CloudCompare](https://www.danielgm.net/cc/) to find the coordinates required to compile the file `Box.txt`.

