from subprocess import DEVNULL, CalledProcessError
from unittest.mock import patch

from dashtools.docker.dockerUtils import _check_docker_installed, _write_dockerfile


@patch("dashtools.docker.dockerUtils.subprocess.check_output")
def test_check_docker_installed_returns_false_when_docker_not_installed(mock_check_output):
    mock_check_output.side_effect = CalledProcessError(1, "docker --help")
    assert _check_docker_installed() == False


@patch("dashtools.docker.dockerUtils.subprocess.check_output")
def test_check_docker_installed_returns_true_when_nothing_raised(mock_check_output):
    assert _check_docker_installed() == True


@patch("dashtools.docker.dockerUtils.subprocess.check_output")
def test_check_docker_installed_calls_check_output(mock_check_output):
    _check_docker_installed()
    mock_check_output.assert_called_with(
        'docker --help', shell=True, stderr=DEVNULL)


@patch("dashtools.docker.dockerUtils.os.path.relpath", return_value="./mocked/rel/path")
@patch("dashtools.docker.dockerUtils.fileUtils", return_value="./mocked/app/root")
def test_write_dockerfile(mocked_fileUtils, mocked_rel_path, tmp_path):
    _write_dockerfile(root_dir="some/root/dir", destination_dir=tmp_path)
    with open(tmp_path / "Dockerfile", "r") as f:
        test_result = f.read()

    expected = """FROM python:3.9-slim
            RUN addgroup --gid 1001 --system dash && \
                adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group dash
            WORKDIR /app
            COPY --chown=dash:dash requirements.txt ./requirements.txt
            RUN pip install -r requirements.txt
            USER dash
            COPY --chown=dash:dash . ./
            CMD gunicorn -b 0.0.0.0:80 ./mocked/rel/path.app:server"""

    assert test_result == "".join(
        [line.strip() + "\n" for line in expected.split("\n")])
