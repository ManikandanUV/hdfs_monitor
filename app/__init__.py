import inotify.adapters
import settings
import zmq
from app import edits_parser, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = create_engine(settings.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=db)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:%s" % settings.ZMQ_PORT)


def get_monitor_list():
    session = Session()
    active_monitors = []
    active_monitors_qry = session.query(models.Monitors).filter(models.Monitors.is_active == True)
    if active_monitors_qry is None:
        return None
    for monitor in active_monitors_qry:
        active_monitors.append([monitor.dir_path, monitor.id])
    print(active_monitors)
    return active_monitors


def save_monitor_notification(details, message):
    session = Session()
    new_message = models.Messages(date_created=details['timestamp'],
                                  date_modified=details['timestamp'],
                                  dir_id=details['dir_id'],
                                  filename=details['filename'],
                                  message=message)
    session.add(new_message)
    session.commit()


def _main():
    i = inotify.adapters.Inotify()
    i.add_watch(settings.EDITS_LOC.encode('UTF-8'))

    try:
        for event in i.event_gen():
            if event is not None:
                # print(event)
                (header, type_names, watch_path, filename) = event
                if ('IN_MOVED_TO' in type_names) and ('edits' in filename.decode('UTF-8')):
                    print('New Edits File Created! Initiating Workflow!')
                    edits_parser.edits_to_xml(filename.decode('UTF-8'))
                    newfiles = edits_parser.get_new_file_names()
                    monitors = get_monitor_list()
                    matches = edits_parser.check_if_monitored(newfiles, monitors)
                    for match in matches:
                        message = "<{}>|{}|{}|{}".format(match['dir_id'],
                                                             match['filename'],
                                                             match['fullpath'],
                                                             match['timestamp'])
                        print(message)
                        save_monitor_notification(match, message)
                        socket.send_string(message)

    finally:
        i.remove_watch(settings.EDITS_LOC.encode('UTF-8'))


if __name__ == '__main__':
    _main()
