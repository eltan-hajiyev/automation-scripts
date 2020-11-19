# Generate liquibase changelog
 liquibase --driver=oracle.jdbc.OracleDriver --classpath=ojdbc7.jar --changeLogFile=db.changelog.yaml --url="jdbc:oracle:thin:@host:1521/EX" --username=username --password=password generateChangeLog


# Split changelog
# Please type 'Author name' and 'File name'! Supports only 'yaml' file.
-a : Author name. Required.
-l : Generated change log file name. Default value: './changelogfolder'
-d : Directory for splited files. Default value: 'db.changelog.yaml'

Example: changeset-split.py -a AuthorName -l db.changelog.yaml -d ./changelogfolder
