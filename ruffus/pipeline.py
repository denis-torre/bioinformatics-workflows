
# Import ruffus
from ruffus import *
from ruffus.combinatorics import *

# Function to create files
import pathlib, time
def createFile(input, output):
    time.sleep(0.1)
    pathlib.Path(output).touch()
    print('\nFinished job:\nINPUT: {input}\nOUTPUT: {output}\n'.format(**locals()))

#############
### Files
#############
fastq_path = '../data/fastq/*.fastq'
genome_path = '../data/genome.fa'

########################################
##### 1. Align Reads
########################################
# Create directory
@follows(mkdir('1-counts'))

# Transform - 1 to 1 operation with regex pattern matching, plus additional input
@transform(fastq_path,
           regex(r'.*/(.*).fastq'),
           add_inputs(genome_path),
           r'1-counts/\1-counts.txt')

def alignReads(infile, outfile):

    createFile(infile, outfile)

########################################
##### 2. Merge counts
########################################
# Create directory
@follows(mkdir('2-merged'))

# Merge - many to 1 operation
@merge(alignReads,
       '2-merged/counts.txt')

def mergeCounts(infile, outfile):

    createFile(infile, outfile)

########################################
##### 3. Split Dataset
########################################
# Create directory
@follows(mkdir('3-groups'))

# Subdivide - one to many operation
@subdivide(mergeCounts,
           formatter(),
           '3-groups/group*.txt',
           '3-groups/group')

def splitGroups(infile, outfiles, outfileRoot):

    for i in range(1, 6):
        outfile = '{outfileRoot}{i}.txt'.format(**locals())
        createFile(infile, outfile)

########################################
##### 4. Differential Expression
########################################
# Create directory
@follows(mkdir('4-differential_expression'))

# Combinations - many to many operation
@combinations(splitGroups,
              formatter(),
              2,
              '4-differential_expression/{basename[0][0]}_vs_{basename[1][0]}.txt')

def runDifferentialExpression(infile, outfile):

    createFile(infile, outfile)

pipeline_run()

########################################
##### 5. Merge
########################################
# Create directory
@follows(mkdir('5-results'))

# Merge - many to pne operation
@merge(runDifferentialExpression,
      '5-results/merged_results.txt')

def mergeResults(infile, outfile):

    createFile(infile, outfile)

#############
### Run
#############
pipeline_run()

#############
### Print
#############
with open('pipeline.png', 'wb') as openfile:
      pipeline_printout_graph(openfile, output_format='png')