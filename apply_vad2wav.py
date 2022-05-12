# apply vad to all the wavs that were extracted from the mp4s


import torch
torch.set_num_threads(1)

import glob, os, tqdm

# load model & utils from torch-hub
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True,
                              onnx=False)
(get_speech_timestamps,
 save_audio,
 read_audio,
 VADIterator,
 collect_chunks) = utils


# get all the valid audio wav extracted
seg_ids_for_conv = [1, 2, 3, 4]
SAMPLING_RATE = 16000

all_wav_paths = []
print("processing segments")
for seg in tqdm.tqdm(seg_ids_for_conv):
    seg_path = f"seg_{seg}/*/*.wav"
    all_wav_paths.extend(glob.glob(seg_path))

print(f"Total wav found: {len(all_wav_paths)}")

for wav in tqdm.tqdm(all_wav_paths):
    if os.path.getsize(wav) >= 500000: # probably not a corruptly saved file
        # do processing
        wav_f = read_audio(wav, sampling_rate=SAMPLING_RATE)
        # get speech timestamps from full audio file
        speech_timestamps = get_speech_timestamps(wav_f, model, sampling_rate=SAMPLING_RATE)
        save_audio(wav,
           collect_chunks(speech_timestamps, wav_f), sampling_rate=SAMPLING_RATE)
    else:
        print(f"{wav} failed.")
