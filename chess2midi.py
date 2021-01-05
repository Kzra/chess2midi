"""
chess2midi converts an annotated PGN file of a chess game to a MIDI file. 
for full documentation please refer to https://github.com/Kzra/chess2midi
"""
import chess.pgn
from midiutil import MIDIFile
import numpy as np 
import random
import argparse
# Parse Command Line Arguments
parser = argparse.ArgumentParser()
parser.add_argument("pgn_file", help="[Input]: pgn file with clock time annotation.")
parser.add_argument("output_MIDI", help ="[Output]: MIDI file")  
parser.add_argument("-tps","--ticks_per_sec",type=int, help="MIDI ticks per chess game second (default = 15)")
parser.add_argument("-bpm","--beats_per_minute",type=int,help="beats per minute (default = 100)")
parser.add_argument("-key","--key_signature",type=str,help="key signature (default = C)")
parser.add_argument("-minor","--minor_key",type=bool,help="use a minor key signature")
args = parser.parse_args()
if args.minor_key:
    print ("minor key turned on")
    minor = True
else:
    minor = False
if args.key_signature:
    print(f"key signature set as {args.key_signature}")
    tone = args.key_signature
    assert tone in ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'], "key signature not recognised, make sure it is upper case and does not contain flats"
else:
    tone = 'C'
if args.ticks_per_sec:
    print(f"ticks per sec set as {args.ticks_per_sec}")
    ticksperSec = args.ticks_per_sec
    assert ticksperSec >= 1 and ticksperSec <= 120, "choose a tps value between 1 and 120"
else:
    ticksperSec = 15
if args.beats_per_minute:
    print(f"beats per minute set as {args.beats_per_minute}")
    tempo = args.beats_per_minute
else:
    tempo = 100
# MIDI and Chess Conversion variables 
ticks = 960 #number of ticks per beat
time = 0 #time starts at 0 ticks
track = 0 #MIDI format 1 
channel  = 0 #Single MIDI channel 
piece2dur = {'P': int(ticks/4), 'B': int(ticks/2), 'N' : int(ticks/2), 'R' : int(ticks), 'Q': int (ticks*2), 'K': int (ticks*4)}
col2maj = {'a': 60, 'b': 62 , 'c': 64, 'd': 65, 'e': 67, 'f': 69, 'g': 71, 'h': 72} 
col2min= {'a': 60, 'b': 62 , 'c': 63, 'd': 65, 'e': 67, 'f': 68, 'g': 71, 'h': 72} 
row2octave = {'1' : -4, '2' : -3, '3' : -2, '4' : -1, '5' : 0, '6' : 1, '7' : 2, '8' : 3}
tone2tranpose = {'C':0, 'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
# transpose and define the scale of non accidental notes 
if minor == True: 
    for key in col2min.keys():
        col2maj[key] = col2maj.get(key,0) + tone2tranpose[tone]
        scale = []
    for value in col2min.values():
        scale.append(value)
    scale = np.array(scale)
else: 
    for key in col2maj.keys():
        col2maj[key] = col2maj.get(key,0) + tone2tranpose[tone]
        scale = []
    for value in col2maj.values():
        scale.append(value)
    scale = np.array(scale)
# Initiliase MIDI file
MyMIDI = MIDIFile(1, eventtime_is_ticks=True, ticks_per_quarternote=ticks)  # One track
MyMIDI.addTempo(track, time, tempo)
# Open PGN file 
pgn = open(args.pgn_file)
example_game = chess.pgn.read_game(pgn) #type is chess.pgn.game
# Extract game time from  header information 
timeControl  = example_game.headers['TimeControl']
if '+' in timeControl:
    timeTotal = int(timeControl.split('+')[0])
    timeAdj = int(timeControl.split('+')[1])
else:
    timeTotal = int(timeControl)
    timeAdj = 0
# Iterate through all moves
i = 1 # move counter
moveTime = 0
for node in example_game.mainline(): #type of node is chess.pgn.ChildNode
    check = False # boolean, has a check or mate occured?
    capture = False #boolean, has a capture occured?
    san = node.san() #standard algebraic notation for the move 
    moveTime += (timeTotal - (node.clock() - timeAdj * i)) # the time for the move, adjusted so that the moves start at 0:00
    time = moveTime * ticksperSec # time in ticks the note(s) will be played
    if node.turn(): accidental = -1 #if its black's move search down for accidentals
    else: accidental = 1 # if it's white's move search up for accidentals
    if '+' in san:
        san = san.replace('+','')
        check = True
    elif '#' in san:
        san = san.replace('#','')
        check = True
    if 'x' in san: 
        san = san.replace('x','')
        capture = True
    if capture == True: 
        velocity = random.randrange(61,100,1) # if a piece has been captured play a louder note
    else: 
        velocity = random.randrange(35,70,1) # else play a quieter note 
    # for castling write a MIDI note for the kings move, and then set san to the rooks move (allowing for a check modifier)
    if 'O-O-O' in san:
        #black's queen castle
        if node.turn():
            if minor == True:
                MyMIDI.addNote(track, channel, col2min['c'] + (12 * 3), time, ticks * 4, velocity)
            else:
                MyMIDI.addNote(track, channel, col2maj['c'] + (12 * 3), time, ticks * 4, velocity)
            san = 'Rd8'
        #white's queen castle
        else: 
            if minor == True:
                MyMIDI.addNote(track, channel, col2min['c'] + (12 * -4), time, ticks * 4 , velocity) 
            else:
                MyMIDI.addNote(track, channel, col2maj['c'] + (12 * -4), time, ticks * 4 , velocity) 
            san = 'Rd1'
    elif 'O-O' in san:
        #black's king castle
        if node.turn():
            if minor == True:
                MyMIDI.addNote(track, channel, col2min['g'] + (12 * 3), time, ticks * 4, velocity)
            else:
                MyMIDI.addNote(track, channel, col2maj['g'] + (12 * 3), time, ticks * 4, velocity)
            san = 'Rf8'
        #white's king castle
        else: 
            if minor == True:
                MyMIDI.addNote(track, channel, col2min['g'] + (12 * -4), time, ticks * 4, velocity) 
            else:
                MyMIDI.addNote(track, channel, col2maj['g'] + (12 * -4), time, ticks * 4, velocity)    
            san = 'Rf1'
    #if there has been a pawn promotion
    if "=" in san: 
        san = san.replace("=","")
        san = san[-1] + san[0:-1]
    x_pos = san[-2] # column letter of the move
    y_pos = san[-1] # row number of the move 
    if san[0].isupper():
         piece = san[0]
    else:
        piece = 'P'
    if minor == True:
        note = col2min[x_pos]
    else:
        note = col2maj[x_pos] 
    if check == True: #if a check or a check mate change the note to the nearest accidental
        while 0 in (note % scale): note += accidental #search up for white, down for black
    pitch = note + (12 * row2octave[y_pos]) #adjust octave based on row
    duration = piece2dur[piece] #adjust note length (in ticks) based on piece identity
    MyMIDI.addNote(track, channel, pitch, time, duration, velocity) # add to MIDI track
    i += 1 
# Write the MIDI File
with open(args.output_MIDI, 'wb') as output_file:
    MyMIDI.writeFile(output_file)
print(f"{args.pgn_file} succesfully converted to {args.output_MIDI}.")