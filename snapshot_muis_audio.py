from Arlo import Arlo
import os
from time import gmtime, strftime
import time

from subprocess import call

USERNAME = os.environ.get('ARLO_USERNAME')
PASSWORD = os.environ.get('ARLO_PASSWORD')

try:
    # Instantiating the Arlo object automatically calls Login(), which returns an oAuth token that gets cached.
    # Subsequent successful calls to login will update the oAuth token.
    arlo = Arlo(USERNAME, PASSWORD)
    # At this point you're logged into Arlo.

    # Get the list of devices and filter on device type to only get the basestation.
    # This will return an array which includes all of the basestation's associated metadata.
    basestations = arlo.GetDevices('basestation')

    # Get the list of devices and filter on device type to only get the camera.
    # This will return an array which includes all of the camera's associated metadata.
    cameras = arlo.GetDevices('camera')

    for camera in list(filter(lambda camera: camera['deviceName'] == 'muis', cameras)):
        url = arlo.StartStream(basestations[0], camera)
        print(url)

        # Record the stream to a file named 'test.mp4'.
        # **Requires ffmpeg 3.4 or greater.**
        # For this example, I'm going to open ffmpeg.
        # Crucially important is the '-t' flag, which specifies a recording time. (See the ffmpeg documentation.)
        # This is just a crude example, but hopefully it will give you some ideas.
        # You can use any number of libraries to do the actual streaming. OpenCV or VLC are both good choices.
        # NOTE: This will print the output of ffmpeg to STDOUT/STDERR. If you don't want that, you will
        # need to pass additional arguments to handle those streams.

        datetime = strftime("%Y%m%d_%H%M%S", gmtime())
        directory = './timelaps/' + camera['deviceName'] + '/'

        # create dir if not exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        # video
        # call(['ffmpeg', '-re', '-i', url, '-t', '500', '-acodec', 'copy', '-vcodec', 'copy', 'test3.mp4'])
        # audio
        # call(['/usr/local/bin/ffmpeg', '-re', '-i', url, '-t', '590', '-vn', '-acodec', 'copy', '-vcodec', 'copy', directory + datetime + '.aac'])
        call(['/usr/local/bin/ffmpeg', '-re', '-i', url, '-t', '590', '-vn', '-acodec', 'libmp3lame', '-ac', '2', '-qscale:a', '4', '-ar', '48000', '-vcodec', 'copy', directory + datetime + '.mp3'])
        # ffmpeg -i video.mp4 -vn - acodec libmp3lame -ac 2 -qscale: a 4 -ar 48000 audio.mp3

        # Starting recording with a camera.
        # arlo.StartRecording(basestations[0], camera);

        # Wait for 4 seconds while the camera records. (There are probably better ways to do this, but you get the idea.)
        # time.sleep(300)

        # Stop recording.
        # arlo.StopRecording(camera);

        # Take the snapshot.
        # arlo.TakeSnapshot(camera['parentId'], camera['deviceId'], camera['xCloudId'],
        #                   camera['properties']['olsonTimeZone']);

        # Tells the Arlo basestation to trigger a snapshot on the given camera.
        # This snapshot is not instantaneous, so this method waits for the response and returns the url
        # for the snapshot, which is stored on the Amazon AWS servers.
        # snapshot_url = arlo.TriggerFullFrameSnapshot(basestations[0], camera)

        # datetime = strftime("%Y%m%d_%H%M%S", gmtime())
        # directory = './timelaps/' + camera['deviceName'] + '/'

        # create dir if not exists
        # if not os.path.exists(directory):
        #     os.makedirs(directory)

        # This method requests the snapshot for the given url and writes the image data to the location specified.
        # In this case, to the current directory as a file named "snapshot.jpg"
        # Note: Snapshots are in .jpg format.
        # arlo.DownloadSnapshot(snapshot_url, directory + datetime + '.jpg')

        # time.sleep(20)

except Exception as e:
    print(e)