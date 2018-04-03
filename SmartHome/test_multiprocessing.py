from multiprocessing import Process
# import FAKEGpio


def print_func(continent='Asia'):
    print('The name of continent is : ', continent)
    # print(proc.name())

def status_table():
    print("%d) Process name: %s PID#:%d Alive: %s" %(i, proc.name, proc.pid, proc.is_alive()))



if __name__ == "__main__":  # confirms that the code is under main function
    names = ['America', 'Europe', 'Africa']
    procs = []
    proc = Process(target=print_func)  # instantiating without any argument
    procs.append(proc)
    proc.start()

    # instantiating process with arguments
    for i,name in enumerate(names):
        # print(name)
        proc = Process(target=print_func, args=(name,),name='process_'+name)
        procs.append(proc)
        proc.start()
        status_table()


    # complete the processes
    for proc in procs:
        proc.join()
        status_table()
