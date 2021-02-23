#convert .ogg files in directory to .wav files
import os 
i=0
for file in os.listdir():
    if file.endswith('.ogg'):
        name = os.path.splitext(file)[0]
        print(name)
        nFile = name + ".wav"
        print(nFile)
        os.system("ffmpeg -i %s %s" %(file, nFile))
        os.system("rm %s" %(file))
        os.system("mv %s audio" %(nFile))
        # x.append(file)
        i+=1
print('the total number of files: ' +str(i))


