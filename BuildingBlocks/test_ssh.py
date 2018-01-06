import subprocess

def copy_remote_file(adress,path_source,file_source,path_target,file_target,ext='.csv'):
    
    adress='192.168.2.112'
    path_source='/home/guy/PythonProjects/'
    file_source='schedule'
    path_target=path_source
    file_target=path_target+file_source+'_'+adress

    result = subprocess.run(['scp','guy@%s'%adress+':'+path_source+file_source+'.csv',
    file_target+'.csv'],stdout=subprocess.PIPE)
    result.check_returncode()
    #cats_csv = result.stdout

if __name__ == "__main__":
        copy_remote_file()
