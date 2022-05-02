import os, json, subprocess, textract, re, ru, isodate
from datetime import datetime

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

# avarage reading speed, words per minute
awpm = 120

contents = os.listdir('./')
contents.sort()
summary = 0


print ('Using avarage reading speed ' + str(awpm) + ' words per minute')

start_time = datetime.now()

for entity in contents:
    entity_minutes = 0
    if os.path.isdir(entity) and 'lecture.md' in os.listdir(entity):
        print ('Folder is ' + entity)
        if os.path.isdir(entity) and 'learn-metadata.json' in os.listdir(entity):
            with open(entity + '/learn-metadata.json', 'r') as file:
                lecture_metadata = json.loads(file.read())
                duration = isodate.parse_duration(lecture_metadata['duration']).seconds
                print ('--Metadata duration is ' + str(int(duration / 60)) + ' minutes')
        with open(entity + '/lecture.md', 'r') as lecture:
            number_of_words = len(lecture.read().split())
            number_of_minutes = round(number_of_words / awpm)            
            print ('--lecture.md has ' + str(number_of_words) + ' words. Reading time is ' + str(number_of_minutes) + ' minutes')
            entity_minutes += number_of_minutes
        if os.path.isdir(entity) and 'assets' in os.listdir(entity):
            assets = os.listdir('./' + entity + '/assets/')
            for asset in assets:
                asset_path = './' + entity + '/assets/' + asset
                if '.mp4' in asset:
                    length = get_length(asset_path)
                    print ('--Video ' + asset + ' is ' + str(int(length // 60)) + ' minutes ' + str(int(length % 60)) + ' seconds long')
                    entity_minutes += round(length / 60)
                if '.pdf' in asset:
                    pdf_bin = textract.process(asset_path, method='tesseract', language='rus')
                    pdf_text = pdf_bin.decode()
                    number_of_words = len(pdf_text.split())
                    number_of_minutes = round(number_of_words / awpm)
                    print ('--PDF ' + asset + ' has ' + str(number_of_words) + ' words. Reading time is ' + str(number_of_minutes) + ' minutes')
                    entity_minutes += number_of_minutes
        print ('--Calculated completion time for ' + entity + ' is ' + str(entity_minutes) + ' minutes')

        summary += entity_minutes

print ('Total read time is ' + str(summary // 60) + ' hours ' + str(summary % 60) + 'minutes' )

end_time = datetime.now()
print ('Script has been running for ' + str((end_time - start_time).seconds // 60) + ' minutes ' + str((end_time - start_time).seconds % 60) + ' seconds')