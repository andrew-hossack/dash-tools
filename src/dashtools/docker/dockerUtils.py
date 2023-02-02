'''
 # @ Author: Andrew Hossack
 # @ Create Time: 2022-06-19 12:25:30
'''


import os
import subprocess
import webbrowser

from dashtools.deploy import fileUtils
from dashtools.deploy.deployHeroku import prompt_user_choice


def _check_docker_installed() -> bool:
    """
    Check if docker is installed.

    :return: True if docker is installed, False otherwise.
    """
    try:
        subprocess.check_output(
            f'docker --help',
            shell=True,
            stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def _write_dockerfile(root_dir: os.PathLike, destination_dir: os.PathLike) -> None:
    """
    Write a Dockerfile to the specified directory.

    :param root_dir: The root directory of the project.
    :param destination_dir: The directory to write the Dockerfile to.
    """
    # Get relative path of app.py file
    rel_path = os.path.relpath(fileUtils.app_root_path(root_dir), root_dir)
    # TODO test if app.py file changes locations
    contents = f"""FROM python:3.9-slim
            RUN addgroup --gid 1001 --system dash && \
                adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group dash
            WORKDIR /app
            COPY --chown=dash:dash requirements.txt ./requirements.txt
            RUN pip install -r requirements.txt
            USER dash
            COPY --chown=dash:dash . ./
            CMD gunicorn -b 0.0.0.0:80 {rel_path}.app:server"""
    with open(os.path.join(destination_dir, 'Dockerfile'), 'w') as f:
        for line in contents.split('\n'):
            f.write(line.strip() + '\n')


def create_image(image_name: str, cwd: os.PathLike) -> None:
    """
    Create a new docker image for the current project.

    :param destination_parent_dir: The directory to create the image in.
    :param image_name: The name of the app.
    :param cwd: The current working directory.
    """
    # 1. Check if docker is installed
    if not _check_docker_installed():
        print('dashtools: docker: error: Docker is not installed!')
        if prompt_user_choice('dashtools: Open Docker website?'):
            webbrowser.open('https://docs.docker.com/get-docker/')
        exit(1)

    # 2. Check if requirements.txt exists in image directory
    if not fileUtils.check_file_exists(cwd, 'requirements.txt'):
        print('dashtools: docker: error: No requirements.txt file found!')
        if prompt_user_choice('dashtools: Generate requirements.txt file?'):
            fileUtils.create_requirements_txt(cwd)
        else:
            exit(
                'dashtools: docker: error: A requirements.txt file is required to create an image!')
    else:
        print('dashtools: docker: init: Requirements file found')
        fileUtils.create_requirements_txt(
            cwd, update=True)

    # 3. Check if Dockerfile exists in image directory
    if not fileUtils.check_file_exists(cwd, 'Dockerfile'):
        print('dashtools: docker: error: No Dockerfile found')
        if prompt_user_choice('dashtools: Create a Dockerfile?'):
            _write_dockerfile(cwd, cwd)
        else:
            print('dashtools: docker: error: Dockerfile needed to create image')
            exit(1)

    # 4. Build image
    print(f'dashtools: docker: init: Building image {image_name}')
    try:
        subprocess.run(
            f'docker build -t {image_name} .',
            shell=True,
            check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        print('dashtools: docker: error: Failed to build image')
        exit(1)

    print(f'dashtools: docker: init: Image {image_name} created!')
    print(
        f'dashtools: Run `docker run -p 8080:80 {image_name}` to start the image on http://localhost:8080')
    print('dashtools: Run `docker container ls -a` to see all images')
