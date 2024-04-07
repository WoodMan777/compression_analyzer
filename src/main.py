import tools, os, hashlib, sqlite3
import time, yaml


config = yaml.safe_load(open("config.yaml", 'r'))
folderpath = config['setup']['folder_in']
outpath = config['setup']['folder_out']
exepath = config['setup']['exepath']
files = os.listdir(folderpath)


print(f"Chosen path: {folderpath}")
print(f"Found {len(files)} files\n")

metricdb = sqlite3.connect('metric.db')
cursorm = metricdb.cursor()
cursorm.execute("""
        CREATE TABLE IF NOT EXISTS Metric (
        id INTEGER PRIMARY KEY,
        hash TINYTEXT,
        value DOULBE
        )
        """)



compressiondb = sqlite3.connect('comression.db')
cursord = compressiondb.cursor()
cursord.execute("""
        CREATE TABLE IF NOT EXISTS Data (
        id INTEGER PRIMARY KEY,
        parameters TEXT,
        time DOUBLE,
        size BIGINT,
        csize BIGINT,
        hash TINYTEXT,
        name TINYTEXT
        )
        """)


print("Checking if randomness for selected files has been already calculated")

for file in files:
    print(f"Checking file {file} ({files.index(file)}/{len(files)})")
    tmphash = tools.calculateHash(folderpath + file)
    filebin = open(folderpath + file, "rb", buffering = 0)
    filebin = filebin.read()
    cursorm.execute('SELECT value FROM Metric WHERE hash = ?',(tmphash,))
    res = cursorm.fetchall()
    if len(res):
        print(f"found {file} in database")
    else:
        print(f"Randomness calculation wasn't found in database. Calculating...")
        matrixtmp = tools.getFastMarkovMatrix(filebin)
        metric = tools.getMarkovRandomness(matrixtmp)
        cursorm.execute('INSERT INTO Metric (hash, value) VALUES (?, ?)',(tmphash, metric))
        metricdb.commit()
        print(f"Calculated randomness for {file}.")

allcmds = tools.generateAllCmdStrings(exepath, config)

for command in allcmds:
    print(f"> Performing test {allcmds.index(command)+1} of {len(allcmds)}")
    for file in files:
        print(f">>file {files.index(file)+1} of {len(files)}")
        cmd = f"{command} {outpath}{file}.7z {folderpath}{file}"
        print(cmd)
        start = time.time()
        os.system(cmd)
        end = time.time()
        orig_size = os.stat(f"{folderpath}{file}").st_size
        comp_size = os.stat(f"{folderpath}{file}.7z").st_size
        tmphash = tools.calculateHash(folderpath+file)
        cursord.execute('''INSERT INTO Metric (parameters, time, size, csize, hash, name) 
                        VALUES (?, ?, ?, ?, ?, ?)''', (command, start-end, orig_size, comp_size, tmphash, file))