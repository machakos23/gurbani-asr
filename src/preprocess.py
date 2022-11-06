import numpy as np, ffmpeg, soundfile as sf

def nextSoundSegment(samples, i, cutoffdb, minsilence, padding):
    cutoff = 10**(-cutoffdb/20.0)
    minsilence = int(minsilence * 16000)
    padding = int(padding * 16000)
       
    # find the start of the sound 
    while i < samples.size:
        if abs(samples[i]) < cutoff:
           i += 25
        else:
            i = max(0, i-padding)
            break

    if i >= samples.size:
        return None
    
    silenceStart = -1; silenceCount = 0; j = i
    
    # now find the end of the sound
    while j < samples.size:
        if abs(samples[j]) < cutoff:
            silenceCount += 25
            if silenceStart == -1:
                silenceStart = j
        else:
            silenceCount = 0
            silenceStart = -1
            
        if silenceCount > minsilence:
            break
        
        j += 25

    if j >= samples.size:
        return (i,samples.size)
    
    return (i, min(silenceStart + padding, samples.size))


def getAllSegments(samples, cutoffdb, minsilence, padding):
    segments = []; end = -1

    while result := nextSoundSegment(samples, end+1, cutoffdb, minsilence, padding):
        _,end = result
        segments.append(result); 

    return segments

# to do - replace the silence removal code with an ffmpeg filter pipeline
def removeSilences(samples, cutoff, minsilence, padding):
     segments = getAllSegments(samples, cutoff, minsilence, padding)
     samples = np.concatenate([samples[start:end] for start,end in segments])
     return samples

def normalize(samples, targetvol):
    meanvol = 10*np.log10(np.mean(samples**2))
    vol = targetvol - meanvol
    process = (
        ffmpeg
        .input('pipe:', format='f32le', ac=1, ar=16000, acodec='pcm_f32le')
        .filter("volume", volume=f'{vol}dB')
        .output('pipe:', format='f32le', ac=1, ar=16000, acodec='pcm_f32le')
        .overwrite_output()
        .run_async(pipe_stdin=True,pipe_stdout=True))
    
    return np.frombuffer(process.communicate(input=samples.tobytes())[0], np.float32)
  
## to maximise accuracy we normalize to closely match training data which was silence removed
def preprocess(filename, vol, cutoffdb, minsilence, padding, fileoutpath=None):
    stream = ffmpeg.input(filename)
    stream = stream.filter("volume", volume=f'{vol}dB')
    stream = stream.output('pipe:', format='f32le', ac=1, ar=16000, acodec='pcm_f32le')
    samples = np.frombuffer(stream.run(capture_stdout=True)[0], np.float32)
    samples = normalize(samples, -25)
    cutoff = 10**(-cutoffdb/20.0)
    minsilence = int(minsilence * 16000)
    samples = removeSilences(samples, cutoff, minsilence, padding)
    
    if fileoutpath: 
         sf.write(fileoutpath, samples, 16000)
    
    return samples
