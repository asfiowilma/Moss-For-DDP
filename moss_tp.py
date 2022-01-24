import mosspy
import zipfile
import os

from rich.console import Console
from rich.prompt import Prompt as prompt
from rich.panel import Panel

folder = ".\\demo" ## CHANGE: to folder containing zipfile of every class 
userid = 000000000 ## CHANGE: to your user id 

console = Console()
extension = ".zip"

def run_moss():
    """ Starts moss """

    m = mosspy.Moss(userid, "python")
    # sesuaikan dengan penamaan berkas.
    # jika tidak menggunakan template, silahkan block comment potongan kode ini
    # template_filename = "./template_labxx/TemplateXX.py"
    # m.addBaseFile(template_filename)

    submission_patternname = f"{folder}/*.py"
    m.addFilesByWildcard(submission_patternname)

    with console.status("Processing... (this may take a while)", spinner="clock"):
        url = m.send()
    
    # akses hasil checker lewat URL ini
    console.print(Panel(f"Check out your plagiarism check results: [cyan underline]{url}[/cyan underline]", title="All Done!"))

def extract_zip_kelas(zipname, toFolder):
    zippedFile = f"{folder}/{zipname}"
    with zipfile.ZipFile(zippedFile, 'r') as zfile:
        files_inside = zfile.infolist()
        for file in files_inside:
            if file.filename.endswith(".rar"):
                file.filename = file.filename[:-4] + extension
            zfile.extract(file, path=toFolder)
    os.remove(zippedFile)


def extract_zip_mahasiswa(zipname, toFolder):
    """ Extract a zip file
        Delete the zip file(s) after extraction
    """
    zippedFile = f"{folder}/{zipname}"
    with zipfile.ZipFile(zippedFile, 'r') as zfile:
        files_inside = zfile.infolist()
        for file in files_inside:
            renamed = f"{zipname[:-4]}_{file.filename}"
            if file.filename.endswith('.py'):
                file.filename = renamed.replace('/', '')
                zfile.extract(file, path=toFolder)
    os.remove(zippedFile)


def extract_zip_of_zips():
    badZips = []
    for zipname in os.listdir(folder):
        if zipname.endswith(extension):
            try:
                extract_zip_kelas(zipname, folder)
            except zipfile.BadZipfile:
                badZips.append(zipname)
    if len(badZips) > 0:
        console.log('[black on yellow underline]There were problems when extracting these files:')
        console.log('[cyan]You probably got no choice but to extract them manually. Delete the zip file afterwards.')
        for badZip in badZips:
            console.log(f'💩 {badZip}')

def clean_up_level_1():
    badNames = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            fileSpec = os.path.join(root, filename)
            if root == folder:    
                renamed = filename            
                if len(filename.split("_")) > 5:
                    renamed = "_".join(filename.split("_")[4:])
                    
                if renamed.endswith(".rar"):
                    renamed = renamed[:-4] + extension
                os.rename(fileSpec, f"{folder}/{renamed}")
            else:
                if filename.endswith(".rar"):
                    filename = filename[:-4] + extension
                os.rename(fileSpec, f"{folder}/{filename}")
            if len(filename) < 14:
                badNames.append(fileSpec)
                
    for root, dirs, files in os.walk(folder):
        # check whether the directory is now empty after deletions, and if so, remove it
        if len(os.listdir(root)) == 0:
            os.rmdir(root)
    
    if len(badNames) > 0:
        console.log('[black on yellow underline]These files may have some weird names:')
        console.log('[cyan]Rename them manually or ask the other TAs to do it.')
        for badName in badNames:
            console.log(f'💩 {badName}')

def clean_up_level_2():
    corrupted = []
    for zipname in os.listdir(folder):
        if zipname.endswith(extension):
            try:
                extract_zip_mahasiswa(zipname, folder)
            except zipfile.BadZipfile:
                corrupted.append(zipname)

    if len(corrupted) > 0:
        console.log(f'[black on yellow underline]These files might be corrupted:')
        console.log('[cyan]Too bad. Lol. (perhaps try extracting them manually)')
        for files in corrupted:
            print(f'💩 {files}')

def rename_files_after_extraction():
    for root, dirs, files in os.walk(folder):
        for filename in files:
            fileSpec = os.path.join(root, filename)
            if filename.endswith('.py'):
                renamed = fileSpec.split('\\')[1] + '_' + filename
                os.rename(fileSpec, f"{folder}/{renamed}")
            else:
                os.remove(fileSpec)
                
    for root, dirs, files in os.walk(folder):
        # check whether the directory is now empty after deletions, and if so, remove it
        if len(os.listdir(root)) == 0:
            os.rmdir(root)

def main():
    console.rule()
    console.print("WELCOME TO MOSS PREPROCESSING PROGRAM", style='bold', justify='center')
    console.print("Brought to you by LIT:fire:", justify='center')
    
    console.rule('[bold bright_green]How to Use', align='center')    
    console.print("- The instructions below are for you to do manually")
    console.print("- Press [cyan]ENTER[/cyan] when you're ready to continue")
    console.print("- Let the program do its magic")
    console.print("[yellow]:warning: These steps are meant to be executed [yellow bold]sequentially[/yellow bold].")
    console.print("  If something goes wrong and you had to rerun the program, [bold]skip the previous steps you've done[/bold].")
    console.print("  Otherwise you will have to restart the entire process.")
    console.print("[yellow]:warning: It's a good idea to keep your file explorer open to see what's going on")
    console.print("- Feel free to customize the program as needed")
    
    console.rule('[bold bright_green]STEP 1:', align='center')    
    console.print(f'> Place zip of zips file in {folder}')
    i = prompt.ask("  [cyan]Continue?", choices=["yes", "skip", 'y', 's'], default='yes')
    if i != 's' and i != 'skip': extract_zip_of_zips()

    console.rule('[bold bright_green]STEP 2:', align='center')    
    console.print('> Clean up dirty files by manually renaming them (files with no extension, wrong name format, etc.)')
    i = prompt.ask("  [cyan]Continue?", choices=["yes", "skip", 'y', 's'], default='yes')
    
    if i != 's' and i != 'skip': clean_up_level_1()
    
    console.rule('[bold bright_green]STEP 3:', align='center')    
    console.print('> Clean up one more time please (files with no extension, wrong name format, etc.)')
    console.print("> Yes this is a pain in the neck, but bear with it")
    i = prompt.ask("  [cyan]Continue?", choices=["yes", "skip", 'y', 's'], default='yes')
    if i != 's' and i != 'skip':clean_up_level_2()    
            
    console.rule('[bold bright_green]STEP 4:', align='center')    
    console.print("> Congrats! You're done cleaning up.")
    console.print("> Press [cyan]ENTER[/cyan] to run moss.")
    i = prompt.ask("  [cyan]Run moss now?", choices=["yes", "skip", 'y', 's'], default='yes')
    if i != 's' and i != 'skip': run_moss()

if __name__ == '__main__':
    main()    
