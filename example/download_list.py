from updown import *
import os
import io
from scipy.io import wavfile
import scipy.signal as sps
import soundfile
import librosa
from tqdm import tqdm


parser = argparse.ArgumentParser(description='Sync ~/Downloads to Dropbox')
parser.add_argument('--token', default=TOKEN, help='Access token' '(see https://www.dropbox.com/developers/apps)')
parser.add_argument('--listpath', default=None, help='path to list of file names')


def main():
    args = parser.parse_args()
    # list1_path = r'C:\Users\amitg\Documents\Deep Voice\HF WAV Manatee Samples\BB_analysis\ManateesList1.txt'
    list1_path = '/home/ubuntu/soundbay/src/ManateesList2.txt'
    # list2_path = r'C:\Users\amitg\Documents\Deep Voice\HF WAV Manatee Samples\BB_analysis\ManateesList2.txt'
    list2_path = './ManateesList2.txt'
    # outfolder = r'C:\Users\amitg\Documents\Deep Voice\HF WAV Manatee Samples\BB_analysis\wavs'
    outfolder = '/home/ubuntu/wavs2/'
    dropbox_folder = '2021-ManateeAcousticsDeepVoice'
    dropbox_subfolder2 = '2017-Jul-08-12-67407878-SGC-RestingHole1A/WAV'
    dropbox_subfolder1 = '2017-Jul-14-17-67407878-SGC-RestingHole1A/WAV'


    if not args.token:
        print('--token is mandatory')
        sys.exit(2)

    dbx = dropbox.Dropbox(args.token)
    print('initiated dropbox api')
    if args.listpath is None:
        listpath = list1_path
        print("list1 was chosen")
    else:
        listpath = args.listpath
        print("examplelist was chosen")
    with open(listpath) as f:
        filenames = f.readlines()

    for it, file in tqdm(enumerate(filenames)):
        file = file.rstrip('\n')
        file = file +'.wav'
        #file = 'attack.wav'
        #dropbox_folder = 'ProjectA'
        #dropbox_subfolder1 = ''
        print("filename:", file)
        data = download(dbx,dropbox_folder,dropbox_subfolder1,name=file) #TODO: change subfolder
        print('downloading file number', it)
        s = io.BytesIO(data)
        data, sr = soundfile.read(s)
        new_rate = 96000
        print(sr)
        print(data.shape)
        number_of_samples = round(len(data) * float(new_rate) / sr)
        print(number_of_samples)
        print('loaded successfully')
        #data = sps.resample(data, number_of_samples)
        data = librosa.resample(data, sr, new_rate)
        print(len(data))
        wav_file = os.path.join(outfolder, file)
        soundfile.write(wav_file, data, new_rate)
        print('saved file: ', file)






if __name__ == '__main__':
    main()
