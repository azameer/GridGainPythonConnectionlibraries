# GridGainPythonConnectionlibraries
This library would enable us to connect to Grid Gain &amp; execute queries.

PREREQUISITES: pypyodbc.py & pythonodbcdriver.py should be in same path of script execution. A few library dependencies need
to be removed before executing GGExecuteQuery.py script. DefaultCacheConfigurationProfile cache(schema) with "id,cacheMode,atomicityMode,
writeSynchronizationMode,backups,statisticsEnabled" coloumns needs to be created in Grid Gain prior to script execution.



USAGE: python /DG/activeRelease/GGExecuteQuery.py

