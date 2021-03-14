out = open("buyStocksCramerFormatted.txt", "w") 

#variables:
line = []
date = ''
location = 1
#company name
a = 1
b = 1
#ticker
c = 1
d = 1
#segment
e = 1
#error correction
numErrors = 0
numRepeats = 0
datesMissing = False
allDates = []

#file header
out.write('Jim Cramer "buy recomendation" stocks presented on "Mad Money" from 07/06/2018 to 03/05/2021\n')
out.write('Compiled by u/shitilostagain on 3/13/2021 using publically available data\n')
out.write('Segment key: F = Featured Stock, D = Discussed Stock, I = Guest Interview, L = Lightning Round, M = Mailbag\n')
out.write('Data compiled from https://madmoney.thestreet.com/screener/index.cfm \n \n \n')
out.write('Ticker:         Date Recomended:        Segment:        Company Name:\n')
out.write('-------------------------------------------------------------------------------------- \n \n')

with open("rawStocksCramer.txt") as f:
	line = f.readline()
	while line:
		#looks for </strong> to determine date
		location = line.find("</strong>")
		if location != -1:
			location += 10

			#check for repetition of dates
			if date == line[location:location+10]:
				numRepeats += 1

			date = line[location:location+10]
			
			#add dates to allDates for error checking:
			allDates.append(date)

			#then go to start of table:
			for x in range(6):
				line = f.readline()

			#after finding the top, then scrolls through table
			while line.find("</table>") == -1:
				#if tickers found, print/output
				if line.find("<td>") > 0:
					#find company name
					a = line.find("<td>")
					b = line.find("(<a")
					
					#find ticker
					c = line.find("target=")
					d = line.find("</a>")

					#find segment
					e = line.find(".gif")

					#file output
					out.write('$')
					out.write(line[c+16:d])
					out.write(',')
					if d-(c+16) == 1:
						out.write('      ')
					if d-(c+16) == 2:
						out.write('     ')
					if d-(c+16) == 3:
						out.write('    ')
					if d-(c+16) == 4:
						out.write('   ')
					if d-(c+16) == 5:
						out.write('  ')
					if d-(c+16) == 6:
						out.write(' ')
					out.write('	')

					out.write(date)
					out.write(',		')
					out.write(line[e-1:e])
					out.write(',		')
					out.write(line[a+4:b-1])
					out.write('\n')

					#verify dates match:
					if date[0:5] != line[line.find("</td><td>")+9:line.find("</td><td>")+14]:
						numErrors += 1

				line = f.readline()
		line = f.readline()

f.close()
out.close()


print("date match errors: ",end='')
print(numErrors)

print("Number of Repetitions: ",end='')
print(numRepeats)

#verify all dates are present
with open('dateMaster.txt') as f:
	line = f.readline()
	index = 0
	while line:
		if allDates[index][0:5] != line[line.find(">")+1:line.find(">")+6]:
			datesMissing = True

		line = f.readline()
		index += 1

f.close()

print("Missing Dates: ",end='')
print(datesMissing)
