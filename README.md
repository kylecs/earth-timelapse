# earth-timelapse
Uses the NASA Earth Image API to get images from a specified location over a specified time interval and create a GIF of the resulting timelapse.

For example, here is a construction site near my university over the last 2 years:
![Timelapse GIF](http://i.imgur.com/8Cy22bB.gif)
# Installation
To install this program on a debian based system, clone the repository:

`git clone https://github.com/kylecs/earth-timelapse.git`

Then run the installation script to download dependencies:

`sudo ./install.sh`

# Running
To make a simple timelapse:
`python earth-timelapse.py --latitude 38.897 --longitude -77.037`

By default, all images are taken from the beginning of 2015 to the current day, and images that recieve a NASA cloud_score of over 0.1 are ommitted.

Use `--start YYYY-MM-DD` and `--end YYYY-MM-DD` to specify custom start and end dates.

Use `--clouds true` to include pictures with clouds

Use `--cloudscore k` to include pictures with a NASA cloud_score below k.

# NASA API Key
By default, the NASA DEMO_KEY will be used which allows 50 API requests per day. For more requests, sign up for an API key at [api.nasa.gov](https://api.nasa.gov/#apply-for-an-api-key). The key is granted and usable instantly.

To use your API key, use the parameter

`--apikey YOUR_KEY`

If you don't want to keep including your API key in the commands, you can create a file `api-key` and paste your API key there.
