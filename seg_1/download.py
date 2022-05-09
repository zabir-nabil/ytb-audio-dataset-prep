# download all videos channel wise
# youtube playlist download

from pytube import YouTube
from tqdm import tqdm
import os
# make a full list of video

seg_id = "seg_1"
lines = open("ytb_single_speaker_segs_1.txt").readlines()

# extra check
# make sure there is no duplicate from previous segs
other_segs_to_check = [
    # "../seg_2/ytb_single_speaker_segs_2.txt",
    # "../seg_3/ytb_single_speaker_segs_3.txt",
    # "../seg_4/ytb_single_speaker_segs_4.txt"
]

prev_stored = []
seg_labels = []
for seg in other_segs_to_check:
    lines_s = open(seg).readlines()
    for line in tqdm(lines_s):
        ch, vids = line.split('|')
        prev_stored.append(ch)
        seg_labels.append(seg)

dup = open("duplicate_channels.txt", "w")

failed_channels = open("failed_channels.txt", "w")

for line in tqdm(lines):
    ch, vids = line.split('|')
    
    if ch in prev_stored:
        try:
            idx = prev_stored.index(ch)
            dup.write(f"{ch} duplicate in {seg_labels[idx]}\n")
        except:
            print("duplicate issue")
            
    os.makedirs(f"{seg_id}_{ch}", exist_ok=True) 
    vid_idx = 0
    for v in tqdm(vids.split(",")):
        try:
            vid = v.strip()
            ytb = YouTube(vid)
            ytb.streams.filter(res="360p").first().download(output_path = f"{seg_id}_{ch}", filename = f"vid_{vid_idx}.mp4")
            vid_idx += 1
        except Exception as e:
            print(f"{v} failed.")
            print(e)
    if vid_idx == 0:
        failed_channels = open("failed_channels.txt", "a")
        failed_channels.write(f"{ch}\n")
        failed_channels.close()