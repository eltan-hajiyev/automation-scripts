# Generate liquibase changelog
#liquibase --driver=oracle.jdbc.OracleDriver --classpath=ojdbc7.jar --changeLogFile=db.changelog.yaml --url="jdbc:oracle:thin:@host:1521/EX" --username=username --password=password generateChangeLog
