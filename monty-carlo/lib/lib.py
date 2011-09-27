def init_parallel(servers=()):
    """
    Initializes a parallel python session
    """
    import sys
    import pp
    
    ppservers = servers
    if len(sys.argv) > 1:
        ncpus = int(sys.argv[1])
        # Creates jobserver with ncpus workers
        job_server = pp.Server(ncpus, ppservers=ppservers)
    else:
        # Creates jobserver with automatically detected number of workers
        job_server = pp.Server(ppservers=ppservers)
    
    if print_enable:
        print "Parallel Python is configured to work with", job_server.get_ncpus(), "workers"
    

def push_job(job):
    pass
        