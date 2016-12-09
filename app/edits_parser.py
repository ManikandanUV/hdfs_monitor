from subprocess import call
from lxml import etree
import datetime
from settings import EDITS_LOC

edit_location = '/data/hadoop/hdfs/namenode/current/'


def edits_to_xml(editfile):
    print("parsing editfile" + editfile)
    call(['hdfs', 'oev', "-i", EDITS_LOC + editfile, "-o", "test.xml"])
    # call(['hdfs', 'oev', "-i", edit_location + editfile, "-o", "test.xml"])


def get_new_file_names():
    edits = etree.parse('test.xml')
    root = edits.getroot()
    newfileops = []
    for record in root:
        if record.find('OPCODE') is not None and record.find('OPCODE').text == 'OP_ADD':
            newfileops.append({'path': record.find(".//PATH").text,
                               'timestamp': int(record.find(".//MTIME").text)})
    return newfileops


def check_if_monitored(newfiles_list, monitors_list):
    dir_matches = []
    for mon_dir in monitors_list:
        for file in newfiles_list:
            if mon_dir[0] in file['path']:
                dir_match = {'dir_name': mon_dir[0],
                             'dir_id': mon_dir[1],
                             'fullpath': file['path'],
                             'filename': file['path'].replace(mon_dir[0], ""),
                             'timestamp': datetime.datetime.fromtimestamp(file['timestamp'] / 1000.0)}
                dir_matches.append(dir_match)

    return dir_matches


if __name__ == "__main__":
    print("Executing Test case")
    edits_to_xml('edits_0000000000027806863-0000000000027806924')
    newfiles = get_new_file_names()
    print(newfiles)
    matches = check_if_monitored(newfiles)
    for match in matches:
        print(match)
