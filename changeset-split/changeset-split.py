#!python
# Generate liquibase changelog
#liquibase --driver=oracle.jdbc.OracleDriver --classpath=ojdbc7.jar --changeLogFile=db.changelog.yaml --url="jdbc:oracle:thin:@host:1521/EX" --username=username --password=password generateChangeLog

import yaml
import re
import os 
import sys
from datetime import date

directoryForSplitedFiles = "./changelogfolder"
changeLogFileYaml = "db.changelog.yaml"
authorName = ""

try:
    v1 = ""
    for v in sys.argv:
        if v1 == "-a":
            authorName = v
        elif v1 == "-l":
            changeLogFileYaml = v
        elif v1 == "-d":
            directoryForSplitedFiles = v
        v1 = v    
except:
    exit()

if not authorName:
    print("Please type 'Author name' and 'File name'! Supports only 'yaml' file.")
    print("-a : Author name. Required.")
    print(f"-l : Generated change log file name. Default value: '{directoryForSplitedFiles}'")
    print(f"-d : Directory for splited files. Default value: '{changeLogFileYaml}'")
    print(f"Example: changeset-split.py -a AuthorName -l {changeLogFileYaml} -d {directoryForSplitedFiles}")
    exit();

def getValue(obj, keys):
    try:
        for k in keys:
            if obj[k]:
                obj = obj[k]
        return obj
    except:
        return ''


def getName(e):
    prefix = date.today().strftime("%Y%m%d") + '-'
    t = getValue(e, ['changeSet', 'changes', 0, 'createTable', 'tableName'])
    if t:
        return prefix + "010-create-table-" + t

    t = getValue(e, ['changeSet', 'changes', 0, 'createIndex', 'tableName'])
    if t:
        return prefix + "010-create-table-" + t
        
    t = getValue(e, ['changeSet', 'changes', 0, 'addUniqueConstraint', 'tableName'])
    if t:
        return prefix + "010-create-table-" + t
        
    t = getValue(e, ['changeSet', 'changes', 0, 'addForeignKeyConstraint', 'baseTableName'])
    if t:
        return prefix + "010-create-table-" + t

    t = getValue(e, ['changeSet', 'changes', 0, 'createSequence', 'sequenceName'])
    if t:
        return prefix + "030-create-sequence"

    t = getValue(e, ['changeSet', 'changes', 0, 'createView', 'viewName'])
    if t:
        return prefix + "040-create-view-" + t
        
    t = getValue(e, ['changeSet', 'changes', 0, 'createProcedure', 'procedureName'])
    if t:
        return prefix + "050-create-procedure-" + t

    return ""


with open(changeLogFileYaml, 'r') as stream:
    os.makedirs(directoryForSplitedFiles, exist_ok=True)
    
    changeSetList = yaml.safe_load(stream)
    
    changeSetListTmp = {}
    for e in changeSetList['databaseChangeLog']:
        fileName = getName(e).replace("_", "-").lower()
        if not fileName:
            print("Error: Unexpected changeSet")
            break;

        if (not getValue(changeSetListTmp, [fileName])):
            changeSetListTmp[fileName] = []
        e['changeSet']['author'] = authorName
        changeSetListTmp[fileName].append(e)

    for k in changeSetListTmp:
        f = open(directoryForSplitedFiles + "/" + k + ".yaml", "w")
        f.write("databaseChangeLog:\n")
        f.write(yaml.dump(changeSetListTmp[k], sort_keys=False))
        f.close()

