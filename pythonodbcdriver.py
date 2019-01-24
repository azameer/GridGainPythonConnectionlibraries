import sys,os
sys.path.append('/DG/activeRelease/lib/python_lib/')
import pypyodbc as pyodbc

class pyodbcdriver:
        
        def __init__(self,IPString,log):
            #setting connection object variables
            self.IPString=IPString
            self.db_obj=None
            self.cursor=None
            self.retry_counter=0
            self.log = log
            
        def retry_count(self,retry_value):
            self.retry_counter=retry_value
            self.log.info("Retry Count : "+str(retry_value))
            
        def get_connection(self):
                conn_str = "DRIVER=/DG/activeRelease/GridGain/lib/libignite-odbc.so;ADDRESS="+self.IPString+"";
                self.log.info("CONNECTION STRING : "+conn_str);
                try:
                    self.db_obj = pyodbc.connect(conn_str)
                    self.log.info("Connection estabilished");
                except pyodbc.Error, err:
                    self.log.error("Connection Error : "+str(err));
                    return -1,str(err)
                self.cursor = self.db_obj.cursor()
                return 0,"Successfully Connected."
        
        def reconnect(self):
            self.log.info("Reconnecting:")
            for i in range(0,self.retry_counter):
                self.log.info("Reconnection : "+str(i+1))
                if(self.db_obj!=-1):
                    self.close_connection()
                    self.log.info("Connection Closed.")
                status = self.get_connection()
                self.log.info("Estabilishing Connection Again")
                if(status!=-1):
                    return;
            self.log.error("Retry count over. Failed to reconnect.")
            return -1

        def execute(self,query,output_flag=0):
                try:
                        self.cursor.execute(query)
                        if output_flag==1:
                            data_list=self.cursor.fetchall()
                            if(len(data_list)==0):
                                return -1,"No data in the table"
                            else:
                                return 0,data_list
                        return 0,"executed"
                except pyodbc.Error, err:
                        self.log.error("Execution error : "+str(err))
                        return -1,str(err)

        def close_connection(self):
                try:
                    if self.cursor:
                        self.cursor.close()
                        self.log.info("Cursor Closed.")
                
                    if self.db_obj:
                        self.db_obj.close()
                        self.log.info("DB Object Closed.")

                    self.db_obj=None
                    self.cursor=None
                except pyodbc.Error, err:
                        self.log.error("Disconnection Error : "+str(err))
                        return -1,str(err)
                self.log.info("Connection closed.")
