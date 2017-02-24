import inotify.adapters
import settings
import requests
import zmq
from app import edits_parser, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# testcode
import datetime

# testcode

db = create_engine(settings.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=db)

context = zmq.Context()
socket = context.socket(zmq.PUB)


# socket.bind("tcp://127.0.0.1:%s" % settings.ZMQ_PORT)


def get_monitor_list():
    url = settings.API_SERVER_URI + "/get_monitors"
    active_monitors = requests.get(url)
    return active_monitors.json()


def save_monitor_notification(details, message):
    url = settings.API_SERVER_URI + "/log_message"
    data = {"timestamp": str(details['timestamp']),
            "dir_id": details['dir_id'],
            "filename": details['filename'],
            "message": message
            }
    log_message = requests.post(url, json=data)
    return log_message


def _main():
    i = inotify.adapters.Inotify()
    print('Adding watch ' + settings.EDITS_LOC)
    i.add_watch(settings.EDITS_LOC.encode('UTF-8'))
    print('Watch added successfully')

    try:
        print('Begin Monitoring')
        for event in i.event_gen():
            print('Raw event')
            print(event)
            if event is not None:
                print(event)
                (header, type_names, watch_path, filename) = event
                if ('IN_MOVED_TO' in type_names) and ('edits' in filename.decode('UTF-8')):
                    print('New Edits File Created! Initiating Workflow!')
                    edits_parser.edits_to_xml(filename.decode('UTF-8'))
                    newfiles = edits_parser.get_new_file_names()
                    monitors = get_monitor_list()
                    print(monitors)
                    if monitors is None:
                        continue
                    matches = edits_parser.check_if_monitored(newfiles, monitors)
                    for match in matches:
                        message = "<{}>|{}|{}|{}".format(match['dir_id'],
                                                             match['filename'],
                                                             match['fullpath'],
                                                             match['timestamp'])
                        print(message)
                        save_event = save_monitor_notification(match, message)
                        socket.send_string(message)

    finally:
        i.remove_watch(settings.EDITS_LOC.encode('UTF-8'))


if __name__ == '__main__':
    # _main()
    print(get_monitor_list())
    sample_message = "<3>|Test|" + str(datetime.datetime.now())
    sample_details = {"timestamp": str(datetime.datetime.now()),
                      "dir_id": 3,
                      "filename": "Test",
                      "message": sample_message}
    test_save = save_monitor_notification(sample_details, sample_message)
    print(test_save.status_code, test_save.json())
