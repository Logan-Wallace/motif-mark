#! usr/bin/env python
# Author: Logan Wallace lwallac2@uoregon.edu

'''The purpose of this program is to generate a drawing of a sequence displaying a gene (line), an 
exon (rectangle) and motifs (hash marks) along the gene by reading in a fasta file holding a gene 
sequence and another text file containing motifs using Pycairo and object oriented programming'''

#Import neccessary modules
import cairo 
import re
import argparse
import math
import random


def oneline_fasta():
    '''This function will take as input a fasta file and write out to a file called "oneline_fasta"'''
    #init some variables
    read_file: str = ""
    header: str = ""
    peptide: str = ""

    #Variable Initialization
    headerDict:dict = {} 

    #open our fasta file to read
    with open(geneFile, 'r') as fasta:
        #loop through our fasta file and grab the header line
        for line in fasta:
            #if we are at a header line grab just that line
            if line[0] == '>':
                header = line
                if header not in headerDict:
                    headerDict[header] = ""
            #if not a header line grab the peptide sequence as 'peptide'
            else:
                peptide = line
                peptide = peptide.strip("\n")
            headerDict[header] += peptide
            peptide = ""

    #open the file to write to as new
    with open("oneline.fasta", 'w') as new:
        for i in headerDict:
            new.write(i + headerDict[i] + "\n")


def reverse_complement(index: str):
    '''This function will return the reverse complement to the input string. Updated to keep string capitalization'''
    rcomp = ""
    for base in index:
        if base == "A":
            base = "T"
        elif base == "T":
            base = "A"
        elif base == "C":
            base = "G"
        elif base == "G":
            base = "C"
        elif base == "a":
            base = "t"
        elif base == "t":
            base = "a"
        elif base == "c":
            base = "g"
        else:
            base = "c"
        rcomp = base + rcomp
    return(rcomp)


#Define some argparse arguments
parser = argparse.ArgumentParser(description = "Arguments for motif-mark-oop.py")
parser.add_argument("-f", "--fasta_file", help = "The name of the fasta file we are reading in", type =str, default = "/Users/loganwallace/bioinfo/Bi625/motif-mark/Figure_1.fasta")
parser.add_argument("-m", "--motifs_file", help = "The name of the motifs text file we are reading in", type =str, default = "/Users/loganwallace/bioinfo/Bi625/motif-mark/Fig_1_motifs.txt")
args = parser.parse_args()
motifFile = args.motifs_file
geneFile = args.fasta_file

#Define some other variables
motifList:list = []
drawingList: list = []
exonStart: int = 0
exonStop: int = 0


class Gene:
    def __init__(self, name, sequence, start, stop, chromosome):
        '''The gene class will include the full gene sequence from our fasta file. Inclusive of exons, introns and motifs. It will contain a search method to search for exons and motifs and store there locations to a drawing object.'''
        
        ###Data
        self.name = name
        self.sequence = sequence
        self.start = start
        self.stop = stop
        self.chromosome = chromosome
        self.motifDict = dict #motif:start1, start2, startn 
        self.exon = tuple() #start, stop, sequence
        self.exonStart = exonStart
        self.exonStop = exonStop
        
        
        ###Methods
    def findExons(self):
        '''This function will find exons within our gene sequence through capitalization and save their location within our gene'''
        #Compile our pattern for capital letter search where '+' means "one or more"
        pattern = re.compile("[A-Z]+")
        #Search our sequence for our pattern (capital letters) and call the result 'Exon'
        Exon = pattern.search(self.sequence)
        #Span gives us the span over which the pattern match was found
        startStop = Exon.span()
        self.exonStart = startStop[0]
        self.exonStop = startStop[1]
        #Group() gives us the pattern match as a string from the match object
        exon_sequence = Exon.group()
        #Store the results as 'exon' (tuple) within the gene object
        exon = (start, stop, exon_sequence)

    def findMotifs(self, motifList):
        '''This function will find motifs within our gene sequence using information from motifs object and save their location within our gene"'''    
        motifDict: dict = {}
        for motif in motifList:
            motifDict[motif] = []
            #create a temporary string variable
            motifString = ""
            #loop through the motif and create our string to compile, replacing y's with c|t
            for letter in motif:
                if letter == "Y":
                    letter = "[C|T]"
                elif letter != "Y":
                    letter = "[" + letter + "]"
                motifString += letter
            query = re.compile("{}".format(motifString))
            upperSequence = self.sequence
            upperSequence = upperSequence.upper()
            found = query.finditer(upperSequence)
            #found is an iterator of match objects so we need to iterate through them and we could save them to a dictionary
            for matchObject in found:
                startStop = matchObject.span()
                motifDict[motif].append(startStop[0])
        self.motifDict = motifDict

class Motifs:
    def __init__(self):
        '''The motif class will be used to create hashmarks along our gene sequence. It will also contain a search method that will parse through a motif.txt file and find all motifs. It will simply contain a list of motifs that we are going to pass to our gene object to search for the motifs.'''

        ###Data
        self.motifList = motifList
    
    ###Methods
    def findMotifs(self, motifFile):
        '''This function with be used to search a text file for motifs and store them as a list'''
        #Open the motifs file and store them as class 'Motif'
        with open(motifFile, 'r') as motifFile:
            #Loop through the file grabbing 'motif' as each one
            for motif in motifFile:
                #If the line is not empty
                if motif != "":
                    #Strip the newline character
                    motif = motif.strip("\n")
                    #Send the string to uppercase
                    motif = motif.upper()
                    #Store the motif as an object of class motif
                    motifList.append(motif)


class Drawing:
    def __init__(self, geneList):
        '''The Drawing class will create a drawing using pycairo and information from all the listed gene objects'''

    ###Methods
    def Draw(self):
        '''This method will draw our genes to a png'''
        #Initialize a dictionary to get some color for the motifs
        motifColor: dict = {}
        #Set up our canvas
        numGenes = len(geneList)
        WIDTH = 850
        HEIGHT = numGenes * 400
        #Create a surface, 'FORMAT_ARGB32' allows for transparency
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
        #Create a context
        ctx = cairo.Context(surface) 
        ctx.set_source_rgb(1, 1, 1)
        ctx.select_font_face("Purisa", cairo.FONT_WEIGHT_BOLD, cairo.FONT_SLANT_ITALIC)
        ctx.set_font_size(60)
        ctx.move_to((WIDTH/4), (100))
        ctx.show_text("MOTIF MARK")

        #Initialize a counter
        geneNum = 0
        #Draw our genes 
        for gene in geneList:
            ctx.set_source_rgb(1,1,1)
            #Draw the line for our gene from start to exon beginning
            geneNum += 1
            geneLength = gene.stop - gene.start
            yCenter = geneNum*320
            exonYMax = yCenter + 80
            exonYMin = yCenter - 80
            ctx.move_to(0, yCenter)
            ctx.line_to(gene.exonStart, yCenter) 
            #Draw our rectangle for our exon
            ctx.rectangle(gene.exonStart, exonYMin, (gene.exonStop - gene.exonStart), 160) # Rectangle(x0, y0, x1, y1) NOPE -> Rectangle (x0, y (bottom), width, height)
            #Draw the line from exon stop to gene end
            ctx.move_to(gene.exonStop, yCenter)
            ctx.line_to(geneLength, yCenter)
            ctx.set_line_width(5)
            ctx.stroke()
            #Add a label to each of our genes
            ctx.set_source_rgb(1, 1, 1)
            ctx.select_font_face("Purisa")
            cairo.FONT_SLANT_ITALIC
            cairo.FONT_WEIGHT_NORMAL
            ctx.set_font_size(18)
            ctx.move_to(0, (yCenter - 50))
            ctx.show_text(gene.name)
            #Make some motif hashes
            motifDict = gene.motifDict
            motifCount = 0 
            for motif in motifDict:
                #If we don't already have a color for that motif
                if motif not in motifColor:
                    #Generate a seed to create a color
                    seed = random.random()
                    motifColor[motif] = seed
                    #Add the motif to the legend
                    random.seed(seed)
                    r = random.random()
                    g = random.random()
                    b = random.random()
                    ctx.set_source_rgb(r, g, b)
                    ctx.select_font_face("Purisa")
                    cairo.FONT_SLANT_ITALIC
                    cairo.FONT_WEIGHT_NORMAL
                    ctx.set_font_size(24)
                    ctx.move_to(((motifCount*150)), (HEIGHT - 100))
                    ctx.show_text(str(motif))
                    motifCount += 1
                elif motif in motifColor:
                    seed = motifColor[motif]
                motifName = str(motif) #get the name of the motif
                motifLength = len(str(motif))
                #Access the list within the dictionary to see the start of the motif within the gene
                for i in gene.motifDict[motif]:
                    motifStart = i 
                    random.seed(seed)
                    r = random.random()
                    g = random.random()
                    b = random.random()
                    ctx.rectangle(motifStart, (yCenter - 40), motifLength, 80)
                    ctx.set_source_rgb(r, g, b)
                    ctx.set_line_width(1)
                    ctx.fill()            
            surface.write_to_png("MarkedMotif.png")

#Create a motif object and use findMotifs() to store the results as a list
motifs = Motifs()
motifs.findMotifs(motifFile)

###Now we have the motifs stored as a list within 'motifs' object

#Turn the fasta file into a oneline fasta using 'oneline' from bioinfo
oneline_fasta()

#Open the fasta file and store the contents as class genes
with open("oneline.fasta", 'r') as geneFile:
    counter: int = 0
    chromosome: str = ""
    geneList:list = []

    for line in geneFile:
        #If the line is a header line we need to extract some information
        if line[0] == ">":
            #Split the line to return a list 
            line = line.split(" ")
            #Remove the '>' character and save the first item as gene name
            gene = re.sub(r'>', '', line[0], count = 1)
            #Split the second string by the ':' character and save the first portion as chromosome and second as start and stop locations
            chromList = line[1].split(":")
            chromList[0] = chromosome 
            startStop = chromList[1]
            startStop = startStop.split("-")
            start = int(startStop[0])
            stop = int(startStop[1])
            #If the 'reverse_complement' flag is evident, we need to remember to reverse the sequence of this gene
            #if line[2] == "(reverse":
            #    reverseComp = True
            counter += 1 
        #If the line is a sequence line
        elif line[0] == "a" or "c" or "t" or "g":
            sequence = line
            #first check the 'reverseComp' flag
            # if reverseComp == True:
            #     #get the reverse complement
            #     sequence = reverse_complement(sequence)
            #     #reset the reverseComp flag
            #     reverseComp = False            
            counter += 1
        #If we have a header and a sequence
        if counter % 2 == 0:
            #We are creating the gene object and appending it to a list simultaneously so our list knows these as gene objects and not strings with 'gene' stored
            geneList.append(Gene(gene, sequence, start, stop, chromosome))

#Now we have created a list of genes and gene objects from that list inclusive of their sequence and positions in the genome. Now we can pass to each gene object the list of motifs with which to search along the gene

#Now we have our gene list, we can search them for exons
for gene in geneList:
    gene.findExons()

#Pass the list of motifs to each gene object to allow them to search themselves for the motifs
for gene in geneList:
    gene.findMotifs(motifs.motifList)

#Now that we have our motifs stored within each of our genes, it's time to create a drawing object
prettyPicture = Drawing(geneList)
prettyPicture.Draw()
    




























