import sys,os,getopt
import traceback
import commands
sys.path.append("/DG/activeRelease/lib/python_lib/")

from pythonodbcdriver import pyodbcdriver ### Using pyodbc to get GG connection handle
import FileLogger

LOG_FILE_PATH = '/DGlogs/GGExecuteQuery.py
logger = FileLogger.logger(LOG_FILE_PATH);
log = logger.getlogger();
connectionObject=None

def Usage():
    print '  This script would insert records in DefaultCacheConfigurationProfile Table of GGain provided no record is present for id=1'
    print '  \n'
    print '  USAGE : python /DG/activeRelease/GGExecuteQuery.py'
    sys.exit(2)

def InsertDefaultCacheConfigurationProfile():
    DefaultCConfigCntQry = 'select count(*) from "DefaultCacheConfigurationProfile".DefaultCacheConfigurationProfile where id=1'
    IdCntDefaultCConfig = connectionObject.execute(DefaultCConfigCntQry,1)
    if IdCntDefaultCConfig == -1:
       log.error("Failed to Execute Query %s"%(DefaultCConfigCntQry))
       sys.exit(1)

    if int(IdCntDefaultCConfig[1][0][0]) == 0:
        InsertDefaultCConfigQry = "insert into \"DefaultCacheConfigurationProfile\".DefaultCacheConfigurationProfile(id,cacheMode,atomicityMode,writeSynchronizationMode,backups,statisticsEnabled) Values(1,'PARTITIONED','TRANSACTIONAL','FULL_SYNC',1,true)"
        Status = connectionObject.execute(InsertDefaultCConfigQry)
        if Status == -1:
           log.error("Failed to Execute Query %s"%(InsertDefaultCConfigQry))
           sys.exit(1)
        log.info("No record present for id=1. Successfully inserted entry into DefaultCacheConfigurationProfile.DefaultCacheConfigurationProfile")
        print "No record present for id=1. Successfully inserted entry into DefaultCacheConfigurationProfile.DefaultCacheConfigurationProfile"
    else:
        log.info("Record for id=1 already exists. No insertion in DefaultCacheConfigurationProfile.DefaultCacheConfigurationProfile")
        print "Record for id=1 already exists. No insertion in DefaultCacheConfigurationProfile.DefaultCacheConfigurationProfile"

def InsertOIDCClientIDScopeInfo():
    OIDCClientIDScopeInfoChkList=['ptths','pttwds']
    InsertOIDCClientIDPtthsScopeInfo="insert into DG.OIDC_CLIENT_ID_AND_SCOPE_INFO (OIDC_CLIENT_TYPE,OIDC_SVR_CLIENT_ID,OIDC_SVR_SCOPE) values ('*','ptths','openid 3gpp:mcptt:ptt_server 3gpp:mcptt:key_management_server 3gpp:mcptt:config_management_server 3gpp:mcptt:group_management_server')"
    InsertOIDCClientIDPttwdsScopeInfo="insert into DG.OIDC_CLIENT_ID_AND_SCOPE_INFO (OIDC_CLIENT_TYPE,OIDC_SVR_CLIENT_ID,OIDC_SVR_SCOPE) values ('3','pttwds','openid 3gpp:mcptt:ptt_server 3gpp:mcptt:key_management_server 3gpp:mcptt:config_management_server 3gpp:mcptt:group_management_server')"
    for OIDCSvrClientID,InsertOIDCClientTypeInfoQry in zip(OIDCClientIDScopeInfoChkList,[InsertOIDCClientIDPtthsScopeInfo,InsertOIDCClientIDPttwdsScopeInfo]):
        OIDCSvrClientIDCntQry = "select count(*) from DG.OIDC_CLIENT_ID_AND_SCOPE_INFO where OIDC_SVR_CLIENT_ID='"+str(OIDCSvrClientID)+"'"
        OIDCSvrClientIDCount = connectionObject.execute(OIDCSvrClientIDCntQry,1)
        if  OIDCSvrClientIDCount == -1:
            log.error("Failed to Execute Query %s"%(OIDCSvrClientIDCntQry))
            sys.exit(1)
        if int(OIDCSvrClientIDCount[1][0][0]) == 0:
            Status = connectionObject.execute(InsertOIDCClientTypeInfoQry)
            if Status == -1:
                log.error("Failed to Execute Query %s"%(InsertOIDCClientTypeInfoQry))
                sys.exit(1)
            log.info("No record present for OIDC_SVR_CLIENT_ID="+OIDCSvrClientID+" in DG.OIDC_CLIENT_ID_AND_SCOPE_INFO. Successfully inserted entry into DG.OIDC_CLIENT_ID_AND_SCOPE_INFO")
            print "No record present for OIDC_SVR_CLIENT_ID="+OIDCSvrClientID+". Successfully inserted entry into DG.OIDC_CLIENT_ID_AND_SCOPE_INFO"
        else:
            log.info("Record for OIDC_SVR_CLIENT_ID="+OIDCSvrClientID+" in DG.OIDC_CLIENT_ID_AND_SCOPE_INFO already exists. No insertion in DG.OIDC_CLIENT_ID_AND_SCOPE_INFO")
            print "Record for OIDC_SVR_CLIENT_ID="+OIDCSvrClientID+" already exists. No insertion in DG.OIDC_CLIENT_ID_AND_SCOPE_INFO"


def InsertOIDCClientRealmMapping():
    OIDCRealmNameChkList=['wds','mcptt','customerdashboard','tpusers']
    InsertOIDCClientWdsRealmName="insert into DG.OIDC_CLIENT_REALM_MAPPING (OIDC_CLIENT_TYPE,OIDC_REALMNAME,ADMIN_REALM_URL) values ('3','wds','http://prod-Keycloak-V1.query.kodiakptt.com:8200/auth/admin/realms/wds')"
    InsertOIDCClientMcPttRealmName="insert into DG.OIDC_CLIENT_REALM_MAPPING (OIDC_CLIENT_TYPE,OIDC_REALMNAME,ADMIN_REALM_URL) values ('*','mcptt','http://prod-Keycloak-V1.query.kodiakptt.com:8200/auth/admin/realms/mcptt')"
    InsertOIDCClientCusDashBoardRealmName="insert into DG.OIDC_CLIENT_REALM_MAPPING (OIDC_CLIENT_TYPE,OIDC_REALMNAME,ADMIN_REALM_URL) values ('101','customerdashboard','http://prod-Keycloak-V1.query.kodiakptt.com:8200/auth/admin/realms/customerdashboard')"
    InsertOIDCClientTpUsrsRealmName="insert into DG.OIDC_CLIENT_REALM_MAPPING (OIDC_CLIENT_TYPE,OIDC_REALMNAME,ADMIN_REALM_URL) values ('102','tpusers','http://prod-Keycloak-V1.query.kodiakptt.com:8200/auth/admin/realms/tpusers')"

    for OIDCRealmName,InsertDefaultCConfigQry in zip(OIDCRealmNameChkList,[InsertOIDCClientWdsRealmName,InsertOIDCClientMcPttRealmName,InsertOIDCClientCusDashBoardRealmName,InsertOIDCClientTpUsrsRealmName]):
        OIDCRealmCntQry = "select count(*) from DG.OIDC_CLIENT_REALM_MAPPING where OIDC_REALMNAME='"+str(OIDCRealmName)+"'"
        OIDCRealmCount = connectionObject.execute(OIDCRealmCntQry,1)
        if  OIDCRealmCount == -1:
            log.error("Failed to Execute Query %s"%(OIDCRealmCntQry))
            sys.exit(1)
        if int(OIDCRealmCount[1][0][0]) == 0:
            Status = connectionObject.execute(InsertDefaultCConfigQry)
            if Status == -1:
                log.error("Failed to Execute Query %s"%(InsertDefaultCConfigQry))
                sys.exit(1)
            log.info("No record present for OIDC_REALMNAME="+OIDCRealmName+". Successfully inserted entry into OIDC_CLIENT_REALM_MAPPING")
            print "No record present for OIDC_REALMNAME="+OIDCRealmName+". Successfully inserted entry into OIDC_CLIENT_REALM_MAPPING"
        else:
            log.info("Record for OIDC_REALMNAME="+OIDCRealmName+" already exists. No insertion in OIDC_CLIENT_REALM_MAPPING")
            print "Record for OIDC_REALMNAME="+OIDCRealmName+" already exists. No insertion in OIDC_CLIENT_REALM_MAPPING"


def CleanUPGGainhandles(flag):
    if(connectionObject!=None and connectionObject!=-1):
        connectionObject.close_connection()
        log.info("Connection Object Closed.")
    log.info("Logger closed.")
    logger.closeLog();
    sys.exit(flag)

################################ Main() ############################################################################################
GG_FQDN=commands.getoutput("egrep '^GG_FQDN=' /DG/activeRelease/dat/CommonConfig.properties | awk -F'=' '{print $2}'").strip()
log.info("GG_FQDN : "+GG_FQDN)
GG_SQL_PORT=str(commands.getoutput("egrep '^GG_SQL_PORT=' /DG/activeRelease/dat/CommonConfig.properties | awk -F'=' '{print $2}'")).strip()
log.info("GG_SQL_PORT : "+GG_SQL_PORT)
GG_IP=commands.getoutput("egrep '^SERVICEPLANE_IP_ADDRESSES=' /DG/activeRelease/dat/containerinit.ini | awk -F'=' '{print $2}'").strip()
log.info("GG_IP : "+GG_IP)

IPArr = (GG_FQDN,GG_IP)
Flag = 1

for IPFQDN in IPArr:
    connectionString = IPFQDN+":"+GG_SQL_PORT
    log.info("Connection String : "+connectionString)

    connectionObject=pyodbcdriver(connectionString,log)
    status,message=connectionObject.get_connection()
    log.info(message)

    if status == 0:
       Flag = 0
       break;

if Flag == 1:
    log.error("IP["+GG_IP+"] or GG_FQDN["+GG_FQDN+"]")
    sys.exit(1)

#--------------------------------------------- Insert in Default cache configuration and CleanUp Conn. Handles ----------------------
InsertDefaultCacheConfigurationProfile()
InsertOIDCClientRealmMapping()
InsertOIDCClientIDScopeInfo()
CleanUPGGainhandles(0)
## Modified on 6/6/2018 12:12
