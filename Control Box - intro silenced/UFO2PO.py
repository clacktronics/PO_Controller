'''
this script converts UFO data into arrays that can be pasted into the arduino IDE



'''

import re,sys

sequencelist = []
loopslist=[]
sequenceLine = 0
loopsline = 0

# This extracts the data into a format similar to desired output
#===============================================================


with open(sys.argv[1]) as sequenceData:
	for line in sequenceData:
		lineNoWhite = line.replace(' ','').strip()
		if lineNoWhite != '' and lineNoWhite[0] != ';':
			if lineNoWhite[:4] == 'sdat':
				sequencelist.append(lineNoWhite[4:].split(','))
				sequencelist[-1].append(delaytime)
				sequenceLine += 1
			elif lineNoWhite[:4] == 'hold':
				delaytime = lineNoWhite[4:]
			elif lineNoWhite[:9] == 'control0,':
				loopslist.append([sequenceLine, 0, int(lineNoWhite[9:])+1])
			elif lineNoWhite == 'seqend':
				loopslist[loopsline][1] = sequenceLine -1
				loopsline += 1

# This is to check if there is any repetition of sequences
#=========================================================

split_sequences = []

for loop_no,loop in enumerate(loopslist):
	split_sequences.append([]) # add a new list to the list
	for i in range(loop[0],loop[1]):
		split_sequences[loop_no].append(sequencelist[i]) 


for seqN,seq in enumerate(split_sequences):
	for CseqN,Cseq in enumerate(split_sequences):
		if seq == Cseq and seqN != CseqN:
			print "sequence %d is then same as sequence %d" % (seqN,CseqN)


# This compiles a new file at output
#===================================

Output_file = open('seqdata_PO.h', 'w')
Output_file.write("unsigned char loops[][3] = {\n")
for lineN,line in enumerate(loopslist):
	line_write = '{'
	for valN,val in enumerate(line):
		if valN == 2:
			line_write += '%d' % val
		else:
			line_write += '%d,' % val
	if lineN+1 == len(loopslist):
		line_write += '} //Sequence %d\n' % (lineN + 1)
		Output_file.write(line_write)
	else:
		line_write += '}, //Sequence %d\n' % (lineN + 1)
		Output_file.write(line_write)
Output_file.write("};\n\n")




Output_file.write("unsigned char sequence[][9] = {\n")
for lineN,line in enumerate(sequencelist):
	line_write = '{'
	for valN,val in enumerate(line):
		if valN == 8:
			line_write += '%s' % val
		else:
			line_write += '%s,' % val

	# seuqnece marker
	note = ''
	for loopN,loopS in enumerate(loopslist):
		if loopS[0] == lineN:
			note = '// Sequence %d' % (loopN + 1)


	if lineN+1 == len(sequencelist):
		line_write += '} %s\n' % note
		Output_file.write(line_write)
	else:
		line_write += '}, %s\n' % note
		Output_file.write(line_write)
Output_file.write("};")
Output_file.close()



