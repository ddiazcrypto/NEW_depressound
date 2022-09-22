from pynput import keyboard
import pyaudio
import wave
import keyboard as kb

class recorder:
    def __init__(self, 
                 wavfile, 
                 chunksize=8192, 
                 dataformat=pyaudio.paInt16, 
                 channels=2, 
                 rate=44100):
        self.filename = wavfile
        self.chunksize = chunksize
        self.dataformat = dataformat
        self.channels = channels
        self.rate = rate
        self.recording = False
        self.pa = pyaudio.PyAudio()

    def start(self):
        #we call start and stop from the keyboard listener, so we use the asynchronous 
        # version of pyaudio streaming. The keyboard listener must regain control to 
        # begin listening again for the key release.
        if not self.recording:
            self.wf = wave.open(self.filename, 'wb')
            self.wf.setnchannels(self.channels)
            self.wf.setsampwidth(self.pa.get_sample_size(self.dataformat))
            self.wf.setframerate(self.rate)
            
            def callback(in_data, frame_count, time_info, status):
                #file write should be able to keep up with audio data stream (about 1378 Kbps)
                self.wf.writeframes(in_data) 
                return (in_data, pyaudio.paContinue)
            
            self.stream = self.pa.open(format = self.dataformat,
                                       channels = self.channels,
                                       rate = self.rate,
                                       input = True,
                                       stream_callback = callback)
            self.stream.start_stream()
            self.recording = True
            print('recording started')
    
    def stop(self):
        if self.recording:         
            self.stream.stop_stream()
            self.stream.close()
            self.wf.close()
            
            self.recording = False
            print('recording finished')


class listener(keyboard.Listener):
    def __init__(self, recorder):
        super().__init__(on_press = self.on_press, on_release = self.on_release)
        self.recorder = recorder
    
    def on_press(self, key):
        if key is None: #unknown event
            pass
        elif isinstance(key, keyboard.KeyCode): #alphanumeric key event
            if key.char == 't': #press q to quit
                self.recorder.stop()
                return False #this is how you stop the listener thread   
                
    def on_release(self, key):
        pass

def start_recording():
    r = recorder("mic6.wav")
    l = listener(r)
    print('press q to record, press t to quit')
    r.start()

def stop_recording():
    r = recorder("mic6.wav")
    l = listener(r)
    print('press q to record, press t to quit')
    r.stop()    

def record():
    r = recorder("mic6.wav")
    l = listener(r)
    print('press q to start recording, press t to stop it')
    l.start() #keyboard listener is a thread so we start it here
    l.join() #wait for the tread to terminate so the program doesn't instantly close