
import sys
import time
from SCSFileObserver import SCSFileObserver, SCSFileChangeLog

def main(path):
    print "Running SCS client"

    observer = SCSFileObserver(path)
    observer.run()

    try:
        while True:
            time.sleep(2)
            observer.changelog.printChanges()
            # print observer.changelog.getChangesPerFile()
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == '__main__':
    main("example_data/")


