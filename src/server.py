import zmq
from stt import Transcriber

atb = Transcriber(pretrain_model='models/pre.pt',
                  dictionary='models/dict.ltr.txt',
                  finetune_model='models/fine.pt',
                  lm_type='kenlm',
                  lm_lexicon='models/lexicon.txt',
                  lm_model='models/kenlm.bin',
                  lm_weight=2.78,
                  word_score=-1.9,
                  beam_size=2500)


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

while True:
    msg = socket.recv_string()
    print(f'server received: {msg}')
    socket.send_string(atb.transcribe([msg])[0])
