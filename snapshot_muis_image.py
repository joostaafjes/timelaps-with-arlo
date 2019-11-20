from arlo import Arlo
import os
from time import gmtime, strftime
import time

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
        # Tells the Arlo basestation to trigger a snapshot on the given camera.
        # This snapshot is not instantaneous, so this method waits for the response and returns the url
        # for the snapshot, which is stored on the Amazon AWS servers.
        snapshot_url = arlo.TriggerFullFrameSnapshot(basestations[0], camera)

        datetime = strftime("%Y%m%d_%H%M%S", gmtime())
        directory = './timelaps/' + camera['deviceName'] + '/'

        # create dir if not exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        # This method requests the snapshot for the given url and writes the image data to the location specified.
        # In this case, to the current directory as a file named "snapshot.jpg"
        # Note: Snapshots are in .jpg format.
        arlo.DownloadSnapshot(snapshot_url, directory + datetime + '.jpg')

        time.sleep(20)

except Exception as e:
    print(e)