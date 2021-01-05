# chess2midi
A python algorithm that converts chess games (in annotated PGN) to MIDI.

**Usage:**
```bash
python chess2midi.py [pgn_file] [output_midi] -tps -bpm -key -minor
```
**Positional arguments:** <br>
```[pgn_file]```: the input pgn, must be an annotated pgn with clock times for both players. Download directly from lichess.com by viewing a game in the analysis board and clicking the "FEN & PGN" tab at the bottom of the page. <br> <br>
```[output_MIDI]```: the name of the output MIDI file to write. <br> <br>
**Optional arguments:** <br>
```-tps```: ticks per second (integer between 1-120), the number of ticks in the MIDI file assigned to an in game second. Lower numbers will shorten the spacing between notes whilst preserving relative differences (default 15).  <br> <br>
```-bpm```: beats per minute (integer), the beats per minute the MIDI file will play back at (default 100). <br> <br>
```-key```: key signature (char), the key signature of the MIDI file (default C). If required must be written with #s e.g. (A# not Bb). <br> <br>
```-minor```: minor key (char), any character is passed the piece will be written using the harmonic minor scale as diatonic notes (default major).  <br> <br>
**Examples:** <br>
```bash
python chess2midi.py [example1.pgn] [example1.mid] -tps 1 -bpm 60 -key B
```
```bash
python chess2midi.py [example2.pgn] [example2.mid] -tps 20 -bpm 100 -minor T
```
