# chess2midi
A python algorithm that converts chess games (in annotated PGN) to MIDI.

**Method** <br>
The algorithm works as follows: <br>
1. Whenever a move is made the column position (A-H) and row position(1-8) are used to sound a note from the chosen scale (default C major). The column position determines the note in the scale (e.g. col A = C, col B = D, ..., col G = B, col H = C) and the row position determines the octave (e.g. a5 = middle C, a1 = middle C - 4 octaves, a8 = middle C + 3 octaves).
2. If a move leads to a check or checkmate, the note is shifted either upward (for white's move) or downward (for black's move) to the nearest accidental (i.e. note not in the chosen scale). 
3. The clock timings of the move are used to determine when the note sounds. To acheive this the clock times are converted to seconds and made cumulative. Any increment on the clock this is accounted for. 
4. The duration of the note is determined by which piece is moved (Pawn = 1/16 note, Bishop/Knight = 1/8 note, Rook = 1/4 note, Queen = 1/2 note, King = whole note).
5. If a move leads to a capture the volume of the note is set as high (random MIDI value between 60 and 100), else it is low-mid (random MIDI value between 30 - 90). 

**Dependencies/Acknowledgements**<br>
The algorithm is written in Python 3.6 and requires the following additional Python libraries to work. 
* [python-chess](https://github.com/niklasf/python-chess) : this is used to parse the PGN file. 
* [MIDIUtil](https://github.com/MarkCWirt/MIDIUtil) : this is used to create the MIDI file. 
* [NumPy](https://numpy.org) : this is used for array manipulation. 

**Usage:**
```bash
python chess2midi.py [pgn_file] [output_midi] -tps -bpm -key -minor
```
**Positional arguments:** <br>
```[pgn_file]```: the input pgn, must be an annotated pgn with clock times for both players. Download directly from lichess.com by viewing a game in the analysis board and clicking the "FEN & PGN" tab at the bottom of the page. An example PGN is included in the directory. <br> <br>
```[output_MIDI]```: the name of the output MIDI file to write. <br> <br>
**Optional arguments:** <br>
```-tps```: ticks per second (integer between 1-120), the number of ticks in the MIDI file assigned to an in game second. Lower numbers will shorten the spacing between notes whilst preserving relative differences (default 15). There are 960 ticks per 1/4 note in the MIDI file. <br> <br>
```-bpm```: beats per minute (integer), the beats per minute the MIDI file will play back at (default 100). <br> <br>
```-key```: key signature (char), the key signature of the MIDI file (default C). If required must be written with #s e.g. (A# not Bb). <br> <br>
```-minor```: minor key (char), if any character is passed the harmonic minor scale will be used to define diatonic notes (default major).  <br> <br>
**Examples:** <br>
```bash
python chess2midi.py [example1.pgn] [example1.mid] -tps 1 -bpm 60 -key B
```
Convert example1.pgn to example1.mid where each in game second accounts for 1 tick in the MIDI file and the file will play back at 60 bpm. Use a B major scale to define the diatonic (i.e. non check/checkmate) notes.  

```bash
python chess2midi.py [example2.pgn] [example2.mid] -tps 20 -bpm 100 -minor T
```

Convert example2.pgn to example2.mid where each in game second accounts for 20 ticks in the MIDI file and the file will play back at 100 bpm. Use a C minor scale to define the diatonic (i.e. non check/checkmate) notes. 
