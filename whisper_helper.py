import sys
import os
import socket
import time
import whisper
from collections import Counter
import pprint
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")


full_file_list = []

def list_files_scandir(path='.', str_include=['mp3','mp4','pmweg','m4a','wav','webm']):
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                if entry.path.lower().endswith(tuple(str_include)) == True:
                    full_file_list.insert(-1, entry.path)
            elif entry.is_dir():
                list_files_scandir(entry.path)

def normalize_directory(lpath, l_os):
    if l_os == 'linux':
        if lpath.endswith('/') == False:
            return lpath + "/"
        else:
            return lpath
        
    elif l_os == 'win':
        if lpath.endswith("\\") == False:
            return lpath + "\\"
        else:
            return lpath

def getfilename(l_path):
    return Path(l_path).stem


def cleanfile(l_filename):
    try:
        os.remove(l_filename)
    except OSError:
        pass

def getWord():
    words = input_string.split()
    wordCount = Counter(words)
    return wordCount

def get_username_computername():
    return os.getlogin(), socket.gethostname()


source_folder_path = ""
destination_folder_path = ""
model_type = "tiny"

# Options
# -s [required]: source directory or file
# -d [required]: destination directory
# -m [optional]: model type [values: tiny, base, small, 
#                medium, large, turbo] - defaults to tiny
# -h [optional]: output usage inforamtion   


if len(sys.argv) > 0:
    n = len(sys.argv)
    for i in range(1, n):
        match sys.argv[i]:
            case "-s":
                #save file
                source_folder_path = sys.argv[i+1]
                i+=1

            case "-d":
                destination_folder_path = sys.argv[i+1]
                i+=1

            case "-m":
                model_type = sys.argv[i+1]
                i+=1

            case "-h":
                print("Usage:\n")
                print("\t $>python.exe whisper_helper.py -m [model:see values] -s [source folder] -d [destination folder]")
                exit()
            
current_user, computer_name = get_username_computername()

str_model_type = model_type
model = whisper.load_model(str_model_type)

sysos = 'win'
if sys.platform.startswith('win') == True:
    sysos = 'win'
else:
    sysos = 'linux'

destination_folder_path = normalize_directory(destination_folder_path, sysos)
if os.path.exists(destination_folder_path) == False:
    os.mkdir(destination_folder_path)

#files to process 
list_files_scandir(source_folder_path)
stats_file = destination_folder_path + "batch_job.txt"

int_count = 0
for str_file in full_file_list:
    int_count+=1
    print("Processing file " + str(int_count) + " of " + str(len(full_file_list)) + ": " + getfilename(str_file))
    start_time = time.time()
    
    #Transcribe the file 
    result = model.transcribe(str_file)
    
    #output file
    output_file = destination_folder_path + getfilename(str_file) + ".decode_optons.txt"
    transcribed_file = destination_folder_path + getfilename(str_file) + ".transcribed.txt"

    cleanfile(output_file)
    cleanfile(transcribed_file)
    
    with open(output_file, 'x', encoding="utf-8") as f:
        pprint.pprint(result, f)

    #print(result["text"])
    elapsed = (time.time() - start_time)

    #append to the results file
    with open(stats_file, "a") as f:
        f.write("filename: " + str_file + "\t" + "Machine: " + computer_name + "\t" + "user: " + current_user + "\t" + "Word Count: " + str(len(result["text"])) + "\t" + "Execution (in secs): "  + str(elapsed) + "\t" + "model used: " + str_model_type + "\n")
    
    #print the transcribed file
    with open(transcribed_file, 'x', encoding="utf-8") as f:
        encoded_line = result['text'].encode("utf-8", errors="ignore")
        decoded_line = encoded_line.decode(encoding="utf-8")
        f.write(decoded_line)

