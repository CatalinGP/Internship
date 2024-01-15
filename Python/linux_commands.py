import subprocess
import shlex
import os


def bash_command_executor(func):
    def wrapper(self, *args, **kwargs):
        command = func(self, *args, **kwargs)
        return self.run_command(command)
    return wrapper


class LinuxCommander:
    """
    A class in Python to encapsulate basic Linux commands.
    """
    def __init__(self):
        self.git_bash_executable = "C:/Program Files/Git/bin/bash.exe"
        if not os.path.isfile(self.git_bash_executable):
            raise FileNotFoundError("bash.exe not found. Please ensure Git Bash is installed.")

    @bash_command_executor
    def run_command(self, command):
        """
        Execute a generic Linux command.

        Args:
        command (str): The Linux command to be executed.

        Returns:
        str: The output of the command or the error message if the command fails.
        """
        try:
            result = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
            return result.decode('utf-8')
        except subprocess.CalledProcessError as e:
            return e.output.decode('utf-8')

    @bash_command_executor
    def list_items(self, directory='.'):
        """
        List items in a specified directory.

        Args:
        directory (str): The directory to list items from. Defaults to the current directory.

        Returns:
        str: Directory listing.
        """
        return self.run_command(f'ls {directory}')

    @bash_command_executor
    def move_or_copy(self, source, destination, is_copy=False):
        """
        Move or copy a file or directory.

        Args:
        source (str): The source file or directory.
        destination (str): The destination path.
        is_copy (bool): True to copy, False to move. Defaults to False.

        Returns:
        str: Command output or error message.
        """
        cmd = 'cp' if is_copy else 'mv'
        return self.run_command(f'{cmd} {source} {destination}')

    @bash_command_executor
    def remove(self, target):
        """
        Remove a file or directory.

        Args:
        target (str): The file or directory to remove.

        Returns:
        str: Command output or error message.
        """
        return self.run_command(f'rm -r {target}')

    @bash_command_executor
    def create_file(self, file_name, content=''):
        """
        Create a file with specified content.

        Args:
        file_name (str): Name of the file to be created.
        content (str): Content to be written to the file. Defaults to empty.

        Returns:
        str: Success message or error message.
        """
        try:
            with open(file_name, 'w') as file:
                file.write(content)
            return f"{file_name} created successfully."
        except IOError as e:
            return str(e)

    @bash_command_executor
    def check_disk_space(self):
        """
        Check disk space usage.

        Returns:
        str: Disk space usage.
        """
        return self.run_command('df -h')

    @bash_command_executor
    def view_file_content(self, file_name):
        """
        View the content of a file.

        Args:
        file_name (str): The name of the file whose content is to be displayed.
    Returns:
    str: The content of the file or an error message.
    """
        return self.run_command(f'cat {file_name}')

    @bash_command_executor
    def search_files(self, directory, pattern):
        """
        Search for files matching a pattern in a specified directory.

        Args:
        directory (str): The directory to search in.
        pattern (str): The search pattern (e.g., '*.txt').

        Returns:
        str: Search results or an error message.
        """
        return self.run_command(f'find {directory} -name {pattern}')

    @bash_command_executor
    def display_system_info(self):
        """
        Display system information.

        Returns:
        str: System information.
        """
        return self.run_command('uname -a')

    @bash_command_executor
    def grep(self, pattern, file_name):
        """
        Search for a pattern in a file using grep.

        Args:
        pattern (str): The pattern to search for.
        file_name (str): The file to search in.

        Returns:
        str: The grep command output or an error message.
        """
        return self.run_command(f'grep {pattern} {file_name}')

    @bash_command_executor
    def scp(self, source, destination, is_remote_to_local=False):
        """
        Copy files between local and remote systems using scp.

        Args:
        source (str): The source file path.
        destination (str): The destination file path.
        is_remote_to_local (bool): True for remote-to-local copy, False for local-to-remote. Defaults to False.

        Returns:
        str: Command output or error message.
        """
        scp_command = f'scp {source} {destination}' if not is_remote_to_local else f'scp {destination} {source}'
        return self.run_command(scp_command)

    @bash_command_executor
    def execute_ssh_command(self, host, command, user=None):
        """
        Execute a command on a remote server via SSH.

        Args:
        host (str): The hostname or IP address of the remote server.
        command (str): The command to be executed on the remote server.
        user (str, optional): The username for SSH. If not provided, the current user is assumed.

        Returns:
        str: The output of the remote command or an error message.
        """
        ssh_command = f'ssh {user}@{host} {command}' if user else f'ssh {host} {command}'
        return self.run_command(ssh_command)


if __name__ == "main":
    try:
        commander = LinuxCommander()
    except FileNotFoundError as e:
        print(e)
