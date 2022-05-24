'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-05-23 00:08:07
 # @ Handle running the app
'''


import os
from dashtools.deploy.fileUtils import verify_procfile, check_file_exists


def run_app(root_path: os.PathLike):
    '''
    Look for a Procfile to run the app, else recursive search for app.py file
    # TODO verify this works for all systems. Not sure if python3 is correct cmd
    '''
    # Check Procfile exists
    if check_file_exists(root_path, 'Procfile'):
        # Look for a Procfile to run the app, else recursive search for app.py file
        proc = verify_procfile(root_path)
        if proc['valid']:
            try:
                print('dashtools: Running From Procfile')
                os.chdir(root_path)
                # NOTE Not too sure if python3 is the right command for all systems, it might need to be changed
                os.system(
                    f'python3 -m {proc["dir"]}.{proc["module"].replace(".py","")}')
            except Exception as e:
                print(e)
    else:
        # Find app.py file in the root_path directory
        for root, dirs, files in os.walk(root_path):
            if 'app.py' in files:
                break
        try:
            print(
                f'dashtools: Running From {root + "/" if root else ""}app.py')
            os.chdir(root)
            # NOTE Not too sure if python3 is the right command for all systems, it might need to be changed
            os.system(f'python3 app.py')
        except Exception as e:
            print(e)
    return
