from subprocess import call
from lxml import etree
#from settings import EDITS_LOC

edit_location = '/data/hadoop/hdfs/namenode/current/'

def edits_to_xml(editfile):
    print("parsing editfile" + editfile)
#    call(['hdfs', 'oev', "-i", EDITS_LOC + editfile, "-o", "test.xml"])
    call(['hdfs', 'oev', "-i", edit_location + editfile, "-o", "test.xml"])
    call(['ls', '-l'])

def get_new_file_names():
    edits = etree.parse('test.xml')
    root = edits.getroot()
    newfileops = []
    for record in root:
        if (record.find('OPCODE') is not None
            and record.find('OPCODE').text == 'OP_ADD'):
            newfileops.append(record.find(".//PATH").text)
    return(newfileops)

def check_if_monitored(paths):
    monitored = ['user/mramakri']
    matches = []
    for dir in monitored:
        for newfilepath in paths:
            if dir in newfilepath:
                matches.append('Monitored directory match!\n Monitor: ' + dir + '\n Match: ' + newfilepath)
    return(matches)

if __name__ == "__main__":
    print("Executing Test case")
    edits_to_xml('edits_0000000000027806863-0000000000027806924')
    newfiles = get_new_file_names()
    print(newfiles)
    matches = check_if_monitored(newfiles)
    for match in matches:
        print(match)

