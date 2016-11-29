import inotify.adapters
import edits_parser

def _main():
    i = inotify.adapters.Inotify()
    i.add_watch(b'/data/hadoop/hdfs/namenode/current/')

    try:
        for event in i.event_gen():
            if event is not None:
                print(event)
                (header, type_names, watch_path, filename) = event
                if ('IN_MOVED_TO' in type_names) and ('edits' in filename.decode('UTF-8')):
                    print('New Edits File Created! Initiating Workflow!')
                    edits_parser.edits_to_xml(filename.decode('UTF-8'))
                    newfiles = edits_parser.get_new_file_names()
                    matches = edits_parser.check_if_monitored(newfiles)
                    for match in matches:
                        print(match)
                    
    finally:
        i.remove_watch(b'/data/hadoop/hdfs/namenode/current/')

if __name__ == '__main__':
    _main()
