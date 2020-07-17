import git
from setup import read_version

def get_repo_version(g):
    current_version = g.describe('--abbrev=0')
    return current_version

def write_version(version):
    with open("VERSION.txt", mode='w') as version_file:
        version_file.write(version)

def main():
    print('Starting pre-commit routine')
    g = git.cmd.Git()
    repo_version = get_repo_version(g)
    current_version = read_version()
    if current_version != repo_version:
        print(f'New version detected. Updating version {current_version} --> {repo_version}')
        write_version(repo_version)
        g.add('.') # add updated version file to stage
    else:
        print('version is up-to-date')

if __name__ == "__main__":
    main()
