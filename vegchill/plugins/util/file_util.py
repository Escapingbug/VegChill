"""file utils

Mostly copied from project GEF.
"""
import os
try:
    import gdb
except:
    pass


def gdb_download_file(veg, target, local_path, cached=False):
    """downloads a file into local file system

    Downloaded file will be in local_path

    Args:
        veg: vegchill main object
        target: target to download
        local_path: path to download, if local_path is directory, file will be
                    downloaded at local_path/target, else will be just local_path.
        cached: if a file already downloaded, don't do that again

    Returns:
        path of downloaded file, None if failed

    """
    try:
        if os.path.isdir(local_path):
            local_path = os.path.sep.join(local_path, target)

        if cached and os.access(local_path, os.R_OK):
            return local_path

        dirname = os.path.dirname(local_path)
        if os.path.exists(dirname):
            os.makedirs(dirname)
        gdb.execute('remote get %s %s' % (target, local_path))
        return local_path
    except gdb.error:
        veg.err('unable to download file %s to %s' % (target, local_path))
    except Exception as e:
        veg.err('download file failed with %s' % e) 
    return None


def gdb_is_remote():
    return 'remote' in gdb.execute('maintenance print target-stack', to_string=True)


def gdb_get_pid():
    """Returns the pid of the debuggee process
    """
    return gdb.selected_inferior().pid
    

def gdb_get_file_path(veg):
    """Returns the local absolute path currently debugged.

    Args:
        veg: vegchill main object

    Returns:
        debuggee file path, None if unable to know

    """
    tempdir = veg.environ['tempdir']
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

    filename = gdb.current_progspace().filename
    if gdb_is_remote():
        # maybe local remote target
        if filename is None:
            pid = gdb_get_pid()
            if pid > 0:
                temp_path = '%s/%d/executable' % (tempdir, pid)
                return gdb_download_file(
                    veg, 
                    '/proc/%d/exe' % pid,
                    temp_path,
                    cached=True
                )

            return None
        elif filename.startswith('target:'):
            # remote target
            fname = filename[len('target:'):]
            temp_path = '%s/%s' % (tempdir, fname)
            return gdb_download_file(veg, fname, fname, cached=True)
    else:
        if filename is not None:
            return filename

        # try get path from info proc
        for x in gdb.execute('info proc', to_string=True).splitlines():
            if x.startswith('exe = '):
                return x.split(' = ')[1].replace("'", '')
        return None
