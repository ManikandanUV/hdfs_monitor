from subprocess import call
import xml.etree.ElementTree as ET
#from settings import EDITS_LOC

edit_location = '/data/hadoop/hdfs/namenode/current/'

def edits_to_xml(editfile):
    print("parsing editfile" + editfile)
#    call(['hdfs', 'oev', "-i", EDITS_LOC + editfile, "-o", "test.xml"])
    call(['hdfs', 'oev', "-i", edit_location + editfile, "-o", "test.xml"])
    call(['ls', '-l'])

def import_edits_xml():
    edits = ET.parse('test.xml')
    root = edits.getroot()
    for record in root:
        for opcode in record.iter('OPCODE'):
            if opcode.text == 'OP_ADD':
                    print(record.itertext())

if __name__ == "__main__":
    print("Executing Test case")
    edits_to_xml('edits_0000000000027754629-0000000000027754766')
    import_edits_xml()

