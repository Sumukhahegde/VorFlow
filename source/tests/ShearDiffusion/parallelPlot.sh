#bash

echo -n "How many files to plot? "
read nfile

for((i=16;i<=$nfile;i++))
	do
		python pickledPlot.py $i
	done

