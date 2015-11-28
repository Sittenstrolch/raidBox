
import sys
import time
from SCSClient import SCSClient

def main(path):
    client = SCSClient(path)
    client.run()

    try:
        # keep the main thread running
        # terminate the application on CTRL+C
        while True:
            time.sleep(2.5)
            client.observer.changelog.printChanges()
            client.sync()
    except KeyboardInterrupt:
        client.stop()

if __name__ == '__main__':
    path = "files/"

    if len(sys.argv) > 1:
        path = sys.argv[1]

    main(path)


