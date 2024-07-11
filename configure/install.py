import subprocess

def install_packages():
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
    subprocess.check_call(['python', '-m', 'spacy', 'download', 'en_core_web_md'])

if __name__ == "__main__":
    install_packages()
