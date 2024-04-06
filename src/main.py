import tools
import os
import hashlib

folderpath = "D:\\Compression\\data_to_compress\\"
files = os.listdir(folderpath)

print(f"Chosen path: {folderpath}")
print(f"Found {len(files)} files\n")


if "metricdb" not in os.listdir():
    print("metricdb wasn't found")
    metricdb = open("metricdb", "w+")
else:
    metricdb = open("metricdb", "a+")

if "compressiondb" not in os.listdir():
    print("compressiondb wasn't found")
    compressiondb = open("compressiondb", "w+")
else:
    compressiondb = open("compressiondb", "a+")


print("Checking if randomness for selected files has been already calculated")

for file in files:
    print(f"Checking file {file} ({files.index(file)}/{len(files)})")
    filebin = open(folderpath + file, "rb", buffering = 0)
    tmphash = hashlib.file_digest(filebin, 'sha512').hexdigest()
    filebin = open(folderpath + file, "rb", buffering = 0)
    filebin = filebin.read()
    if tmphash in metricdb:
        print(f"found {file} in database")
    else:
        print(f"Randomness calculation wasn't found in database. Calculating...")
        matrixtmp = tools.getFastMarkovMatrix(filebin)
        metric = tools.getMarkovRandomness(matrixtmp)
        metricdb.write(f"{tmphash},{metric}\n")
        print(f"Calculated randomness for {file}.")

        

